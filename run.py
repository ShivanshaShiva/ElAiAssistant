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



    




if __name__ == '__main__':
    
    # Run the system monitor UI only after successful login
    from main import launch_system_monitor
    launch_system_monitor()
    # This runs SystemMonitorApp from main.py
   

