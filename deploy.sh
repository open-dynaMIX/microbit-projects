#!/usr/bin/env bash
set -e

if ! [ -d "/media/MICROBIT" ]; then
    # mount micro:bit of not mounted already
    mounted=true
    pmount /dev/sdb MICROBIT
fi

put () {
    # instead of `ufs put`, `uflash` could also be used. But that only works for one
    # single file.
    # When using `ufs put`, the file to execute must be called `main.py`.
    echo "processing files $@"
    echo "minifying files"
    for file in "$@"
    do
        pyminify --remove-literal-statements --rename-globals --output "/tmp/$(basename $file)" "$file"
    done
    echo "Putting minified files"
    for file in "$@"
    do
        ufs put "/tmp/$(basename $file)" "$(basename $file)"
    done
    sync
    echo "removing minified file"
    rm "/tmp/$(basename $1)"
}

echo "removing all files"
for file in $(ufs ls); do
    echo "Removing remote file $file"
    ufs rm "$file"; done
put "$@"

if [ "$mounted" = true ]; then
    # unmount micro:bit, but only if we had to mount it at the beginning.
    pumount /dev/sdb
fi
