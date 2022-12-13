if status is-interactive
    # Commands to run in interactive sessions can go here
end

# PATH variables

fish_add_path /opt/homebrew/bin
fish_add_path $HOME/bin
fish_add_path $HOME/bin/scripts
fish_add_path $HOME/.cargo/bin

# other path variables

set HOMEBREW_NO_ENV_HINTS
export CPATH=/opt/homebrew/include
export LIBRARY_PATH=/opt/homebrew/lib
export PMIP_CBC_LIBRARY=/Users/francesco/workspace/for-lab/cbclib/libCbc.dylib
# set -a LD_LIBRARY_PATH $HOME/francesco/workspace/for-lab/cbclib

# functions

function where
    command type -a $argv[1]
end

function stream
    command webtorrent $argv[1] --iina
end

function latest
    history --reverse | tail -n 20
end

function create_link
    set url $argv[1]
	set fname $argv[2]
	set fcontent "[InternetShortcut]"\n"URL="$url
    command echo $fname
    command echo $fcontent > $fname
end

# aliases

alias pivpn="sudo /opt/homebrew/opt/openvpn/sbin/openvpn --config /Users/francesco/mbp.ovpn"
alias l="exa"
alias ll="exa -l"
alias la="exa -la"
alias gc="git clone"
alias p="python3"
alias pp="python3 -m pip"
alias py="ipython"
alias m="micro"
alias c="code -n"
alias src="source $HOME/.config/fish/config.fish"
alias cfg="micro $HOME/.config/fish/config.fish"
alias newenv="python3 -m venv venv"
alias makee="make -j$(nproc)"

# bootstrapping thefuck
thefuck --alias | source
