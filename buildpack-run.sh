#!/bin/bash

#conan config install https://github.com/ultimaker/conan-config.git
#conan profile new default --detect --force
#git clone https://github.com/Ultimaker/CuraEngine.git
#cd CuraEngine
#conan install . --build=missing --update
#cmake --preset release
#cmake --build --preset release
#source build/generators/Release/conanrun.sh

echo "Fetching printer definitions from Cura"
curl -L https://github.com/Ultimaker/Cura/archive/refs/heads/4.13.zip > cura-4-13.zip
unzip -q cura-4-13.zip
export CURA_ENGINE_SEARCH_PATH=/Cura-4.13/resources/definitions

echo "Done with Buildpack Run"

