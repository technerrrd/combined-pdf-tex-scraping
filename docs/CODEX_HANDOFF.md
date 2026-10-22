# Codex project handoff

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


## 2026-10-22 active Science corrections

The user requested implementation of the approved Class 6/Class 8 formatting plan and downloadable LyX packages with all dependencies. Email delivery was explicitly withdrawn. Work is in the maintained `main` checkout, with changes uncommitted. Shared semantic question rendering handles native top-level enumeration, lowercase alphabetic case parts, regular-weight prompts, full-width answer rules, and native TeX/LyX tables. Case-only marks and standalone OR are intentionally omitted from printed output but retained in metadata. The original DOCX/PDF sources are unchanged.

All 17 actual table pictures (12 Class 6, 5 Class 8) were independently checked cell by cell by a smaller-model reviewer against their source images. The table manifest is keyed by original image SHA-256 and fails on changed reviewed sources. Original table media is retained for provenance but excluded from rendered content. Question diagrams still use the one-time 0.5 multiplier. Source inventories are unchanged: Class 6 has 354 source rows/450 rendered items; Class 8 has 405/525.

The first Class 6 candidate passed compilation and source checks (128 TeX pages, 108 LyX pages). A smaller-model reviewer inspected all 108 LyX pages and recorded hashes in `tmp/science-review-class6/review-lyx.json`. The temperature table on page 72 extended past the text margin; its widths have since been corrected. Three separate questions after that table now use nested alphabetic enumeration. A second rebuild is required before final review/publication. Source-only spacing quirks such as `Sarasvatiregion` and older notes/header observations were recorded without rewriting source text. Current builds stage under `tmp/science-corrections-staged/`; existing final folders and external releases are still untouched. Tests currently have 7 focused passes and a prior 89-pass offline run. Real integration must be rerun definitively, and all final PDF pages must be inspected before final publication.

## 2026-10-17 portable main-branch migration

The reviewed portable source change was pushed to `origin/main` as commit `5264332` (`feat: preserve complete science build context`).

The maintained Git checkout was advanced to current `origin/main` and prepared as the portable source of truth for moving the project to another computer. The completed Science question adapters and Class 6 read-only source audit were promoted from ignored temporary files to `tools/rebuild_class8_science_practice.py`, `tools/rebuild_class6_science_practice.py`, and `tools/audit_class6_science.py`. They now derive provenance from the current checkout, use repository-local cache/output paths, and contain no dependency on the old sibling clean clone. `README.md` documents their prerequisites and commands.

The active overlay was reconciled rather than copied wholesale. The maintained branch keeps successful-publication snapshot cleanup and its existing subscript/arrow identity tests. It gains the verified Windows LyX configured-profile fallback, equation-boundary prose validation, triangle/congruence/transliteration normalization, `COVID-19` PDF line-break handling without weakening `x-19`, true/false answer blanks, MCQ pre-option figures, rounded LyX scaling, current Class 6 workbook mapping, and the template settings used by the completed books. Regression coverage was added for the new question writer behavior and identifier normalization.

Exact-checkout validation on Windows: `pytest -q tests -k 'not xlsx'` passed 82 tests with 5 deselected; the real compiler integration passed 1 test with 86 deselected in 86.23 seconds; all three `tools/` scripts passed bytecode compilation; `git diff --check` passed. Pytest emitted only an optional cache-write warning caused by the checkout's older ACL ownership. No Linux or configured CI run is claimed.

Generated `stage2/output/` content, scraped caches, virtual environments, logs, secrets, and the separately supplied untracked Class 6 question DOCX/PDF inputs remain intentionally excluded from Git. To reproduce Class 6 on a new computer, copy those question pairs into `Class 6th Science/` and restore/populate `input/scraped/`; the tracked workbook, note references, source code, tests, adapters, and complete handoff context are in Git.

## 2026-10-17 Class 6 Science notes and questions completed

The Class 6 Science book is complete for workbook-selected Chapters 3, 4, 6, 7, 11, and 12. `stage2/output/Final-Science_Class6th/` contains editable TeX and LyX sources, media, a 122-page direct-TeX PDF, a 103-page themed-LyX PDF, `manifest.json`, and a passed validation report. All 163 files were copied atomically and SHA-256 verified at `D:\Science-Book-Releases\Science_Class6th/`; the top-level release report now records the new chapter set, page counts, practice inventory, source commit `96c07186d420839e657f19316e39bb99895e51a9`, dirty overlay, and uncommitted supplied question inputs. Released PDF hashes are `9aefa0919abdc95c784a1afedcc35789c317ed51b357e0f3f9c09cd2c28cbe8c` for TeX and `fb8363d6b579e08edf7408e18f8f552a34409f91e4fd1b5e8ff2ea81f24f0c97` for LyX.

