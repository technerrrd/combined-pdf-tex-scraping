"""Read-only completeness checks against parsed content and both generated PDFs."""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'stage2'))
import inline_content as inline
from build_support import ValidationError

ARTIFACT = re.compile(
    r'edurev|durev|^edur$|table of contents|^chapter notes\s*:|chapter notes\s*\|\s*science class|'
    r'^\d+\s*(?:of|/)\s*\d+$|^\d{2}/\d{2}/\d{2}|^https?://|^Firefox$|'
    r'^view (solution|more)|multiple choice question|^try yourself:|short-answer-questions-.*/', re.I)
NORMALIZATION = 'NFKC; ligatures; lowercase; whitespace/line-wrap joins; discretionary hyphens; equivalent math symbols; list markers and standalone bold section numbers; punctuation removal. Full normalized lines, never prefixes.'


def norm(text):
    text = unicodedata.normalize('NFKC', text).lower().replace('\u00ad', '')
    text = text.replace('◦', '°')
    text = re.sub(r'--+|[–—]', '', text)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    for symbol, macro in sorted(inline.SYMBOLS.items(), key=lambda pair: -len(pair[1])):
        text = re.sub(re.escape(macro.lower()) + r'(?![a-z])', lambda _: symbol.lower(), text)
    text = re.sub(r'\\(?:frac|dfrac|tfrac|sqrt|text|mathrm|mathbf|mathit|left|right)\b', '', text)
    text = re.sub(r'\\(?:begin|end)\{[^}]+\}', '', text)
    # Preserve operator identity: opposite inequalities/arrows are not equivalent.
    operators = {'→':' to ', '⟶':' to ', '←':' leftarrow ', '↔':' leftrightarrow ', '⇌':' rightleftharpoons ', '×':' times ', '÷':' div ', '±':' pm ', '≈':' approx ', '≤':' leq ', '≥':' geq ', '≠':' neq ', '∞':' infty ', '∴':' therefore ', '°':' circ ', '·':' cdot ', '=':' equals ', '+':' plus ', '−':' minus '}
    for symbol, word in operators.items(): text = text.replace(symbol, word)
    text = re.sub(r'[^\S\n]+', ' ', text)
    text = re.sub(r'(?<=\w)-(?=\w)', '', text)
    text = text.replace('-', ' minus ')
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    return re.sub(r'[^\w]+', '', text, flags=re.UNICODE)


def title_key(text):
    return norm(re.sub(r'^(?:chapter\s+notes\s*[:\-]?|chapter\s+\d+\s*[:.\-]?|\d+\s*[.:-]?)\s*', '', text, flags=re.I))


def text_elements(elements):
    values = []
    for e in elements:
        if e['type'] in ('body', 'heading'):
            values.append(inline.plain(e['segments']) if 'segments' in e else e['text'])
        elif e['type'] == 'list': values.extend(inline.plain(s) for _, s in e['items'])
        elif e['type'] == 'table': values.extend(inline.plain(c) if isinstance(c, list) else c for row in e['rows'] for c in row)
    return '\n'.join(values)


def validate_ranges(entries, chapters, pages):
    expected = [c['num'] for c in chapters]
    if not isinstance(entries, list): raise ValidationError('Chapter map must be a JSON list')
    selected = []
    seen = set()
    previous = 0
    for entry in entries:
        if not isinstance(entry, dict) or any(type(entry.get(k)) is not int for k in ('chapter', 'start_page', 'end_page')):
            raise ValidationError('Map entries require integer chapter, start_page, end_page')
        number, start, end = entry['chapter'], entry['start_page'], entry['end_page']
        if number in seen or not (1 <= start <= end <= pages) or start <= previous:
            raise ValidationError('Invalid, duplicate, overlapping or unordered chapter ranges')
        seen.add(number); previous = end
        if number in expected: selected.append(entry)
    if [r['chapter'] for r in selected] != expected: raise ValidationError('Chapter map does not match selected chapter order')
    return selected


def map_pdf(doc, chapters, explicit=None, generated=False):
    if explicit is not None: return validate_ranges(explicit, chapters, len(doc))
    markers = []
    # Generated PDFs carry chapter bookmarks. Reference PDFs may carry them too.
    for level, title, page, *_ in doc.get_toc():
        if level == 1 and page > 0: markers.append((page, title))
    if not markers and not generated:
        for i, page in enumerate(doc):
            for block in page.get_text('dict')['blocks']:
                lines = block.get('lines', [])
                block_text = ' '.join(''.join(s['text'] for s in l['spans']) for l in lines)
                if re.match(r'chapter\s+(?:notes\s*[:\-]|\d+\b)', block_text, re.I):
                    markers.append((i + 1, block_text))
    markers = sorted(set(markers), key=lambda x: x[0])
    matches = []
    for ch in chapters:
        candidates = [(p, t) for p, t in markers if title_key(t) == title_key(ch['name']) or
                      (not generated and re.match(rf'^chapter\s+{ch["num"]}(?:\D|$)', t, re.I))]
        if len(candidates) != 1:
            raise ValidationError(f"Ambiguous PDF mapping for chapter {ch['num']} ({ch['name']}); provide --chapter-map for the reference PDF")
        start, _ = candidates[0]
        later = [p for p, _ in markers if p > start]
        matches.append(dict(chapter=ch['num'], start_page=start, end_page=min(later) - 1 if later else len(doc)))
    return validate_ranges(matches, chapters, len(doc))


