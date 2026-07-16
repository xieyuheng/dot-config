alias l "ls -hCF"
alias ll "ls -hlF"
alias lll "ls -halF"
alias mv " mv -vi"
# alias rm " timeout 3 rm -Iv --one-file-system "
alias rm " rm -v "
alias df " df -h "
alias du " du -h "

function cd
    builtin cd $argv
    builtin cd (pwd -P)
end

set -gx MANPAGER "less --quit-if-one-screen --mouse --raw-control-chars"
