# Project instructions

- Read HANDOFF.md and docs/CODEX_HANDOFF.md before starting work.
- Check the current Git branch and working-tree status before changes.
- Maintain AGENTS.md for concise durable instructions, HANDOFF.md for the latest operational state, and docs/CODEX_HANDOFF.md for detailed context, design rationale, known problems, assumptions, and next steps.
- Read CLAUDE.md for the inherited pipeline and formatting specifications. Preserve those rules unless the user changes them; flag discrepancies between the notes and implementation.
- Use repository-relative paths in documentation.
- Preserve user changes and avoid committing inputs, generated outputs, environments, logs, or secrets.
- Publish combined Class 6-8 releases outside the checkout. The Windows default is `D:\Science-Book-Releases`; keep the destination configurable and record the source Git commit and dirty state.
- The root-level `Class 6th Science/`, `Class 7th Science/`, `Class 8th Science/`, and `Science-notes-links.xlsx` are intentional tracked Linux test references; do not treat them as generated output.
- Commit and push only when authorized by the user; standing authorization for automatic pushes has not been established.
- Before pushing, verify the remote and review the diff and relevant validation results. Never force-push without explicit authorization.
- Before token-intensive, page-by-page visual inspection of generated PDFs, ask the user whether to run it for that release and default to skipping it when declined. This opt-in does not weaken mandatory compilation, structural validation, or file-integrity checks.
- Never include credentials or secrets in project files or handoff notes. Use existing Git authentication or interactive sign-in.

## Pipeline

- Primary: stage0/scrape_chapters.py reads input/CHAPTER-LINKS and reuses stage2/html_source.py and stage2/convert.py to produce TeX and LyX.
- Use cached HTML as the source; stage0/validate_against_pdf.py is a read-only completeness check against an optional PDF.
- Keep the PDF/DOCX pipeline as a fallback.
- XLSX chapter inputs may pair formula and infographic URLs. Preserve workbook
  order and keep each chapter's formula content before its infographic pages.
- Preserve html5lib parsing, inline spacing, source image order, and the LyX template.
- Do not invent missing source content or transcribe formulas from images; see CLAUDE.md for detailed exceptions and formatting rules.
- Use only supplied questions, answers, solutions, explanations, and options. Never generate, infer, complete, or rewrite them; flag missing or unclear content rather than supply replacements.
- Format supplied assertion-reason options in the same two-column checkbox grid as MCQs: A/B on the first row, C/D on the second. Preserve source option wording and order; never insert fixed or missing options.
- If assertion-reason options are supplied once as common instructions for a section, repeat those exact options beneath each pair in that section's scope; flag unclear scope instead of assuming applicability.
- Report duplicate questions, missing options, incomplete statements, and conflicting DOCX/PDF wording; do not silently correct or delete source content or choose between conflicting sources.
- Verify each question file's chapter from source identifiers and the authoritative chapter map before insertion; flag ambiguous or mismatched placement.
- Record question counts by type for every chapter and verify every supplied question, option, answer, table, and figure appears in both compiled outputs; counts alone do not establish completeness.
- Question diagrams must render at 50% of their otherwise selected width and height in both TeX and LyX PDFs: apply an additional 0.5 sizing factor once, preserve aspect ratio and original image files, and keep source content/order intact. This overrides general image sizing only for question figures; notes and infographic sizing stay unchanged. The rule is documented but implementation/rebuilding is deferred until explicitly requested.
- In question banks, add clear question-type headings and restart top-level numbering at 1 in every question-type block. If a type reappears after another type, repeat its heading and restart that block at 1; preserve subquestion labels, source order, and wording. Use only source-defined or clearly supported types, not guessed mark categories.

## Handoff maintenance

Update HANDOFF.md after meaningful work and whenever a handoff is requested, including:

- Current objective and branch
- Completed work and key decisions
- Tests run and their results
- Known issues and next steps
- Windows/Linux setup differences

When editing CLAUDE.md, follow its version increment rule.

## Strict build maintenance

- Read README.md for the current CLI and validation contract.
- Keep all primary builds staged until TeX and LyX compile and structural/reference checks pass.
- Preserve previous output on every failure; do not introduce a partial-success mode.
- Keep URL-keyed caches validated and replace them atomically.
- Never guess reference chapter mappings or silently flatten unsupported equations.
- Run offline regressions after relevant changes and compiler integration tests after parser/writer/build changes.
- Record actual platform test results separately from configured CI jobs; do not claim unexecuted CI passed.
- Maintain backward compatibility with legacy DOCX segments and preserve the fallback scripts.