def coverage(lines, target, chapter, label, page_range):
    normalized = norm(target)
    lines = [re.sub(r'^\s*(?:\d+\.|[a-zA-Z][.)])\s+', '', line) for line in lines]
    usable = [line for line in lines if norm(line) and not ARTIFACT.search(line.strip()) and not re.fullmatch(r'chapter\s+\d+', line.strip(), re.I)]
    if not usable: raise ValidationError(f'Chapter {chapter}: no extractable reference text; OCR is not performed')
    unmatched = [line for line in usable if norm(line) not in normalized]
    present = len(usable) - len(unmatched)
    return dict(chapter=chapter, target=label, present=present, total=len(usable), coverage=present / len(usable), unmatched=unmatched, page_range=page_range)


def reference_lines(page):
    lines = []
    in_quiz = False
    positioned = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            value = ''.join(span['text'] for span in line['spans']).strip()
            y0, y1 = line['bbox'][1], line['bbox'][3]
            positioned.append((y0, line['bbox'][0], y1, value, line))
    for y0, _, y1, value, line in sorted(positioned):
        if re.search(r'multiple choice question|^try yourself:', value, re.I):
            in_quiz = True
        if in_quiz:
            if re.match(r'^view solution', value, re.I): in_quiz = False
            continue
        if value:
            if value.isdigit() and (y0 < 45 or y1 > page.rect.height - 55): continue
            if re.fullmatch(r'\d+(?:\.\d+)+', value) and any(span['size'] > 13 or 'bold' in span['font'].lower() for span in line['spans']): continue
            lines.append(value)
    return lines


def generated_text(doc, page_range):
    lines = []
    for page_number in range(page_range['start_page'] - 1, page_range['end_page']):
        page = doc[page_number]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                value = ''.join(span['text'] for span in line['spans']).strip()
                y0, y1 = line['bbox'][1], line['bbox'][3]
                in_margin = y0 < 80 or y1 > page.rect.height - 35
                running_heading = (re.match(r'^\d*\s*chapter\s+\d+\.\s+', value, re.I) or
                                   re.match(r'^\d+(?:\.\d+)+\s+\S', value))
                if re.fullmatch(r'\d+', value) or (in_margin and running_heading): continue
                if value: lines.append(value)
    return '\n'.join(lines)


def validate_reference(reference, chapters, outputs, threshold=.95, mapping=None):
    import pymupdf
    rows = []
    with pymupdf.open(reference) as ref:
        ranges = map_pdf(ref, chapters, mapping)
        source = {}
        for r in ranges:
            source[r['chapter']] = ([line for p in range(r['start_page']-1, r['end_page']) for line in reference_lines(ref[p])], r)
        for ch in chapters:
            lines, r = source[ch['num']]
            rows.append(coverage(lines, ch['name'] + '\n' + text_elements(ch['elements']), ch['num'], 'parsed', r))
        for label, path in outputs.items():
            with pymupdf.open(path) as generated:
                output_ranges = map_pdf(generated, chapters, generated=True)
                for r in output_ranges:
                    lines, source_range = source[r['chapter']]
                    text = generated_text(generated, r)
                    rows.append(coverage(lines, text, r['chapter'], label, source_range))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--chapter-map', type=Path)
    parser.add_argument('--coverage-threshold', type=float, default=.95)
    args = parser.parse_args(argv)
    report = dict(status='failed', reference_status='failed', errors=[])
    try:
        if not 0 < args.coverage_threshold <= 1: raise ValidationError('Threshold must be in (0,1]')
        manifest = json.loads((args.build_dir / 'manifest.json').read_text(encoding='utf-8'))
        mapping = json.loads(args.chapter_map.read_text(encoding='utf-8-sig')) if args.chapter_map else None
        outputs = {k: args.build_dir / v for k, v in manifest['pdfs'].items()}
        rows = validate_reference(args.pdf, manifest['chapters'], outputs, args.coverage_threshold, mapping)
        report.update(coverage=rows, normalization=NORMALIZATION)
        if any(r['coverage'] < args.coverage_threshold for r in rows): raise ValidationError('Reference coverage below threshold')
        report.update(status='passed', reference_status='passed')
    except (ValueError, OSError, ValidationError) as exc:
        report['errors'].append(str(exc))
    # Separate report name preserves the original build acceptance record.
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['status'] == 'passed' else 2


if __name__ == '__main__': raise SystemExit(main())
