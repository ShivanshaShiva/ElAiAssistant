#!/usr/bin/env python3
"""
El AI Assistant and Sanskrit NLP Tool.
This is the main entry point for running the application.
"""

import os
import sys

# Ensure we're in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run the main application
from kivy_app.main import ElAIApp

if __name__ == '__main__':
    ElAIApp().run()