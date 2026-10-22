import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil

import pymupdf


def hashes(directory):
    return {path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in directory.rglob('*') if path.is_file()}


def atomic_bytes(path, content):
    temporary = path.with_name(path.name + '.pending')
    temporary.write_bytes(content)
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('staging', type=Path)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('--release-dir', type=Path, default=Path('D:/Science-Book-Releases'))
    parser.add_argument('--classes', type=int, nargs='+', choices=(6, 8), default=[6, 8])
    args = parser.parse_args()
    staging, workspace, release = args.staging.resolve(), args.workspace.resolve(), args.release_dir.resolve()
    tag = datetime.now().strftime('%Y%m%d-%H%M%S')
    prepared = []
    reports = {}
    for number in dict.fromkeys(args.classes):
        module = f'Final-Science_Class{number}th'
        source = staging / module
        report = json.loads((source / 'report.json').read_text(encoding='utf-8'))
        review = json.loads((source / 'visual-review.json').read_text(encoding='utf-8'))
        if report.get('status') != 'passed' or review.get('status') != 'passed':
            raise ValueError('Publication requires build and visual acceptance: ' + module)
        manifest = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
        for label, filename in manifest['pdfs'].items():
            if hashlib.sha256((source / filename).read_bytes()).hexdigest() != review['documents'][label]['pdf_sha256']:
                raise ValueError('PDF changed after visual acceptance: ' + filename)
        reports[number] = report
        expected = hashes(source)
        destinations = [workspace / 'stage2' / 'output' / module, release / f'Science_Class{number}th']
        for destination in destinations:
            allowed = workspace / 'stage2' / 'output' if destination.is_relative_to(workspace) else release
            if destination.parent != allowed:
                raise ValueError('Publication target outside expected directory')
            destination.parent.mkdir(parents=True, exist_ok=True)
            pending = destination.with_name(destination.name + '.pending-' + tag)
            shutil.copytree(source, pending)
            if hashes(pending) != expected:
                raise ValueError('Staged copy differs: ' + str(pending))
            archive_root = (workspace / 'stage2' / ('output-obsolete-science-' + tag)
                            if destination.is_relative_to(workspace) else release / ('archive-science-' + tag))
            archive_root.mkdir(parents=True, exist_ok=True)
            prepared.append((pending, destination, archive_root / destination.name, expected))
    top_path = release / 'release-report.json'
    original_json = top_path.read_bytes()
    original_text = (release / 'release-report.txt').read_bytes()
    top = json.loads(original_json)
    promoted = []
    try:
        for pending, destination, backup, expected in prepared:
            existed = destination.exists()
            if existed:
                os.replace(destination, backup)
            try:
                os.replace(pending, destination)
            except OSError:
                if existed:
                    os.replace(backup, destination)
                raise
            promoted.append((destination, backup, existed))
            if hashes(destination) != expected:
                raise ValueError('Published copy differs: ' + str(destination))
        for number in dict.fromkeys(args.classes):
            module = f'Final-Science_Class{number}th'
            source = staging / module
            manifest = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
            pages = {}
            for label, filename in manifest['pdfs'].items():
                with pymupdf.open(source / filename) as document:
                    pages[label] = len(document)
            practice = reports[number]['structure']['practice_questions']
            item = {'class': number, 'module': f'Science_Class{number}th',
                    'chapters': [chapter['num'] for chapter in manifest['chapters']],
                    'images': reports[number]['structure'].get('image', 0), 'pages': pages,
                    'compiler_diagnostics': reports[number].get('compiler_diagnostics', []),
                    'reference_status': reports[number]['reference_status'], 'coverage': [],
                    'practice_questions': {'source_rows': practice['total_source_rows'],
                                           'rendered_items': practice['total_rendered_items'],
                                           'converted_tables': practice['converted_table_count'],
                                           'case_parts': practice['case_part_count'],
                                           'answer_lines': practice['answer_line_count']},
                    'visual_review': 'all pages inspected'}
            top['classes'] = [entry for entry in top['classes'] if entry['class'] != number] + [item]
            provenance = manifest['question_sources']
            top['source_by_class'] = [entry for entry in top.get('source_by_class', []) if entry['class'] != number] + [
                {'class': number, 'git_commit': provenance['git_commit'], 'git_dirty': provenance['git_dirty']}]
        top['classes'].sort(key=lambda entry: entry['class'])
        top['updated_at'] = datetime.now().astimezone().isoformat()
        atomic_bytes(top_path, (json.dumps(top, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
        text = ['Status: passed', 'Updated at: ' + top['updated_at']]
        text.extend(f"Class {item['class']}: chapters {item['chapters']}; pages {item['pages']}" for item in top['classes'])
        atomic_bytes(release / 'release-report.txt', ('\n'.join(text) + '\n').encode('utf-8'))
    except Exception:
        for destination, backup, existed in reversed(promoted):
            os.replace(destination, destination.with_name(destination.name + '.failed-' + tag))
            if existed:
                os.replace(backup, destination)
        atomic_bytes(top_path, original_json)
        atomic_bytes(release / 'release-report.txt', original_text)
        raise
    print('Published and hash-verified Science classes ' + str(args.classes) + '; previous versions archived: ' + tag)


if __name__ == '__main__':
    main()
