"""Build the supplied Class 7 Science chapters as a validated LyX-only book."""
from __future__ import annotations

import json
import os
from pathlib import Path

import rebuild_class8_science_practice as build

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / 'Science-notes-links.xlsx'
QUESTIONS_DIR = Path(os.environ.get('SCIENCE_INPUT_ROOT', ROOT)) / 'Class 7th Science'
CHAPTER_NUMBERS = (4, 5, 6, 7, 8, 9)
MODULE = 'Final-Science_Class7th'

build.WORKBOOK = WORKBOOK
build.QUESTIONS_DIR = QUESTIONS_DIR
build.CHAPTER_NUMBERS = CHAPTER_NUMBERS
build.MODULE = MODULE
build.QUESTION_HEADINGS = {
    'Very Short Questions': 'Very Short Answer Questions',
    'Short Questions': 'Short Question Answers',
    'Long Questions': 'Descriptive Answer Questions',
    'Very Long Questions': 'Long Answer Questions',
}
build.ANSWER_LINES_FROM_MARKS = True
build.TRUE_FALSE_INLINE_BLANKS = True
build.SOURCE_ISSUES = [{
    'chapter': chapter, 'kind': 'duplicate_generic_prompt',
    'source_questions': [35, 36],
    'detail': 'Both prompts say Match the following: with distinct supplied native tables.',
    'resolution': 'Both tables and prompts are preserved in source order.',
} for chapter in CHAPTER_NUMBERS] + [{
    'chapter': 5, 'kind': 'supplied_typo', 'source_questions': [11],
    'detail': 'Both Physical change andChange in size only',
    'resolution': 'Retained the supplied wording without correction.',
}]


def question_paths(chapter):
    stem = f'Chapter-{chapter}-Questions-Class7th-Science'
    return QUESTIONS_DIR / (stem + '.docx'), QUESTIONS_DIR / (stem + '.pdf')


def source_hashes():
    hashes = {WORKBOOK.name: build.sha256(WORKBOOK)}
    if build.tracked_sha256(Path(WORKBOOK.name)) != hashes[WORKBOOK.name]:
        raise ValueError('Workbook differs from the checked-out revision')
    for chapter in CHAPTER_NUMBERS:
        note = QUESTIONS_DIR / f'Chapter-{chapter}-Notes-Class7th-Science.pdf'
        hashes[note.name] = build.sha256(note)
        for path in question_paths(chapter):
            hashes[path.name] = build.sha256(path)
    return hashes


build.question_paths = question_paths
build.source_hashes = source_hashes


def main():
    before = source_hashes()
    output = Path(os.environ.get('SCIENCE_OUTPUT_DIR', ROOT / 'tmp' / 'class7-staged'))
    args = [
        '--links', str(WORKBOOK), '--sheet', 'Class 7th',
        '--chapters', ','.join(map(str, CHAPTER_NUMBERS)),
        '--module', MODULE, '--title', 'Class 7th Science',
        '--output-dir', str(output),
        '--cache-dir', os.environ.get('SCIENCE_CACHE_DIR', str(ROOT / 'input' / 'scraped')),
        '--offline', '--lyx-only',
    ]
    status = build.scrape_chapters.main(args)
    if status:
        return status
    if source_hashes() != before:
        raise ValueError('Supplied sources changed during build')
    path = output / MODULE / 'manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    manifest['question_image_scale'] = .5
    manifest['source'] = {'git_commit': build.git_commit(), 'git_dirty': True}
    manifest['question_sources'] = {
        'git_commit': build.git_commit(), 'git_dirty': True,
        'question_files_committed': all(
            build.tracked_sha256(Path(QUESTIONS_DIR.name) / source.name) == build.sha256(source)
            for chapter in CHAPTER_NUMBERS for source in question_paths(chapter)),
        'source_hashes': before,
        'adapter_sha256': build.sha256(Path(__file__)),
        'shared_adapter_sha256': build.sha256(Path(build.__file__)),
        'question_layout_sha256': build.sha256(ROOT / 'stage2' / 'question_layout.py'),
        'table_manifest_sha256': build.sha256(ROOT / 'tools' / 'science_table_manifest.py'),
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
