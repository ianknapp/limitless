#!/bin/bash

# CuraEngine installed van the Apt Heroku buildpack
# But we also need the printer definition configs from Cura itself
# They differ per release so fetch the right ones

echo "Fetching printer definitions from Cura"
# The version number isn't easily found, so parse it ourselves
CuraEngine help > cura_help.txt 2>&1
version_line=$(cat cura_help.txt | grep "Cura_SteamEngine version")
echo "Version string is $version_line"
# We only need the first X.XX part of the version number
version_number=${version_line#*version } | cut -d '.' -f 1-2
echo "Version number is $version_number"
# Write it to file so we can export it later
# We could set it as a Heroku env var, but it might/will change
# We can't export it from here as it won't get set on the running server
echo $version_number > cura_version.txt

echo "Downloading: https://github.com/Ultimaker/Cura/archive/refs/heads/$version_number.zip"
curl -L https://github.com/Ultimaker/Cura/archive/refs/heads/$version_number.zip > cura-code.zip
unzip -q cura-code.zip


echo "Done with Buildpack Run"

