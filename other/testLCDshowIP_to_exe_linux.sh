#!/bin/bash
# Linux build script for testLCDshowIP.py using Nuitka

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

mainfilename="testLCDshowIP"

# Set output filename with date
datenow=$(date +%m%d)
outfilename="testLCDshowIP_linux-${datenow}"

# Backup existing build if it exists
if [ -d "${outfilename}" ]; then
    mv -f "${outfilename}" "${outfilename}.bak"
fi

# Build with Nuitka
python3 -m nuitka --standalone --clean-cache=all \
	--remove-output \
	--include-data-files="../resource/*=resource/" \
	--output-filename="${outfilename}" \
	${mainfilename}.py

echo "Build complete! Executable created in ${outfilename}/"