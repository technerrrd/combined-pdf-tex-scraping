# Codex project handoff

## 2026-10-15 Science source refresh

The authoritative workbook now selects Class 6 Chapters 3, 4, 6, 7, 11, and 12; Class 7 Chapters 4-10; and Class 8 Chapters 3, 4, 7-10, and 12. The XLSX opened successfully, contains one row per selected chapter, and uses valid HTTPS EduRev links. Source synchronization adds Class 6 note PDFs for Chapters 3, 4, and 6, removes the formerly tracked Class 6 references for Chapters 8-10 because they are no longer selected, replaces Class 7 note PDFs for Chapters 5 and 9, and retains the existing Class 7 Chapter 10 note because it remains selected and the active export did not supply a replacement.

Seven Class 8 Science question DOCX/PDF pairs were added for the workbook-selected Chapters 3, 4, 7, 8, 9, 10, and 12. Each DOCX passed ZIP integrity and document-structure checks, and each PDF opened successfully. The question PDFs total 45 pages. All 1,542 substantive DOCX text-run checks matched the paired PDFs, and every detected A-D option sequence was complete. The five new or replaced note PDFs total 79 pages and contain extractable text.

Two source facts require preservation and review. The file pair named for Chapter 4 contains electricity material corresponding to workbook Chapter 4, but its DOCX title and PDF heading both identify it as Chapter 3. Class 8 Chapter 3 source rows 31 and 32 repeat the prompt `Match the following:` but carry distinct embedded figures, so they were retained as separate supplied questions. No other exact repeated row text was found. This review does not replace the later question-type/count, table/figure ordering, equation, answer, or compiled-output completeness audits required before publishing a generated book.

This is a source-only Git update. It does not modify converters, generated books, caches, or the active export's uncommitted pipeline overlay. No TeX/LyX compilation, reference-PDF coverage, exhaustive page-by-page visual inspection, Linux execution, or configured CI execution is claimed. The publication clone is `tmp/codex-push-dev-20260924/` on `dev`, based on `6b156ffd7c4e35ab13640a4d36283445ae5e8d3e`; a fresh remote fetch confirmed `origin/dev` and `origin/main` at the same commit before preparation.

## 2026-10-15 Class 6 Maths complete build

The Class 6 Maths complete book is published at `stage2/output/Class6-Maths-Complete/`. It combines the existing validated offline notes/infographic build for workbook-selected Chapters 6-10 with five supplied DOCX/PDF question pairs. The direct TeX PDF has 80 pages and the themed LyX PDF has 72 pages. The book contains 347 top-level supplied questions and 73 supplied question figures; all figures have exactly half their otherwise selected dimensions in both formats, while notes and infographic sizing remains unchanged.

Both compiler paths and all mandatory structural, source-content, rendered-content, equation, figure, ordering, numbering, option, hash, and chapter-range checks passed. All 985 substantive Word prose checks matched the paired source PDFs, and compiled prose checks found no missing supplied question text. Reported source issues remain unchanged: sublabel-count differences in Chapters 6, 7, 9, and 10, plus the recorded exact duplicate prompts in Chapters 6, 7, and 9. No source content was invented, corrected, or deleted.

Windows offline regressions passed with 81 tests and 5 XLSX-dependent deselections; the real compiler integration passed with 1 test and 85 deselections. No Linux or configured CI execution was performed. Representative pages were rendered and inspected; exhaustive page-by-page review was not opted into and was skipped.

## 2026-10-14 Class 7 and 8 Maths diagram rebuilds

The Class 7 and Class 8 complete Maths books were rebuilt and atomically published with the documented one-time 0.5 question-diagram scale. Class 7 contains 477 top-level questions and 33 question figures across Chapters 9-15; its PDFs are 94 pages (TeX) and 77 pages (LyX). Class 8 contains 484 questions and 54 figures across Chapters 8-14; its PDFs are 110 pages (TeX) and 91 pages (LyX). Structural/content validation, figure hashes and ordering, compiler checks, and representative visual review passed for both books.

The active export also contains a narrow Windows LyX fallback for repeated empty-log exit 11 failures from a fresh isolated profile and a dotless-i normalization used for pdfTeX-extracted transliteration. These changes were validated locally but remain outside the source-only Git update described above. Windows offline regressions passed with 81 tests and 5 deselections, and real compiler integration passed with 1 test and 85 deselections. No Linux or CI execution was claimed; exhaustive page-by-page review was not opted into.

## 2026-10-10 Class 7 Maths source publication and saved sizing rule

The user authorized pushing all newly supplied Class 7 Maths question DOCX/PDF files and the agreed 50% question-diagram sizing rule. Chapters 9-15 supply seven pairs, 14 files total. The seven DOCX ZIP packages and document structures opened successfully; all seven PDFs opened, totaling 51 pages. Copied inputs match their originals by SHA-256. Formula PDFs and unrelated/generated files are excluded. Source chapter placement, wording conflicts, type/count audits, and complete question content comparisons remain future conversion checks; file integrity alone does not establish those results.

