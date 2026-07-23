-- ~/.config/wezterm/wezterm.lua

local wezterm = require 'wezterm'
local theme = require 'theme'
return {
  -- front_end = "Software",
  scrollback_lines = 1000000,
  enable_scroll_bar = true,
  keys = {
    {key = 't', mods = 'CTRL', action = wezterm.action.SpawnTab 'CurrentPaneDomain'},
    {key = 'w', mods = 'CTRL', action = wezterm.action.CloseCurrentTab {confirm = true}},
  },
  font = wezterm.font_with_fallback({
    'Unifont',
    'Noto Sans Mono',
    'Noto Sans CJK SC',
  }),
  font_size = 16,
  cell_width = 0.5,
  colors = theme.colors,
}
