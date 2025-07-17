# function fish_prompt
#   set last_status $status
#   printf '\n'
#   printf '  '
#   if test $last_status -gt 0
#     set_color $fish_color_error --bold
#     printf '%s ' $last_status
#   end
#   set_color $fish_color_normal
#   printf '%s@%s %s' (whoami) (hostname) (pwd)
#   set_color $fish_color_operator --bold
#   printf '%s' (__fish_git_prompt)
#   set_color $fish_color_normal
#   printf '\n\n'
# end
