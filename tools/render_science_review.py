import argparse
from pathlib import Path

import pymupdf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    for pdf in sorted(args.directory.glob('*-*.pdf')):
        destination = args.output / pdf.stem
        destination.mkdir(parents=True, exist_ok=True)
        with pymupdf.open(pdf) as document:
            for index, page in enumerate(document):
                page.get_pixmap(matrix=pymupdf.Matrix(1.35, 1.35), alpha=False).save(destination / f'page-{index + 1:03}.png')
            print(pdf.name, len(document), flush=True)


if __name__ == '__main__':
    main()
