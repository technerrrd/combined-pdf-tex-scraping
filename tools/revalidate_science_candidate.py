import argparse
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('class_number', type=int, choices=(6, 8))
    parser.add_argument('candidate', type=Path)
    parser.add_argument('--recompile-tex', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / 'stage0'))
    adapter = importlib.import_module(f'rebuild_class{args.class_number}_science_practice')
    build = adapter.build if args.class_number == 6 else adapter
    import build_support
    candidate = args.candidate.resolve()
    old_report = json.loads((candidate / 'report.json').read_text(encoding='utf-8'))

    def reuse_compiled(directory, module, programs, diagnostics=None):
        directory = Path(directory)
        for suffix in ('.tex', '.lyx'):
            filename = module + suffix
            if suffix == '.tex' and args.recompile_tex:
                continue
            if (directory / filename).read_bytes() != (candidate / filename).read_bytes():
                raise ValueError('Candidate source changed; recompilation is required: ' + filename)
        for name in ('structure.tex', 'background.pdf', 'chapterhead1.pdf', 'placeholder.jpg'):
            if (directory / name).read_bytes() != (candidate / name).read_bytes():
                raise ValueError('Candidate theme changed; recompilation is required: ' + name)
        generated_media = {path.name: path.read_bytes() for path in (directory / 'media').iterdir() if path.is_file()}
        compiled_media = {path.name: path.read_bytes() for path in (candidate / 'media').iterdir() if path.is_file()}
        if generated_media != compiled_media:
            raise ValueError('Candidate media changed; recompilation is required')
        outputs = {}
        for label in ('tex', 'lyx'):
            filename = module + '-' + label + '.pdf'
            if label == 'tex' and args.recompile_tex:
                job = module + '-tex'
                for iteration in range(1, 5):
                    build_support.command([programs['pdflatex'], '-no-shell-escape', '-interaction=nonstopmode',
                                           '-halt-on-error', '-file-line-error', '-jobname=' + job, module + '.tex'],
                                          directory, directory / f'tex-pass-{iteration}.log')
                    log = (directory / (job + '.log')).read_text(errors='replace')
                    unresolved = re.search(r'undefined references|Citation .+ undefined|Reference .+ undefined|Rerun to get|Label\(s\) may have changed|rerunfilecheck Warning', log, flags=re.I)
                    if iteration >= 2 and not unresolved:
                        break
                else:
                    raise ValueError('TeX references remain unresolved after four passes')
                found = build_support.latex_diagnostics(log, 'tex')
                if any(item['severity'] == 'error' for item in found):
                    raise ValueError('TeX compiler reported unsafe layout')
                if diagnostics is not None:
                    diagnostics.extend(found)
            else:
                shutil.copy2(candidate / filename, directory / filename)
            build_support.pdf_check(directory / filename)
            outputs[label] = directory / filename
        for path in candidate.glob('*.log'):
            if args.recompile_tex and (path.name.startswith('tex-') or path.name == module + '-tex.log'):
                continue
            shutil.copy2(path, directory / path.name)
        exported = candidate / (module + '-lyx.tex')
        if exported.exists():
            shutil.copy2(exported, directory / exported.name)
        if diagnostics is not None:
            diagnostics.extend(item for item in old_report.get('compiler_diagnostics', [])
                               if not args.recompile_tex or item['document'] != 'tex')
        return outputs

    build_support.compile_documents = reuse_compiled
    arguments = ['--links', str(adapter.WORKBOOK), '--sheet', f'Class {args.class_number}th',
                 '--module', adapter.MODULE, '--title', f'Class {args.class_number}th Science',
                 '--output-dir', os.environ['SCIENCE_OUTPUT_DIR'], '--cache-dir', os.environ['SCIENCE_CACHE_DIR'], '--offline']
    status = build.scrape_chapters.main(arguments)
    if status == 0:
        adapter.update_manifest()
    raise SystemExit(status)


if __name__ == '__main__':
    main()
