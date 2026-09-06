#!/bin/sh
# Rebuild the adaway.py zipapp. Run it after every change under lib/.
set -e

PYTHON="${PYTHON:-python3}"
BUILD_DIR=build

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

cp __main__.py "$BUILD_DIR"/
cp -r lib "$BUILD_DIR"/

"$PYTHON" -m pip install --quiet --target "$BUILD_DIR" -r requirements.txt

# Bytecode is interpreter specific and only bloats the archive
find "$BUILD_DIR" -name '__pycache__' -type d -exec rm -rf {} +

"$PYTHON" -m zipapp "$BUILD_DIR" -o adaway.py -p '/usr/bin/env python' --compress
chmod +x adaway.py

rm -rf "$BUILD_DIR"

echo "Built adaway.py"
