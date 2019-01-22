#!/usr/bin/env bash

# Script to count number of files in a folder that is receiving files via wget
# and if the number has not changed in a minute, stop and issue a message via
# Telegram bot.

token=$2
chatid=$3

shopt -s nullglob  # don't count empty dir as file

register=()

i=0
while sleep 60
do
    downloaded=($1/*)
    downloaded=${#downloaded[@]}
    register[$i]=$downloaded
    index=$((i - 1))
    if [[ $i -gt 0 && $downloaded -eq register[$index] ]]; then
        echo $downloaded
        echo "Stopped"
        curl -s -X POST https://api.telegram.org/bot$token/sendMessage -d chat_id=$chatid -d text="Wget reached timeout of 60 seconds. Number of files in $1: $downloaded" > /dev/null
        break
    fi
    let i+=1
done