The question inventory is 354 source rows and 450 rendered items, 75 per chapter after expanding only supplied true/false and fill-in groups. All 1,224 extracted DOCX prose fragments occur in their paired PDFs, and chapter-aware compiled checks found zero missing supplied question text in either final PDF. Eighteen supplied question figures retain source order and the required one-time `0.5` sizing factor. Assertion-reason options render A/B then C/D, and question-type headings and top-level numbering restart for each type block.

Source issues were reported rather than repaired. Chapter 12's question DOCX/PDF internally says Chapter 11, while its filename, authoritative workbook mapping, and astronomy content identify Chapter 12, so it was placed under Chapter 12 without modifying the sources. Chapters 3, 11, and 12 each contain two exact generic `Match the following:` prompts with distinct figures; each pair was preserved in order.

A narrow normalization change now treats multi-letter/digit identifiers such as `COVID-19` as equivalent when pdfTeX inserts a line break after the hyphen, while one-letter subtraction such as `x-19` remains distinct from `x19`. The two focused validator/workbook tests passed. The non-integration suite produced 81 passes and four dependency-only failures because the available older sibling Windows environment lacks `openpyxl`; the actual workbook was parsed successfully by the build and focused workbook test. The real TeX/LyX compiler integration passed in 76.35 seconds. Representative cover, assertion-reason, match-table, and question-figure pages from both PDFs were rendered and visually inspected without clipping, overlap, or broken grids. Exhaustive page-by-page inspection remained skipped under the user's earlier choice; independent reference coverage is `not checked`.

Three failed Class 6 staging directories were moved intact to `stage2/output-obsolete-class6-20261017/`, outside active output discovery. `stage2/output/` now contains only `Final-Science_Class6th/`, `Final-Science_Class8th/`, and the three final Maths folders. The active export has no Git metadata; the maintained clone is clean on `dev` at `96c07186d420839e657f19316e39bb99895e51a9`. No commit or push was authorized or performed.

## 2026-10-16 output-folder cleanup

The user approved removing every non-final directory from `stage2/output/`. Thirty accessible legacy outputs, dated snapshots, and failed staging directories were permanently deleted. Twenty-eight old temporary directories could not be read, deleted, re-ACL'd, or moved individually: they have execute-only permissions originating from an older sandbox identity, and both native Windows and WSL permission repair were denied by the filesystem. The user then explicitly approved moving them to another folder.

