# Handoff

## 2026-10-22 Git migration checkpoint

- The user explicitly authorized committing and pushing the current project-source changes to `origin/main` so work can continue on another computer. This is a one-off authorization, not standing permission for future automatic pushes.
- Includes the shared semantic question writers, Science adapters, reviewed table manifest, OMML preservation, header/validator corrections, regression tests, review/publication/portable-package tools, and these handoffs. Class 8 is completed and published; Class 6 formatting is implemented but its final rebuild, validation, page review, and publication remain pending.
- Validated source state: 16 focused tests passed; offline suite 99 passed with 5 deselected; real compiler integration 1 passed in 138.18s. All 293 Class 8 PDF pages passed smaller-model review. No new implementation changes were made for this Git checkpoint.
- Generated outputs, downloads, staging/review images and reports, caches, environments, logs, and secrets are excluded. Existing intentionally tracked class reference inputs remain tracked; no new supplied inputs are added.
- To continue elsewhere, clone/pull `main` from the configured repository and work from that checkout root. The legacy export's maintained checkout is currently `tmp/codex-push-dev-20260924/`; that nesting is not required on the new machine. Read the latest handoffs before rebuilding.
- Copy the separately supplied Class 6 question DOCX/PDF pairs into `Class 6th Science/` (or select their parent with `SCIENCE_INPUT_ROOT`). Copy validated offline caches separately and select the appropriate one with `SCIENCE_CACHE_DIR`; these are not in Git. Class 8 question pairs are already tracked. Select a staging destination with `SCIENCE_OUTPUT_DIR`.
- Install `requirements.txt`, LyX 2.4+, and TeX Live as documented in README. Use a short Windows checkout/test-temp path to avoid the 260-character media-path failure. Do not copy a Windows virtual environment to another machine; recreate it there. Linux/CI tests have not been run locally.
- Next Class 6 action: rebuild with the latest shared adapter/header/OMML changes, rerun mandatory source/structure/compilation/integrity checks, use smaller-model testing and the already-requested full-page review, and publish only after acceptance. The old review-pending ZIP is not an approved release.


## 2026-10-22 Class 8 corrections completed and published

- Scope is now Class 8 only. The maintained `main` checkout at `tmp/codex-push-dev-20260924/` remains dirty at `3f3a43b8cf4881753252a45db4ceaba0e2a13798`. No commit/push is authorized or performed.
- The missing OMML content is repaired: three Chapter 9 cubic-unit superscripts and four Chapter 12 food-chain arrows. Worksheet row/event extraction now preserves supported math in source order and rejects unsupported OMML; paired source audits include complete math-bearing paragraphs.
- Regular-weight native questions, per-type numbering resets, alphabetic nested case parts, omitted case marks/OR with retained metadata, full-width answer rules, five native tables, and one-time half-scale diagrams pass structural/content checks. Inventory: 405 source rows, 525 top-level rendered items, 80 case parts, 19 omitted OR labels, 538 answer lines, four genuine question diagrams. All five original table-image byte streams are retained under `media/originals/` and checked against reviewed hashes.
- Corrected long running-header boxes separate titles from folios in both formats. The validator now excludes isolated wrapped header blocks without dropping unrecognized top-margin body text. Final PDFs are 163 TeX and 130 LyX pages.
- Smaller-model subagents individually reviewed all 293 final pages. Hash-backed records are `tmp/s8boxedreview/review-tex.json` and `review-lyx.json`; acceptance is stored in `tmp/s8complete/Final-Science_Class8th/visual-review.json`. Both reviews passed. Minor supplied-image/legacy notes-spacing observations are recorded, without rewriting source text; three non-clipping notes-only TeX overfull warnings remain.
- Actual Windows tests: 16 focused and 99 offline passed (5 deselected); real compiler integration passed 1 test in 138.18s using short absolute `tmp/it23c/`. Earlier sandbox/long-path attempts were not counted as passes. Only the known optional pytest-cache ACL warning remains. No Linux/CI execution is claimed.
- Both real compilers succeeded. Validator-only refresh reused byte-identical PDFs after all sources/themes/rendered media matched; original non-rendered media was added for provenance. Final candidate: `tmp/s8complete/Final-Science_Class8th/`. Download: `stage2/downloads/Final-Class-8-Science-LyX.zip` (172 book files plus OPEN-ME; SHA-256 `6e9b1ee65d128722ead3f9401dd484fbf938299824020d81e4ac3b20b38ac6df`). ZIP CRC and every packaged member hash passed; extract all files before opening LyX.
- Atomically published and SHA-256-verified all 184 files to `stage2/output/Final-Science_Class8th/` and external `Science_Class8th/` under the configured release root. Previous local output is recoverable at `stage2/output-obsolete-science-20261022-112710/Final-Science_Class8th/`; previous external output is under `archive-science-20261022-112710/Science_Class8th/` in the release root. The combined release report was updated for Class 8 only. Aggregate tree hashes confirm Class 6 local/external and Class 7 external files are unchanged. Class 6 remains review-pending and is not included in this publication.


