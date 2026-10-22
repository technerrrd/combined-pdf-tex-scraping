import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


def package(directory, destination):
    report = json.loads((directory / 'report.json').read_text(encoding='utf-8'))
    if report.get('status') != 'passed':
        raise ValueError('Only validated books can be packaged')
    if not (directory / 'DELIVERY-STATUS.txt').exists() and report.get('visual_review', {}).get('status') != 'passed':
        raise ValueError('Final packages require completed visual acceptance')
    lyx_files = list(directory.glob('*.lyx'))
    if len(lyx_files) != 1:
        raise ValueError('Expected exactly one main LyX file')
    source = lyx_files[0].read_text(encoding='utf-8')
    for reference in re.findall(r'^\s*filename\s+(.+)$', source, flags=re.M):
        reference = reference.strip().strip('"')
        resolved = (directory / reference).resolve()
        if not resolved.is_relative_to(directory.resolve()) or not resolved.is_file():
            raise ValueError('Nonportable or missing LyX dependency: ' + reference)
    files = [path for path in directory.rglob('*') if path.is_file() and (
        path.relative_to(directory).parts[0] == 'media' or
        path.suffix.lower() in {'.lyx', '.png', '.jpg', '.jpeg', '.bib', '.ist'} or
        path.name in {'structure.tex', 'background.pdf', 'chapterhead1.pdf', 'manifest.json', 'report.json', 'report.txt', 'visual-review.json', 'DELIVERY-STATUS.txt'}
    )]
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.pending.zip')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, directory.name + '/' + path.relative_to(directory).as_posix())
        archive.writestr('OPEN-ME.txt',
                         'Extract this entire ZIP first. Open ' + directory.name + '/' + lyx_files[0].name +
                         ' in LyX 2.4 or newer. Keep its media folder and theme files alongside it.\n' +
                         ('IMPORTANT: Read DELIVERY-STATUS.txt inside the book folder. This is a review-pending candidate, not an approved final release.\n'
                          if (directory / 'DELIVERY-STATUS.txt').exists() else ''))
    with zipfile.ZipFile(temporary) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP integrity check failed')
        for path in files:
            name = directory.name + '/' + path.relative_to(directory).as_posix()
            if hashlib.sha256(archive.read(name)).digest() != hashlib.sha256(path.read_bytes()).digest():
                raise ValueError('ZIP member mismatch: ' + name)
    temporary.replace(destination)
    return {'path': str(destination), 'files': len(files),
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(json.dumps(package(args.directory, args.destination), indent=2))


if __name__ == '__main__':
    main()
