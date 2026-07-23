#!/usr/bin/env bash
set -euo pipefail

dir="$HOME/.local/share/fcitx5/themes/fcitx5-dark"

if [ -d "$dir/.git" ]; then
  git -C "$dir" pull
else
  git clone https://github.com/evansan/fcitx5-dark "$dir"
fi

echo "ok"
