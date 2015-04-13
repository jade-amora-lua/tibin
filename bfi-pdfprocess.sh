#!/bin/bash

rarfile="$1"

passwd=$(cat ~/etc/sensible-data/bfi.pwd)

unrar e -p${passwd} "${rarfile}" /home/tiago/comuna/bfi/

#rm -rf /tmp/bfi.explode
#rm /tmp/bfi.rar

TXT=/home/tiago/comuna/bfi/043288-1.txt
PDF=/home/tiago/comuna/bfi/043288-1.pdf

pdftotext /home/tiago/comuna/bfi/043288-1.pdf /home/tiago/comuna/bfi/043288-1.txt

printf -v NUMBER '%03d' "$(grep -A1 -e '^Estado No$' /home/tiago/comuna/bfi/043288-1.txt | tail -1)"
DATE=$(grep -A1 -e '^F. EMISION$' "${TXT}" | tail -1)
printf -v DAY '%02d' "$(echo $DATE | sed -e 's/\([0-9]\{2\}\).*/\1/' -e 's/^0*//')"
printf -v MONTH '%02d' "$(echo $DATE | sed -e 's/[0-9]\{2\}[ ]\([0-9]\)\{2\}.*/\1/' -e 's/^0*//')"
printf -v YEAR '%04d' "20$(echo $DATE | sed -e 's/^.*\([0-9]\{2\}\)$/\1/' -e 's/^0*//')"

newname="ec-${NUMBER}-${YEAR}-${MONTH}-${DAY}"

mv "${PDF}" "/home/tiago/comuna/bfi/${newname}.pdf"
mv "${TXT}" "/home/tiago/comuna/bfi/${newname}.txt"
