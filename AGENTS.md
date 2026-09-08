# Project instructions

- Read HANDOFF.md before starting work.
- Check the current Git branch and working-tree status before changes.
- Maintain AGENTS.md for durable project instructions and HANDOFF.md for current progress, decisions, validation, and next steps.
- Read CLAUDE.md for the inherited pipeline and formatting specifications. Preserve those rules unless the user changes them; flag discrepancies between the notes and implementation.
- Use repository-relative paths in documentation.
- Preserve user changes and avoid committing inputs, generated outputs, environments, logs, or secrets.
- Commit and push only when authorized by the user; standing authorization for automatic pushes has not been established.
- Before pushing, verify the remote and review the diff and relevant validation results. Never force-push without explicit authorization.
- Never include credentials or secrets in project files or handoff notes. Use existing Git authentication or interactive sign-in.

## Pipeline

- Primary: stage0/scrape_chapters.py reads input/CHAPTER-LINKS and reuses stage2/html_source.py and stage2/convert.py to produce TeX and LyX.
- Use cached HTML as the source; stage0/validate_against_pdf.py is a read-only completeness check against an optional PDF.
- Keep the PDF/DOCX pipeline as a fallback.
- Preserve html5lib parsing, inline spacing, source image order, and the LyX template.
- Do not invent missing source content or transcribe formulas from images; see CLAUDE.md for detailed exceptions and formatting rules.

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
