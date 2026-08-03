#!/usr/bin/env bash

copy * ~/.config/fish
cp "$(dirname "$0")/../path.list" ~/.config/path.list