`AGENTS.md` and `CLAUDE.md` v4.8 now record the rule: multiply the normally selected question-diagram width by an additional `0.5` exactly once, retaining aspect ratio so height halves too, in both TeX and LyX. Preserve source image files, labels, content, and order. This override applies only to embedded question figures and takes precedence over general sizing defaults; notes and full-page infographics keep their existing sizing. It is half of the otherwise selected dimensions, not a fixed 50% text width and not cumulative resizing on each rebuild. Keep the original baseline sizing available when implementing it. Validate both compiler paths, content/image checks, and representative readability before replacing any output in a later authorized build.

This is documentation and source publication only. The user explicitly deferred implementation: no pipeline or one-off adapter changes, no conversion, and no PDF regeneration. The Class 8 completed books still have their prior diagram dimensions. The existing `dev` publication clone is `tmp/codex-push-dev-20260924/`; origin is the configured `technerrrd/combined-pdf-tex-scraping` repository. Both remote branches were fetched and confirmed at `d8ffb3d` before preparation; publish this change by fast-forward to `origin/dev` and `origin/main`, with no force push. The previously local completed Class 8 operational record below is included in this documentation publication. Windows file-integrity/hash validation and documentation/diff review are the checks for this update; no application tests, compilers, Linux execution, or CI results are claimed. Next steps require separate user authorization for sizing implementation or Class 7 book conversion, and must preserve the strict source-only rules.

## 2026-10-10 Class 8 Maths final build and publication

The authorized source publication completed before conversion. Commit `d8ffb3da9a24feb0f8e12b8b6f1ce26960d6f401` contains the question rules and seven DOCX/PDF pairs (14 files), pushed by fast-forward to both `origin/main` and `origin/dev` and verified against live remote heads. The clone at `tmp/codex-push-dev-20260924/` is clean on `dev`. Generated output and one-off scripts remain ignored. This completion record was added locally after the push.

Published `stage2/output/Class8-Maths-Complete/` after staged TeX and LyX compilation and strict acceptance checks. The themed PDF has 98 pages and the direct TeX PDF has 120 pages. Editable sources, media, `manifest.json`, `report.json`, and `question-source-audit.json` accompany them. Existing `stage2/output/Class8-Maths/` remains intact. Final report status is passed, errors and compiler diagnostics are empty. Mandatory structure, editable equation, rendered prose, image fingerprint/order, chapter mapping, and question completeness checks passed. All 14 final input hashes match the pushed files. Optional independent formula-reference PDF coverage remains not checked, separately from the completed supplied question-PDF comparisons.

Chapter 8-14 question counts are respectively 68, 68, 70, 69, 70, 69, and 70 (484 total); 54 question figures were preserved. Word prose was checked against all seven source PDFs, and question prose was checked per chapter in both compiled books. Type headings and top-level numbering restart for each block, including repeated types. Source sublabels, OR alternatives, wording, equations, figures, and supplied options remain in source order. Common assertion-reason options are repeated only within their source-defined section and displayed in A/B then C/D checkbox grids. No question or answer content was generated.

Unresolved source issues are intentionally preserved in the audit: Chapter 10 has 20 Word numbered paragraphs versus 15 visible PDF sublabels, so matched explicit labels are used and remaining Word labels retained; Chapter 14 includes one empty math node and source Q56's unfinished clause `To make decorative pieces,`. No equation or clause was invented and no exact duplicate prompts were found. These are author follow-ups, not conversion errors to repair by inference.

The ignored adapter `tmp/build_math8_complete.py` uses the established parser, writers, compilation, and validation pipeline, with strict DOCX/OMML parsing, supplied figure extraction, PDF sublabel alignment, and question-block rendering. It rejects unsupported math rather than flattening it. Local symbol support maps the supplied implication glyph to an equivalent native equation command, and currency comparison accepts the inherited equivalent rupee rendering without changing amounts. The active export has no Git metadata and differs from the published clone in pre-existing pipeline files; the manifest accurately records `git_dirty: true`, published source commit, adapter SHA-256, pipeline hashes, and input hashes. No application source changes were committed for this build. Repeatable general-purpose question ingestion remains future work.

Actual Windows verification: offline regressions 81 passed and 5 deselected; real compiler integration 1 passed and 85 deselected. No Linux or configured CI results were claimed. The user declined exhaustive page-by-page visual review. Representative cover, assertion-reason grid, and dataset pages were checked; one overflowing dataset line was moved to a new line, both formats recompiled, and all acceptance checks rerun before atomic replacement. Final output has no reported compiler warnings. Use the existing sibling Windows `.venv` and validated `input/scraped/` cache to reproduce the local build. Next: author review of the source issues and optional future independent reference coverage.

