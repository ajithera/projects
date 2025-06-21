#!/bin/bash

# Function to print error message and exit
error_exit() {
    echo "Error: $1"
    exit 1
}

# Check for interactive shell and sudo permissions
# Allow bypass if RUN_FROM_APPLESCRIPT=1 is set (for AppleScript/Automator)
if [ -z "$RUN_FROM_APPLESCRIPT" ]; then
    if ! tty -s; then
        echo "\n[ERROR] This script must be run in an interactive shell."
        echo "Please run it from a terminal window, not from a non-interactive environment."
        exit 1
    fi
else
    echo "[INFO] Running from AppleScript/Automator (RUN_FROM_APPLESCRIPT=1), skipping interactive shell check."
fi

# Check if sudo is required and available
if command -v sudo &> /dev/null; then
    if ! sudo -n true 2>/dev/null; then
        echo "\n[INFO] Sudo permissions are required for some steps."
        echo "You may be prompted for your password."
        if ! sudo -v; then
            echo "\n[ERROR] Sudo authentication failed or not available."
            echo "Please ensure you have sudo privileges and run this script interactively."
            exit 1
        fi
    fi
else
    echo "\n[WARNING] 'sudo' command not found. Some dependencies may fail to install."
fi

echo "Setting up PDF-ZHA..."

# Step 1: Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || error_exit "Failed to install Homebrew"
    echo "Homebrew installed successfully."
fi

# Step 2: Install Python 3.11 specifically
echo "Installing Python 3.11..."
brew install python@3.11 || error_exit "Failed to install Python 3.11"
brew link python@3.11 || error_exit "Failed to link Python 3.11"

# Verify Python version
PYTHON_CMD="python3.11"
if ! command -v $PYTHON_CMD &> /dev/null; then
    error_exit "Python 3.11 installation failed"
fi

# Step 3: Ensure pip is up to date
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip || error_exit "Failed to upgrade pip"

# Step 4: Install setuptools first
echo "Installing setuptools..."
$PYTHON_CMD -m pip install --upgrade setuptools wheel || error_exit "Failed to install setuptools"

# Step 5: Create and activate virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv venv || error_exit "Failed to create virtual environment"
source venv/bin/activate || error_exit "Failed to activate virtual environment"

# Step 6: Pre-install critical packages
echo "Installing critical dependencies..."
pip install --upgrade pip setuptools wheel || error_exit "Failed to install critical dependencies"

# Step 7: Install all requirements
echo "Installing project requirements..."
pip install -r requirements.txt || error_exit "Failed to install requirements"

echo "Setup completed successfully! Virtual environment is activated."

# Step 4: Activate the virtual environment
source venv/bin/activate

# Step 5: Install required packages
pip install -r requirements.txt

# Step 6: Run the Flask server
python server.py &
SERVER_PID=$!

# Step 7: Wait for the server to start
sleep 5

# Step 8: Open the index.html file in the default browser
open index.html

# Step 9: Wait for the user to close the browser
read -p "Press [Enter] once you have closed the browser to stop the server and clean up."

# Step 10: Stop the server
kill $SERVER_PID

# Step 11: Deactivate and delete the virtual environment
deactivate
rm -rf venv
