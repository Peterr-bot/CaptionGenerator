#!/usr/bin/env python3
import os
import sys
import subprocess

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Run the actual script
subprocess.run([os.path.join(script_dir, "run.sh")], check=True)