## 2026-10-10 Class 8 Maths source publication and build

- User authorized pushing the current rules and all seven chapter question DOCX/PDF pairs before completing the Class 8 Maths book. Publishing to both `origin/main` and `origin/dev` by fast-forward; no force push.
- All 14 source files opened successfully (61 PDF pages); copied files match SHA-256, including the existing Chapter 8 filename with a space before `.pdf`. Word lock files and unrelated files are excluded. Content comparison and chapter/type audits are still pending for the build.
- Rules are in `CLAUDE.md` v4.7 and `AGENTS.md`; retained the clone's newer release history while importing the rule updates. Staged diff and whitespace checks reviewed. No code changes or new compiler/test results in this source publication.
- Page-by-page visual inspection was declined for this release. Mandatory compilation, structural, rendered-content, equation, and image checks still apply. Build is pending; preserve existing output on failure.

## 2026-10-10 Additional approved question-source rules

The user approved all four suggested additions. `AGENTS.md` and `CLAUDE.md` (v4.7) now require reporting duplicate questions, missing options, incomplete statements, and conflicting DOCX/PDF wording without silently correcting, deleting, deduplicating, or selecting conflicting content. Verify each question file's chapter using source identifiers and the authoritative chapter map before insertion, flagging ambiguous or mismatched placement.

For each chapter, record question counts by type, including repeated type blocks, and verify every supplied question, option, answer, table, and figure in both compiled outputs with source content and order preserved. Counts alone do not prove completeness; missing or mismatched content must be reported before publication.

Assertion-reason options supplied once as common section instructions may be repeated exactly beneath each pair covered by that section, using the two-column checkbox grid. This exception permits repetition of supplied content only; options must never be generated or imported from an assumed standard list. Unclear applicability requires review.

This remains a documentation-only preparation step for Class 8 chapter questions; parser/writer behavior and existing books have not changed. The active Windows export has no `.git`; the existing clone at `tmp/codex-push-dev-20260924/` remains clean on `dev`, one commit ahead of cached `origin/dev`, without a remote refresh. Four-document diff review, rule-consistency searches, and whitespace checks were performed on Windows; no tests, conversions, builds, commits, pushes, or Linux checks were run. Pre-edit copies are under `tmp/question-rules-followup-before-20261010/`. Next, inspect source files for chapter mappings, counts, and issues before conversion; automatic question ingestion remains incomplete.

## 2026-10-10 Current question-formatting decisions

The current objective is to document the user's question rules before processing the newly supplied Class 8 chapter files. This update changes documentation only. The active Windows workspace has no `.git`; the existing clone at `tmp/codex-push-dev-20260924/` is on `dev`, with a clean working tree and one commit ahead of its cached `origin/dev`. No remote refresh, commit, or push was performed.

- **Source-only content:** use only supplied questions, answers, solutions, explanations, and options. Never generate, infer, complete, or rewrite them. Flag missing or unclear content for review; preserve supplied content even when familiar standard wording exists.
- **Assertion-reason layout:** use the MCQ two-column checkbox grid in both TeX and LyX, with A/B on the first row and C/D on the second. Preserve source option wording and order. The former fixed-option requirement in `CLAUDE.md` is removed; example placeholders refer only to supplied content. Missing options must not be supplied from the former fixed list. This decision supersedes the stacked options in the earlier Science build; existing outputs have not been regenerated.
- **Numbering:** start top-level numbering at 1 in every question-type block, repeating the heading and restarting at 1 if a type reappears. Preserve source subquestion and alternative labels and their order. This overrides the former blanket instruction to strip every numbering prefix.

`AGENTS.md` and `CLAUDE.md` (v4.6) carry the durable rules. The converter's automatic coverage of question types and chapter-file ingestion remains incomplete; this documentation update adds no parser or writer behavior. Inspect and map the supplied files before the next conversion, and flag missing options or unclear content rather than manufacture replacements.

Validation for this update consists of four-document diff review, conflicting-instruction searches, and whitespace checks. No application tests, TeX/LyX builds, or Linux checks were run. Pre-edit copies are retained under `tmp/question-rules-before-20261010/`.

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
- Added exclusive publication locks and rollback; successful replacements now remove the previous output after the atomic swap instead of accumulating timestamped release folders.
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

On 2026-09-24, consolidated the newest Class 6 and 7 Science folders into the existing complete Science release at `D:\Science-Book-Releases`, preserving Class 8. Class 6/7 copies were SHA-256 verified. The top-level report now records per-class source provenance because the preserved Class 8 files were built from an older commit. Cleanup of the duplicate `D:\Science-Book-Releases-Classes6-7` folder was attempted after verification but stopped when its `Science_Class6th-lyx.pdf` was locked by another process; the folder is partially present. Ask the user to close that PDF before retrying; do not terminate an unknown process. Earlier failed staging and consolidation backup folders were removed.

