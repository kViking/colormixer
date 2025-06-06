#!/bin/bash

# wbuild.sh - Build and package ColorMixer for Windows
#
# Usage:
#   ./wbuild.sh                # Auto-bump patch version from latest ColorMixerInstaller-*.exe
#   ./wbuild.sh 1.2.3          # Use 1.2.3 as the version
#   ./wbuild.sh --version 1.2.3 # Use 1.2.3 as the version
#   ./wbuild.sh --nobuild      # Skip Flet build, only compile installer
#   ./wbuild.sh --nobuild 1.2.3 # Skip build, use 1.2.3 as the version
#   ./wbuild.sh 1.2.3 --nobuild # Use 1.2.3 as the version, skip build
#   ./wbuild.sh --nobump       # Use max version found, do not auto-bump
#   ./wbuild.sh -h | --help     # Show this help message
#   ./wbuild.sh --notify "message" [priority] # Send a notification directly
#
# This script will:
#   - Determine the version to use (from argument, --version, or by bumping the latest installer)
#   - Build the Flet Windows app (unless --nobuild is given)
#   - Compile the Inno Setup installer with the correct version
#
# Requirements:
#   - Flet CLI installed and in PATH
#   - Inno Setup 6 installed at /c/Program Files (x86)/Inno Setup 6/ISCC.exe
#   - Run from the project root directory

version=""
nobuild=0
nobump=0
pending_version=""

# Function to display colored notifications
# Usage: notify --message "text" [--priority 3] [--tags ":emoji:"]
notify() {
    local title="CMixer Compiler"
    local message=""
    local priority=3
    local tags="wbuild"
    # Parse named arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --message)
                message="$2"
                shift 2
                ;;
            --priority)
                priority="$2"
                shift 2
                ;;
            --tags)
                # Remove leading/trailing whitespace, replace spaces with commas
                tags="$2 $tags"
                tags="$(echo $tags | xargs | tr ' ' ',')"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    if [ -z "$message" ]; then
        echo -e "\033[1;31mError: notify function requires --message argument\033[0m"
        return 1
    fi
    ntfy send --title="$title" --priority="$priority" --tags "$tags" dwight-homelab-shout $message
}

# Allow direct CLI usage: ./wbuild.sh --notify "message" [priority]
if [[ "$1" == "--notify" ]]; then
    shift
    # Support both old positional and new named usage for CLI
    if [[ "$1" == --* ]]; then
        notify "$@"
    else
        notify --message "$1" --priority "${2:-3}" --tags ":bell:"
    fi
    exit 0
fi