## 2026-10-22 downloadable candidates; final publication blocked

- Maintained branch is `main`, HEAD `3f3a43b8cf4881753252a45db4ceaba0e2a13798`; implementation is uncommitted. No commit/push performed. Active export has no Git metadata.
- Both Class 6/8 candidates compile and pass current structural/content checks. PDF pages: Class 6 TeX/LyX 128/108; Class 8 163/130. Independently image-reviewed native tables total 17 (12/5); case parts 72/80; answer lines 498/538.
- Actual Windows tests: 10 focused passed; 92 offline passed, 5 deselected; real compiler integration 1 passed, 96 deselected in 145.03s using short `tmp/it22/`. Earlier integration failed with a 261-character media path; successful path was 195. No CI/Linux result claimed.
- BLOCKER: final visual review found three Class 8 Chapter 9 density prompts missing supplied superscript 3 after cm. Confirmed DOCX XML contains `m:oMath/m:sSup` exponent 3; plain cell/paragraph text extraction omits it. Existing prose audits omit OMML too and missed this. Implement conservative OMML extraction and strict source/compiled validation, then rebuild both Class 8 formats. Never guess formulas.
- Smaller-model reviewers inspected all Class 6 baseline pages and all 130 Class 8 LyX pages. Final Class 6 changed TeX pages 27,69,87,108,128 require reinspection. Complete final Class 8 TeX coverage is unconfirmed; reviewer reached at least p108 before usage limit. Do not synthesize passing review records. Review agents hit their usage limit before final coverage/records completed.
- Portable CRC/member-SHA-verified REVIEW-PENDING ZIPs are available in active export `stage2/downloads/Class-6-Science-LyX-Review-Pending.zip` (147 files) and `stage2/downloads/Class-8-Science-LyX-Review-Pending.zip` (163 files). Explicit DELIVERY-STATUS.txt is included in each. Extract the entire ZIP first. These are not approved final releases.
- Original final output folders and external releases remain unchanged. Next: repair/test OMML, rebuild Class 8, complete requested smaller-model visual inspection, run visual acceptance, atomically publish, regenerate final ZIPs. No publication until all required checks pass.


## 2026-10-22 Science question formatting rebuild in progress

- User approved correcting Class 6 and Class 8 Science questions in both writers: regular-weight native enumeration, nested alphabetic parts, full-width answer rules, one rule per case mark, removal of printed case marks and OR, and native tables from reviewed pictures. Downloadable portable LyX packages are requested; email is no longer requested. No commit or push is authorized.
- Implementation is in the maintained `main` checkout under `tmp/codex-push-dev-20260924/`. Shared rendering is `stage2/question_layout.py`; source parsing remains in the two `tools/rebuild_class*_science_practice.py` adapters. The SHA-256-keyed `tools/science_table_manifest.py` contains 17 verified tables (12 Class 6, 5 Class 8); the earlier estimate of 18 was corrected after complete inventory. A smaller-model reviewer checked all cells against all 17 original images.
- First Class 6 candidate compiled and passed source checks at `tmp/science-corrections-staged/Final-Science_Class6th/` (128 TeX pages, 108 LyX pages). All 108 initial LyX pages were reviewed; `tmp/science-review-class6/review-lyx.json` records page hashes and findings. The temperature-table width was corrected after that review, so the first candidate is not final. The refreshed Class 6/Class 8 builds are running sequentially; final page review, final source checks, publication and download packages remain pending.
- Latest focused tests: 7 passed. Prior offline run: 89 passed, 4 deselected. Integration requires a definitive rerun after full builds; older session output was inconclusive. Original final outputs and external releases remain intact. Legacy notes observations include a long running header and source text `Sarasvatiregion`; preserve source wording and report separately from question-layout corrections.