Publication now deletes the old-output snapshot after a successful atomic swap, retaining rollback during the swap but preventing per-release sibling folders. README, tests, and handoff docs were updated. Tests could not run in this execution environment: there is no project `.venv`, the bundled Python lacks pytest/PyMuPDF, and no system Python is on PATH. `git diff --check` passed. The previously recorded Class 6/7 and Class 8 build validations remain the available compiler results.

On 2026-09-24, built and published a separate Class 6-7 Science release to `D:\Science-Book-Releases-Classes6-7`, preserving the existing full Class 6-8 release at `D:\Science-Book-Releases`. The workbook-selected chapters are Class 6 Chapters 7-12 and Class 7 Chapters 4-10. No Practice Questions section or question files were added. TeX and LyX source/PDF outputs compiled and passed structural/rendered-source validation; reference PDFs were not checked. Output counts: Class 6, 93 images, 56 TeX pages and 51 LyX pages; Class 7, 151 images, 96 TeX pages and 82 LyX pages. The report records source commit `7e43406122f6a17c3660a3d02755d26ae7b9ee94` and a dirty source tree.

This release exposed two rendered-text normalization gaps. `stage0/validate_against_pdf.py` now normalizes TeX subscripts such as `SO_2` to PDF-extracted `SO2`, and maps `\\rightarrow` to the rendered arrow; `tests/test_pipeline.py` covers both. Windows offline regressions passed (81 passed, 5 deselected), and `git diff --check` passed. The standalone compiler integration fixture remains failing during TeX pass 1 because its generated fixture references an absent `media/5139bcf6230362a2e593b614b26e15e01b72435b82d067f58362907207eea19b.jpg`; this is distinct from the full release, whose real TeX/LyX outputs compiled. Representative pages were reviewed; page-by-page visual review was skipped. No commit or push was made.

The 2026-09-24 update adds explicit question-type headings and restarts top-level numbering at 1 in every type block, including a repeated type after another group. Class 8 Maths Chapter 8 is published under `stage2/output/Class8-Maths/`: MCQs are 1-20, Assertion and Reason 1-9, Problem-Solving 1-25, Case-Based 1-3, repeated Problem-Solving 1-10, and Fill in the Blanks 1. The 68 source questions, order, wording, subquestion markers, and graph were checked against the supplied DOCX/PDF; both TeX and LyX outputs passed compilation and structural/rendered-content validation with 244 source text checks each. No mark categories were inferred where the source lacked mark information.

The same change preserves the Class 6-8 Science reference PDF contents while renaming the 20 tracked files to the consistent `Chapter-<N>-Notes-Class<Class>th-Science.pdf` form. Every renamed pair had identical SHA-256 content before and after. Ancillary files and new worksheet source files were not added.

The code changes support editable inline math in MCQ prompts/options for TeX/LyX, keep LyX Formula insets on their own source lines, and retry a LyX batch export only when a fresh user directory created its first-run configuration but no export. Regression tests cover these cases.

This dev update was prepared from remote commit `1c2ce84` (`feat: add class 6-8 maths sources`). Verify the final commit and push status from Git history rather than relying on this handoff text alone.

Validation for this documentation update found 68 regular tests passing with the integration-marked test deselected. The real compiler integration is not currently green: temporary-worktree runs ended at LyX export with silent exit code 11, while a run from the canonical checkout compiled further and then failed closed because TeX PDF validation could not match the fixture's rendered matrix line. This task did not change application code; treat this as a current compiler/validation issue to investigate, not as a reason to weaken acceptance checks.

## Known bugs, limits, and risks

- The standalone real compiler integration fixture currently fails in TeX pass 1 because its expected media image is missing; see Current work. Do not weaken fail-closed acceptance. The actual Class 6-7 release compiled successfully through TeX and LyX.
- Three reference-only Class 8 Chapter 9 lines remain unmatched: one diagram caption and two wrapped practice-link fragments. Coverage remains above the required threshold; the score is diagnostic, not proof of perfect fidelity.
- Class 8 Chapter 3 was an earlier calibration run and has not been republished after the newest normalization fixes.
- Unsupported equations and complex HTML table spans/nesting deliberately fail for review. The project does not perform OCR, formula-image transcription, or infer equations from prose.
- HTML question-bank detection and broader fallback equation extraction remain outside the completed scope.
- Direct TeX intentionally retains a plain book design while LyX retains the Legrand theme. Theme unification was excluded.
- Old chapter-number caches are not silently reused. An online build must populate URL-keyed entries before offline use.
- Failed staging directories and stale lock/recovery artifacts may remain after interruption. Inspect them before removal; successful publication no longer retains old output snapshots.
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
