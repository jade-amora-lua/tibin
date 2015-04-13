#!/bin/sh

SPACE_LEFT=$(df --output=avail /home | tail -1 )

if [ $SPACE_LEFT -lt 500000 ]
then
    echo "You have only $SPACE_LEFT bytes available on home."
fi
