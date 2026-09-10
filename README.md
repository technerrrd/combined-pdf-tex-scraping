# Reliable note generation

The primary pipeline turns EduRev chapter links into editable TeX and themed LyX,
then compiles both to PDF. Output is published only after downloads, structure,
compilation, and any requested reference-PDF checks pass.

## Setup

Use Python 3.12 or newer, LyX 2.4, and TeX Live with pdfLaTeX. Create a project
virtual environment and install the complete dependency list:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

On Ubuntu or Debian, the repository setup script installs the system packages and
creates `.venv-linux`:

```bash
./setup-linux.sh
```

Compilers `pdflatex`, `kpsewhich`, and `lyx` must be on PATH; standard Windows
LyX installations are also discovered. The pipeline automatically selects
LyX's offscreen Qt backend on a headless Linux host while preserving an explicit
`QT_QPA_PLATFORM`, `DISPLAY`, or `WAYLAND_DISPLAY` configuration.

The existing theme needs the LaTeX extra, science, and font packages. On Ubuntu:

```bash
sudo apt-get install lyx texlive-latex-extra texlive-fonts-extra texlive-science poppler-utils
```

Preflight reports missing dependencies before fetching. Currency uses `tfrupee`
(which provides `\rupee`) and `newunicodechar`, so literal rupee symbols remain
editable while textual `Rs.` and `INR` forms are normalized. This replaces the
unavailable `rupee.sty` dependency.

## Build a module

Put one chapter URL per line in `input/CHAPTER-LINKS`, optionally followed by
` - Chapter<N>`. Chapter titles come from the URL slug. Input order is retained.
For example:

```text
https://edurev.in/t/123/Chapter-Notes-Matter - Chapter1
https://edurev.in/t/456/Chapter-Notes-Light - Chapter2
```

```powershell
.venv/Scripts/python.exe stage0/scrape_chapters.py --links input/CHAPTER-LINKS --module ScienceNotes --title "Science Notes"
```

Linux uses the same arguments:

```bash
.venv-linux/bin/python stage0/scrape_chapters.py --links input/CHAPTER-LINKS --module ScienceNotes --title "Science Notes"
```

| Option | Behavior |
| --- | --- |
| `--links PATH` | Defaults to `input/CHAPTER-LINKS`, relative to the repository. |
| `--module NAME` | Safe output filename; defaults to the links filename stem. The old positional name remains an alias. |
| `--title TEXT` | Cover title; defaults to module name. |
| `--chapters 1,3-5` | Select chapter numbers, retaining links-file order. |
| `--output-dir PATH` | Parent directory for published modules and diagnostic staging directories; default `stage2/output`. |
| `--cache-dir PATH` | URL-keyed cache root; default `input/scraped`. |
| `--refresh` | Re-fetch selected pages and images, replacing cached data only after validation. |
| `--offline` | Require valid cached pages and images. Cannot combine with refresh. |
| `--pdf PATH` | Explicit reference PDF. No automatic PDF selection. |
| `--chapter-map PATH` | Explicit reference chapter page ranges when mapping is ambiguous; requires `--pdf`. |
| `--coverage-threshold 0.95` | Required coverage per chapter for parsed content and each compiled PDF; range `(0, 1]`. |

Relative command-line paths resolve from the current directory. Defaults resolve
from the repository. Both compilers are mandatory, including offline builds.

Published `stage2/output/ScienceNotes/` contains:

- `ScienceNotes.tex` and `ScienceNotes.lyx`, plus media and theme assets.
- `ScienceNotes-tex.pdf` and `ScienceNotes-lyx.pdf`.
- `ScienceNotes-lyx.tex`, the LyX-exported source, and compiler logs.
- `manifest.json`, `report.json`, and the readable `report.txt`.

Direct TeX retains its plain book design; LyX retains the existing Legrand theme.
Theme unification is outside this change.

## Validation, failures, and recovery

Pages must contain substantive chapter content; recognizable login/error pages
are rejected. Images must decode. Network timeouts, connection errors, HTTP 429,
and server errors get at most three attempts, honoring `Retry-After`.

Caches use SHA-256 of the full source URL. Old `Chapter<N>/page.html` caches are
not trusted as URL-identified entries: perform one online build to populate the
new cache. Legacy fallback image caches remain unchanged.

