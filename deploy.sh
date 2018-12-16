#!/bin/bash

DST="/Applications/Ableton Live 9 Suite.app/Contents/App-Resources/MIDI Remote Scripts/JPSX1"

cp $PWD/src/* "$DST"

for file in $(ls "$DST" | grep pyc); do echo "Deleting: "$file; rm -f "$DST/$file"; done

# for file in $(ls); do f=$(echo $file | cut -d'.' -f 1); p=".py"; uncompyle6 $file > ../_Framework/$f$p; done;
