# Handoff

## Current objective and branch

- Implemented reliable note generation plus balanced page spacing and diagram sizing.
- Branch: dev, tracking origin/dev.
- Working in the Git clone; the downloaded source folder remains unchanged.
- User authorized pushing the balanced-layout changes to origin/dev. Earlier reliability changes were pushed on 2026-09-08.

## Completed work and decisions

- Added validated URL-keyed page/image caches, bounded retries, atomic cache writes, offline and refresh modes.
- Added mandatory dependency/compiler preflight, staged builds, TeX and LyX-exported PDF compilation, bounded passes/timeouts, and retained logs.
- Publication checks source structure, rendered prose, chapter bookmarks, and embedded image fingerprints/order. Previous successful output survives failed builds; successful replacements retain a timestamped snapshot.
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

## Tests and results

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

## Known limits and next steps

- Class 8 Chapter 9 is published under the ignored `stage2/output/Class8-Ch9-Solutes/` directory with editable TeX/LyX, both PDFs, compiler logs, manifest, and validation reports.
- Three reference-only lines remain unmatched: one diagram caption and two wrapped practice-link fragments. Coverage remains above the required threshold; the score is diagnostic rather than proof of perfect fidelity.
- Class 8 Chapter 3 was an earlier calibration run and has not been republished after the newer normalization fixes.
- Unsupported equations and complex HTML table spans/nesting fail for review. No OCR, formula-image transcription, or inferred equations from prose is performed.
- HTML question-bank detection and expanded fallback equation extraction are outside this change.
- Direct TeX retains a plain book design while LyX retains the Legrand theme; theme unification was excluded.
- Old chapter-number HTML caches are not silently reused; populate URL-keyed caches with an online build before offline operation.
- Diagnostic staging directories and previous snapshots are retained. Inspect stale publication locks and recovery directories after an interrupted publication; do not delete them blindly.
- See README.md for commands and explicit chapter-map JSON. Final local fixture outputs and diagnostics are under ignored tmp/ directories.
- GitHub authentication and repository push permission were verified earlier; branch protections were not tested. Commit/push only when authorized.

## Windows/Linux setup differences

- Windows environment: .venv/Scripts/python.exe. Linux environment: .venv-linux/bin/python. Both are ignored by Git.
- Created an isolated Ubuntu test environment; installed Ubuntu python3-venv and its pip/setuptools wheel dependencies because ensurepip was initially unavailable.
- Root requirements.txt covers the primary pipeline and retained fallback dependencies. System LyX and TeX Live packages are still required separately.
- Windows standard LyX installations are discovered if lyx is not on PATH. Linux/headless CI uses QT_QPA_PLATFORM=offscreen.
- Git uses the clone-local OpenSSL HTTP backend after Schannel failed. No global safe-directory setting was added.
- The original Codex task still points at the downloaded folder, so clone writes require the approved sibling-directory access. Open the clone as the project for future work.
- Preserve Git line-ending handling; do not copy identical files solely to change CRLF/LF.
