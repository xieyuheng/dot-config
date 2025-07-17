function fish_prompt
  set last_status $status

  printf '\n'
  printf '  '

  printf '%s %s' (prompt_login) (pwd)

  set_color $fish_color_operator
  printf '%s' (fish_vcs_prompt)

  if test $last_status -ne 0
    set_color $fish_color_error
    printf ' [%s]' $last_status
  end

  printf '\n'

  set_color $fish_color_operator
  if fish_is_root_user
    printf '# '
  else
    printf '$ '
  end

  set_color $fish_color_normal
end
