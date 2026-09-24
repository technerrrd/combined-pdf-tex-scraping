# Handoff

## 2026-09-24 one-folder Science release

- Consolidated the newest Class 6 and 7 Science outputs into the existing complete release at `D:\Science-Book-Releases`, preserving its Class 8 output. Class 6/7 files were SHA-256 checked after copying; the root report now identifies source provenance per class because the preserved Class 8 output came from an older commit.
- Removed the obsolete failed staging exports and consolidation backups. Removal of the duplicate successful folder `D:\Science-Book-Releases-Classes6-7` was blocked because `Science_Class6th-lyx.pdf` is open/locked; its folder remains partially present. Ask the user to close that PDF before retrying cleanup; do not terminate an unknown process.
- Changed successful atomic publication to delete its temporary previous-output snapshot after the swap, avoiding a new dated sibling folder for every future release while retaining rollback if the swap fails. `README.md` and handoff docs were updated.
- Tests could not be run in this execution environment: the Git clone has no `.venv`, the bundled Python runtime lacks pytest/PyMuPDF, and no system Python was available. `git diff --check` passed. The prior build report still records the Class 6/7 and Class 8 compiler/structure results.

## 2026-09-24 Class 6-7 Science release (no practice questions)

- Built the two workbook-selected books from validated URL-keyed caches, without adding a Practice Questions section or importing any question-bank files. The atomic subset release is at `D:\Science-Book-Releases-Classes6-7`; the prior complete Class 6-8 release at `D:\Science-Book-Releases` was preserved.
- Class 6 covers Chapters 7-12 (93 images; 56-page TeX PDF and 51-page LyX PDF). Class 7 covers Chapters 4-10 (151 images; 96-page TeX PDF and 82-page LyX PDF). Both editable sources and all four PDFs compiled; structural and rendered-source validation passed. Reference PDFs were not checked for this release.
- The release report records source commit `7e43406122f6a17c3660a3d02755d26ae7b9ee94` and `git_dirty: true`. The working diff adds safe PDF-text normalization for TeX subscripts and `\\rightarrow`, with regression tests, because the Class 7 source uses `SO_2` and reaction equations that extract differently from compiled PDFs.
- Windows offline regression tests: 81 passed, 5 deselected. The separate compiler integration fixture failed during TeX pass 1; the real Class 6/7 books compiled through both TeX and LyX. Representative covers and chapter pages were visually checked; exhaustive page-by-page review was skipped.
- No commit or push was made for the normalization fix; the current `dev` clone remains dirty. The build used URL-keyed caches and no new workbook or question inputs were modified.

## 2026-09-24 Class 8 Maths question-type numbering and dev update

- Updated and published `stage2/output/Class8-Maths/` with Chapter 8 questions from the supplied DOCX/PDF pair. Replaced generic Section A-F labels with explicit type headings and independent numbering in every block: MCQ 1-20, Assertion and Reason 1-9, Problem-Solving 1-25, Case-Based 1-3, repeated Problem-Solving 1-10, and Fill in the Blanks 1.
- Preserved question wording/order and subquestion markers; did not infer mark-based categories. Both PDFs compiled and passed structural/rendered-content validation (244 text checks per output); 68 questions and the source graph were checked. Updated practice pages were reviewed.
- The root Science reference PDF names now follow `Chapter-<N>-Notes-Class<Class>th-Science.pdf`. All 20 renamed files were matched byte-for-byte to the prior tracked PDFs by SHA-256; no contents changed. Untracked ancillary/source PDFs were not added.
- Added durable question-type heading/numbering instructions to `AGENTS.md` and `CLAUDE.md`; bumped the CLAUDE tag to v4.5.
- Code changes include MCQ inline math support in both writers, standalone LyX Formula insets, the first-run LyX userdir retry, and regression tests. Tests: 81 passed when excluding xlsx tests; all four xlsx tests fail because `openpyxl` is not installed in the available environment. `git diff --check` passes. Commit `8d74c55` was pushed to `origin/dev` after reviewing the remote, staged diff, and validation results.

## Current objective and branch

- Publish the Class 6 and 7 Science books from `Science-notes-links.xlsx` without adding practice questions. Preserve the existing complete Class 6-8 release and keep generated releases outside the checkout.
- Branch: dev, based on `7e43406`; the current uncommitted validation-normalization change is recorded in the Class 6-7 release report as dirty.
- Working in the Git clone; the downloaded source folder remains unchanged.
- No commit or push is authorized for the current normalization change.

