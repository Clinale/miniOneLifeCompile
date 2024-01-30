#!/bin/bash
set -e
PLATFORM=$(cat PLATFORM_OVERRIDE)
if [[ $PLATFORM != 1 ]] && [[ $PLATFORM != 5 ]]; then PLATFORM=${1-1}; fi
if [[ $PLATFORM != 1 ]] && [[ $PLATFORM != 5 ]]; then
	echo "Usage: 1 for Linux (Default), 5 for XCompiling for Windows"
	exit 1
fi

pushd .
cd "$(dirname "${0}")/.."

##### Configure and Make
COMPILE_ROOT=$(pwd)
if [[ $PLATFORM == 1 ]]; then
	TARGET_PATH="${COMPILE_ROOT}/output/linux/server"
elif [[ PLATFORM == 2 ]]; then
	TARGET_PATH="${COMPILE_ROOT}/output/mac/server"
elif [[ $PLATFORM == 4 ]]; then
	TARGET_PATH="${COMPILE_ROOT}/output/raspberry/server"
elif [[ $PLATFORM == 5 ]]; then
    TARGET_PATH="${COMPILE_ROOT}/output/windows/server"
fi

cd OneLife/server
./configure $PLATFORM

make

cd ../..


##### Create Game Folder
mkdir -p ${TARGET_PATH}
cd ${TARGET_PATH}

FOLDERS="objects transitions categories tutorialMaps"
TARGET="."
LINK="${COMPILE_ROOT}/OneLifeData7"
${COMPILE_ROOT}/miniOneLifeCompile/util/createLinks.sh $PLATFORM "$FOLDERS" $TARGET $LINK


cp -rn ${COMPILE_ROOT}/OneLife/server/settings .

cp ${COMPILE_ROOT}/OneLife/server/firstNames.txt .
cp ${COMPILE_ROOT}/OneLife/server/lastNames.txt .
cp ${COMPILE_ROOT}/OneLife/server/wordList.txt .

cp ${COMPILE_ROOT}/OneLifeData7/dataVersionNumber.txt .


##### Copy to Game Folder and Run
if [[ $PLATFORM == 5 ]]; then mv ${COMPILE_ROOT}/OneLife/server/OneLifeServer.exe .; fi
if [[ $PLATFORM == 1 ]]; then mv ${COMPILE_ROOT}/OneLife/server/OneLifeServer .; fi

popd
# ./runServer.sh
echo "Compile Server Done"
