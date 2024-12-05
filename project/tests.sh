#!/bin/bash
# Print the current working directory
echo "Current directory: $(pwd)"

# List the files in the current directory to verify that tests.py is present
echo "Listing files:"
ls -l ./project/
python3 -m unittest discover -s . -p "tests.py"
