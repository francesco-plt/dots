function fish_prompt
  
  # prompt character depends on
  # return value of last command

  set -l last_status $status

  if test $last_status -eq 0
    set pmptcolor brcyan
    set pmptchar '>'
  else
    set pmptcolor red
    set pmptchar '✗'
  end

  # [hostname@user]

  set hname (hostname)
  if test (string sub --start=-6 $hname) = ".local"
    set hname (string sub -e -6 $hname)
  end
  if test (string length $hname) -gt 3
    set hname (string sub -l 3 $hname)
  end

  set user (whoami)
  if test (string length $user) -gt 3
    set user (string sub -l 3 $user)
  end

  # curdir prompt

  set curdir (basename $PWD)
  if test "$curdir" = (basename $HOME)
    set curdir '~'
  end
  if test (string length $curdir) -gt 6
    set curdir (string sub -s 1 -l 6 $curdir)'..'
  end

  set_color brblack; echo '['$hname'@'$user']'
  set_color $pmptcolor; echo $curdir' '$pmptchar' '
end

# printing return value of last
# command in case of error
function fish_right_prompt
  if test $status -ne 0
    echo (set_color red)'('$status')'
  end
end