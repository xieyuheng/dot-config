function fish_prompt
  set last_status $status

  printf '\n'
  printf '  '

  set_color $fish_color_normal
  printf '%s@%s %s' (whoami) (hostname) (pwd)

  set_color $fish_color_operator
  printf '%s' (fish_vcs_prompt)

  if test $last_status -ne 0
    set_color $fish_color_error --bold
    printf ' [%s]' $last_status
  end

  set_color $fish_color_normal
  printf '\n'

  if fish_is_root_user
    printf '# '
  else
    printf '$ '
  end
end
