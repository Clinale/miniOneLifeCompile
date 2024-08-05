#!/bin/bash
set -e
if [ $# -lt 1 ] ; then
   echo "Usage: $0 release_name"
   exit 1
fi

./cleanOldBuildsAndOptionallyCaches.sh
./server.sh

cd ../output/linux
mv server OneLifeServer_v$1
echo "done building OneLifeServer_v$1"

#zip -r -q OneLife_Linux_v$1.zip OneLife_v$1
#echo "done zipping OneLife_Linux_v$1.zip"
