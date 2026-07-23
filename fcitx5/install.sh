#!/usr/bin/env bash

cp profile ~/.config/fcitx5/profile

if [ ! -d ~/.local/share/fcitx5/themes/fcitx5-dark ]; then
  git clone https://github.com/evansan/fcitx5-dark ~/.local/share/fcitx5/themes/fcitx5-dark
fi
