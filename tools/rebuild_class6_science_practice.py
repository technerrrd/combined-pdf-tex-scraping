"""Build the complete Class 6 Science book with all supplied worksheets."""
from __future__ import annotations

import json
import os
from pathlib import Path

import rebuild_class8_science_practice as build


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "Science-notes-links.xlsx"
QUESTIONS_DIR = Path(os.environ.get('SCIENCE_INPUT_ROOT', ROOT)) / "Class 6th Science"
CHAPTER_NUMBERS = (3, 4, 6, 7, 11, 12)
MODULE = "Final-Science_Class6th"


build.WORKBOOK = WORKBOOK
build.QUESTIONS_DIR = QUESTIONS_DIR
build.CHAPTER_NUMBERS = CHAPTER_NUMBERS
build.MODULE = MODULE
build.SOURCE_ISSUES = [{
    "chapter": 12,
    "kind": "internal_chapter_title_mismatch",
    "source": "Chapter-12-Questions-Class6th-Science.docx/pdf",
    "detail": "The internal title says Chapter 11; filename, workbook mapping, and astronomy content identify Chapter 12.",
    "resolution": "Placed under Chapter 12 without editing the supplied source files.",
}, {
    "chapter": 3,
    "kind": "duplicate_generic_prompt",
    "source_questions": [32, 33],
    "detail": "Both supplied prompts are exactly 'Match the following:' and have distinct source figures.",
    "resolution": "Both were preserved in source order.",
}, {
    "chapter": 11,
    "kind": "duplicate_generic_prompt",
    "source_questions": [34, 35],
    "detail": "Both supplied prompts are exactly 'Match the following:' and have distinct source figures.",
    "resolution": "Both were preserved in source order.",
}, {
    "chapter": 12,
    "kind": "duplicate_generic_prompt",
    "source_questions": [32, 33],
    "detail": "Both supplied prompts are exactly 'Match the following:' and have distinct source figures.",
    "resolution": "Both were preserved in source order.",
}]


def question_paths(chapter: int) -> tuple[Path, Path]:
    stem = f"Chapter-{chapter}-Questions-Class6th-Science"
    return QUESTIONS_DIR / f"{stem}.docx", QUESTIONS_DIR / f"{stem}.pdf"


def source_hashes():
    hashes = {WORKBOOK.name: build.sha256(WORKBOOK)}
    if build.tracked_sha256(Path(WORKBOOK.name)) != hashes[WORKBOOK.name]:
        raise ValueError("Workbook does not match the checked-out Git revision")
    for chapter in CHAPTER_NUMBERS:
        note = QUESTIONS_DIR / f"Chapter-{chapter}-Notes-Class6th-Science.pdf"
        hashes[note.name] = build.sha256(note)
        relative = Path("Class 6th Science") / note.name
        if build.tracked_sha256(relative) != hashes[note.name]:
            raise ValueError(f"Note source does not match the checked-out Git revision: {note.name}")
        for path in question_paths(chapter):
            hashes[path.name] = build.sha256(path)
    return hashes


build.question_paths = question_paths
build.source_hashes = source_hashes


def update_manifest():
    path = Path(os.environ.get('SCIENCE_OUTPUT_DIR', ROOT / "stage2" / "output")) / MODULE / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest.update({
        "question_image_scale": 0.5,
        "question_sources": {
            "git_commit": build.git_commit(),
            "git_dirty": True,
            "question_files_committed": False,
            "source_hashes": source_hashes(),
            "adapter_sha256": build.sha256(Path(__file__)),
            "question_layout_sha256": build.sha256(ROOT / 'stage2' / 'question_layout.py'),
            "table_manifest_sha256": build.sha256(ROOT / 'tools' / 'science_table_manifest.py'),
            "shared_adapter_sha256": build.sha256(Path(build.__file__)),
            "convert_sha256": build.sha256(ROOT / "stage2" / "convert.py"),
            "scrape_chapters_sha256": build.sha256(ROOT / "stage0" / "scrape_chapters.py"),
        },
    })
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    args = [
        "--links", str(WORKBOOK),
        "--sheet", "Class 6th",
        "--module", MODULE,
        "--title", "Class 6th Science",
        "--output-dir", os.environ.get('SCIENCE_OUTPUT_DIR', str(ROOT / "stage2" / "output")),
        "--cache-dir", os.environ.get('SCIENCE_CACHE_DIR', str(ROOT / "input" / "scraped")),
        "--offline",
    ]
    status = build.scrape_chapters.main(args)
    if status == 0:
        update_manifest()
    raise SystemExit(status)
