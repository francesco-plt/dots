if status is-interactive
    # Commands to run in interactive sessions can go here
end

# PATH variables

fish_add_path /opt/homebrew/bin
fish_add_path $HOME/bin
fish_add_path $HOME/bin/scripts
fish_add_path $HOME/.cargo/bin
fish_add_path $HOME/go/bin
fish_add_path $HOME/.aido

# other path variables

set HOMEBREW_NO_ENV_HINTS
export CPATH=/opt/homebrew/include
export LIBRARY_PATH=/opt/homebrew/lib

# login greeting

function fish_greeting
    printf "%s%s\n%s\n%s\n%s\n%s\n" \
        (set_color brcyan)(whoami)": " (set_color brblack)"Hey ChatGPT, write an haiku on fish shell" \
        (set_color brcyan)"ChatGPT: "(set_color normal)"Welcome to "(set_color brgreen)"fish"(set_color normal)", the friendly interactive shell" \
        "Elegant prompts, autosuggestions as well" \
        "A joy to use, it's heaven sent" \
        "An improved experience, time well spent"
end

# functions

function gcm
    command git add . && git commit -m $argv[1] && git push
end

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

function logg
     command cat $argv[1] | less
 end

# aliases

alias l="exa"
alias ll="exa -l"
alias la="exa -la"
alias gc="git clone"
alias p="python3"
alias pp="python3 -m pip"
alias py="python3 -m IPython"
alias pv="python3 --version"
alias ppf="python3 -m pip freeze > requirements.txt"
alias m="micro"
alias c="code"
alias cn="code -n"
alias ci="code-insiders"
alias cii="code-insiders -n"
alias src="source $HOME/.config/fish/config.fish"
alias cfg="micro $HOME/.config/fish/config.fish"
alias newenv="python3 -m venv venv"
alias makee="make -j$(nproc)"
alias h="aido"

# bootstrapping thefuck
thefuck --alias | source

# tabtab source for electron-forge package
# uninstall by removing these lines or running `tabtab uninstall electron-forge`
[ -f /opt/homebrew/lib/node_modules/electron-forge/node_modules/tabtab/.completions/electron-forge.fish ]; and . /opt/homebrew/lib/node_modules/electron-forge/node_modules/tabtab/.completions/electron-forge.fish
