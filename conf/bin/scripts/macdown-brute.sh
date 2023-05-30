#!/bin/bash
# Title: Macdown.sh
# Description: Bruteforce SRCFILE files downloaded from mac-torrent-download.net
# Author: Joan Bono (@joan_bono)
# Version: 1.0.0
# Last Modified: jbono @ 20200102
# Fixed version
# Modified to support both rars and dmgs
# with one script

RED='\033[0;31m'
GREEN='\033[0;32m'
NOCOLOR='\033[0m'
BOLD='\033[1m'

SRCFILE=$1

if [ "${SRCFILE}" == "" ]; then
    echo "[-] No source file provided."
    exit 0
fi

if [ ${SRCFILE##*.} == "dmg" ]; then
    for x in {{a..z},{0..9}}; do
        for y in {{a..z},{0..9}}; do
            for z in {{a..z},{0..9}}; do
                echo -n "mac-torrent-download.net_${x}${y}${z}" | hdiutil attach -stdinpass "${SRCFILE}" > /dev/null 2>&1
                if [ "$?" -eq 0 ]; then
                    echo  -ne "${GREEN}${BOLD}[+] Found password:${NOCOLOR} mac-torrent-download.net_${x}${y}${z}\n"
                    exit 0
                fi
                echo -ne "${RED}${BOLD}[-] Tested password:${NOCOLOR} mac-torrent-download.net_${x}${y}${z}\n"
            done
        done
    done
elif [ ${SRCFILE##*.} == "rar" ]; then
    for x in {{a..z},{0..9}}; do
        for y in {{a..z},{0..9}}; do
            for z in {{a..z},{0..9}}; do
                echo -n "mac-torrent-download.net_${x}${y}${z}" | unrar x "${SRCFILE}" > /dev/null 2>&1
                if [ "$?" -eq 0 ]; then
                    echo  -ne "${GREEN}${BOLD}[+] Found password:${NOCOLOR} mac-torrent-download.net_${x}${y}${z}\n"
                    exit 0
                fi
                echo -ne "${RED}${BOLD}[-] Tested password:${NOCOLOR} mac-torrent-download.net_${x}${y}${z}\n"
            done
        done
    done
else
    ext=${SRCFILE##*.}
    echo "extension $ext not valid. quitting..."
    exit 0
fi
