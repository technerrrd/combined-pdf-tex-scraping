#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This installer supports Ubuntu and Debian systems with apt-get." >&2
  exit 1
fi

sudo apt-get update
sudo apt-get install -y \
  python3 python3-venv lyx poppler-utils \
  texlive-latex-extra texlive-fonts-extra texlive-science

python3 -m venv .venv-linux
.venv-linux/bin/python -m pip install --upgrade pip
.venv-linux/bin/python -m pip install -r requirements.txt

echo "Linux setup complete. Run: .venv-linux/bin/python -m pytest -q"
