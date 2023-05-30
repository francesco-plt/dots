#!/bin/env sh
# bash script to count all pages
# of all pdfs in a specific folder

exec 2>/dev/null
curfolder=$(pwd)
echo -n 'total number of pages in ('$curfolder'): '
for i in *.pdf; do pdfinfo "$i" | grep "^Pages:"; done | awk '{s+=$2} END {print s}'
