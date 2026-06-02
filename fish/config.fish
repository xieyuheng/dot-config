
# pnpm
set -gx PNPM_HOME "/home/xyh/.local/share/pnpm"
if not string match -q -- "$PNPM_HOME/bin" $PATH
  set -gx PATH "$PNPM_HOME/bin" $PATH
end
# pnpm end

# opencode
fish_add_path /home/xyh/.opencode/bin

# emacs
set -x EMACS_NATIVE_COMPILATION_CACHE_DIR "$HOME/.cache/emacs/eln-cache/"
