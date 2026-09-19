"""Build the Class 6-8 Science books as one atomic external release."""
import argparse
import json
import os
from pathlib import Path
import re
import tempfile
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pymupdf

from build_support import atomic_write, publish
import scrape_chapters


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE_DIR = Path(os.environ.get(
    'SCIENCE_RELEASE_DIR',
    'D:/Science-Book-Releases' if os.name == 'nt' else ROOT.parent / 'Science-Book-Releases'))
CLASSES = {
    6: {'sheet': 'Class 6th', 'module': 'Science_Class6th', 'title': 'Science Class 6th'},
    7: {'sheet': 'Class 7th', 'module': 'Science_Class7th', 'title': 'Science Class 7th'},
    8: {'sheet': 'Class 8th', 'module': 'Science_Class8th', 'title': 'Science Class 8th'},
}
MAIN_NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG_REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workbook', type=Path, default=ROOT / 'Science-notes-links.xlsx')
    parser.add_argument('--release-dir', type=Path, default=DEFAULT_RELEASE_DIR)
    parser.add_argument('--cache-dir', type=Path, default=ROOT / 'input' / 'scraped')
    parser.add_argument('--classes', default='6,7,8', help='Comma-separated subset of 6,7,8')
    parser.add_argument('--image-scale', type=float, default=.75)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--refresh', action='store_true')
    modes.add_argument('--offline', action='store_true')
    parser.add_argument('--reference', action='append', default=[], metavar='CLASS=PDF',
                        help='Optional combined reference PDF for a class; repeat as needed')
    parser.add_argument('--chapter-map', action='append', default=[], metavar='CLASS=JSON',
                        help='Optional chapter map matching a --reference class')
    parser.add_argument('--coverage-threshold', type=float, default=.95)
    return parser.parse_args(argv)


def keyed_paths(values, option):
    result = {}
    for value in values:
        match = re.fullmatch(r'([678])=(.+)', value)
        if not match: raise ValueError(f'{option} must use CLASS=PATH with class 6, 7, or 8')
        class_number = int(match.group(1))
        if class_number in result: raise ValueError(f'Duplicate {option} for class {class_number}')
        result[class_number] = Path(match.group(2)).resolve()
    return result


def selected_classes(value):
    try: selected = [int(item.strip()) for item in value.split(',') if item.strip()]
    except ValueError as exc: raise ValueError('--classes must contain only 6,7,8') from exc
    if not selected or len(selected) != len(set(selected)) or set(selected) - set(CLASSES):
        raise ValueError('--classes must be a unique comma-separated subset of 6,7,8')
    return selected


def _shared_strings(archive):
    root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
    return [''.join(node.text or '' for node in item.iter(f'{{{MAIN_NS}}}t'))
            for item in root.findall(f'{{{MAIN_NS}}}si')]


def workbook_rows(path, wanted_sheets):
    """Read the simple chapter/url worksheets with the Python standard library."""
    with ZipFile(path) as archive:
        strings = _shared_strings(archive)
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        relationships = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        targets = {node.attrib['Id']: node.attrib['Target'] for node in relationships}
        sheets = {}
        for node in workbook.find(f'{{{MAIN_NS}}}sheets'):
            name = node.attrib['name']
            relation = node.attrib[f'{{{REL_NS}}}id']
            sheets[name] = 'xl/' + targets[relation].lstrip('/')
        missing = set(wanted_sheets) - set(sheets)
        if missing: raise ValueError('Workbook is missing sheets: ' + ', '.join(sorted(missing)))
        result = {}
        for name in wanted_sheets:
            sheet = ET.fromstring(archive.read(sheets[name]))
            rows = []
            for row in sheet.findall(f'.//{{{MAIN_NS}}}row'):
                values = {}
                for cell in row.findall(f'{{{MAIN_NS}}}c'):
                    column = re.match(r'[A-Z]+', cell.attrib['r']).group()
                    value = cell.find(f'{{{MAIN_NS}}}v')
                    if value is None: continue
                    text = strings[int(value.text)] if cell.attrib.get('t') == 's' else value.text
                    values[column] = text.strip()
                if re.search(r'\d+', values.get('A', '')) and values.get('B', '').startswith(('http://', 'https://')):
                    rows.append((int(re.search(r'\d+', values['A']).group()), values['B']))
            if not rows or len({number for number, _ in rows}) != len(rows):
                raise ValueError(f'{name} has missing or duplicate chapter rows')
            result[name] = rows
        return result


