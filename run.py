#!/usr/bin/env python3
"""
El AI Assistant and Sanskrit NLP Tool.
This is the main entry point for running the application.
"""

import os
import sys
import logging
from kivy.logger import Logger

# Set up logging
Logger.setLevel(logging.INFO)

# Add the required code for Android permissions
try:
    # Android specific imports
    # Will only work on Android
    from android.permissions import request_permissions, Permission
    
    # Request permissions when running on Android
    def request_android_permissions():
        """Request necessary Android permissions."""
        permissions = [
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.CAMERA,
            Permission.RECORD_AUDIO,
            Permission.ACCESS_FINE_LOCATION
        ]
        request_permissions(permissions)
        
    request_android_permissions()
except ImportError:
    # Not running on Android, no need to request permissions
    pass

# Import the application
from kivy_app.main import ElAIApp

if __name__ == '__main__':
    # Check if GitHub access is restricted to owner
    def check_github_owner():
        """Check if the GitHub repo is accessed by the owner."""
        # This is a basic implementation. In a real app, you would use
        # GitHub API to verify the user identity.
        # For now, we'll just proceed with a log message since this is demo code
        owner_name = "ShivanshaShiva"
        owner_email = "nkg7060@gmail.com"
        Logger.info(f"GitHub access should be restricted to owner: {owner_name} ({owner_email})")
        return True
    
    # Verify owner (would be a real check in production)
    check_github_owner()
    
    # Run the application
    app = ElAIApp()
    app.run()