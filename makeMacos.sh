#!/bin/bash
set -e
if [ $# -lt 1 ] ; then
   echo "Usage: $0 release_name"
   exit 1
fi

./cleanOldBuildsAndOptionallyCaches.sh
./compile.sh 2

cp ./util/translator.py ../output/mac/client
cd ../output/mac/
python3 client/translator.py
mv client OneLife_v$1
echo "done building OneLife_v$1"

zip -r -q OneLife_Mac_v$1.zip OneLife_v$1
echo "done zipping OneLife_Windows_v$1.zip"