def release_summary(staging, class_numbers, image_scale):
    source = scrape_chapters.source_revision()
    result = {'status': 'passed', 'source': source, 'image_scale': image_scale, 'classes': []}
    for class_number in class_numbers:
        module = CLASSES[class_number]['module']
        directory = staging / module
        manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
        report = json.loads((directory / 'report.json').read_text(encoding='utf-8'))
        pages = {}
        for label, filename in manifest['pdfs'].items():
            with pymupdf.open(directory / filename) as document: pages[label] = len(document)
        image_count = sum(1 for chapter in manifest['chapters'] for item in chapter['elements'] if item['type'] == 'image')
        result['classes'].append({
            'class': class_number, 'module': module,
            'chapters': [chapter['num'] for chapter in manifest['chapters']],
            'images': image_count, 'pages': pages,
            'compiler_diagnostics': report.get('compiler_diagnostics', []),
            'reference_status': report.get('reference_status', 'not checked'),
            'coverage': report.get('coverage', []),
        })
    return result


def write_release_report(staging, report):
    atomic_write(staging / 'release-report.json', json.dumps(report, indent=2, ensure_ascii=False).encode('utf-8'))
    lines = [f"Status: {report['status']}", f"Git commit: {report.get('source', {}).get('git_commit')}",
             f"Git dirty: {report.get('source', {}).get('git_dirty')}", f"Image scale: {report.get('image_scale')}"]
    for item in report.get('classes', []):
        lines.append(f"Class {item['class']}: chapters {item['chapters']}; images {item['images']}; pages {item['pages']}; reference {item['reference_status']}")
        for diagnostic in item['compiler_diagnostics']:
            lines.append(f"  {diagnostic['severity'].upper()} [{diagnostic['document']}/{diagnostic['kind']}]: {diagnostic['message']}")
    lines.extend(report.get('errors', []))
    atomic_write(staging / 'release-report.txt', '\n'.join(lines).encode('utf-8'))


def main(argv=None):
    args = arguments(argv)
    try:
        classes = selected_classes(args.classes)
        if not 0 < args.image_scale <= 1: raise ValueError('--image-scale must be in (0,1]')
        if not args.workbook.is_file(): raise ValueError('Workbook does not exist')
        references = keyed_paths(args.reference, '--reference')
        chapter_maps = keyed_paths(args.chapter_map, '--chapter-map')
        if set(chapter_maps) - set(references): raise ValueError('--chapter-map requires a matching --reference')
        rows = workbook_rows(args.workbook, [CLASSES[number]['sheet'] for number in classes])
        destination = args.release_dir.resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=destination.name + '-', dir=destination.parent))
        with tempfile.TemporaryDirectory(prefix='science-links-') as links_root:
            links_root = Path(links_root)
            for number in classes:
                config = CLASSES[number]
                links = links_root / f'class-{number}.txt'
                links.write_text('\n'.join(f'{url} - Chapter{chapter}' for chapter, url in rows[config['sheet']]) + '\n', encoding='utf-8')
                build_args = ['--links', str(links), '--module', config['module'], '--title', config['title'],
                              '--output-dir', str(staging), '--cache-dir', str(args.cache_dir),
                              '--coverage-threshold', str(args.coverage_threshold), '--image-scale', str(args.image_scale)]
                if args.offline: build_args.append('--offline')
                if args.refresh: build_args.append('--refresh')
                if number in references: build_args.extend(['--pdf', str(references[number])])
                if number in chapter_maps: build_args.extend(['--chapter-map', str(chapter_maps[number])])
                code = scrape_chapters.main(build_args)
                if code: raise RuntimeError(f'Class {number} build failed with exit code {code}')
        report = release_summary(staging, classes, args.image_scale)
        write_release_report(staging, report)
        publish(staging, destination)
        print(f'Published Science release: {destination}')
        return 0
    except Exception as exc:
        report = {'status': 'failed', 'source': scrape_chapters.source_revision(),
                  'image_scale': getattr(args, 'image_scale', None), 'classes': [], 'errors': [str(exc)]}
        if 'staging' in locals() and staging.exists(): write_release_report(staging, report)
        print(f'Release failed: {exc}', file=os.sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
