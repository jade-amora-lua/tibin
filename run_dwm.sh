#!/bin/bash
while true
do
    while true
    do
        text=$(date +'%F %R')
        # text+=" - $(sensors it8718-isa-0a10 | grep temp1 | awk '{print $2}')"
        echo $text
        xsetroot -name "$text"
        sleep 1m
    done &
    /home/tiago/src/dwm/dwm
done

