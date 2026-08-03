set -x GOPATH $HOME/.go
set PATH $PATH $GOPATH/bin

# https://goproxy.io/
# Set the GOPROXY environment variable
set -x GOPROXY "https://goproxy.io,direct"