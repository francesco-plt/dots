: '
Fish shell configuration file
Author: francesco-plt (https://github.com/francesco-plt/dots)
'

### login greeting :)
function fish_greeting
    printf "%s%s\n%s\n%s\n%s\n%s\n" \
        (set_color brcyan)(whoami)": " (set_color brblack)"Hey ChatGPT, write an haiku on fish shell" \
        (set_color brcyan)"ChatGPT: "(set_color normal)"Welcome to "(set_color brgreen)"fish"(set_color normal)", the friendly interactive shell" \
        "Elegant prompts, autosuggestions as well" \
        "A joy to use, it's heaven sent" \
        "An improved experience, time well spent"
end

### variables

# PATH variables
fish_add_path /opt/homebrew/bin
fish_add_path $HOME/bin
fish_add_path $HOME/bin/scripts
fish_add_path $HOME/.cargo/bin
fish_add_path $HOME/go/bin
fish_add_path $HOME/.aido
fish_add_path $HOME/.zokrates/bin

# ENV variables
export HOMEBREW_NO_ENV_HINTS=true
export CPATH=/opt/homebrew/include
export LIBRARY_PATH=/opt/homebrew/lib
export MICRO_TRUECOLOR=1

### functions
function where
    command type -a $argv[1]
end

function latest
    history --reverse | tail -n 20
end

function resolve_did
    set base_url "https://dev.uniresolver.io/1.0/identifiers/"
    set did $argv[1]
    command curl "$base_url$did"
end

function get_container_ip
    command docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $argv[1]
end

function git_push
    command git add . && git commit -m $argv[1] && git push
end

function stream_btvideo
    command webtorrent $argv[1] --iina
end

function create_shortcut
    set url $argv[1]
	set fname $argv[2]
	set fcontent "[InternetShortcut]"\n"URL="$url
    command echo $fname
    command echo $fcontent > $fname
end

function setvenv
    mkdir venv
    python3 -m venv ./venv
    source venv/bin/activate
    which python
end

### aliases

# general purpose
alias l="exa"
alias ll="exa -l"
alias la="exa -la"
alias gc="git clone"
alias temp="cd /tmp"
alias b="bat --theme='Monokai Extended Origin'"
alias src="source $HOME/.config/fish/config.fish"
alias cfg="micro $HOME/.config/fish/config.fish"
alias makee="make -j$(nproc)"
alias get_ip="curl icanhazip.com"

# editor
alias m="micro"
alias c="code"
alias cn="code -n"
alias ci="code-insiders"
alias cii="code-insiders -n"

# package managers, python
alias p="python3"
alias pp="python3 -m pip"
alias py="python3 -m IPython"
alias pv="python3 --version"
alias ppf="python3 -m pip freeze > requirements.txt"
alias newenv="python3 -m venv venv"
alias pip-upgrade-all='pip list --outdated --format=json | jq ".[] | [.name] | @tsv" | sed "s/\"//g" | xargs -n1 pip3 install --upgrade'

# package managers, nodejs
alias npm="npm --no-audit"
alias npmrun="npm run build && npm run start"


### external configuration

# pnpm
set -gx PNPM_HOME "/Users/francesco/Library/pnpm"
if not string match -q -- $PNPM_HOME $PATH
  set -gx PATH "$PNPM_HOME" $PATH
end

# source iterm2 integration
# test -e {$HOME}/.iterm2_shell_integration.fish ; and source {$HOME}/.iterm2_shell_integration.fish ; or true
source ~/.iterm2_shell_integration.fish

# pyenv
pyenv init - | source

# Secretive.app# pnpm
set -gx PNPM_HOME "/Users/francesco/Library/pnpm"
if not string match -q -- $PNPM_HOME $PATH
  set -gx PATH "$PNPM_HOME" $PATH
end
set -x SSH_AUTH_SOCK /Users/francesco/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh

# source other custom configurations
source $HOME/.config/fish/misc.fish