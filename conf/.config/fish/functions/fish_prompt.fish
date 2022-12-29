function fish_prompt
  echo ''
  set curdir (basename $PWD)
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

  # shortening hostname
  # if it ends with .local
  # ..macOS ಠ_ಠ
  set hname (hostname)
  if test (string sub --start=-6 $hname) = ".local"
    set hname (string sub -e -6 $hname)
  end

  echo (set_color brcyan)(whoami)' '(set_color brblack)$hname
  echo (set_color brpurple)'['$curdir']' (set_color purple)'➜ '
end

# good old minimal prompt in case we get tired of the above verobosity
# function fish_prompt
#   echo ''
#   set_color cyan; echo (basename $PWD)
#   set_color purple; echo '➜ '
# end