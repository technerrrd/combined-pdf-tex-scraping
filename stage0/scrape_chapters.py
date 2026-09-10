"""Build complete TeX/LyX modules and both PDFs, publishing only validated results."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'stage2'))


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('module_alias', nargs='?')
    parser.add_argument('--links', type=Path, default=ROOT / 'input' / 'CHAPTER-LINKS')
    parser.add_argument('--module')
    parser.add_argument('--title')
    parser.add_argument('--chapters')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'stage2' / 'output')
    parser.add_argument('--cache-dir', type=Path, default=ROOT / 'input' / 'scraped')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--refresh', action='store_true')
    modes.add_argument('--offline', action='store_true')
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--chapter-map', type=Path)
    parser.add_argument('--coverage-threshold', type=float, default=.95)
    return parser.parse_args(argv)


def select_chapters(chapters, selection):
    numbers = [c['num'] for c in chapters]
    if len(set(numbers)) != len(numbers): raise ValueError('Duplicate chapter numbers')
    if not chapters: raise ValueError('No chapters in links file')
    if selection is None: return chapters
    selected = set()
    for token in selection.split(','):
        if not re.fullmatch(r'\d+(?:-\d+)?', token): raise ValueError('Use chapter numbers/ranges, e.g. 1,3-5')
        bounds = list(map(int, token.split('-')))
        start, end = bounds[0], bounds[-1]
        if start > end: raise ValueError('Reversed chapter range')
        if end - start > len(chapters): raise ValueError('Chapter range exceeds available chapters')
        selected.update(range(start, end + 1))
    if selected - set(numbers): raise ValueError(f'Unknown chapters: {sorted(selected - set(numbers))}')
    return [c for c in chapters if c['num'] in selected]


def module_name(args):
    if args.module and args.module_alias and args.module != args.module_alias:
        raise ValueError('Conflicting positional module and --module')
    name = args.module or args.module_alias or args.links.stem
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,99}', name) or name.upper() in {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1,10)), *(f'LPT{i}' for i in range(1,10))}:
        raise ValueError('Module must be a safe filename: letters, digits, hyphens and underscores')
    return name


def rendered_text(doc, page_range, furniture):
    """Return PDF text with page numbers and repeated document headings removed."""
    from validate_against_pdf import norm
    furniture_keys = {norm_value for value in furniture if (norm_value := norm(value))}
    lines = []
    for page_number in range(page_range['start_page'] - 1, page_range['end_page']):
        page = doc[page_number]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                stripped = ''.join(span['text'] for span in line['spans']).strip()
                normalized = norm(stripped)
                y0, y1 = line['bbox'][1], line['bbox'][3]
                in_margin = y0 < 80 or y1 > page.rect.height - 35
                if not normalized or re.fullmatch(r'\d+(?:\.\d+)*', stripped):
                    continue
                running_heading = (re.match(r'^\d*\s*chapter\s+\d+\.\s+', stripped, re.I) or
                                   re.match(r'^\d+(?:\.\d+)+\s+\S', stripped))
                if in_margin and (running_heading or normalized in furniture_keys):
                    continue
                lines.append(stripped)
    return norm('\n'.join(lines))


def check_structure(chapters, directory, module, outputs):
    import inline_content as inline
    from build_support import ValidationError, validate_image
    from validate_against_pdf import map_pdf, norm
    import pymupdf
    tex = (directory / (module + '.tex')).read_text(encoding='utf-8')
    lyx = (directory / (module + '.lyx')).read_text(encoding='utf-8')
    stats = {}
    prose = {}
    headings = {}
    images = {}
    heading_counts = {}
    list_items = 0
    for ch in chapters:
        prose[ch['num']] = []
        headings[ch['num']] = [ch['name']]
        images[ch['num']] = []
        for e in ch['elements']:
            kind = e['type']; stats[kind] = stats.get(kind, 0) + 1
            if kind == 'heading':
                heading_counts[e['level']] = heading_counts.get(e['level'], 0) + 1
                headings[ch['num']].append(inline.plain(e['segments']) if 'segments' in e else e['text'])
            if kind == 'list': list_items += len(e['items'])
            if kind == 'image':
                asset = directory / 'media' / e['filename']
                validate_image(asset.read_bytes())
                images[ch['num']].append(pymupdf.Pixmap(asset.read_bytes()).digest)
                if 'media/' + e['filename'] not in tex or 'media/' + e['filename'] not in lyx:
                    raise ValidationError(f'Missing image reference: {e["filename"]}')
            segments = []
            if 'segments' in e: segments.append(e['segments'])
            if kind == 'list': segments.extend(s for _, s in e['items'])
            if kind == 'table': segments.extend(c for r in e['rows'] for c in r if isinstance(c, list))
            for runs in segments:
                if kind != 'heading':
                    prose[ch['num']].extend(s['text'] for s in inline.adapt(runs) if s['kind'] == 'text' and len(norm(s['text'])) >= 3)
                rendered = inline.tex(runs)
                if rendered and rendered not in tex: raise ValidationError('Generated TeX lost source content')
                for s in inline.adapt(runs):
                    if s['kind'] == 'math' and inline.lyx([s]) not in lyx and s['text'].replace('\\', '\\backslash\n') not in lyx:
                        raise ValidationError('Generated LyX lost an equation')
    expected = [(r'\chapter{', len(chapters)), (r'\begin{tabular}', stats.get('table', 0))]
    for marker, count in expected:
        if tex.count(marker) < count: raise ValidationError(f'Missing structural element: {marker}')
    for level, count in heading_counts.items():
        layout = {'section':'Section', 'subsection':'Subsection', 'subsubsection':'Subsubsection'}[level]
        if tex.count('\\' + level + '{') < count or lyx.count('\\begin_layout ' + layout + '\n') < count:
            raise ValidationError(f'Missing heading structure: {level}')
    if lyx.count('\\begin_inset Tabular') < stats.get('table', 0): raise ValidationError('Generated LyX lost tables')
    if tex.count('\\item ') < list_items or sum(lyx.count('\\begin_layout ' + name + '\n') for name in ('Itemize', 'Enumerate')) < list_items:
        raise ValidationError('Generated document lost list items')
    if stats.get('list') and not any(x in lyx for x in ('\\begin_layout Itemize', '\\begin_layout Enumerate')):
        raise ValidationError('Generated LyX lost lists')
    for label, path in outputs.items():
        with pymupdf.open(path) as doc:
            ranges = map_pdf(doc, chapters, generated=True)
            for ch, r in zip(chapters, ranges):
                raw_text = norm('\n'.join(doc[p].get_text() for p in range(r['start_page']-1, r['end_page'])))
                if not raw_text: raise ValidationError(f'{label}: empty chapter {ch["num"]}')
                missing_headings = [value for value in headings[ch['num']] if norm(value) not in raw_text]
                if missing_headings: raise ValidationError(f'{label}: chapter {ch["num"]} lost headings: {missing_headings}')
                text = rendered_text(doc, r, headings[ch['num']])
                placed = [info['digest'] for p in range(r['start_page']-1, r['end_page']) for info in doc[p].get_image_info(hashes=True)]
                cursor = 0
                for digest in images[ch['num']]:
                    try: cursor = placed.index(digest, cursor) + 1
                    except ValueError as exc: raise ValidationError(f'{label}: chapter {ch["num"]} lost or reordered an image') from exc
                missing = [value for value in prose[ch['num']] if norm(value) not in text]
                if missing: raise ValidationError(f'{label}: rendered chapter {ch["num"]} lost text: {missing}')
    return stats


def build(args):
    from build_support import (BuildError, ValidationError, cached_fetch, cache_path, validate_image,
                               atomic_write, preflight, compile_documents, publish, write_report)
    from validate_against_pdf import validate_reference, NORMALIZATION
    import requests
    import html_source
    import convert
    from scrape_images import parse_links
    module = module_name(args)
    if not 0 < args.coverage_threshold <= 1: raise ValueError('Coverage threshold must be in (0,1]')
    if args.chapter_map and not args.pdf: raise ValueError('--chapter-map requires --pdf')
    if args.pdf and not args.pdf.is_file(): raise ValueError('Reference PDF does not exist')
    if not args.links.is_file(): raise ValueError('Chapter links file does not exist')
    chapters = select_chapters(parse_links(args.links), args.chapters)
    mapping = json.loads(args.chapter_map.read_text(encoding='utf-8-sig')) if args.chapter_map else None
    for ch in chapters:
        if urlparse(ch['url']).scheme not in ('http', 'https'): raise ValueError('Only HTTP(S) chapter links supported')
    output_root = args.output_dir.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=module + '-', dir=output_root))
    report = dict(status='failed', reference_status='not checked', errors=[], coverage=[], normalization=NORMALIZATION)
    try:
        programs = preflight()
        if not (convert.TEMPLATE_DIR / 'main.lyx').is_file(): raise BuildError('Required LyX template is missing')
        media = staging / 'media'; media.mkdir()
        combined = []
        with requests.Session() as session:
            session.headers.update({'User-Agent': html_source._UA})
            for ch in chapters:
                try:
                    data = cached_fetch(session, ch['url'], cache_path(args.cache_dir, ch['url'], 'pages'),
                        lambda data: html_source.parse_html(data.decode('utf-8-sig'), ch['url']), args.refresh, args.offline)
                    elements = html_source.parse_html(data.decode('utf-8-sig'), ch['url'])
                    for el in elements:
                        if el['type'] != 'image': continue
                        try:
                            image = cached_fetch(session, el['url'], cache_path(args.cache_dir, el['url'], 'images'), validate_image, args.refresh, args.offline)
                            # URL hash prevents cross-chapter basename collisions.
                            import io
                            from PIL import Image
                            with Image.open(io.BytesIO(image)) as im:
                                extension = '.png' if im.format == 'PNG' else '.jpg'
                                el['scale'] = html_source.fit_image_scale(el['scale'], im.width, im.height)
                                encoded = io.BytesIO()
                                im.convert('RGB').save(encoded, format='PNG' if extension == '.png' else 'JPEG')
                            el['filename'] = hashlib.sha256(el['url'].encode()).hexdigest() + extension
                            atomic_write(media / el['filename'], encoded.getvalue())
                        except (BuildError, ValueError, OSError) as exc:
                            report['errors'].append(f"Chapter {ch['num']} image {el['url']}: {exc}")
                    ch['elements'] = elements
                    combined.append(dict(type='heading', level='chapter', text=ch['name'], number=ch['num']))
                    combined.extend(elements)
                except (BuildError, ValueError, OSError) as exc:
                    report['errors'].append(f"Chapter {ch['num']} {ch['url']}: {exc}")
        if report['errors']: raise BuildError('Selected chapters are incomplete')
        convert.write_tex(combined, staging / (module + '.tex'), media)
        convert.write_lyx(combined, staging / (module + '.lyx'), media, template_dir=convert.TEMPLATE_DIR)
        convert.copy_template_assets(convert.TEMPLATE_DIR, staging)
        import inline_content as inline
        tex_path = staging / (module + '.tex')
        source = tex_path.read_text(encoding='utf-8').replace(r'\begin{document}', r'\usepackage{hyperref}' + '\n' + r'\begin{document}' + '\n' + r'\title{' + inline.escape(args.title or module) + r'}\maketitle')
        tex_path.write_text(source, encoding='utf-8')
        lyx_path = staging / (module + '.lyx')
        source = lyx_path.read_text(encoding='utf-8')
        source = source.replace('\\end_preamble', '\\usepackage{amsmath}\n\\end_preamble', 1)
        # Preserve the cover design while replacing its sample module and class.
        source = source.replace('centering Maths Module I', 'centering ' + inline.escape(args.title or module).replace('\\', '\\backslash\n'))
        source = source.replace('Large Class 7', 'Large \\backslash\nstrut ')
        lyx_path.write_text(source, encoding='utf-8')
        outputs = compile_documents(staging, module, programs)
        report['structure'] = check_structure(chapters, staging, module, outputs)
        if args.pdf:
            report['reference_status'] = 'failed'
            report['coverage'] = validate_reference(args.pdf, chapters, outputs, args.coverage_threshold, mapping)
            if any(r['coverage'] < args.coverage_threshold for r in report['coverage']): raise ValidationError('Reference coverage below threshold')
            report['reference_status'] = 'passed'
        manifest = dict(module=module, title=args.title or module, chapters=chapters, pdfs={k: p.name for k,p in outputs.items()})
        atomic_write(staging / 'manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
        report['status'] = 'passed'; write_report(staging, report)
        publish(staging, output_root / module)
        print(f'Published complete module: {output_root / module}')
        return 0
    except Exception as exc:
        report['status'] = 'failed'; report['errors'].append(str(exc)); write_report(staging, report)
        print(f'Build failed: {exc}\nDiagnostics: {staging}', file=sys.stderr)
        return 2 if isinstance(exc, ValidationError) else 1


def main(argv=None):
    try:
        return build(arguments(argv))
    except SystemExit as exc:
        return 0 if exc.code == 0 else 1
    except (ImportError, ValueError, OSError) as exc:
        print(f'Setup error: {exc}\nInstall requirements.txt and check command inputs.', file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
