function fish_prompt
  echo ''
  set_color cyan; echo (basename $PWD) 
  set_color purple; echo '➜ '
end