#!/bin/bash
# Build StudentAI for macOS
# Run from the project root in your virtual environment:
#   source .venv/bin/activate
#   bash build_mac.sh

set -e
echo "=== Student AI Support — macOS Build ==="

# Download llamafile binary if needed (macOS version, no .exe)
if [ ! -f "bin/llamafile" ]; then
    echo "Downloading llamafile binary..."
    VERSION="0.10.1"
    curl -L -o bin/llamafile \
        "https://github.com/mozilla-ai/llamafile/releases/download/${VERSION}/llamafile-${VERSION}-thin"
    chmod +x bin/llamafile
fi

# Clean previous build
rm -rf dist build

# Run PyInstaller
echo "Running PyInstaller..."
pyinstaller student_ai.spec

# Create models folder (students download model on first run)
mkdir -p "dist/StudentAI.app/Contents/MacOS/models"

# NOTE: macOS Gatekeeper will block unsigned apps.
# Students will need to: right-click the app > Open > Open anyway (first time only).
# To avoid this, sign with an Apple Developer certificate:
#   codesign --deep --force --sign "Developer ID Application: YOUR NAME" dist/StudentAI.app

VERSION=$(date +%Y-%m-%d)
echo "Creating zip archive..."
cd dist && zip -r "../StudentAI-macOS-${VERSION}.zip" StudentAI.app && cd ..

echo ""
echo "Done! Distribute: StudentAI-macOS-${VERSION}.zip"
echo "Students unzip and double-click StudentAI.app"
echo ""
echo "IMPORTANT: First launch requires right-click > Open due to Gatekeeper."
