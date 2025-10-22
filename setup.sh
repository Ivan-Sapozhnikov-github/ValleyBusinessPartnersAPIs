#!/bin/bash
# Setup script for Valley Business Partners API Tools (Linux/Mac)

echo "========================================"
echo "Valley Business Partners API Tools"
echo "Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Error installing dependencies"
    echo "You may need to install them manually:"
    echo "  pip install -r requirements.txt"
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp config.example.env .env
    echo "✓ .env file created"
    echo ""
    echo "⚠ IMPORTANT: Edit .env and add your API keys:"
    echo "  - GOOGLE_API_KEY"
    echo "  - OPENAI_API_KEY"
    echo ""
else
    echo ".env file already exists"
    echo ""
fi

# Create output directory
if [ ! -d output ]; then
    mkdir output
    echo "✓ output/ directory created"
else
    echo "output/ directory already exists"
fi
echo ""

# Run installation test
echo "Running installation test..."
python test_installation.py
test_result=$?
echo ""

# Summary
echo "========================================"
echo "SETUP COMPLETE"
echo "========================================"
echo ""

if [ $test_result -eq 0 ]; then
    echo "✓ Setup successful!"
    echo ""
    echo "Next steps:"
    echo "  1. Edit .env and add your API keys"
    echo "  2. Run the application:"
    echo "     source venv/bin/activate"
    echo "     python main.py"
    echo ""
    echo "For help, see:"
    echo "  • README.md - Full documentation"
    echo "  • QUICKSTART.md - Quick start guide"
    echo "  • examples/ - Example scripts"
else
    echo "⚠ Setup completed with warnings"
    echo "Please check the errors above and:"
    echo "  1. Make sure all dependencies are installed"
    echo "  2. Edit .env and add your API keys"
    echo "  3. Run: python test_installation.py"
fi

echo ""
echo "========================================"
