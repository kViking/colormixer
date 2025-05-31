#!/bin/bash

# Check for --nobump flag
nobump=false
for arg in "$@"; do
    if [[ "$arg" == "--nobump" ]]; then
        nobump=true
        break
    fi
done

# Increment MyAppVersion in inno-colormixer.iss (assumes semantic versioning: vMAJOR.MINOR.PATCH)
if ! $nobump; then
    current_version=$(grep '#define MyAppVersion "' ./inno-colormixer.iss | sed -E 's/.*"([0-9]+\.[0-9]+\.[0-9]+)".*/\1/')
    if [[ $current_version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
        major="${BASH_REMATCH[1]}"
        minor="${BASH_REMATCH[2]}"
        patch="${BASH_REMATCH[3]}"
        new_version="$major.$minor.$((patch + 1))"
        sed -i "s/#define MyAppVersion \"v$major.$minor.$patch\"/#define MyAppVersion \"$new_version\"/" ./inno-colormixer.iss
        echo "Version bumped: v$major.$minor.$patch -> $new_version"
    else
        echo "Could not parse current version."
        exit 1
    fi
else
    echo "Skipping version bump due to --nobump flag."
fi

flet build windows .;
if [ $? -ne 0 ]; then
    echo "Build failed. Please check the output for errors."
    exit 1
fi
echo "Build completed successfully."
echo "Compiling Inno Setup installer..."
iscc="/c/Program Files (x86)/Inno Setup 6/ISCC.exe"
if [ -f "$iscc" ]; then
    "$iscc" ./inno-colormixer.iss
    if [ $? -ne 0 ]; then
        echo "Inno Setup compilation failed. Please check the output for errors."
        exit 1
    fi
else
    echo "Inno Setup not found at $iscc. Please install it or update the path."
    exit 1
fi
echo "Inno Setup installer compiled successfully."