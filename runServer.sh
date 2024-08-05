#!/bin/bash
set -e

serverShutdown() {
    server_path=$1
    echo "" 
    echo "Shutting down server"
    echo ""

    serverPID=`pgrep OneLifeServer`
    if [ -z $serverPID ]
    then
        echo "Server not running!"
    else    
        echo -n "1" > $server_path/settings/shutdownMode.ini

        echo "" 
        echo "Set server shutdownMode, waiting for server to exit"
        echo ""

        while kill -CONT $serverPID 1>/dev/null 2>&1; do sleep 1; done

        echo "" 
        echo "Server has shutdown"
        echo ""
    fi
}

serverStartUp() {
    server_path=$1
    echo "" 
    echo "Re-launching server"
    echo ""

    echo "    Setting shutdownMode to 0"
    echo -n "0" > $server_path/settings/shutdownMode.ini


    cd $server_path

    echo "    Running ServerLinux"
    nohup ./OneLifeServer &
    echo "    Done re-launching server"

}


PLATFORM=$(cat PLATFORM_OVERRIDE)
if [[ $PLATFORM != 1 ]] && [[ $PLATFORM != 5 ]]; then PLATFORM=${1-1}; fi
if [[ $PLATFORM != 1 ]] && [[ $PLATFORM != 5 ]]; then
	echo "Usage: 1 for Linux (Default), 5 for XCompiling for Windows"
	exit 1
fi
cd "$(dirname "${0}")/.."
COMPILE_ROOT=$(pwd)
if [[ $PLATFORM == 1 ]]; then
        TARGET_PATH="${COMPILE_ROOT}/output/linux/server"
else
        TARGET_PATH="${COMPILE_ROOT}/output/windows/server"
fi

serverShutdown ${TARGET_PATH}
#serverStartUp ${TARGET_PATH}
