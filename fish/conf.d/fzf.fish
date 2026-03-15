# fzf --fish | source

function fzf-cd
  cd $(find * -type d | fzf)
end