## Completed work and decisions

- Pulled the shared latest `origin/dev` and `origin/main` commit, including `docs/CODEX_HANDOFF.md` and the atomic Science release tooling.
- Added XLSX chapter-source support with an explicit sheet, strict four-column schema, blank-row handling, chapter validation, and narrow repair of missing `https://` on EduRev links.
- Added ordered formula/infographic chapter builds. Embedded EduRev infographic PDFs are validated, cached, rendered at 200 DPI, and placed uncropped after the formula section.
- Added paired reference-directory validation: formula text coverage remains at least 95%, while infographic PDFs require matching page counts and rendered-page similarity.
- Preserved plain-text equations inside explicit MathML, added the Unicode square-root operator, and normalized browser-print fi/fl control-glyph artifacts without weakening unknown-equation rejection.
- Added full-page infographic output for TeX and LyX, transparent-image flattening for stable PDF fingerprints, Maths chapter banners, and the school name on both covers.
- Published `stage2/output/Class6-Maths/` with editable TeX/LyX sources and both compiled PDFs.
- Added validated URL-keyed page/image caches, bounded retries, atomic cache writes, offline and refresh modes.
- Added mandatory dependency/compiler preflight, staged builds, TeX and LyX-exported PDF compilation, bounded passes/timeouts, and retained logs.
- Publication checks source structure, rendered prose, chapter bookmarks, and embedded image fingerprints/order. Previous successful output survives failed builds; after a successful atomic swap, the previous output is removed rather than retained as a dated folder.
- Added exclusive publication locks and rollback for failed directory replacement.
- Added explicit module/title/input/output/cache/chapter selection flags and reference validation options; retained positional module alias.
- Replaced positional reference mapping and prefix matching with explicit/unambiguous chapter ranges and complete normalized-line comparisons against parsed content and both PDFs.
- Added JSON/text build reports and a manifest; standalone reference validation prints JSON without overwriting the build report.
- Added typed inline text/bold/scripts/math, supported LaTeX/MathJax/Presentation MathML conversion, native LyX equations and table cells, and legacy DOCX segment compatibility.
- Preserved legacy currency behavior using tfrupee. Direct TeX images stay in source order; LyX exports use the pdfLaTeX format to avoid unnecessary EPS conversion.
- Added regression fixtures, offline tests, compiler acceptance testing, and GitHub Actions jobs for Windows/Linux offline tests and Linux compiler integration.
- Added README.md; updated AGENTS.md and migrated CLAUDE.md to v4.1. Legacy fallback instructions remain available.
- Added natural bottom spacing to TeX, themed LyX, and fallback LyX output so short pages do not stretch their paragraphs and lists.
- Content diagrams are sized after decoding from their real dimensions, retain smaller source-requested sizes, and are capped at about 52% text width and 30% usable page height without cropping, distortion, or reordering.
- Live-PDF validation now ignores page furniture and embedded EduRev quiz controls while retaining separate heading and prose checks; equivalent degree glyphs normalize consistently.
- Updated README.md and CLAUDE.md v4.2 with the durable layout defaults.
- Headless Linux runs now select Qt's offscreen backend automatically unless a display or explicit Qt platform is already configured.
- Added `setup-linux.sh` for Ubuntu/Debian, Linux command documentation, and sparse CI checkouts that omit the large reference set from routine jobs.
- Added 20 validated reference PDFs under the three root-level Class Science folders and the original `Science-notes-links.xlsx` workbook; `.gitattributes` marks PDFs/workbooks as binary.
- Chapter headings now carry their source numbers into TeX/LyX counter resets, section numbering, and themed banner filenames; sequential numbering remains the fallback for unnumbered inputs.
- Tightened section, subsection, and subsubsection spacing in both output paths and retained `\raggedbottom`.
- Added `newunicodechar` rupee handling alongside `tfrupee`, preserving literal `₹` while continuing to normalize `Rs.` and `INR`.
- Added legacy `_sp` JPEG/PNG content-image discovery, sparse-page content-root selection, and filtering for EduRev promotional/course tables without suppressing substantive tables.
- Added `\rightarrow` to the explicit-equation allowlist after the live Class 7 source used the standard command.
- Rendered-content validation now keeps adjacent styled prose together, ignores numbered running headings ending in a period, and normalizes combining accents that PDF text extraction separates from their base letters.
- Rejoins a closing TeX delimiter split across an inline bold boundary in malformed live HTML while retaining explicit equation validation.
- Reduced the Legrand chapter-banner title size so long Class 8 chapter names remain inside the page.
- Published complete live-source modules under `stage2/output/Class6-Science/`, `stage2/output/Class7-Science/`, and `stage2/output/Class8-Science/`, each with editable TeX/LyX sources and PDFs from both compiler paths.

