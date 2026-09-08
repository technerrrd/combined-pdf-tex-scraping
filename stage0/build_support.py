"""Validated downloads, compiler execution and transactional publication."""
import email.utils
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
import requests
from PIL import Image


class BuildError(RuntimeError):
    pass


class ValidationError(BuildError):
    pass


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists(): temporary.unlink()


def cache_path(root, url, kind):
    return Path(root) / kind / (hashlib.sha256(url.encode()).hexdigest() + ('.html' if kind == 'pages' else '.bin'))


def validate_image(data):
    with Image.open(io.BytesIO(data)) as img: img.verify()
    with Image.open(io.BytesIO(data)) as img:
        img.load()
        if not img.width or not img.height: raise ValueError('Empty image')


def retry_delay(header, attempt):
    try: return max(0, float(header))
    except (ValueError, TypeError):
        try: return max(0, (email.utils.parsedate_to_datetime(header) - datetime.now(timezone.utc)).total_seconds())
        except (ValueError, TypeError, OverflowError): return 2 ** attempt


def cached_fetch(session, url, path, validate, refresh=False, offline=False):
    if refresh and offline: raise BuildError('refresh and offline cannot be combined')
    if path and path.exists() and not refresh:
        try:
            data = path.read_bytes(); validate(data); return data
        except (ValueError, OSError) as exc:
            if offline: raise BuildError(f'{url}: invalid cached content: {exc}') from exc
    if offline: raise BuildError(f'{url}: offline cache miss')
    for attempt in range(3):
        response = None
        try:
            response = session.get(url, timeout=(10, 30))
            if response.status_code == 429 or 500 <= response.status_code < 600:
                if attempt < 2:
                    time.sleep(retry_delay(response.headers.get('Retry-After'), attempt)); continue
            response.raise_for_status()
            data = response.content
            validate(data)
            if path: atomic_write(path, data)
            return data
        except (requests.Timeout, requests.ConnectionError) as exc:
            if attempt < 2: time.sleep(2 ** attempt); continue
            raise BuildError(f'{url}: network failed after 3 attempts: {exc}') from exc
        except (requests.RequestException, ValueError, OSError) as exc:
            raise BuildError(f'{url}: {exc}') from exc
        finally:
            if response is not None: response.close()
    raise BuildError(f'{url}: retry limit reached')


def executable(name):
    found = shutil.which(name)
    if not found and os.name == 'nt' and name == 'lyx':
        candidates = sorted(Path(os.environ.get('ProgramFiles', 'C:/Program Files')).glob('LyX*/bin/lyx.exe'))
        found = str(candidates[-1]) if candidates else None
    if not found: raise BuildError(f'Missing compiler: {name}. Install it and add it to PATH.')
    return found


def preflight():
    import importlib
    for dependency in ('requests', 'bs4', 'html5lib', 'PIL', 'matplotlib', 'pymupdf'):
        try: importlib.import_module(dependency)
        except ImportError as exc: raise BuildError(f'Missing Python dependency: {dependency}; install requirements.txt') from exc
    programs = {name: executable(name) for name in ('pdflatex', 'lyx', 'kpsewhich')}
    # Packages required by the existing writers and template; fail before fetching.
    missing = []
    for package in ('amsmath', 'amssymb', 'graphicx', 'float', 'enumitem', 'tfrupee', 'tikz', 'avant', 'mathptmx', 'hyperref', 'bookmark', 'titletoc', 'fancyhdr', 'mdframed', 'booktabs', 'lipsum', 'babel', 'xcolor', 'microtype', 'calc', 'makeidx'):
        check = subprocess.run([programs['kpsewhich'], package + '.sty'], capture_output=True, timeout=20)
        if check.returncode or not check.stdout.strip(): missing.append(package)
    if missing: raise BuildError('Missing LaTeX packages: ' + ', '.join(missing))
    return programs


def compiler_environment(environ=None, platform_name=None):
    """Return a compiler environment that also works on headless Linux hosts."""
    environment = dict(os.environ if environ is None else environ)
    current_platform = os.name if platform_name is None else platform_name
    if current_platform != 'nt' and not environment.get('DISPLAY') and not environment.get('WAYLAND_DISPLAY'):
        environment.setdefault('QT_QPA_PLATFORM', 'offscreen')
    environment.update(openin_any='p', openout_any='p')
    return environment


