#!/bin/bash
set -e
if [ $# -lt 1 ] ; then
   echo "Usage: $0 release_name"
   exit 1
fi
./applyFixesAndOverride.sh
./cleanOldBuildsAndOptionallyCaches.sh
./compile.sh 1

cp ./util/translator.py ../output/linux/client
cd ../output/linux
# python3 client/translator.py
mv client OneLife_v$1
echo "done building OneLife_v$1"

zip -r -q OneLife_Linux_v$1.zip OneLife_v$1
echo "done zipping OneLife_Linux_v$1.zip"
