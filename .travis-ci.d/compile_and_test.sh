#!/bin/bash

source /LCIO/.travis-ci.d/init_x86_64.sh

cd /LCIO
mkdir build
cd build
cmake -GNinja -C $ILCSOFT/ILCSoft.cmake ..
ninja
ctest --output-on-failure

