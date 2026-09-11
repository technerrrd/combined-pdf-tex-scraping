"""HTML5 chapter parser preserving source order and explicit scientific notation."""
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
import inline_content as inline

_UA = 'Mozilla/5.0 (compatible; NotesBuilder/4.1)'
_HEADINGS = {'h2': 'section', 'h3': 'subsection', 'h4': 'subsubsection'}
_NOISE_RE = re.compile(r'^(view more|view solution|join for free|table of contents|explore courses|download|attempt test)\b', re.I)
_HEADING_NUM_RE = re.compile(r'^(?:Q\d+\.?\s+|\d+(?:\.\d+)*\.?\s+|\([a-zA-Z0-9]+\)\s+)')
_PUNCT = str.maketrans({'\u00ad': '', '\u200b': '', '\u200c': '', '\u200d': '', '\ufeff': '', '‘': "'", '’': "'", '“': '"', '”': '"', '–': '--', '—': '---', '…': '...'})
MAX_IMAGE_WIDTH = .52
MAX_IMAGE_HEIGHT = .30
IMAGE_SCALE_FACTOR = .75
# A4 with the primary TeX margins has about 1.54 times as much usable height as width.
TEXT_HEIGHT_TO_WIDTH = 1.54
_CONTENT_IMAGE_RE = re.compile(r'_(?:lg|sp)\.(?:jpe?g|png|gif)(?:\?[^\s"\'>]*)?$', re.I)
_PROMO_TABLE_CLASSES = {
    'clearalldoubts', 'coursedatatable', 'coursedetialsboxipad', 'nw-dsgn-pp',
    'explorelgoutrgbox', 'gglsrcprsbox',
}
_PROMO_TABLE_RE = re.compile(
    r'clear all your doubts|join for free|\b\d+\s+videos?\s*\|\s*\d+\s+docs?'
    r'|explore courses for|edurev notes directly in your google search', re.I)
_EXTRA_CALLOUT_RE = re.compile(r'^(?:fun fact!?|do you know\??|did you know\??)\b', re.I)


def clean_text(text):
    return text.translate(_PUNCT)


def is_content_image(src):
    return bool(src and _CONTENT_IMAGE_RE.search(src))


def fallback_content_root(soup):
    semantic = soup.find('article') or soup.find('main')
    if semantic:
        return semantic
    candidates = []
    for div in soup.select('div.contenttextdiv'):
        heading_count = len(div.find_all(list(_HEADINGS)))
        block_count = len(div.find_all(['p', 'ul', 'ol']))
        if heading_count and block_count:
            candidates.append((heading_count, len(div.get_text(' ', strip=True)), div))
    if not candidates:
        return soup.body or soup
    max_headings = max(count for count, _, _ in candidates)
    return min((entry for entry in candidates if entry[0] == max_headings),
               key=lambda entry: entry[1])[2]


def is_noise_table(table):
    for node in (table, *table.parents):
        classes = ({str(value).lower() for value in node.get('class', [])}
                   if isinstance(node, Tag) else set())
        if classes & _PROMO_TABLE_CLASSES:
            return True
    return bool(_PROMO_TABLE_RE.search(table.get_text(' ', strip=True)))


def is_extra_material(node):
    """Identify optional callouts and embedded quiz widgets, not chapter prose."""
    for current in (node, *node.parents):
        if not isinstance(current, Tag):
            continue
        classes = {str(value).lower() for value in current.get('class', [])}
        if (current.get('id') == 'content_questions'
                or 'nq2_card' in classes
                or any(value.startswith('question_block_') for value in classes)):
            return True
        if current.name == 'blockquote':
            text = clean_text(current.get_text(' ', strip=True))
            if _EXTRA_CALLOUT_RE.match(text):
                return True
    return False


def find_content_root(soup):
    # Images can precede explr_htmlcnt_dv; do not restrict to that div.
    images = soup.find_all('img', src=is_content_image)
    if len(images) < 2:
        return fallback_content_root(soup)
    current = images[0].parent
    while current and current.name != 'body':
        if len(current.find_all('img', src=is_content_image)) == len(images) and current.find(['p', 'h2', 'ul', 'ol']):
            return current
        current = current.parent
    return soup.body or soup


def _segments(node):
    runs = inline.from_html(node, any(getattr(p, 'name', None) in ('strong', 'b') for p in node.parents))
    for item in runs:
        if item['kind'] == 'text': item['text'] = clean_text(item['text'])
    return runs


def _segments_text(runs):
    return re.sub(r'\s+', ' ', inline.plain(runs)).strip()


def pick_scale(width):
    return min([.25, .4, .5, .6, .75], key=lambda s: abs(s - width / 700)) if width else .6


def fit_image_scale(requested, width, height):
    """Fit an image within the balanced page box without enlarging or distorting it."""
    if width <= 0 or height <= 0:
        raise ValueError('Decoded image dimensions must be positive')
    height_limited_width = MAX_IMAGE_HEIGHT * TEXT_HEIGHT_TO_WIDTH * (width / height)
    fitted = min(requested, MAX_IMAGE_WIDTH, height_limited_width)
    return round(fitted * IMAGE_SCALE_FACTOR, 3)


