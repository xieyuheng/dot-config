#!/bin/bash

shopt -s nullglob

# feh --bg-fill ~/.wallpapers/arch/istheorederarch.png

cd ~/.wallpapers/ji
# cd ~/.wallpapers/kushufu-chusuiliang

while true; do
        files=()
        for i in *.jpg *.png; do
                [[ -f $i ]] && files+=("$i")
        done
        range=${#files[@]}
        ((range)) && feh --bg-fill "${files[RANDOM % range]}"
        sleep 256s
done
