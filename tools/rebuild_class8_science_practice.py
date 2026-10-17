"""Build a complete Science book with supplied chapter worksheets."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "stage0"))
sys.path.insert(0, str(ROOT / "stage2"))

import chapter_sources
import scrape_chapters
from docx import Document
from docx.oxml.ns import qn
import pymupdf
from PIL import Image
from convert import pick_scale

WORKBOOK = ROOT / "Science-notes-links.xlsx"
QUESTIONS_DIR = ROOT / "Class 8th Science"
CHAPTER_NUMBERS = (3, 4, 7, 8, 9, 10, 12)
MODULE = "Science_Class8th"


def workbook_rows(path: Path, sheet_name: str):
    """Read the small source map from OOXML, avoiding a missing openpyxl install."""
    ns = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "pkg": "http://schemas.openxmlformats.org/package/2006/relationships",
    }
    with zipfile.ZipFile(path) as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {item.attrib["Id"]: item.attrib["Target"] for item in relationships}
        selected = next((item for item in workbook.find("main:sheets", ns)
                         if item.attrib["name"] == sheet_name), None)
        if selected is None:
            raise ValueError(f"Workbook sheet not found: {sheet_name}")
        target = targets[selected.attrib[f"{{{ns['rel']}}}id"]]
        worksheet_path = (target.lstrip("/") if target.startswith("/")
                          else posixpath.normpath(posixpath.join("xl", target)))
        shared_strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = ["".join(node.text or "" for node in item.iter(f"{{{ns['main']}}}t"))
                              for item in shared_root]
        worksheet = ET.fromstring(archive.read(worksheet_path))

        def cell_value(cell):
            kind = cell.attrib.get("t")
            if kind == "inlineStr":
                return "".join(node.text or "" for node in cell.iter(f"{{{ns['main']}}}t"))
            value = cell.find("main:v", ns)
            if value is None or value.text is None:
                return ""
            if kind == "s":
                return shared_strings[int(value.text)]
            return value.text

        rows = []
        for row in worksheet.findall(".//main:sheetData/main:row", ns):
            cells = {}
            for cell in row.findall("main:c", ns):
                col = re.match(r"[A-Z]+", cell.attrib["r"]).group()
                cells[col] = cell_value(cell)
            rows.append(cells)
        if not rows:
            raise ValueError(f"Workbook sheet is empty: {sheet_name}")
        headers = tuple(rows[0].get(col, "").strip() for col in "ABCDE")
        if headers[:2] in {
            ("Chapter", "Chapter Links"),
            ("Chapters", "Science Links"),
        } and not any(headers[2:]):
            chapters = []
            for row_number, row in enumerate(rows[1:], start=2):
                label = row.get("A", "").strip()
                link = row.get("B", "").strip()
                if not label and not link:
                    continue
                if not label or not link:
                    raise ValueError(f"Workbook row {row_number} has a missing chapter or link")
                match = re.search(r"chapter\s*[- ]?\s*(\d+)", label, re.I)
                if not match:
                    raise ValueError(f"Workbook row {row_number} has no chapter number: {label}")
                number = int(match.group(1))
                url = chapter_sources.normalize_edurev_url(link, "/t/")
                slug_match = re.search(r"/t/\d+/([^/#?]+)", url)
                title = re.sub(r"^Chapter-Notes-", "", slug_match.group(1), flags=re.I) if slug_match else ""
                title = title.replace("-", " ").strip()
                chapters.append({"num": number, "name": title or label,
                                 "url": url, "formula_url": url, "infographic_url": None})
            if not chapters:
                raise ValueError(f"Workbook sheet has no chapter rows: {sheet_name}")
            return chapters
        expected = chapter_sources.WORKBOOK_HEADERS
        duplicate_name = headers == ("Chapter Name",) + expected
        if headers[:4] != expected and not duplicate_name:
            raise ValueError(f"Unexpected Science workbook headers: {headers!r}")
        chapters = []
        for row_number, row in enumerate(rows[1:], start=2):
            values = [row.get(col, "").strip() for col in "ABCD"]
            if duplicate_name:
                values = [row.get(col, "").strip() for col in "BCDE"]
                if row.get("A", "").strip():
                    values[0] = row["A"].strip()
            if not any(values):
                continue
            if any(not value for value in values[:3]):
                raise ValueError(f"Workbook row {row_number} has a missing required value")
            name, label, formula, infographic = values
            match = re.fullmatch(r"Chapter-(\d+)", label, re.I)
            if not match:
                raise ValueError(f"Invalid chapter number in workbook row {row_number}: {label}")
            number = int(match.group(1))
            if name.casefold() == "periimeter and area":
                name = "Perimeter and Area"
            chapters.append({
                "num": number,
                "name": name,
                "url": chapter_sources.normalize_edurev_url(formula, "/t/"),
                "formula_url": chapter_sources.normalize_edurev_url(formula, "/t/"),
                "infographic_url": chapter_sources.normalize_edurev_url(infographic, "/p/") if infographic else None,
            })
        if not chapters:
            raise ValueError(f"Workbook sheet has no chapter rows: {sheet_name}")
        return chapters


original_parse_sources = chapter_sources.parse_chapter_sources


def parse_sources(path, sheet=None):
    if Path(path).suffix.lower() == ".xlsx":
        return workbook_rows(Path(path), sheet)
    return original_parse_sources(path, sheet)


chapter_sources.parse_chapter_sources = parse_sources


def clean(text: str) -> str:
    text = text.replace("\u00ad", "").replace("\u2006", " ")
    text = re.sub(r"\s*-\s+", "-", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def without_mark_annotation(text: str) -> str:
    """Remove a trailing mark value embedded in a worksheet prompt."""
    return re.sub(r"\s*\(\d+\)\s*$", "", clean(text))


def body(text: str, bold=False, page_break_before=False):
    element = {"type": "body", "segments": [(clean(text), bool(bold))]}
    if page_break_before:
        element["page_break_before"] = True
    return element


def heading(text: str, level="subsection"):
    return {"type": "heading", "level": level, "text": clean(text)}


def compact(value: str) -> str:
    value = value.translate({1: "fl", 2: "fi", 3: "fl"})
    value = value.replace("ﬂ", "fl").replace("ﬁ", "fi").replace("ﬀ", "ff")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def fuzzy_present(target: str, source: str) -> bool:
    if target in source:
        return True
    search_at = 0
    while True:
        start = source.find(target[:25], search_at)
        if start < 0:
            return False
        cursor = start
        for char in target:
            cursor = source.find(char, cursor)
            if cursor < 0:
                break
            cursor += 1
        if cursor >= 0 and cursor - start <= len(target) * 2 + 250:
            return True
        search_at = start + 1


def question_paths(chapter: int) -> tuple[Path, Path]:
    stem = f"Chapter-{chapter}-Questions-Class8th-Science"
    return QUESTIONS_DIR / f"{stem}.docx", QUESTIONS_DIR / f"{stem}.pdf"


def row_question(row):
    number = int(row.cells[0].text.strip())
    lines = [clean(line) for line in row.cells[1].text.splitlines() if clean(line)]
    marks = row.cells[2].text.strip()
    if not lines:
        raise ValueError(f"Question {number} has no text")
    return number, lines, marks


def labeled_options(lines, question_number):
    options = []
    current = None
    question_lines = []
    for line in lines:
        match = re.match(r"^([a-d])[.)]\s*(.*)$", line, re.I)
        if match:
            if current is not None:
                options.append(current)
            current = match.group(2).strip()
        elif current is None:
            question_lines.append(line)
        else:
            current += " " + line
    if current is not None:
        options.append(current.strip())
    if len(options) != 4:
        raise ValueError(
            f"Question {question_number} must have four supplied options; found {len(options)}"
        )
    return question_lines, options


def source_pdf_audit(document: Document, pdf_path: Path) -> int:
    with pymupdf.open(pdf_path) as reader:
        pdf_text = compact("\n".join(page.get_text() for page in reader))
    checks = []
    for table in document.tables:
        for node in table._tbl.iter(qn("w:t")):
            value = node.text or ""
            target = compact(value)
            if len(target) >= 8:
                checks.append((value, target))
    missing = [value for value, target in checks if not fuzzy_present(target, pdf_text)]
    if missing:
        raise ValueError(
            f"{pdf_path.name}: {len(missing)} DOCX text fragments are absent from the supplied PDF: "
            f"{missing[:8]}"
        )
    return len(checks)


def paragraph_images(document: Document, paragraph, media_dir: Path, chapter: int):
    images = []
    extent = paragraph._element.find(f".//{qn('wp:extent')}")
    try:
        cx_emu = int(extent.get("cx", "0")) if extent is not None else 0
    except (TypeError, ValueError):
        cx_emu = 0
    base_scale = pick_scale(cx_emu)
    for blip in paragraph._element.iter(qn("a:blip")):
        rid = blip.get(qn("r:embed"))
        if not rid or rid not in document.part.related_parts:
            raise ValueError(f"Chapter {chapter}: unresolved question image relationship {rid!r}")
        part = document.part.related_parts[rid]
        filename = f"ch{chapter}_questions_{rid}.png"
        target = media_dir / filename
        media_dir.mkdir(parents=True, exist_ok=True)
        with Image.open(BytesIO(part.blob)) as opened:
            rendered = opened.convert("RGB")
            if target.exists():
                with Image.open(target) as existing:
                    if existing.convert("RGB").tobytes() != rendered.tobytes():
                        raise ValueError(f"Question image collision: {filename}")
            else:
                rendered.save(target, format="PNG", optimize=True)
        images.append({
            "type": "image",
            "filename": filename,
            "scale": base_scale * 0.5,
            "base_scale": base_scale,
            "sha256": hashlib.sha256(part.blob).hexdigest(),
        })
    return images


def row_events(document: Document, row, media_dir: Path, chapter: int):
    events = []
    for paragraph in row.cells[1].paragraphs:
        for line in paragraph.text.splitlines():
            line = clean(line)
            if line:
                events.append(("text", line))
        for image in paragraph_images(document, paragraph, media_dir, chapter):
            events.append(("image", image))
    return events


def classify_question(lines, marks, number):
    first = lines[0].casefold()
    if first.startswith("state whether the given statement is true or false"):
        return "True or False"
    if first.startswith("fill in the blanks"):
        return "Fill in the Blanks"
    option_lines = [line for line in lines if re.match(r"^[a-d][.)]\s*", line, re.I)]
    if option_lines:
        if first.startswith("assertion (a):"):
            return "Assertion and Reason"
        return "Multiple Choice Questions"
    if first.startswith("match"):
        return "Match the Following"
    match = re.search(r"\d+", marks)
    if not match:
        raise ValueError(f"Question {number} has no numeric mark value")
    return {
        1: "Very Short Questions",
        2: "Short Questions",
        3: "Long Questions",
        4: "Case-Based Questions",
        5: "Very Long Questions",
    }.get(int(match.group()), "")


SOURCE_ISSUES = [{
    "chapter": 4,
    "kind": "internal_chapter_title_mismatch",
    "source": "Chapter-4-Questions-Class8th-Science.docx/pdf",
    "detail": "The internal title says Chapter 3; filename, workbook mapping, and electricity content identify Chapter 4.",
    "resolution": "Placed under Chapter 4 with the user's explicit confirmation; source files were not edited.",
}, {
    "chapter": 3,
    "kind": "duplicate_generic_prompt",
    "source_questions": [31, 32],
    "detail": "Both supplied prompts are exactly 'Match the following:' and have distinct source figures.",
    "resolution": "Both were preserved in source order.",
}]

original_download_images = scrape_chapters.download_content_images
original_check_structure = scrape_chapters.check_structure
questions_inserted = set()
expected_practice_text = {}
question_metadata = {}
question_images = []


def practice_elements(chapter: int, media_dir: Path):
    docx_path, pdf_path = question_paths(chapter)
    document = Document(docx_path)
    if len(document.tables) < 2:
        raise ValueError(f"{docx_path.name} does not contain its question table")
    pdf_checks = source_pdf_audit(document, pdf_path)
    rows = [row for row in document.tables[1].rows if row.cells[0].text.strip().isdigit()]
    numbers = [int(row.cells[0].text.strip()) for row in rows]
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"Chapter {chapter}: question rows are not contiguous: {numbers}")

    result = [{"type": "heading", "level": "section", "text": "Practice Questions",
               "page_break_before": True}]
    expected = []
    current_heading = None
    block_number = 0
    type_counts = Counter()
    rendered_item_counts = Counter()
    local_images = []

    def ensure_heading(title):
        nonlocal current_heading, block_number
        if not title:
            raise ValueError(f"Chapter {chapter}: unsupported question type")
        if current_heading != title:
            result.append(heading(title))
            expected.append(title)
            current_heading = title
            block_number = 0

    def add_source_body(display, source, bold=False, page_break_before=False):
        result.append(body(display, bold, page_break_before))
        source = clean(source)
        if source:
            expected.append(source)

    def add_writing_lines(count):
        for _ in range(count):
            result.append(body("______________________________________________"))

    def add_true_false(display, source):
        result.append({"type": "true_false", "segments": [(clean(display), True)]})
        expected.append(clean(source))

    for row in rows:
        number, lines, marks = row_question(row)
        title = classify_question(lines, marks, number)
        ensure_heading(title)
        type_counts[title] += 1
        events = row_events(document, row, media_dir, chapter)
        images = [value for kind, value in events if kind == "image"]
        local_images.extend(images)

        if title in {"Multiple Choice Questions", "Assertion and Reason"}:
            question_lines, options = labeled_options(lines, number)
            if title == "Assertion and Reason":
                if len(question_lines) < 2 or not question_lines[1].casefold().startswith("reason (r):"):
                    raise ValueError(f"Chapter {chapter} question {number}: incomplete assertion/reason pair")
            prompt = " ".join(question_lines)
            result.append({
                "type": "mcq",
                "text": prompt,
                "options": options,
                "pre_option_images": images,
            })
            expected.extend([*question_lines, *options])
            rendered_item_counts[title] += 1
            continue

        if title in {"True or False", "Fill in the Blanks"}:
            add_source_body(lines[0], lines[0], bold=True)
            for item_number, line in enumerate(lines[1:], start=1):
                display = f"{item_number}. {line}"
                if title == "True or False":
                    add_true_false(display, line)
                else:
                    add_source_body(display, line, bold=True)
            rendered_item_counts[title] += len(lines) - 1
            continue

        block_number += 1
        first_text = True
        for kind, value in events:
            if kind == "image":
                result.append(value)
                continue
            if first_text:
                add_source_body(f"{block_number}. {value}", value, bold=True)
                first_text = False
            else:
                add_source_body(value, value, bold=True)
        if first_text:
            raise ValueError(f"Chapter {chapter} question {number}: no visible text")
        rendered_item_counts[title] += 1
        if title in {"Very Short Questions", "Short Questions"}:
            add_writing_lines(1)
        elif title in {"Long Questions", "Very Long Questions", "Case-Based Questions"}:
            add_writing_lines(3)

    for image in local_images:
        if abs(image["scale"] / image["base_scale"] - 0.5) > 1e-9:
            raise ValueError(f"Chapter {chapter}: question image is not half-scale")
    question_images.extend({"chapter": chapter, **image} for image in local_images)
    metadata = {
        "source_docx": docx_path.name,
        "source_pdf": pdf_path.name,
        "source_rows": len(rows),
        "rendered_items": sum(rendered_item_counts.values()),
        "counts_by_type": dict(type_counts),
        "rendered_items_by_type": dict(rendered_item_counts),
        "source_figures": len(local_images),
        "docx_pdf_prose_checks": pdf_checks,
    }
    return result, expected, metadata


def add_practice_after_chapter_images(elements, chapter, session, media, args, report):
    original_download_images(elements, chapter, session, media, args, report)
    number = chapter["num"]
    if number in CHAPTER_NUMBERS:
        if number in questions_inserted:
            raise ValueError(f"Chapter {number} practice questions were inserted twice")
        questions, expected, metadata = practice_elements(number, media)
        elements.extend(questions)
        expected_practice_text[number] = expected
        question_metadata[number] = metadata
        questions_inserted.add(number)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_sha256(relative_path: Path) -> str:
    """Hash a file as stored in HEAD without relying on a sibling clean clone."""
    data = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "-C", str(ROOT),
         "show", f"HEAD:{relative_path.as_posix()}"],
    )
    return hashlib.sha256(data).hexdigest()


def source_hashes():
    hashes = {WORKBOOK.name: sha256(WORKBOOK)}
    if tracked_sha256(Path(WORKBOOK.name)) != hashes[WORKBOOK.name]:
        raise ValueError("Workbook does not match the checked-out Git revision")
    for chapter in CHAPTER_NUMBERS:
        for path in question_paths(chapter):
            hashes[path.name] = sha256(path)
            relative = Path("Class 8th Science") / path.name
            if tracked_sha256(relative) != hashes[path.name]:
                raise ValueError(f"Source does not match the checked-out Git revision: {path.name}")
    return hashes


def verify_practice_before_publish(chapters, directory, module, outputs):
    result = original_check_structure(chapters, directory, module, outputs)
    if questions_inserted != set(CHAPTER_NUMBERS):
        raise ValueError(f"Practice questions were not inserted for all chapters: {questions_inserted}")
    import pymupdf
    from validate_against_pdf import map_pdf, norm

    rendered_by_output = {}
    for label, path in outputs.items():
        with pymupdf.open(path) as pdf:
            ranges = map_pdf(pdf, chapters, generated=True)
            rendered_by_output[label] = {
                chapter["num"]: scrape_chapters.rendered_text(
                    pdf,
                    page_range,
                    [chapter["name"], "Practice Questions"],
                )
                for chapter, page_range in zip(chapters, ranges)
            }

    for chapter in CHAPTER_NUMBERS:
        checks = {}
        for label, rendered_by_chapter in rendered_by_output.items():
            expected = expected_practice_text[chapter]
            rendered = rendered_by_chapter[chapter]
            missing = [text for text in expected if norm(text) not in rendered]
            if missing:
                raise ValueError(
                    f"{label}: Chapter {chapter} Practice Questions text missing from compiled PDF: "
                    f"{missing[:8]}"
                )
            checks[label] = {"source_text_items_checked": len(expected), "missing": 0}
        question_metadata[chapter]["compiled_prose_checks"] = checks

    tex = (directory / f"{module}.tex").read_text(encoding="utf-8")
    lyx = (directory / f"{module}.lyx").read_text(encoding="utf-8")
    for image in question_images:
        expected_tex = f"width={image['scale']}\\textwidth]{{media/{image['filename']}}}"
        expected_lyx = f"filename media/{image['filename']}"
        expected_lyx_width = f"width {int(round(image['scale'] * 100))}text%"
        if expected_tex not in tex or expected_lyx not in lyx or expected_lyx_width not in lyx:
            raise ValueError(f"Question image scale/reference mismatch: {image['filename']}")

    result["practice_questions"] = {
        "chapters": {str(ch): question_metadata[ch] for ch in CHAPTER_NUMBERS},
        "total_source_rows": sum(item["source_rows"] for item in question_metadata.values()),
        "total_rendered_items": sum(item["rendered_items"] for item in question_metadata.values()),
        "question_images": {"count": len(question_images), "scale_factor": 0.5},
        "source_issues": SOURCE_ISSUES,
        "source_hashes": source_hashes(),
    }
    return result


scrape_chapters.download_content_images = add_practice_after_chapter_images
scrape_chapters.check_structure = verify_practice_before_publish


def git_commit() -> str:
    return subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "-C", str(ROOT),
         "rev-parse", "HEAD"],
        text=True,
    ).strip()


def update_manifest():
    path = ROOT / "stage2" / "output" / MODULE / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest.update({
        "question_image_scale": 0.5,
        "question_sources": {
            "git_commit": git_commit(),
            "git_dirty": True,
            "source_hashes": source_hashes(),
            "adapter_sha256": sha256(Path(__file__)),
            "convert_sha256": sha256(ROOT / "stage2" / "convert.py"),
            "scrape_chapters_sha256": sha256(ROOT / "stage0" / "scrape_chapters.py"),
        },
    })
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    args = [
        "--links", str(WORKBOOK),
        "--sheet", "Class 8th",
        "--module", MODULE,
        "--title", "Class 8th Science",
        "--output-dir", str(ROOT / "stage2" / "output"),
        "--cache-dir", str(ROOT / "input" / "scraped"),
        "--offline",
    ]
    status = scrape_chapters.main(args)
    if status == 0:
        update_manifest()
    raise SystemExit(status)
