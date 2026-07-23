local wezterm = require 'wezterm'
return {
  -- front_end = "Software",
  scrollback_lines = 1000000,
  enable_scroll_bar = true,
  keys = {
    {key = 't', mods = 'CTRL', action = wezterm.action.SpawnTab 'CurrentPaneDomain'},
    {key = 'w', mods = 'CTRL', action = wezterm.action.CloseCurrentTab {confirm = true}},
  },
  font = wezterm.font('Unifont'),
  font_size = 16,
  cell_width = 0.5,
  colors = {
    foreground = '#ffffff',
    background = '#000000',
    ansi = {
      '#2E3436',
      '#a40000',
      '#4E9A06',
      '#C4A000',
      '#3465A4',
      '#75507B',
      '#ce5c00',
      '#babdb9',
    },
    brights = {
      '#555753',
      '#EF2929',
      '#8AE234',
      '#FCE94F',
      '#729FCF',
      '#AD7FA8',
      '#fcaf3e',
      '#EEEEEC',
    },
  },
}
