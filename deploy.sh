#!/usr/bin/env bash
set -e

if ! [ -d "/media/MICROBIT" ]; then
  mounted=true
  pmount /dev/sdb MICROBIT
fi

uflash
sync
echo "Putting common.py"
ufs put ./games/common.py
sync
echo "Putting $1"
ufs put "$1"

sync
if [ "$mounted" = true ]; then
  pumount /dev/sdb
fi