Every run builds in a unique staging directory. Publication requires both PDFs,
resolved compiler references, source-content and embedded-image checks, and unambiguous chapter
bookmarks. Failed staging directories retain reports and logs; they are never
presented as completed modules. Previous successful output is unchanged.
Successful replacements retain the old module as `<module>.previous-<timestamp>`.
Review and remove old diagnostics/snapshots manually when no longer needed.

Generated pages use natural bottom spacing. Content diagrams preserve their
aspect ratio and source order, retain smaller source-requested sizes, and are
limited to a balanced box of about 52% text width and 30% usable page height.
Current and legacy EduRev content-image suffixes (`_lg` and `_sp`, JPEG or PNG)
are accepted. Promotional course tables and calls to join EduRev are excluded;
substantive chapter tables remain content. Cover and chapter-heading artwork
remains controlled by the templates.

Chapter and section numbering follows the chapter numbers supplied in the links
file, including gaps. Chapter-banner filenames use the same source numbers.

Publication uses an exclusive lock. If interrupted during publication, inspect
`.<module>.publish.lock`, the staging directory, and the previous snapshot before
removing the stale lock or restoring the previous directory.

Reference checks compare complete normalized text lines against parsed source
and both generated PDFs, separately for each chapter. Normalization handles
ligatures, wrapping, list markers, and supported notation while distinguishing
opposite arrows/inequalities. The report lists missing lines and reference page
ranges. Coverage is a diagnostic measure, not proof of perfect fidelity.
Scanned/empty references require external OCR; this pipeline does not perform OCR.
Ambiguous mappings and low coverage block publication. Without `--pdf`, reference
coverage is explicitly **not checked**; all other checks still apply.

An explicit map is a JSON list of inclusive, one-based page ranges:

```json
[
  {"chapter": 1, "start_page": 1, "end_page": 8},
  {"chapter": 2, "start_page": 9, "end_page": 15}
]
```

Ranges must be ordered, nonoverlapping, within the PDF, and cover the selected
chapters in source order. Full-module maps may include unselected chapters.

Recheck a completed module without modifying its acceptance report:

```powershell
.venv/Scripts/python.exe stage0/validate_against_pdf.py --build-dir stage2/output/ScienceNotes --pdf input/reference.pdf
```

The standalone check prints JSON to stdout; redirect it to a separate file if
needed. Build exit codes: `0` success, `1` setup/fetch/parse/compile failure, `2`
completeness failure. No incomplete-output override is provided.

## Scientific notation

HTML sub/superscripts and Unicode notation remain typed content, including in
headings, lists, and table cells. Explicit `$...$`, `$$...$$`, `\(...\)`, `\[...\]`,
MathJax scripts, and Presentation MathML become editable math. Embedded TeX
annotations take precedence over alternate MathML/visual renderings.

Supported MathML includes identifiers, numbers, operators, rows, fractions,
roots, scripts, fences, accents, and matrices. Complex HTML table spans/nesting
are rejected for review rather than flattened. Unknown constructs/commands fail
with a review message rather than silently flattening. This is a conservative
math converter, not a general TeX interpreter. Formula images stay images;
ordinary prose and plain numbers are not guessed to be equations.

## Tests and maintenance

```powershell
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pytest -q -m integration --basetemp=tmp/integration-test
```

```bash
.venv-linux/bin/python -m pytest -q
.venv-linux/bin/python -m pytest -q -m integration --basetemp=tmp/integration-test
```

The first command runs offline unit/regression tests. The second invokes real
compilers, validates a complete fixture module, rejects a bad reference, and
checks that a missing asset cannot overwrite good output. Missing compilers fail
integration tests; they are not silently skipped. CI runs offline tests on Windows
and Linux and a compiler-equipped Linux integration job.

The root-level `Class 6th Science/`, `Class 7th Science/`, and `Class 8th Science/`
folders are intentionally tracked reference PDFs. `Science-notes-links.xlsx`
contains the corresponding source links. Generated output, caches, temporary
files, credentials, and documents placed under `input/` remain untracked.

The PDF/DOCX fallback is retained; its legacy formatting guidance remains in
`CLAUDE.md`. Use `AGENTS.md` for maintenance instructions and `HANDOFF.md` for the
current state.
