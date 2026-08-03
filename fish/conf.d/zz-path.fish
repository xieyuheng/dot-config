# Single source of truth for PATH: ~/.config/path.list.
# Order in the file = priority order (earlier lines come first).

if test -f "$HOME/.config/path.list"
    set -gx PATH
    while read -l line
        set line (string trim "$line")
        if test -z "$line"
            continue
        end
        if string match -q '#*' "$line"
            continue
        end
        set -a PATH (string replace '~' "$HOME" "$line")
    end < "$HOME/.config/path.list"
end
