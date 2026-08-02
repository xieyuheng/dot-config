#!/usr/bin/env bash
# Copy user.js into the current Firefox profile so that browser.startup.page=3 ("Open previous windows and tabs") applies on every startup without GUI.
# Requires Firefox to have been run at least once to create the profile dir.

set -euo pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

profile=$(find "$HOME/.mozilla/firefox" -maxdepth 1 -type d -name '*.default*' 2>/dev/null | head -1)

if [ -z "$profile" ]; then
    echo "No Firefox profile found in ~/.mozilla/firefox. Run Firefox once and retry." >&2
    exit 1
fi

cp "$dir/user.js" "$profile/user.js"
echo "Installed user.js into $profile"