def command(args, directory, log, timeout=180):
    environment = compiler_environment()
    try:
        result = subprocess.run(args, cwd=directory, env=environment, capture_output=True, timeout=timeout)
        atomic_write(log, result.stdout + result.stderr)
    except subprocess.TimeoutExpired as exc:
        atomic_write(log, (exc.stdout or b'') + (exc.stderr or b'') + b'\nCompiler timed out')
        raise BuildError(f'Compiler timed out; see {log.name}') from exc
    if result.returncode: raise BuildError(f'Compiler failed ({result.returncode}); see {log.name}')
    return (result.stdout + result.stderr).decode('utf-8', errors='replace')


def pdf_check(path):
    import pymupdf
    if not path.exists() or not path.stat().st_size: raise BuildError(f'Missing PDF: {path.name}')
    with pymupdf.open(path) as doc:
        if not len(doc): raise BuildError(f'Empty PDF: {path.name}')


def compile_documents(directory, module, programs):
    directory = Path(directory)
    outputs = {}
    # Export LyX to its own TeX file, then compile with the same bounded pipeline.
    # This preserves both sources and gives full control over passes/log checks.
    exported = module + '-lyx.tex'
    command([programs['lyx'], '-batch', '-E', 'pdflatex', exported, module + '.lyx'], directory, directory / 'lyx-export.log')
    if not (directory / exported).exists(): raise BuildError('LyX did not export TeX')
    # LyX sometimes emits absolute PNG paths; keep only paths within this build portable.
    export_path = directory / exported
    export_text = export_path.read_text(encoding='utf-8')
    export_text = export_text.replace('{' + directory.resolve().as_posix() + '/', '{')
    export_path.write_text(export_text, encoding='utf-8')
    for source, label in ((module + '.tex', 'tex'), (exported, 'lyx')):
        job = module + '-' + label
        for iteration in range(1, 5):
            command([programs['pdflatex'], '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', '-jobname=' + job, source], directory, directory / f'{label}-pass-{iteration}.log')
            log_path = directory / (job + '.log')
            log = log_path.read_text(errors='replace') if log_path.exists() else ''
            unresolved = re.search(r'undefined references|Citation .+ undefined|Reference .+ undefined|Rerun to get|Label\(s\) may have changed|rerunfilecheck Warning', log, re.I)
            if iteration >= 2 and not unresolved: break
        else: raise BuildError(f'{label}: unresolved references after four passes')
        if re.search(r'LaTeX Error|not found|Missing character:', log, re.I):
            raise BuildError(f'{label}: missing asset, glyph or LaTeX error; see {job}.log')
        pdf = directory / (job + '.pdf'); pdf_check(pdf); outputs[label] = pdf
    return outputs


def publish(staging, destination):
    staging, destination = Path(staging).resolve(), Path(destination).resolve()
    if destination == staging or destination in staging.parents or staging in destination.parents:
        raise BuildError('Staging and destination must be separate directories')
    backup = destination.with_name(destination.name + '.previous-' + str(time.time_ns()))
    lock = destination.with_name('.' + destination.name + '.publish.lock')
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise BuildError(f'Publication lock exists: {lock}; another build may be publishing') from exc
    os.close(descriptor)
    moved = False
    try:
        if destination.exists(): destination.rename(backup); moved = True
        try:
            staging.rename(destination)
        except OSError:
            if moved: backup.rename(destination)
            raise
    finally:
        lock.unlink()
    # Keep the previous successful module as a recoverable snapshot.


def write_report(directory, report):
    atomic_write(Path(directory) / 'report.json', json.dumps(report, indent=2, ensure_ascii=False).encode('utf-8'))
    lines = [f"Status: {report['status']}", 'Reference coverage: ' + report.get('reference_status', 'not checked')]
    lines.extend(report.get('errors', []))
    for row in report.get('coverage', []):
        lines.append(f"Chapter {row['chapter']} / {row['target']}: {row['present']}/{row['total']} ({row['coverage']:.1%})")
        lines.extend('  Missing: ' + text for text in row['unmatched'])
    atomic_write(Path(directory) / 'report.txt', '\n'.join(lines).encode('utf-8'))
