"""
Main application file for the El AI Assistant and Sanskrit NLP Tool.
This is the entry point for the Kivy app.
"""

import os
import threading
import time
from typing import Optional, Dict, Any

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.utils import platform

# Import screens
from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.sanskrit_screen import SanskritScreen
from kivy_app.screens.code_generation_screen import CodeGenerationScreen
from kivy_app.screens.repository_screen import RepositoryScreen
from kivy_app.screens.model_training_screen import ModelTrainingScreen
from kivy_app.screens.data_comparison_screen import DataComparisonScreen
from kivy_app.screens.settings_screen import SettingsScreen
from kivy_app.screens.about_screen import AboutScreen
from kivy_app.screens.instruction_screen import InstructionScreen

# Import utils and models
from kivy_app.models.model_handler import ModelHandler
from kivy_app.utils.file_manager import FileManager
from kivy_app.utils.notification_manager import NotificationManager
from kivy_app.utils.sanskrit_nlp import SanskritNLP


class ElAIApp(App):
    """Main application class for the El AI Assistant and Sanskrit NLP Tool."""
    
    # Component managers
    model_handler = ObjectProperty(None)
    file_manager = ObjectProperty(None)
    notification_manager = ObjectProperty(None)
    sanskrit_nlp = ObjectProperty(None)
    
    # UI components
    screen_manager = ObjectProperty(None)
    
    # App information
    version = StringProperty('0.1.0')
    
    def __init__(self, **kwargs):
        """Initialize the application."""
        super(ElAIApp, self).__init__(**kwargs)
        
        # Initialize component managers
        self.model_handler = ModelHandler()
        self.file_manager = FileManager()
        self.notification_manager = NotificationManager()
        self.sanskrit_nlp = SanskritNLP()
        
        # Set up data loading flag
        self._data_loaded = False
        self._loading_thread = None
        
        # For Android, set the window to fullscreen
        if platform == 'android':
            Window.fullscreen = 'auto'
    
    def _load_initial_data(self, dt):
        """Load initial data in a background thread."""
        if self._loading_thread is None or not self._loading_thread.is_alive():
            self._loading_thread = threading.Thread(target=self._load_data_thread)
            self._loading_thread.daemon = True
            self._loading_thread.start()
    
    def _load_data_thread(self):
        """Background thread for loading data."""
        try:
            # Initialize the model handler (this might take time)
            try:
                # Try to load any saved API keys
                # This is a placeholder - in a real app you'd load from secure storage
                api_keys = {}
                
                # Initialize models if API keys are available
                if api_keys.get('openai'):
                    self.model_handler.initialize_openai(api_keys['openai'])
                
                if api_keys.get('gemma'):
                    self.model_handler.initialize_gemma(api_keys['gemma'])
            except Exception as e:
                Logger.error(f"Failed to initialize models: {e}")
            
            # Load any other necessary data
            # For example, load saved settings, recent files, etc.
            
            # Mark data as loaded
            self._data_loaded = True
            
            # Schedule notification in main thread
            Clock.schedule_once(self._on_data_loaded)
            
        except Exception as e:
            Logger.error(f"Error loading initial data: {e}")
            # Show error in main thread
            Clock.schedule_once(lambda dt: self.notification_manager.error(
                f"Error loading initial data: {str(e)}"
            ))
    
    def _on_data_loaded(self, dt):
        """Called when initial data is loaded."""
        if self._data_loaded:
            # Update UI to reflect loaded data
            self.notification_manager.info("Ready to use")
    
    def build(self):
        """Build the application UI."""
        # Create the screen manager
        self.screen_manager = ScreenManager(transition=SlideTransition())
        
        # Add screens
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(SanskritScreen(name='sanskrit'))
        self.screen_manager.add_widget(CodeGenerationScreen(name='code_generation'))
        self.screen_manager.add_widget(RepositoryScreen(name='repository'))
        self.screen_manager.add_widget(ModelTrainingScreen(name='model_training'))
        self.screen_manager.add_widget(DataComparisonScreen(name='data_comparison'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.add_widget(AboutScreen(name='about'))
        self.screen_manager.add_widget(InstructionScreen(name='instruction'))
        
        # Schedule loading of initial data
        Clock.schedule_once(self._load_initial_data, 0.5)
        
        return self.screen_manager
    
    def on_stop(self):
        """Clean up resources when the app is closing."""
        # Save any unsaved data
        # For example, save settings, recent files, etc.
        
        # Clean up any open resources
        try:
            # Clean temp files older than 7 days
            self.file_manager.clean_temp_files(days_old=7)
        except:
            pass
    
    def navigate_to(self, screen_name):
        """Navigate to a specific screen."""
        if self.screen_manager.has_screen(screen_name):
            self.screen_manager.current = screen_name
        else:
            self.notification_manager.error(f"Screen '{screen_name}' not found")


if __name__ == '__main__':
    ElAIApp().run()