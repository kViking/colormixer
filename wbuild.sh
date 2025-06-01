#!/bin/bash

version=""

# Parse arguments for --version or a single positional version argument
for ((i=1; i<=$#; i++)); do
    arg="${!i}"
    if [[ "$arg" == "--version" ]]; then
        # Get the next argument as the version string
        if [[ -n "${@:$((i+1)):1}" ]]; then
            version="${@:$((i+1)):1}"
            ((i++))
        else
            echo "Error: --version requires a version string"
            exit 1
        fi
    elif [[ -z "$version" && $i -eq 1 && "$#" -eq 1 && ! "$arg" =~ ^- ]]; then
        # Accept a single positional argument as the version string if no flag is given
        version="$arg"
    fi
done

# Get current version from highest ColorMixerInstaller-*.exe filename
if [[ -z "$version" ]]; then
    latest_installer=$(ls ColorMixerInstaller-*.exe 2>/dev/null | sort -V | tail -n 1)
    if [[ $latest_installer =~ ColorMixerInstaller-([0-9]+\.[0-9]+\.[0-9]+)\.exe$ ]]; then
        current_version="${BASH_REMATCH[1]}"
        if [[ $current_version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
            major="${BASH_REMATCH[1]}"
            minor="${BASH_REMATCH[2]}"
            patch="${BASH_REMATCH[3]}"
            new_version="$major.$minor.$((patch + 1))"
            echo "Version bumped: $current_version -> $new_version"
            version="$new_version"
        else
            echo "Could not parse current version from installer filename."
            exit 1
        fi
    else
        echo "No existing installer found. Defaulting to 0.1.0."
        version="0.1.0"
    fi
else
    echo "Using provided version: $version"
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
    "$iscc" /DMyAppVersion=$version ./inno-colormixer.iss
    if [ $? -ne 0 ]; then
        echo "Inno Setup compilation failed. Please check the output for errors."
        exit 1
    fi
else
    echo "Inno Setup not found at $iscc. Please install it or update the path."
    exit 1
fi
echo "Inno Setup installer compiled successfully."