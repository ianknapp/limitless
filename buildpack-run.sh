#!/bin/bash

# Specify the desired version
desired_version="5.5.0"

echo "Fetching printer definitions from Cura"
# The version number isn't easily found, so parse it ourselves
echo $desired_version > cura_version.txt

echo "Downloading: https://github.com/Ultimaker/Cura/archive/refs/heads/$desired_version.zip"
curl -L https://github.com/Ultimaker/Cura/archive/refs/heads/$desired_version.zip > cura-code.zip
unzip -q cura-code.zip

echo "Installing the Tweaker library to auto-orient STL files"
pip install git+https://github.com/ChristophSchranz/Tweaker-3.git

echo "Done with Buildpack Run"
