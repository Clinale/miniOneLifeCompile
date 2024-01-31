#!/bin/bash
set -e
if [ $# -lt 1 ] ; then
   echo "Usage: $0 release_name"
   exit 1
fi

./compile.sh 5

cp ./util/translator.py ../output/windows/client
python3 ../output/windows/client/translator.py

mv ../output/windows/client ../output/windows/OneLife_v$1
echo "done building OneLife_v$1"

zip -r -q ../output/windows/OneLife_Windows_v$1.zip ../output/windows/OneLife_v$1
echo "done zipping OneLife_Windows_v$1.zip"