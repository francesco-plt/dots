function fish_prompt
  echo ''
  
  set curdir (basename $PWD)
  set dircolor brpurple

  set homedir (basename $HOME)
  # shortening user home directory
  # for brevity
  if test "$curdir" = "$homedir"
    set curdir '~'
  end

  # and shortening any other directory
  # to char1char2char3char4...charN if
  # the directory name is longer than
  # 6 chars
  if test (string length $curdir) -gt 6
    set curdir (string sub -s 1 -l 4 $curdir)'..'(string sub -s -1 $curdir)
  end

  # if the directory we're in is called docs
  # and the parent is a repo (it has a .git folder)
  # we'll just show the repo name + docs emoji
  if test "$curdir" = "docs"
    set parentdir (basename (dirname $PWD))
    if test -d ../.git
      set curdir "📚 $curdir/d"
    end
  end

  # if the directory we're in is a .git repository
  # we'll show the repo name + git emoji
  if test -d .git
    set curdir "🐙 $curdir"
  end

  # if there is a python virtual environment
  # active we'll show the python emoji
  if test -n "$VIRTUAL_ENV"
    set curdir "🐍 $curdir"
  end

  # shortening hostname
  # if it ends with .local
  # ..macOS ಠ_ಠ
  set hname (hostname)
  if test (string sub --start=-6 $hname) = ".local"
    set hname (string sub -e -6 $hname)
  end

  # and now let's customize the prompt:
  set pmptchar '➜'
  if test $status -ne 0
    set pmptchar 'x'
  end
  
  echo (set_color brblack)'{'(set_color brcyan)(whoami)(set_color brblack)'|'(set_color brgreen)$hname(set_color brblack)'}'
  echo (set_color $dircolor)'['$curdir']' (set_color purple)$pmptchar' '
end

# good old minimal prompt in case we get tired of the above verobosity
# function fish_prompt
#   echo ''
#   set_color cyan; echo (basename $PWD)
#   set_color purple; echo '➜ '
# end