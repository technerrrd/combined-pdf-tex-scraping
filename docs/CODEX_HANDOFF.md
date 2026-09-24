# Codex project handoff

## Project purpose and goals

This repository turns ordered EduRev science-note chapter links into editable TeX and themed LyX books, compiles both formats to PDF, validates source structure and optional reference coverage, and publishes output only after every required check passes. It also retains a PDF/DOCX fallback for pages that cannot be scraped.

The durable goals are:

- faithful transcription without invented or silently flattened content;
- preservation of chapter numbering, headings, inline formatting, notation, lists, tables, and image order;
- reproducible online and offline builds using validated caches;
- deterministic TeX and LyX compilation on Windows and Linux;
- failure isolation, rollback, and atomic publication of individual modules and Class 6-8 releases;
- traceable reports that record inputs, validation, compiler diagnostics, and Git state.

## Current architecture

The primary flow is:

1. `stage0/scrape_chapters.py` parses CLI options and ordered chapter links.
2. `stage0/build_support.py` handles validated URL-keyed caches, retries, staging, compiler preflight, reference checks, reports, locks, rollback, and publication.
3. `stage2/html_source.py` parses EduRev HTML with `html5lib` into ordered structural elements.
4. `stage2/inline_content.py` represents and renders typed text, bold, scripts, and supported math.
5. `stage2/convert.py` writes direct TeX and themed LyX, preserves chapter counters, handles images, and supports legacy DOCX input.
6. Both outputs compile to PDF. Structural, embedded-image, compiler, and optional reference-PDF checks must pass before staged output replaces the last successful module.

`stage0/release_science.py` reads `Science-notes-links.xlsx` and builds selected Class 6-8 books as one atomic release outside the checkout. The fallback path remains `stage0/scrape_images.py` -> `stage1/convert_document_v4.py` -> `stage2/convert.py`.

Important configuration and data:

- `input/CHAPTER-LINKS`: default ordered module links.
- `input/scraped/`: ignored URL-keyed cache; legacy chapter-number caches are not trusted as URL identities.
- `Science-notes-links.xlsx`: authoritative Class 6-8 release map.
- `Class 6th Science/`, `Class 7th Science/`, `Class 8th Science/`: tracked reference PDFs.
- `Final-lyx_template/`: Legrand LyX theme and output-critical assets.
- `requirements.txt`, `pytest.ini`, `setup-linux.sh`, and `.github/workflows/`: dependency and validation contract.
- `stage2/output/`: ignored module output and diagnostics. Complete science releases default to `D:\Science-Book-Releases` on Windows and remain configurable.

## Completed work

- Implemented validated URL-keyed page/image caches, bounded retries, atomic cache writes, and explicit offline/refresh modes.
- Added mandatory Python/compiler preflight, unique staging directories, bounded TeX/LyX compilation, retained logs, and fail-closed publication.
- Added exclusive publication locks, rollback, and timestamped snapshots of replaced successful output.
- Added explicit module/title/link/output/cache/chapter/reference/page-map/coverage/image-scale options while retaining the legacy positional module alias.
- Replaced guessed reference mapping and prefix matching with explicit or unambiguous page ranges and complete normalized-line comparisons against parsed content and both generated PDFs.
- Added JSON/text reports and manifests without allowing standalone validation to overwrite build acceptance reports.
- Added typed inline text, bold, sub/superscripts, supported TeX/MathJax/Presentation MathML, native LyX equations and table cells, and legacy DOCX segment compatibility.
- Preserved source chapter numbers, including gaps, in TeX/LyX counters, bookmarks, section numbering, and chapter-banner filenames.
- Added natural bottom spacing and balanced diagram sizing that preserves aspect ratio, source-requested smaller sizes, and image order.
- Preserved literal rupee symbols with `tfrupee` plus `newunicodechar`; textual `Rs.` and `INR` forms still normalize correctly.
- Added current and legacy EduRev content-image suffixes, sparse-page content-root selection, and filtering for navigation, promotions, optional callouts, and embedded quizzes without suppressing substantive tables.
- Added Windows/Linux offline regression coverage, real compiler integration, headless Linux Qt handling, and `setup-linux.sh`.
- Added atomic Class 6-8 releases with source commit/dirty-state reporting.
- Added 20 reference PDFs covering 360 pages and the authoritative three-sheet source-link workbook.

## Current work

The 2026-09-24 update adds explicit question-type headings and restarts top-level numbering at 1 in every type block, including a repeated type after another group. Class 8 Maths Chapter 8 is published under `stage2/output/Class8-Maths/`: MCQs are 1-20, Assertion and Reason 1-9, Problem-Solving 1-25, Case-Based 1-3, repeated Problem-Solving 1-10, and Fill in the Blanks 1. The 68 source questions, order, wording, subquestion markers, and graph were checked against the supplied DOCX/PDF; both TeX and LyX outputs passed compilation and structural/rendered-content validation with 244 source text checks each. No mark categories were inferred where the source lacked mark information.

The same change preserves the Class 6-8 Science reference PDF contents while renaming the 20 tracked files to the consistent `Chapter-<N>-Notes-Class<Class>th-Science.pdf` form. Every renamed pair had identical SHA-256 content before and after. Ancillary files and new worksheet source files were not added.

