"""Read-only source audit for the Class 6 Science question pairs."""
from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import rebuild_class6_science_practice as class6


def main():
    build = class6.build
    media = ROOT / "tmp" / "class6-science-audit-media"
    chapters = build.workbook_rows(class6.WORKBOOK, "Class 6th")
    result = {"chapters": {}, "source_issues": []}
    for chapter in class6.CHAPTER_NUMBERS:
        docx_path, pdf_path = class6.question_paths(chapter)
        document = build.Document(docx_path)
        rows = [row for row in document.tables[1].rows if row.cells[0].text.strip().isdigit()]
        duplicates = defaultdict(list)
        for row in rows:
            number, lines, _marks = build.row_question(row)
            duplicates[build.clean(" ".join(lines))].append(number)
        _elements, _expected, metadata = build.practice_elements(chapter, media)
        with build.pymupdf.open(pdf_path) as pdf:
            pdf_title = build.clean(pdf[0].get_text())[:500]
            pdf_pages = len(pdf)
        docx_title = build.clean(" ".join(cell.text for cell in document.tables[0].rows[0].cells))
        exact_duplicates = [
            {"questions": numbers, "text": text}
            for text, numbers in duplicates.items()
            if len(numbers) > 1
        ]
        result["chapters"][str(chapter)] = {
            **metadata,
            "docx_internal_title": docx_title,
            "pdf_first_page_text": pdf_title,
            "pdf_pages": pdf_pages,
            "exact_duplicate_prompts": exact_duplicates,
        }
        for duplicate in exact_duplicates:
            result["source_issues"].append({
                "chapter": chapter,
                "kind": "duplicate_prompt",
                **duplicate,
            })
    result["workbook_chapters"] = [item["num"] for item in chapters]
    result["total_source_rows"] = sum(
        item["source_rows"] for item in result["chapters"].values()
    )
    result["total_rendered_items"] = sum(
        item["rendered_items"] for item in result["chapters"].values()
    )
    result["total_question_figures"] = sum(
        item["source_figures"] for item in result["chapters"].values()
    )
    output = ROOT / "tmp" / "class6_science_source_audit.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
