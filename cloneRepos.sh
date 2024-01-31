#!/bin/bash
set -e
cd "$(dirname "${0}")/.."

CODE_REPO="https://github.com/Clinale/OneLife.git"
DATA_REPO="https://github.com/Clinale/OneLifeData7.git"
GEMS_REPO="https://github.com/Clinale/minorGems.git"

if [[ ! -d OneLife ]]; then git clone $CODE_REPO OneLife; fi
if [[ ! -d OneLifeData7 ]]; then git clone $DATA_REPO OneLifeData7; fi
if [[ ! -d minorGems ]]; then git clone $GEMS_REPO minorGems; fi