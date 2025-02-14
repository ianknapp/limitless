#!/bin/bash

# Hardcode the desired Cura version
version_number="5.5.0"

echo "Downloading: https://github.com/Ultimaker/Cura/archive/refs/tags/$version_number.zip"
curl -L https://github.com/Ultimaker/Cura/archive/refs/tags/$version_number.zip > cura-code.zip
unzip -q cura-code.zip

# Add the new CuraEngine to the PATH
export PATH="/app/Cura-$version_number/build:$PATH"

echo $version_number > cura_version.txt

echo "Installing the Tweaker library to auto-orient STL files"
pip install git+https://github.com/ChristophSchranz/Tweaker-3.git

echo "Done with Buildpack Run"