## Tests and results

- Ubuntu Python 3.14 on 2026-09-22: 82 regular tests passed; one integration-marked test was deselected.
- The real TeX/LyX compiler integration passed: 1 integration test passed, 82 regular tests were deselected. Complex matrix markup is now handled by equation checks instead of being compared as literal rendered prose.
- Validated all 24 Maths reference PDFs (131 pages total) and the XLSX container. The workbook resolves to Class 6 Chapters 6-10, Class 7 Chapters 9-15, and Class 8 Chapters 8-14.
- Documentation reconciliation on 2026-09-22: 68 regular tests passed; one integration-marked test was deselected.
- The real compiler integration was attempted from both the temporary documentation worktree and the canonical checkout. Worktree runs reached LyX but failed with silent exit code 11 and an empty `lyx-export.log`. The canonical-checkout run compiled further but failed closed because TeX PDF validation reported the matrix line `A matrix: \begin{matrix}1 & 0 \\ 0 & 1\end{matrix}.` as missing. No application code changed in that task; investigate this current compiler/validation regression before treating integration as green.
- Ubuntu Python 3.14 on 2026-09-15: 73 regular tests passed; one integration-marked test was deselected.
- Real TeX/LyX compiler integration passed before the later regression: 1 test passed, 73 deselected.
- The online and offline Class 6 Maths builds both passed and published transactionally. TeX produced 36 A4 pages; LyX produced 34 A4 pages.
- Formula reference coverage passed for every chapter and both compiler paths: Chapter 6 100%, Chapter 7 100%, Chapter 8 98.9%, Chapter 9 100% rendered, and Chapter 10 96.8%.
- Infographic validation passed with page counts 1, 2, 1, 1, and 3 for Chapters 6-10. Every page of both PDFs was reviewed in contact sheets; the final post-cover-change raster comparison was pixel-identical for all unchanged pages.
- Windows Python 3.12: 44 offline tests passed.
- Ubuntu WSL Python 3.14: 44 offline tests passed.
- After live-site parser fixes, Windows Python 3.12: 47 offline tests passed.
- Windows LyX 2.4 / TeX Live 2025: real compiler integration passed. The fixture produces both editable formats and both PDFs; supplied reference coverage reaches 100% for parsed content, TeX PDF, and LyX PDF.
- Integration also confirms a deliberately incomplete reference returns code 2 and a missing cached image returns code 1, without changing the last successful output.
- Unit tests cover compiler failures/timeouts, interrupted cache writes, publication rollback, ambiguous/duplicate mappings, scanned references, full-line mismatches, 95% boundaries, math rejection, lists/tables/images, and legacy DOCX/currency rendering.
- Rendered fixture pages reviewed: cover, contents, body, equations, tables, image placement, and nested lists. Existing book-style blank verso pages remain intentional.
- Python dependency check passed; source syntax and CI YAML checked; git diff --check passed.
- GitHub-hosted CI status for the balanced-layout change has not yet been observed. Linux compilers are not installed locally; compiler acceptance ran on Windows.
- Windows Python 3.12 after the balanced-layout change: 54 regular tests passed; one integration-marked test was intentionally deselected from that run.
- Windows LyX 2.4 / TeX Live 2025 after the balanced-layout change: the explicit compiler integration test passed in 61.64 seconds.
- Class 8 Science Chapter 9 was rebuilt from the validated URL cache. Parsed, TeX-PDF, and LyX-PDF reference coverage each reached 98.93% across reference pages 1-20; structural checks found 36 headings, 40 lists, and all 20 ordered images.
- Visually reviewed every page of both Chapter 9 PDFs plus full-size detail pages. Section 1.3 uses normal spacing, diagrams remain readable and uncropped, and page counts decreased from 20 to 18 for TeX and from 19 to 16 for LyX.
- Ubuntu WSL Python 3.14 after Linux optimization: 55 regular tests passed; `setup-linux.sh` passed `bash -n`. That WSL installation has no LyX/TeX binaries, so Linux compiler validation remains assigned to GitHub Actions.
- Windows Python 3.12 after Linux optimization: 55 regular tests passed and the real TeX/LyX compiler integration passed in 64.73 seconds.
- All 20 tracked reference PDFs opened successfully (360 pages total); the workbook ZIP is valid and contains 7 Class 8, 7 Class 7, and 6 Class 6 links.
- The first post-push Linux compiler job reached pytest but failed because sparse checkout omitted the relative `tmp/` parent used by `--basetemp`; the workflow now uses the runner's absolute temporary directory. GitHub actions were also updated to their Node 24 major versions.
- Windows Python 3.12 on 2026-09-10: 58 regular tests passed; one integration-marked test was deselected.
- Windows LyX 2.4 / TeX Live 2025 on 2026-09-10: the real compiler integration passed in 67.69 seconds. An initial invocation failed before collection because its temporary parent directory did not exist; rerunning with a valid workspace path passed.
- Ubuntu Python 3.14 on 2026-09-11: 65 regular tests passed; one integration-marked test was deselected.
- Ubuntu system pdfLaTeX and LyX successfully compiled all three full modules through both output paths. Class 6 produced 56-page TeX and 49-page LyX PDFs; Class 7 produced 96-page TeX and 82-page LyX PDFs; Class 8 produced 96-page TeX and 83-page LyX PDFs.
- Structural validation passed for every published module, including all source headings, body runs, lists, ordered image fingerprints, and chapter bookmarks. Every generated page was reviewed in contact sheets, and all final LyX chapter openings were rechecked at higher resolution after the banner adjustment.