# Parse arguments for --version, --nobuild, --nobump, or a single positional version argument
for ((i=1; i<=$#; i++)); do
    arg="${!i}"
    if [[ "$arg" == "-h" || "$arg" == "--help" ]]; then
        echo -e "\033[1;36m\nUsage:\033[0m"
        echo -e "  \033[1;32m./wbuild.sh\033[0m                # Auto-bump patch version from latest ColorMixerInstaller-*.exe"
        echo -e "  \033[1;32m./wbuild.sh 1.2.3\033[0m          # Use 1.2.3 as the version"
        echo -e "  \033[1;32m./wbuild.sh --version 1.2.3\033[0m # Use 1.2.3 as the version"
        echo -e "  \033[1;32m./wbuild.sh --nobuild\033[0m      # Skip Flet build, only compile installer"
        echo -e "  \033[1;32m./wbuild.sh --nobuild 1.2.3\033[0m # Skip build, use 1.2.3 as the version"
        echo -e "  \033[1;32m./wbuild.sh 1.2.3 --nobuild\033[0m # Use 1.2.3 as the version, skip build"
        echo -e "  \033[1;32m./wbuild.sh --nobump\033[0m       # Use max version found, do not auto-bump"
        echo -e "  \033[1;32m./wbuild.sh -h | --help\033[0m     # Show this help message"
        echo -e "  \033[1;32m./wbuild.sh --notify \"message\" [priority]\033[0m # Send a notification directly"
        echo -e "\n\033[1;36mOptions:\033[0m"
        echo -e "  \033[1;33m-h, --help\033[0m      Show this help message and exit."
        echo -e "  \033[1;33m--version VER\033[0m   Specify version to use."
        echo -e "  \033[1;33m--nobuild\033[0m       Skip Flet build, only compile installer."
        echo -e "  \033[1;33m--nobump\033[0m        Use max version found, do not auto-bump."
        echo -e "  \033[1;33m--notify \"message\" [priority]\033[0m Send a notification directly."
        echo -e "\n\033[1;36mThis script will:\033[0m"
        echo -e "  - Determine the version to use (from argument, --version, or by bumping the latest installer)"
        echo -e "  - Build the Flet Windows app (unless --nobuild is given)"
        echo -e "  - Compile the Inno Setup installer with the correct version"
        echo -e "\n\033[1;36mRequirements:\033[0m"
        echo -e "  - Flet CLI installed and in PATH"
        echo -e "  - Inno Setup 6 installed at /c/Program Files (x86)/Inno Setup 6/ISCC.exe"
        echo -e "  - Run from the project root directory\n"
        exit 0
    fi
    if [[ "$arg" == "--nobuild" ]]; then
        nobuild=1
        continue
    fi
    if [[ "$arg" == "--nobump" ]]; then
        nobump=1
        continue
    fi
    if [[ "$arg" == "--version" ]]; then
        # Get the next argument as the version string
        if [[ -n "${@:$((i+1)):1}" ]]; then
            version="${@:$((i+1)):1}"
            ((i++))
        else
            echo -e "\033[1;31mError: --version requires a version string\033[0m"
            notify --message "Error: --version requires a version string" --priority 5 --tags ":x:"
            exit 1
        fi
        continue
    fi
    # Accept a positional argument as the version string if no flag is given
    if [[ -z "$pending_version" && ! "$arg" =~ ^- ]]; then
        pending_version="$arg"
    fi
done

# If version wasn't set by --version, use the positional argument if present
if [[ -z "$version" && -n "$pending_version" ]]; then
    version="$pending_version"
fi

# Get current version from highest ColorMixerInstaller-*.exe filename
if [[ -z "$version" ]]; then
    latest_installer=$(ls ColorMixerInstaller-*.exe 2>/dev/null | sort -V | tail -n 1)
    if [[ $latest_installer =~ ColorMixerInstaller-([0-9]+\.[0-9]+\.[0-9]+)\.exe$ ]]; then
        current_version="${BASH_REMATCH[1]}"
        if [[ $current_version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
            major="${BASH_REMATCH[1]}"
            minor="${BASH_REMATCH[2]}"
            patch="${BASH_REMATCH[3]}"
            if [[ $nobump -eq 1 ]]; then
                version="$current_version"
                echo -e "\033[1;32mUsing max version found: $version (no bump)\033[0m"
            else
                new_version="$major.$minor.$((patch + 1))"
                version="$new_version"
                echo -e "\033[1;32mVersion bumped: $current_version -> $new_version\033[0m"
                echo -e "\033[1;32mUsing auto-bumped version: $version\033[0m"
            fi
        else
            echo -e "\033[1;31mCould not parse current version from installer filename.\033[0m"
            notify --message "Could not parse current version from installer filename." --priority 5 --tags ":x:"
            exit 1
        fi
    else
        version="0.1.0"
        echo -e "\033[1;33mNo existing installer found. Defaulting to 0.1.0.\033[0m"
        echo -e "\033[1;32mUsing auto-bumped version: $version\033[0m"
    fi
else
    echo -e "\033[1;32mUsing provided version: $version\033[0m"
fi

if [[ $nobuild -eq 0 ]]; then
    echo -e "\033[1;34mBuilding Flet Windows app...\033[0m"
    flet build windows .;
    if [ $? -ne 0 ]; then
        echo -e "\033[1;31mBuild failed. Please check the output for errors.\033[0m"
        notify --message "Flet build failed" --priority 5 --tags ":x:"
        exit 1
    fi
    echo -e "\033[1;32mBuild completed successfully.\033[0m"
    notify --message "Build completed successfully." --priority 3 --tags ":white_check_mark:"
else
    echo -e "\033[1;33mSkipping Flet build (--nobuild specified).\033[0m"
fi

echo -e "\033[1;34mCompiling Inno Setup installer...\033[0m"
iscc="/c/Program Files (x86)/Inno Setup 6/ISCC.exe"
if [[ -z "$version" ]]; then
    echo -e "\033[1;31mError: version is empty before calling ISCC. Aborting.\033[0m"
    notify --message "Error: version is empty before calling ISCC. Aborting." --priority 5 --tags ":x:"
    exit 1
fi
export COLORMIXER_VERSION="$version"
if [ -f "$iscc" ]; then
    "$iscc" inno-colormixer.iss
    if [ $? -ne 0 ]; then
        echo -e "\033[1;31mInno Setup compilation failed. Please check the output for errors.\033[0m"
        notify --message "Inno Setup compilation failed" --priority 5 --tags ":x:"
        exit 1
    fi
else
    echo -e "\033[1;31mInno Setup not found at $iscc. Please install it or update the path.\033[0m"
    notify --message "Inno Setup not found at $iscc. Please install it or update the path." --priority 5 --tags ":x:"
    exit 1
fi
echo -e "\033[1;32mInno Setup installer compiled successfully.\033[0m"
notify --message "Inno Setup installer compiled successfully" --priority 3 --tags ":tada:"