The code changes support editable inline math in MCQ prompts/options for TeX/LyX, keep LyX Formula insets on their own source lines, and retry a LyX batch export only when a fresh user directory created its first-run configuration but no export. Regression tests cover these cases.

This dev update was prepared from remote commit `1c2ce84` (`feat: add class 6-8 maths sources`). Verify the final commit and push status from Git history rather than relying on this handoff text alone.

Validation for this documentation update found 68 regular tests passing with the integration-marked test deselected. The real compiler integration is not currently green: temporary-worktree runs ended at LyX export with silent exit code 11, while a run from the canonical checkout compiled further and then failed closed because TeX PDF validation could not match the fixture's rendered matrix line. This task did not change application code; treat this as a current compiler/validation issue to investigate, not as a reason to weaken acceptance checks.

## Known bugs, limits, and risks

- The 2026-09-22 real compiler integration currently fails as described above. Reproduce the matrix text-extraction/normalization mismatch against the current TeX Live/LyX environment before making pipeline changes.
- Three reference-only Class 8 Chapter 9 lines remain unmatched: one diagram caption and two wrapped practice-link fragments. Coverage remains above the required threshold; the score is diagnostic, not proof of perfect fidelity.
- Class 8 Chapter 3 was an earlier calibration run and has not been republished after the newest normalization fixes.
- Unsupported equations and complex HTML table spans/nesting deliberately fail for review. The project does not perform OCR, formula-image transcription, or infer equations from prose.
- HTML question-bank detection and broader fallback equation extraction remain outside the completed scope.
- Direct TeX intentionally retains a plain book design while LyX retains the Legrand theme. Theme unification was excluded.
- Old chapter-number caches are not silently reused. An online build must populate URL-keyed entries before offline use.
- Failed staging directories, previous snapshots, and stale lock/recovery artifacts may remain after interruption. Inspect them before removal.
- GitHub-hosted CI results must be observed directly; configured or previously passing jobs are not evidence that a new commit passed.

## Important design decisions

- **HTML is the primary source; PDF is an oracle.** EduRev HTML retains semantic headings, emphasis, lists, images, and tables that browser-printed PDFs lose. Reference PDFs detect omissions but never replace parsed source content.
- **Use `html5lib`.** EduRev markup omits closing tags. HTML5 implied-end-tag behavior prevents one malformed paragraph or list item from swallowing a chapter.
- **Fail closed and preserve the last good output.** Missing dependencies, compilers, assets, ambiguous mappings, low coverage, unsupported math/tables, or structural mismatches block publication. There is no partial-success override.
- **Cache by the full source URL.** Chapter numbers alone cannot prove that cached content belongs to the requested link. Cache validation and atomic replacement protect offline reproducibility.
- **Preserve semantics and order.** Source numbering, inline whitespace, list depth, typed notation, and image order take precedence over cosmetic rewriting.
- **Keep the fallback pipeline.** It is less reliable than semantic HTML but remains necessary when a source page cannot be scraped.
- **Publish releases outside Git.** Generated books and diagnostics are large artifacts. Reports record the exact commit and dirty state instead of committing outputs.

## Assumptions and workflow conventions

- `Science-notes-links.xlsx` is the authoritative release map; preserve worksheet order and chapter order.
- Root class PDF folders are intentional tracked reference inputs, not generated output.
- `README.md` defines the current CLI and acceptance contract; `CLAUDE.md` preserves inherited detailed formatting/fallback rules.
- Use a fresh ignored virtual environment. Do not commit environments, caches, output, logs, temporary files, credentials, or local release artifacts.
- Run offline tests after relevant changes and compiler integration after parser, writer, build, template, or validation changes.
- Ask before token-intensive page-by-page visual review. Compilation, structural validation, and file-integrity checks are always required.
- Update `HANDOFF.md` with current branch/objective, work completed, commands actually run, results, known issues, next steps, and platform differences. Update this file when durable context or design decisions change.
- Commit and push only with explicit authorization. Review remotes, status, diff, and validation first; never force-push without explicit authorization.

## Suggested next steps

1. Investigate the current compiler integration failure, starting with the fixture matrix line's TeX-PDF extraction and normalization; retain fail-closed behavior.
2. Republish Class 8 Chapter 3 with current normalization and compare both compiled formats with its reference.
3. Investigate the three diagnostic Chapter 9 unmatched lines without weakening complete-line comparison or the coverage threshold.
4. Add HTML question-bank recognition only with fixtures covering MCQ, assertion-reasoning, provided answers, and writing-line precedence.
5. Expand conservative equation/table support only when unsupported constructs can remain editable and fail clearly when unsafe.

## Platform notes

- Windows Python: `.venv/Scripts/python.exe`; Linux Python: `.venv-linux/bin/python`.
- Canonical builds require LyX 2.4, TeX Live/pdfLaTeX, and the documented extra/science/font packages. Linux setup also installs Poppler utilities.
- Standard Windows LyX installations are discovered if `lyx` is absent from `PATH`. Headless Linux selects Qt's offscreen backend unless an explicit Qt/display configuration exists.
- Preserve Git line-ending handling. Do not create copy-only CRLF/LF diffs.
- Linux and Windows results must be reported separately. Do not claim a compiler or CI result that was not actually run and observed.