## 2026-10-17 portable main-branch handoff

- The reviewed portable source change was pushed to `origin/main` as commit `5264332` (`feat: preserve complete science build context`).
- Prepared the maintained checkout on `main` for migration to another computer. Promoted the completed Science practice adapters and Class 6 source-audit helper from ignored temporary files into tracked, machine-independent scripts under `tools/`; removed sibling-checkout assumptions and documented their use in `README.md`.
- Reconciled the active build overlay without importing stale reversions: retained automatic cleanup of successful publication snapshots and existing equation/operator normalization checks, while adding the verified Windows LyX fallback, display-equation prose handling, question true/false blanks, pre-option figures, rounded LyX image scaling, Class 6 workbook map, and `COVID-19` line-break normalization.
- Preserved the complete Class 6/Class 8 operational history in both handoffs and the production template settings used by the final books. Generated outputs, caches, environments, logs, secrets, and the separately supplied untracked Class 6 question inputs remain outside Git; the tools explain what must be copied separately for a rebuild.
- Validation of the exact prepared checkout: 82 offline tests passed with 5 XLSX-construction tests deselected; real TeX/LyX integration passed with 1 test and 86 deselected in 86.23 seconds; all three tracked tools passed bytecode compilation; `git diff --check` passed. The only warning was pytest's inability to write its optional cache under the ACL-owned checkout. No Linux or configured CI result is claimed.

## 2026-10-17 Class 6 Science completed

- Completed and atomically published `stage2/output/Final-Science_Class6th/` for workbook-selected Chapters 3, 4, 6, 7, 11, and 12. The direct-TeX PDF is 122 pages and the themed-LyX PDF is 103 pages; editable TeX/LyX sources, media, manifest, and reports are included. The same 163 files were hash-verified and promoted to `D:\Science-Book-Releases\Science_Class6th/`, and the combined release report was updated.
- Preserved 354 supplied question rows as 450 rendered items, including all supplied options and expanded true/false and fill-in statements. All 1,224 extracted DOCX prose fragments were found in the paired source PDFs, and compiled-output checks report zero missing supplied question text in either PDF. Eighteen question figures remain in source order and use the required one-time `0.5` sizing factor.
- Recorded source issues without rewriting them: the Chapter 12 question files internally say Chapter 11, although their filenames, authoritative map, and astronomy content identify Chapter 12; Chapters 3, 11, and 12 each contain a pair of identical generic `Match the following:` prompts with distinct supplied figures. All were preserved in source order.
- Fixed a narrow validator false negative for letter-number identifiers broken at PDF line endings (`COVID-19` versus `COVID-\n19`) while preserving subtraction identity (`x-19` remains distinct from `x19`). The focused tests passed (2/2), offline regressions produced 81 passes plus four dependency-only failures because the older sibling test environment lacks `openpyxl`, and the real compiler integration passed (1/1). Representative TeX/LyX pages were visually checked without clipping, overlap, or broken grids; exhaustive page-by-page review remained skipped as previously agreed.
- Moved the three failed Class 6 staging attempts out of the active output folder into `stage2/output-obsolete-class6-20261017/`. `stage2/output/` now contains only the five current final folders. The maintained clone remains clean on `dev` at `96c07186d420839e657f19316e39bb99895e51a9`; no commit or push was authorized or performed.

## 2026-10-16 output cleanup completed

