#!/bin/bash
set -e

PLATFORM=$1
FOLDERS=$2
TARGET=$3
LINK=$4
for f in $FOLDERS; do
	rm -rf $TARGET/$f;
	cp -r $LINK/$f $TARGET; 
done;
