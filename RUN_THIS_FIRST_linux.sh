#!/bin/bash

# Add NVM's npm path to PATH dynamically for every user
NVM_DIR="$HOME/.nvm"
NODE_VERSION="v18.20.4"
NPM_PATH="$NVM_DIR/versions/node/$NODE_VERSION/bin"

# Check if NVM directory exists and add to PATH
if [ -d "$NPM_PATH" ]; then
    export PATH="$PATH:$NPM_PATH"
    
    # Persist PATH in .bashrc or .bash_profile for future sessions
    if [[ "$SHELL" == */bash ]]; then
        PROFILE_FILE="$HOME/.bashrc"
        [[ -f "$HOME/.bash_profile" ]] && PROFILE_FILE="$HOME/.bash_profile"
        
        if ! grep -q "$NPM_PATH" "$PROFILE_FILE"; then
            echo "export PATH=\$PATH:$NPM_PATH" >> "$PROFILE_FILE"
            echo "Added NVM and Node.js to your PATH permanently in $PROFILE_FILE"
        else
            echo "NVM and Node.js are already added to your PATH in $PROFILE_FILE"
        fi
    fi
else
    echo "- Error: Node.js version $NODE_VERSION not found. Please install it using NVM."
    exit 1
fi

# Check if Python 3.10 or 3.11 is installed
python3.11 --version 2>&1 | grep -q -E "Python 3\.(10|11)\."
if [ $? -ne 0 ]; then
    echo "- Error: Incompatible Python version found"
    echo ""
    echo "Please install either Python 3.10 or 3.11."
    echo ""
    read -n1 -r -p "Press any key to continue..."
    exit
else
    echo "Compatible Python version found: $(python3.11 --version)"
fi

# Check if npm is installed
npm --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "- Error: NPM not installed"
    echo "? Continuing will try and install Node automatically, CTRL+C to cancel."
    read -n1 -r -p "Press any key to continue..."
    python helpers/download_node_linux.py
    echo ""
    echo "Please restart the script to check if Node was installed correctly."
    echo "If it's not working, you can install it manually from https://nodejs.org/"
    read -n1 -r -p "Press any key to continue..."
    exit
else
    # If npm is installed, display the version
    echo "- NPM is installed. Version: $(npm --version)"
fi

# Check if git is installed
command -v git >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "- Error: Git not installed"
    echo "? Continuing will try and install Git automatically, CTRL+C to cancel."
    read -n1 -r -p "Press any key to continue..."
    python helpers/download_git_linux.py
    echo ""
    echo "Please restart the script to check if Git was installed correctly."
    echo "If it's not working then you can install it manually from https://git-scm.com/downloads"
    read -n1 -r -p "Press any key to continue..."
    exit
fi

# Make START_linux.sh executable
chmod +x START_linux.sh
echo "START_linux.sh is now executable."

echo "All prerequisites are installed, you can now run the START file."
read -n1 -r -p "Press any key to continue..."

export PATH=$PATH:/home/zia/.nvm/versions/node/v18.20.4/bin