To remove the clutter without touching inaccessible contents, the four verified final folders were moved into a clean staging container, the old `stage2/output/` container—then holding only the 28 protected remnants—was renamed to the sibling `stage2/output-obsolete-protected-20261016/`, and the clean container was renamed back to `stage2/output/`. The active output directory now contains exactly `Final-Science_Class8th/`, `Final-Class6-Maths-Complete/`, `Final-Class7-Maths-Complete/`, and `Final-Class8-Maths-Complete/`. All 571 final files were SHA-256 checked before and after the swap, and all four reports remain `passed`. The external `D:\Science-Book-Releases\` tree was not changed. Deleting the single quarantine directory still requires a Windows process with permission to alter those legacy ACLs; it is outside the active output directory and no longer clutters normal output discovery. No compiler/test rerun, commit, or push was needed or performed.

## 2026-10-16 final output folder labels

At the user's request, the four most recently completed current output folders were renamed to `stage2/output/Final-Science_Class8th/`, `stage2/output/Final-Class6-Maths-Complete/`, `stage2/output/Final-Class7-Maths-Complete/`, and `stage2/output/Final-Class8-Maths-Complete/`. Before each move, the source and target were resolved beneath `stage2/output/`, all sources were confirmed present, and all targets were confirmed absent. Every file was hashed before and after the rename: the verified file counts are 179, 158, 96, and 138 respectively. No content changed. Staging directories, dated prior-output snapshots, notes-only outputs, and `D:\Science-Book-Releases\` were deliberately left unchanged. No rebuild, test rerun, commit, or push was required or performed.

## 2026-10-16 Class 8 Science notes and questions completed

The Class 8 Science book is complete for workbook-selected Chapters 3, 4, 7, 8, 9, 10, and 12. `stage2/output/Final-Science_Class8th/` contains editable TeX and LyX sources, media, a 152-page direct-TeX PDF, a 123-page themed-LyX PDF, `manifest.json`, and the final validation report. The same validated output was copied atomically to `D:\Science-Book-Releases\Science_Class8th\`; the release root report was updated, and the displaced Class 8 release remains recoverable at `D:\Science-Book-Releases\Science_Class8th.previous-20261016-142128\`. SHA-256 verification was performed for every one of the 179 staged files before the swap. The released PDF hashes are `D97BAAFD6A0D78BDAF6998F618D5FAA6556EEFF54E34AE332CC18D37700B517B` for TeX and `714000D5C858D42E5E5C42120B9E58F6A5A8A6C96D54CAD42EBF66BD4648B45E` for LyX.

The question inventory is 405 source rows and 525 rendered items. Each chapter renders 75 items after expanding only the supplied true/false and fill-in statement groups. The final report stores per-chapter source and rendered counts by type. Nine supplied question figures are preserved in source order and validated at exactly `scale / base_scale == 0.5` in both writers, while notes and infographic sizing remain unchanged. Every one of the 1,555 extracted DOCX prose fragments was found in its paired source PDF. Chapter-aware compiled-output checks found zero missing supplied question text in either final PDF. Assertion-reason choices use the required A/B first row and C/D second row grid; headings and numbering restart for each type block.

Two source observations are intentionally reported without repair. The Chapter 4 DOCX/PDF internally says Chapter 3, but the filename, authoritative workbook mapping, and electricity content identify Chapter 4; the user explicitly confirmed this is only an internal naming error and directed placement under Chapter 4. The source files remain unchanged. Chapter 3 source questions 31 and 32 share the exact generic prompt `Match the following:` but carry distinct source figures, so both were retained in order. No questions, choices, answers, explanations, or missing wording were invented or rewritten.

The ignored local adapter `tmp/rebuild_class8_science_practice.py` was generalized from Chapter 3 to all seven chapters. It uses the established workbook order and validated offline HTML cache, strictly classifies only source-supported types, expands supplied statement groups, extracts figures, records input hashes, compares DOCX prose against the paired PDFs, validates compiled prose, and fails closed on mismatches. `stage2/convert.py` gained narrow support for `pre_option_images` in MCQs and a `true_false` element that places the answer blank without the earlier long-line overflow. LyX percentage scaling now rounds the computed value. These local changes are reflected as dirty overlay state in the manifest; they have not been committed.

The final report is `passed`, errors are empty, both compilers completed, both PDFs reopen, and mandatory structure, chapter placement, source hashes, question counts/options, image references/scales, and compiled prose checks passed. Representative cover, MCQ, assertion-reason, match, figure, short/long-answer, true/false, fill-in, and final pages from both compiler paths were rasterized and inspected without clipping, overlap, broken grids, or unreadable layout. Exhaustive page-by-page review was skipped with the user's agreement. Optional independent notes/reference-PDF coverage was not run and remains `not checked`; this is separate from the completed DOCX/PDF question-pair comparison.

Actual Windows test results: `pytest -q tests -k 'not xlsx'` produced 80 passes, 5 deselections, and one unrelated failure because the retained Class 6 workbook fixture expects Chapters 7-12 while the current tracked workbook contains Chapters 3, 4, 6, 7, 11, and 12. The final real compiler integration test passed in 96.52 seconds. No Linux or configured CI result is claimed. The active export has no Git metadata. The maintained publication clone `tmp/codex-push-dev-20260924/` remains clean on `dev` at `96c07186d420839e657f19316e39bb99895e51a9`; no commit or push was authorized or performed. Future work is limited to optional author review of the two reported source observations, optional reference coverage, or promoting the local ingestion/writer changes into maintained source under separate authorization.

## 2026-10-15 Class 6 Maths question build

The Class 6 Maths complete book is published at `stage2/output/Final-Class6-Maths-Complete/`. It combines the existing validated offline notes/infographic build for workbook-selected Chapters 6-10 with the five newly supplied DOCX/PDF question pairs. Publication remained staged until both TeX and LyX compiled and all structural, source-content, rendered-content, equation, figure, ordering, numbering, option, hash, and chapter-range checks passed. Failed staging attempts never replaced prior output. The final direct TeX PDF has 80 pages; the themed LyX PDF has 72 pages. The notes-only `stage2/output/Class6-Maths/` directory is unchanged.

The final question inventory is 347 top-level questions and 73 supplied figures: Chapter 6 has 70 questions/18 figures, Chapter 7 has 70/12, Chapter 8 has 67/1, Chapter 9 has 70/33, and Chapter 10 has 70/9. Per-type counts and repeated blocks are stored in `question-source-audit.json` and `report.json`; top-level numbering restarts at 1 in each repeated type block. Both compiled PDFs passed 1,086 question-prose checks each, and all 985 substantive DOCX run-boundary checks were found in the paired source PDFs. Each question image records `scale / base_scale == 0.5`; validation rejects any other ratio. `manifest.json` now records `question_image_scale: 0.5` plus all ten input hashes, adapter and pipeline hashes, source commit `6b156ffd7c4e35ab13640a4d36283445ae5e8d3e`, and the dirty local input/overlay state.

Source discrepancies were retained rather than repaired. Chapters 6, 7, 9, and 10 have different counts of numbered Word paragraphs and visible PDF sublabels; printed labels were aligned to adjacent supplied prose, while blank or equation-only Word list items kept their source sequence. Exact duplicate prompts were reported for Chapter 6 source questions 39/48; Chapter 7 questions 5/8/10, 37/38, 44/47, and 53/54; and Chapter 9 questions 40/42/47 and 32/53. No source prose was unmatched between DOCX and PDF, and no questions, choices, equations, answers, or missing text were invented or silently corrected.

The ignored one-off adapter `tmp/build_math8_complete.py` was generalized for Class 6. Additions are conservative OMML matrix handling, text treatment for underscore-only placeholders, safe image-first LyX question layouts, literal rupee conversion to the required TeX/LyX command, local TeX paragraph flexibility without changing source wording, and explicit half-scale validation/manifest metadata. The final report is `passed` with empty compiler diagnostics and no overfull-box warning. Representative covers, MCQ and assertion-reason grids, diagram-heavy questions, case-based content, fill-in pages, and rupee rendering from both compiler paths were rasterized and visually checked. Exhaustive page-by-page review was not opted into and was skipped. The build did not rerun independent formula/infographic reference coverage; the paired question PDF comparison is separate and passed.

Windows checks after the build: offline regression suite 81 passed with 5 XLSX-dependent tests deselected; the real compiler integration test passed with 85 tests deselected. No Linux or configured CI execution is claimed. The active folder remains a legacy export without Git metadata, so no branch exists there. No commit or push was requested or performed. Future publication of the new Class 6 source inputs must use the clean publication clone and a separately authorized commit/push; generated outputs and the local adapter remain excluded.

## 2026-10-14 Class 7 and Class 8 Maths complete rebuild

The requested rebuild is complete. `stage2/output/Final-Class7-Maths-Complete/` now contains editable TeX/LyX sources plus a 94-page direct-TeX PDF and 77-page themed-LyX PDF for Chapters 9-15. It includes 477 top-level supplied questions and 33 supplied question figures. `stage2/output/Final-Class8-Maths-Complete/` contains a 110-page direct-TeX PDF and 91-page themed-LyX PDF for Chapters 8-14, with the previously audited 484 questions and 54 figures. Both outputs were staged and published atomically only after both compiler paths and all mandatory checks passed; previous successful output remained intact during failed attempts.

The documented question-diagram override is implemented by retaining each otherwise selected `base_scale` and writing `scale = base_scale * 0.5` once. An independent final-state audit found only the exact ratio `0.5` for every question figure in both books. Notes images and infographic pages retain their prior behavior. Both manifests explicitly record `question_image_scale: 0.5`; provenance records source commit `6b156ffd7c4e35ab13640a4d36283445ae5e8d3e`, the active export's dirty overlay state, the clean published source clone, and adapter/pipeline/source hashes.

Class 7 source audit results are deliberately retained in `question-source-audit.json`: Chapters 9-14 have differing DOCX numbered-paragraph and visible-PDF-label counts, so printed labels were aligned to adjacent supplied prose and blank/equation-only labels follow the same supplied list sequence. Chapter 9 has the unmatched DOCX fragment `. One is drawn with between 6 cm and`; Chapter 14 has one full DOCX angle-copy paragraph unmatched in its supplied PDF; Chapter 11 questions 21 and 22 share the exact prompt `Match the following`. These are reported conflicts, not repaired source content. Class 8 retains the already documented Chapter 10 label mismatch, Chapter 14 empty math placeholder, and incomplete Q56 clause `To make decorative pieces,`.

Windows LyX 2.4 began returning exit 11 with an empty log when forced to use a newly isolated profile, including for an older known-good Class 7 LyX source. The configured user profile exported the same document successfully. `stage0/build_support.py` now tries the isolated profile first and, on Windows only, falls back to the same batch export with the configured LyX profile; it continues to fail closed if that attempt fails. The generated PDFs have empty compiler diagnostics. `stage0/validate_against_pdf.py` also normalizes the dotless-i glyph emitted by pdfTeX extraction for macron-accented transliteration, with a regression asserting `B¯ıjagan. ita` compares to `Bījagaṇita` without weakening other symbols.

Final checks on Windows: strict build reports passed for both books; PDF files reopen successfully; TeX/LyX source structure, rendered prose, equations, question counts/options, image fingerprint/order, chapter bookmarks, source hashes, and half-scale ratios passed. Representative covers, assertion-reason grids, and question-diagram pages from both compiler paths were rendered to PNG and visually inspected without clipping, overlap, broken grids, or unreadable diagrams. Exhaustive page-by-page inspection was not opted into and was skipped as instructed. Offline regressions were 81 passed and 5 deselected with XLSX tests excluded; the real compiler integration was 1 passed and 85 deselected. An unfiltered `tests/` run produced 81 passes and four dependency-only failures because this sibling Windows `.venv` lacks `openpyxl`. A prior repository-root pytest invocation was invalid because pytest collected retained build directories with restricted permissions; it is not a product-test failure. No Linux or CI run is claimed.

The active legacy export has no Git metadata. The publication clone at `tmp/codex-push-dev-20260924/` remains clean on `dev` at `6b156ff`, matching cached `origin/dev` and `origin/main`. No commit or push was authorized or performed. The generalized local adapter remains `tmp/build_math8_complete.py`; automatic reusable question ingestion is still future work.

## 2026-10-10 Class 7 Maths source publication and saved sizing rule

The user authorized pushing all newly supplied Class 7 Maths question DOCX/PDF files and the agreed 50% question-diagram sizing rule. Chapters 9-15 supply seven pairs, 14 files total. The seven DOCX ZIP packages and document structures opened successfully; all seven PDFs opened, totaling 51 pages. Copied inputs match their originals by SHA-256. Formula PDFs and unrelated/generated files are excluded. Source chapter placement, wording conflicts, type/count audits, and complete question content comparisons remain future conversion checks; file integrity alone does not establish those results.

`AGENTS.md` and `CLAUDE.md` v4.8 now record the rule: multiply the normally selected question-diagram width by an additional `0.5` exactly once, retaining aspect ratio so height halves too, in both TeX and LyX. Preserve source image files, labels, content, and order. This override applies only to embedded question figures and takes precedence over general sizing defaults; notes and full-page infographics keep their existing sizing. It is half of the otherwise selected dimensions, not a fixed 50% text width and not cumulative resizing on each rebuild. Keep the original baseline sizing available when implementing it. Validate both compiler paths, content/image checks, and representative readability before replacing any output in a later authorized build.

This is documentation and source publication only. The user explicitly deferred implementation: no pipeline or one-off adapter changes, no conversion, and no PDF regeneration. The Class 8 completed books still have their prior diagram dimensions. The existing `dev` publication clone is `tmp/codex-push-dev-20260924/`; origin is the configured `technerrrd/combined-pdf-tex-scraping` repository. Both remote branches were fetched and confirmed at `d8ffb3d` before preparation; publish this change by fast-forward to `origin/dev` and `origin/main`, with no force push. The previously local completed Class 8 operational record below is included in this documentation publication. Windows file-integrity/hash validation and documentation/diff review are the checks for this update; no application tests, compilers, Linux execution, or CI results are claimed. Next steps require separate user authorization for sizing implementation or Class 7 book conversion, and must preserve the strict source-only rules.

## 2026-10-10 Class 8 Maths final build and publication

The authorized source publication completed before conversion. Commit `d8ffb3da9a24feb0f8e12b8b6f1ce26960d6f401` contains the question rules and seven DOCX/PDF pairs (14 files), pushed by fast-forward to both `origin/main` and `origin/dev` and verified against live remote heads. The clone at `tmp/codex-push-dev-20260924/` is clean on `dev`. Generated output and one-off scripts remain ignored. This completion record was added locally after the push.

Published `stage2/output/Final-Class8-Maths-Complete/` after staged TeX and LyX compilation and strict acceptance checks. The themed PDF has 98 pages and the direct TeX PDF has 120 pages. Editable sources, media, `manifest.json`, `report.json`, and `question-source-audit.json` accompany them. Existing `stage2/output/Class8-Maths/` remains intact. Final report status is passed, errors and compiler diagnostics are empty. Mandatory structure, editable equation, rendered prose, image fingerprint/order, chapter mapping, and question completeness checks passed. All 14 final input hashes match the pushed files. Optional independent formula-reference PDF coverage remains not checked, separately from the completed supplied question-PDF comparisons.

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