- `stage2/output/` now contains only the four verified current folders: `Final-Science_Class8th/`, `Final-Class6-Maths-Complete/`, `Final-Class7-Maths-Complete/`, and `Final-Class8-Maths-Complete/`.
- Permanently removed 30 accessible older outputs, dated snapshots, and failed staging directories. Windows denied deletion, ownership changes, and individual moves for 28 execute-only directories created by an older sandbox account, so the user approved moving them elsewhere. Their common former output container is now the single sibling quarantine `stage2/output-obsolete-protected-20261016/`.
- The clean output container was rebuilt by extracting the four final folders, renaming the old container to the quarantine name, and restoring the clean container as `stage2/output/`. All 571 files across the four final folders matched their pre-move SHA-256 hashes and all four reports remain `passed`. External releases were unchanged. No rebuild, commit, or push was performed.

## 2026-10-16 Final output folder labels

- Renamed the four most recently completed current outputs to make them easy to identify: `stage2/output/Final-Science_Class8th/`, `stage2/output/Final-Class6-Maths-Complete/`, `stage2/output/Final-Class7-Maths-Complete/`, and `stage2/output/Final-Class8-Maths-Complete/`.
- Verified every file by SHA-256 before and after the moves: 179, 158, 96, and 138 files respectively. Staging directories, dated previous-output snapshots, notes-only folders, and the external `D:\Science-Book-Releases\` publication were not renamed. No rebuild, commit, or push was performed.

## 2026-10-16 Class 8 Science completed

- Completed and atomically published `stage2/output/Final-Science_Class8th/` for workbook-selected Chapters 3, 4, 7, 8, 9, 10, and 12, combining the supplied notes with all seven supplied DOCX/PDF question pairs. The direct-TeX PDF is 152 pages and the themed-LyX PDF is 123 pages; editable sources, media, manifest, and reports are included. The external release is `D:\Science-Book-Releases\Science_Class8th\`; its previous version is recoverable at `D:\Science-Book-Releases\Science_Class8th.previous-20261016-142128\`.
- Preserved 405 source question rows as 525 rendered items, including expanded supplied true/false and fill-in statements. Per-chapter type counts are in `stage2/output/Final-Science_Class8th/report.json`. All 1,555 DOCX prose fragments were found in the paired PDFs, and compiled prose checks found no missing supplied question text in either output. Nine question figures retain source order and use the required one-time `0.5` sizing factor in both formats.
- Chapter 4's internal question title says Chapter 3. The user explicitly confirmed this is an internal naming mistake and that the files belong to Chapter 4; the source files were not edited. Chapter 3 source questions 31 and 32 both say `Match the following:` but have distinct figures, so both were preserved in order.
- Extended the local ignored adapter `tmp/rebuild_class8_science_practice.py` for all seven chapters and added narrow writer support in `stage2/convert.py` for pre-option MCQ figures and true/false answer blanks. Question-type headings, per-block numbering restarts, assertion-reason A/B then C/D grids, supplied wording, and image order were validated.
- Final `report.json` status is `passed`; both PDFs reopen, both compiler paths pass, structural checks pass, and source/compiled prose checks report zero missing items. Representative pages from every affected layout were rendered and visually inspected without clipping, overlap, or broken grids. Exhaustive page-by-page review was skipped as agreed; independent notes-reference PDF coverage remains `not checked`.
- Windows validation: targeted offline regressions produced 80 passes, 5 deselections, and one unrelated stale Class 6 workbook-expectation failure; the final real compiler integration passed in 96.52 seconds. No Linux or CI execution is claimed. The active export has no `.git`; the clean publication clone remains on `dev` at `96c07186d420839e657f19316e39bb99895e51a9`. The manifest records that commit and dirty local adapter/writer overlay state. No commit or push was requested or performed.

## 2026-10-15 Class 6 Maths completed

- Completed and atomically published `stage2/output/Final-Class6-Maths-Complete/` from the validated offline Class 6 Maths notes cache and the five supplied DOCX/PDF question pairs for Chapters 6-10. Both editable TeX/LyX sources and compiled PDFs passed; direct TeX is 80 pages and themed LyX is 72 pages. The earlier `stage2/output/Class6-Maths/` notes-only output remains preserved.
- The book contains 347 top-level questions and 73 supplied question figures. Per-chapter question/figure counts are Chapter 6: 70/18, Chapter 7: 70/12, Chapter 8: 67/1, Chapter 9: 70/33, and Chapter 10: 70/9. Compiled prose checks found no missing supplied question text in either PDF. All question figures have an exact `scale / base_scale` ratio of `0.5`; notes and infographic sizing are unchanged. `manifest.json` records `question_image_scale: 0.5`, input hashes, the adapter hash, pipeline hashes, source commit `6b156ffd7c4e35ab13640a4d36283445ae5e8d3e`, and dirty local-input/overlay state.
- Preserved and reported source issues without correction or deletion: DOCX/PDF sublabel-count differences in Chapters 6, 7, 9, and 10; the exact duplicate Chapter 6 prompts at source questions 39/48; Chapter 7 duplicate prompts at 5/8/10, 37/38, 44/47, and 53/54; and Chapter 9 duplicate prompts at 40/42/47 and 32/53. All 985 substantive DOCX prose checks across the five paired question PDFs matched; labels were aligned to adjacent supplied prose, with blank/equation-only Word list items retaining their source sequence.
- Extended the ignored local adapter `tmp/build_math8_complete.py` to support Class 6 Chapters 6-10, conservative OMML matrices, text-only underscore placeholders, image-first LyX question layouts, literal rupee rendering, per-question-section TeX line breaking, and explicit half-scale validation/manifest metadata. Unsupported content still fails closed; no questions, answers, options, equations, or missing wording were generated.
- Final `report.json`/`report.txt` status is `passed`, with empty compiler diagnostics and no reported overfull boxes. TeX/LyX source structure, chapter bookmarks, numbering/type blocks, options, equations, image order/fingerprints, source hashes, and compiled prose passed. Representative covers, MCQ/assertion-reason grids, diagram-heavy pages, case-based pages, and fill-in pages from both PDFs were rendered and inspected. Exhaustive page-by-page review was not opted into and was skipped; independent formula/infographic reference coverage was not rerun, while supplied question PDF/DOCX comparison passed.
- Windows verification: offline regressions 81 passed and 5 XLSX-dependent cases deselected; real compiler integration 1 passed and 85 deselected. No Linux or CI execution claimed. The active export has no `.git`; no commit or push was requested or performed.

## 2026-10-14 Class 7 and 8 Maths rebuilt with half-size question diagrams

- Rebuilt and published `stage2/output/Final-Class7-Maths-Complete/` and `stage2/output/Final-Class8-Maths-Complete/` from validated offline caches and the supplied question DOCX/PDF pairs. Existing outputs were preserved through failed staging attempts and replaced only after both TeX and LyX PDFs passed compilation and strict structural/content checks.
- Class 7 contains 477 top-level questions and 33 supplied question figures across Chapters 9-15; direct TeX is 94 pages and themed LyX is 77 pages. Class 8 contains 484 questions and 54 figures across Chapters 8-14; direct TeX is 110 pages and themed LyX is 91 pages.
- Every question figure records an exact `scale / base_scale` ratio of `0.5` in both books. Notes and infographic sizing were unchanged. Manifests record `question_image_scale: 0.5`, source commit `6b156ffd7c4e35ab13640a4d36283445ae5e8d3e`, dirty overlay state, adapter/pipeline hashes, and source hashes.
- Class 7 source issues were preserved and reported: DOCX/PDF sublabel-count differences in Chapters 9-14; one unmatched DOCX prose fragment in Chapter 9; one unmatched DOCX paragraph in Chapter 14; and the exact duplicate prompt `Match the following` at Chapter 11 questions 21-22. No content was invented, corrected, or deleted. Class 8 retains its reported Chapter 10 label difference and Chapter 14 empty math placeholder/incomplete Q56 clause.
- Added a narrow Windows compiler fallback: after isolated LyX-profile attempts fail with the observed empty-log exit 11, retry the same noninteractive export with the configured LyX profile and still fail closed on error. Added dotless-i PDF extraction normalization for pdfTeX transliteration (`B¯ıja` equivalent to `Bīja`) with regression coverage.
- Validation: both final reports are `passed`, compiler diagnostics are empty, and source/compiled prose, editable math, image order/fingerprints, chapter mapping, numbering/type blocks, options, and source hashes passed. Representative covers, assertion-reason grids, and diagram pages from both compiler paths were rendered and inspected; exhaustive page-by-page review was not opted into and was skipped.
- Windows tests: 81 passed, 5 deselected when excluding XLSX tests; real compiler integration 1 passed, 85 deselected. The unfiltered suite had 81 passes and four XLSX failures because the available sibling `.venv` lacks `openpyxl`; an earlier repository-root invocation was invalid because it collected retained restricted build directories. No Linux or CI execution claimed.
- The active export still has no `.git`. The publication clone `tmp/codex-push-dev-20260924/` is clean on `dev` at `6b156ff`, matching cached `origin/dev` and `origin/main`. No commit or push was requested or performed.

## 2026-10-10 Class 7 Maths sources and deferred diagram sizing

- User authorized publishing the newly added Class 7 Maths question files and the previously agreed 50% diagram rule. Publication scope is seven DOCX/PDF pairs for Chapters 9-15 (14 files), `AGENTS.md`, `CLAUDE.md` v4.8, and both handoff documents. Formula PDFs, temporary files, and generated books are excluded. Use the clean `dev` clone at `tmp/codex-push-dev-20260924/` and fast-forward publication to the previously used `origin/main` and `origin/dev`; remote fetched and both heads confirmed at `d8ffb3d` before changes.
- All seven Word packages passed ZIP integrity and document-read checks; all seven PDFs opened (51 pages). Source copies match SHA-256. This verifies file integrity, not question content, chapter mapping, or completeness for conversion; those audits remain pending.
- Saved sizing rule: apply an additional 0.5 factor once to the otherwise selected question-diagram dimensions in both TeX and LyX; preserve proportions, source files, labels, and order. Notes and infographic sizing retain existing behavior. Never compound the factor on later rebuilds or interpret it as a fixed 50% text-width setting.
- Implementation and rebuilding remain deferred per the user. No converter, adapter, or generated PDF was changed. Existing Class 8 PDFs retain their previous sizes; the source publication also carries the prior completed Class 8 build record below.
- Validation for this update: Windows source file integrity/hash checks, documentation consistency and diff/whitespace review. No build, regression tests, compiler tests, Linux execution, or CI execution needed or claimed for this documentation/source-only change. Next: apply the sizing rule and build Class 7 only when separately requested, after source-content audits.

## 2026-10-10 Class 8 Maths completed

- Completed the user's objective: pushed rules and all 14 supplied question files, then built Chapters 8-14 with 484 top-level questions and 54 supplied question figures. No questions, options, answers, explanations, or missing source content were generated.
- The publication clone at `tmp/codex-push-dev-20260924/` is clean on `dev`. Commit `d8ffb3da9a24feb0f8e12b8b6f1ce26960d6f401` was fast-forward pushed to both `origin/main` and `origin/dev`; live remote heads were verified. Generated books and temporary build adapters were excluded from Git. This final operational note is local, added after that push.
- Published `stage2/output/Final-Class8-Maths-Complete/`: themed LyX PDF 98 pages, direct TeX PDF 120 pages, editable sources, media, manifest, and validation reports. The existing `stage2/output/Class8-Maths/` was preserved. Both compilers and all mandatory structural, rendered-prose, equation, and image-order checks passed; final compiler diagnostics are empty. All 14 source hashes still match the pushed inputs.
- Source issues preserved and reported: Chapter 10 Word/PDF sublabel differences; Chapter 14 an empty math placeholder and unfinished source Q56 clause `To make decorative pieces,`. No exact duplicate prompts were found. Per-chapter question counts are 68, 68, 70, 69, 70, 69, 70 for Chapters 8-14 respectively.
- Windows tests: offline regressions 81 passed, 5 deselected; separate real compiler integration 1 passed, 85 deselected. No Linux or CI execution claimed. Optional independent reference-PDF coverage was not checked; supplied question PDF/DOCX content comparison and compiled-output checks passed for all seven chapters.
- Page-by-page visual review was declined. Representative cover, assertion-reason grid, and corrected long-data-line pages were inspected. Assertion-reason options use A/B then C/D checkbox grids and supplied wording; numbering restarts per block and source sublabels are retained.
- Build used validated offline caches with the local adapter `tmp/build_math8_complete.py` and sibling Windows `.venv`; automatic question ingestion in application code remains incomplete. The active export has no `.git` and includes a pre-existing pipeline overlay. Manifest records source commit, dirty state, adapter/pipeline hashes, and source hashes. Next: review the reported source issues with the author; do not complete them automatically.

## 2026-10-10 Class 8 Maths source publication and build

- User authorized pushing the current rules and all seven chapter question DOCX/PDF pairs before completing the Class 8 Maths book. Publishing to both `origin/main` and `origin/dev` by fast-forward; no force push.
- All 14 source files opened successfully (61 PDF pages); copied files match SHA-256, including the existing Chapter 8 filename with a space before `.pdf`. Word lock files and unrelated files are excluded. Content comparison and chapter/type audits are still pending for the build.
- Rules are in `CLAUDE.md` v4.7 and `AGENTS.md`; retained the clone's newer release history while importing the rule updates. Staged diff and whitespace checks reviewed. No code changes or new compiler/test results in this source publication.
- Page-by-page visual inspection was declined for this release. Mandatory compilation, structural, rendered-content, equation, and image checks still apply. Build is pending; preserve existing output on failure.

## 2026-10-10 Additional question-source checks

- User approved all suggested additions. Updated `AGENTS.md`, `CLAUDE.md` (v4.7), and `docs/CODEX_HANDOFF.md` with source-problem reporting, verified chapter placement, and per-chapter completeness checks.
- Report duplicate questions, missing options, incomplete statements, and DOCX/PDF wording conflicts without silently correcting, deleting, or choosing conflicting content. Verify source chapter identifiers against the authoritative chapter map before insertion; flag ambiguities.
- Record question counts by type for every chapter and verify each supplied question, option, answer, table, and figure in both compiled outputs; counts alone are insufficient.
- Exact assertion-reason options supplied once as common section instructions may be repeated beneath every pair in their stated scope. Missing options still must not be generated; unclear scope requires review.
- Objective remains documentation preparation for Class 8 question processing. Active export has no `.git`; the existing clone at `tmp/codex-push-dev-20260924/` remains clean on `dev`, one commit ahead of cached `origin/dev`. No remote refresh performed.
- Validation: reviewed the four-document diff, rule consistency, and whitespace checks on Windows. No tests, conversions, builds, commits, pushes, or Linux checks run. Pre-edit copies are under `tmp/question-rules-followup-before-20261010/`.
- Next step: inspect the supplied chapter files and report mappings, counts, and source issues before conversion. Automatic question ingestion remains incomplete; no application code or generated books changed.

## 2026-10-10 Question-formatting rules update

- Objective: document the user's rules before processing the newly supplied Class 8 chapter questions. Documentation only; no conversion, build, commit, or push.
- Active workspace is a legacy export without `.git`. The existing clone at `tmp/codex-push-dev-20260924/` is on `dev`, clean, with one local commit ahead of its cached `origin/dev`; no remote refresh was run for this update.
- Updated `AGENTS.md` and `CLAUDE.md` (v4.6): use only supplied questions, answers, solutions, explanations, and options. Never generate, infer, complete, or rewrite them; flag missing or unclear content.
- Assertion-reason options must use the MCQ two-column checkbox grid (A/B first row, C/D second), preserving source wording and order. Removed the fixed-option insertion requirement and replaced the examples with source-content placeholders. This supersedes the stacked assertion-reason layout recorded for the 2026-09-23 Science build.
- Top-level numbering restarts at 1 for every question-type block, including repeated types. Source subquestion and alternative labels are preserved; the older blanket numbering-strip instruction has been narrowed.
- Validation: reviewed the four-document diff and checked for conflicting fixed-option/numbering instructions and whitespace errors. No application tests or compilers run because only documentation changed.
- Next step: inspect and map the supplied chapter question files before conversion; missing options/content require review. These rules do not add automatic question ingestion or change existing generated books.
- Platform: edits and checks performed on Windows; no Linux validation run. Pre-edit copies retained under `tmp/question-rules-before-20261010/`.

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
