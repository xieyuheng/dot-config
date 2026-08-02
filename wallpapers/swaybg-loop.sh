#!/bin/bash

lockfile=/tmp/swaybg-loop.lock
exec 9>"$lockfile"
flock -n 9 || exit 0

while true; do
        img=$(find ~/.wallpapers -maxdepth 2 -type f -name '*.png' ! -path '*/.git*' 2>/dev/null | shuf -n 1)
        if [[ -n $img ]]; then
                killall swaybg 2>/dev/null
                swaybg -i "$img" -m fill &
        fi
        sleep 256s
done
