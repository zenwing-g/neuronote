#!/bin/bash

# Update package list
sudo apt update

# Check if a virtual environment exists
if [ -d "venv" ]; then
    echo -e "\e[32mVirtual environment found. Activating...\e[0m"
else
    echo -e "\e[34mNo virtual environment found. Creating one named venv...\e[0m"
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install Python libraries inside the venv
pip install --upgrade pip
pip install pyqt6 pybind11 markdown2 jinja2 colorama

# Install system packages
sudo apt install -y cmake ninja-build g++ pkg-config sqlite3 pybind11-dev

# Install SQLite Browser (optional, for GUI database management)
sudo apt install -y sqlitebrowser

echo -e "\e[32mAll required packages installed successfully.\e[0m"
