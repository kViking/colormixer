#!/bin/bash

sed -i 's/#define MyAppVersion "0.1.3"/#define MyAppVersion "0.1.4"/' ./inno-colormixer.iss;
flet build windows .;
if [ $? -ne 0 ]; then
    echo "Build failed. Please check the output for errors."
    exit 1
fi
echo "Build completed successfully."
echo "Compiling Inno Setup installer..."
iscc="/c/Program Files (x86)/Inno Setup 6/ISCC.exe"
if [ -f "iscc" ]; then
    "iscc" ./inno-colormixer.iss
    if [ $? -ne 0 ]; then
        echo "Inno Setup compilation failed. Please check the output for errors."
        exit 1
    fi
else
    echo "Inno Setup not found at $iscc. Please install it or update the path."
    exit 1
fi
echo "Inno Setup installer compiled successfully."
