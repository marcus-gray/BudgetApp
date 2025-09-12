#!/bin/bash
# Build script for Budget App on Unix-like systems (macOS/Linux)

set -e  # Exit on any error

echo "🚀 Budget App Build Script"
echo "=========================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "src/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   (The directory containing src/main.py)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Make build script executable
chmod +x build.py

# Run the build
echo "🔨 Starting build process..."
python build.py

echo "✅ Build script completed!"

# Instructions for user
echo ""
echo "📋 Next steps:"
echo "1. Check the 'dist' folder for your executable"
echo "2. Test the application before distribution"
echo "3. The ZIP file contains everything needed for distribution"
echo ""

# Deactivate virtual environment
deactivate