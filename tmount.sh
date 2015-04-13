#!/bin/bash
# set -x

if [ x"$1" = x ] ; then
    cd /dev/disk/by-label
    ls
    exit
fi

command="${0##*/}"

case $command in
    "tmount" )
        echo "Mounting"
        udisksctl mount --block-device /dev/disk/by-label/"$1"
        ;;
    "tumount" )
        echo "Unmounting"
        udisksctl unmount --block-device /dev/disk/by-label/"$1"
        ;;
esac

echo "$0"
echo $command
