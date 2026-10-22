import argparse
import hashlib
import json
from pathlib import Path

import pymupdf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('book', type=Path)
    parser.add_argument('review', type=Path)
    args = parser.parse_args()
    manifest = json.loads((args.book / 'manifest.json').read_text(encoding='utf-8'))
    acceptance = {'status': 'passed', 'scope': 'Every PDF page inspected; corrected question formatting accepted',
                  'documents': {}, 'legacy_observations': []}
    for label, filename in manifest['pdfs'].items():
        record = json.loads((args.review / f'review-{label}.json').read_text(encoding='utf-8'))
        if record.get('status') != 'passed':
            raise ValueError('Visual review did not pass: ' + label)
        with pymupdf.open(args.book / filename) as document:
            page_count = len(document)
        pages = record['pages_reviewed']
        if [item['page'] for item in pages] != list(range(1, page_count + 1)):
            raise ValueError('Visual review does not cover every page: ' + label)
        for item in pages:
            png = args.review / Path(filename).stem / f"page-{item['page']:03}.png"
            actual = hashlib.sha256(png.read_bytes()).hexdigest()
            if actual != item['sha256']:
                raise ValueError('A page changed after visual review: ' + str(png))
        acceptance['documents'][label] = {'pages': page_count, 'page_reviews': pages,
                                           'pdf_sha256': hashlib.sha256((args.book / filename).read_bytes()).hexdigest()}
        acceptance['legacy_observations'].extend(record.get('legacy_observations', record.get('observations', [])))
    (args.book / 'visual-review.json').write_text(json.dumps(acceptance, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    path = args.book / 'report.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    report['visual_review'] = {'status': 'passed', 'all_pages_inspected': True,
                               'pages': {label: item['pages'] for label, item in acceptance['documents'].items()},
                               'legacy_observations': acceptance['legacy_observations']}
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    with (args.book / 'report.txt').open('a', encoding='utf-8') as stream:
        stream.write('\nVisual review: every final PDF page inspected; corrected question layouts passed.\n')
    print(json.dumps(report['visual_review'], indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