def parse_html(html, base_url=''):
    soup = BeautifulSoup(html, 'html5lib')
    title = soup.title.get_text(' ', strip=True) if soup.title else ''
    if re.search(r'access denied|just a moment|sign in|log in|captcha|not found|forbidden', title, re.I) or soup.find('input', attrs={'type': 'password'}):
        raise ValueError('Blocked, login or error page; chapter content unavailable')
    root = find_content_root(soup)
    elements = []

    def image(node):
        src = node.get('src', '')
        if not is_content_image(src): return
        url = urljoin(base_url, src)
        if not url.startswith(('http://', 'https://')): raise ValueError(f'Invalid image URL: {url}')
        width = re.search(r'width:\s*([\d.]+)px', node.get('style', ''))
        width = float(width[1]) if width else float(node.get('width', 0)) if str(node.get('width', '')).isdigit() else 0
        elements.append(dict(type='image', filename=urlparse(url).path.rsplit('/', 1)[-1], url=url, scale=pick_scale(width)))

    def paragraph(node):
        # Split around images so they stay between surrounding text.
        runs = []
        def flush():
            nonlocal runs
            text = _segments_text(runs)
            if text and not _NOISE_RE.match(text): elements.append(dict(type='body', text=text, segments=runs))
            runs = []
        def visit(child):
            if getattr(child, 'name', None) == 'img':
                flush(); image(child)
            elif getattr(child, 'name', None) and child.find('img'):
                for c in child.children: visit(c)
            else:
                runs.extend(_segments(child))
        for child in node.children: visit(child)
        flush()

    def walk(node, depth=0):
        name = getattr(node, 'name', None)
        if name is None: return
        if is_extra_material(node): return
        if name in ('nav', 'footer', 'header', 'style'): return
        if name == 'img': image(node); return
        if name in _HEADINGS:
            runs = _segments(node)
            if runs and runs[0]['kind'] == 'text': runs[0]['text'] = _HEADING_NUM_RE.sub('', runs[0]['text'])
            text = _segments_text(runs)
            if text and not _NOISE_RE.match(text): elements.append(dict(type='heading', level=_HEADINGS[name], text=text, segments=runs))
            return
        if name == 'p': paragraph(node); return
        if name in ('ul', 'ol'):
            items = []
            def flush():
                nonlocal items
                if items: elements.append(dict(type='list', ordered=name == 'ol', items=items)); items = []
            for li in node.find_all('li', recursive=False):
                runs = []
                def visit_item(child):
                    nonlocal runs
                    child_name = getattr(child, 'name', None)
                    if child_name in ('ul', 'ol', 'img'):
                        if _segments_text(runs): items.append((depth, runs)); runs = []
                        flush(); walk(child, depth + 1 if child_name != 'img' else depth)
                    elif child_name and child.find(['img', 'ul', 'ol']):
                        for nested in child.children: visit_item(nested)
                    else:
                        runs.extend(_segments(child))
                for child in li.children: visit_item(child)
                if _segments_text(runs) and not _NOISE_RE.match(_segments_text(runs)): items.append((depth, runs))
            flush(); return
        if name == 'table':
            if is_noise_table(node):
                return
            if 'tbl_cntnt' in node.get('class', []) and node.find(string=re.compile(r'^\s*Table of Contents\s*$', re.I)):
                return
            if node.find('table') or any(cell.get('rowspan', '1') != '1' or cell.get('colspan', '1') != '1' for cell in node.find_all(['td', 'th'])):
                raise ValueError('Complex table spans/nesting require review; refusing to flatten cells')
            rows = [[_segments(cell) for cell in row.find_all(['td', 'th'], recursive=False)] for row in node.find_all('tr')]
            rows = [r for r in rows if r]
            if rows and 'table of contents' not in ' '.join(_segments_text(c) for r in rows for c in r).lower():
                elements.append(dict(type='table', rows=rows))
            for img in node.find_all('img'): image(img)
            return
        if name in ('math', 'mjx-container') or 'katex' in node.get('class', []) or (name == 'script' and node.get('type', '').startswith('math/tex')):
            runs = _segments(node)
            elements.append(dict(type='body', text=_segments_text(runs), segments=runs)); return
        if name == 'script': return
        for child in node.children: walk(child, depth)
    walk(root)
    if not any(e['type'] in ('body', 'list', 'table') for e in elements):
        raise ValueError('Empty chapter: no substantive content found')
    return elements


def fetch(url, cache_path=None):
    # Compatibility entry point; the primary orchestrator owns URL-keyed caches.
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'stage0'))
    from build_support import cached_fetch
    import requests
    return cached_fetch(requests.Session(), url, Path(cache_path) if cache_path else None,
                        lambda data: parse_html(data.decode('utf-8'), url)).decode('utf-8')