## Known limits and next steps

- The Class 6 Maths browser-print references contain a few extraction artifacts or stale lines (`Construction of Square` and duplicated accessible equation text). Coverage remains above the required 95%, and exact unmatched lines are retained in `stage2/output/Class6-Maths/report.txt`.
- The tracked reference PDFs are not uniformly current. Class 6 Chapter 11 contains the Chapter 10 topic and reaches only 9.33% against the live Chapter 11 source; Class 8 Chapter 4 and Class 7 Chapter 6 contain older wording. Several other Class 6 references also predate substantial live rewrites.
- Reference-checked attempts were retained as diagnostic staging directories and were not published. The final full-class outputs were published from validated URL caches after both compiler and structural/rendered-content checks passed, with optional reference status recorded as `not checked` because the supplied references are stale or incorrect.
- The LyX cover still contains the template's hard-coded `V.L Memorial Public School` line; no replacement school name was supplied.
- The earlier standalone Class 8 Chapter 9 output remains under the ignored `stage2/output/Class8-Ch9-Solutes/` directory. Its three reference-only unmatched lines were one diagram caption and two wrapped practice-link fragments; coverage remained above the required threshold.
- Class 8 Chapter 3 was an earlier calibration run and has not been republished after the newer normalization fixes.
- Unsupported equations and complex HTML table spans/nesting fail for review. No OCR, formula-image transcription, or inferred equations from prose is performed.
- HTML question-bank detection and expanded fallback equation extraction are outside this change.
- Direct TeX retains a plain book design while LyX retains the Legrand theme; theme unification was excluded.
- Old chapter-number HTML caches are not silently reused; populate URL-keyed caches with an online build before offline operation.
- Failed diagnostic staging directories are retained. Successful replacements no longer retain prior output snapshots. Inspect stale publication locks and recovery directories after an interrupted publication; do not delete them blindly.
- See README.md for commands and explicit chapter-map JSON. Final local fixture outputs and diagnostics are under ignored tmp/ directories.
- GitHub authentication and repository push permission were verified; the user explicitly authorized this dev-branch push.

## Windows/Linux setup differences

- Windows environment: .venv/Scripts/python.exe. Linux environment: .venv-linux/bin/python. Both are ignored by Git.
- Created an isolated Ubuntu test environment; installed Ubuntu python3-venv and its pip/setuptools wheel dependencies because ensurepip was initially unavailable.
- Root requirements.txt covers the primary pipeline and retained fallback dependencies. System LyX and TeX Live packages are still required separately.
- Windows standard LyX installations are discovered if lyx is not on PATH. Linux/headless execution automatically uses `QT_QPA_PLATFORM=offscreen` when no display or explicit Qt platform is present.
- Git uses the clone-local OpenSSL HTTP backend after Schannel failed. No global safe-directory setting was added.
- The original Codex task still points at the downloaded folder, so clone writes require the approved sibling-directory access. Open the clone as the project for future work.
- Preserve Git line-ending handling; do not copy identical files solely to change CRLF/LF.
