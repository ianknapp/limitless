#!/bin/bash

conan config install https://github.com/ultimaker/conan-config.git
conan profile new default --detect --force
git clone https://github.com/Ultimaker/CuraEngine.git
cd CuraEngine
conan install . --build=missing --update
cmake --preset release
cmake --build --preset release
source build/generators/Release/conanrun.sh

