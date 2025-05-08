"""
Main application file for the El AI Assistant and Sanskrit NLP Tool.
This is the entry point for the Kivy app.
"""

import os
import threading
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.logger import Logger

# Import utility modules
from kivy_app.utils.file_manager import FileManager
from kivy_app.utils.notification_manager import NotificationManager
from kivy_app.utils.sanskrit_nlp import SanskritNLP

# Import models
from kivy_app.models.model_handler import ModelHandler

# Import screens
from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.sanskrit_screen import SanskritScreen
from kivy_app.screens.code_generation_screen import CodeGenerationScreen
from kivy_app.screens.instruction_screen import InstructionScreen
from kivy_app.screens.settings_screen import SettingsScreen
from kivy_app.screens.repository_screen import RepositoryScreen
from kivy_app.screens.data_comparison_screen import DataComparisonScreen
from kivy_app.screens.model_training_screen import ModelTrainingScreen
from kivy_app.screens.about_screen import AboutScreen

class ElAIApp(App):
    """Main application class for the El AI Assistant and Sanskrit NLP Tool."""
    
    # Utilities
    model_handler = ObjectProperty(None)
    file_manager = ObjectProperty(None)
    notification_manager = ObjectProperty(None)
    sanskrit_nlp = ObjectProperty(None)
    
    # UI
    screen_manager = ObjectProperty(None)
    
    # App info
    version = StringProperty('0.1.0')
    
    def __init__(self, **kwargs):
        """Initialize the application."""
        super(ElAIApp, self).__init__(**kwargs)
        
        # Initialize managers
        self.model_handler = ModelHandler()
        self.file_manager = FileManager()
        self.notification_manager = NotificationManager()
        
        # Create data directory
        data_dir = os.path.join(os.path.expanduser('~'), '.elai', 'data')
        sanskrit_data_dir = os.path.join(data_dir, 'sanskrit')
        os.makedirs(sanskrit_data_dir, exist_ok=True)
        
        # Initialize Sanskrit NLP
        self.sanskrit_nlp = SanskritNLP(data_dir=sanskrit_data_dir)
        
        # Schedule initial data loading
        Clock.schedule_once(self._load_initial_data, 0.5)
    
    def _load_initial_data(self, dt):
        """Load initial data in a background thread."""
        # Start loading thread
        loading_thread = threading.Thread(target=self._load_data_thread)
        loading_thread.daemon = True
        loading_thread.start()
        
        # Schedule UI update when loading is complete
        Clock.schedule_once(self._on_data_loaded, 1.5)
    
    def _load_data_thread(self):
        """Background thread for loading data."""
        try:
            # Initialize basic utilities
            # No intensive operations here - just placeholders
            Logger.info("ElAIApp: Loading initial data...")
        except Exception as e:
            Logger.error(f"ElAIApp: Error loading data: {e}")
    
    def _on_data_loaded(self, dt):
        """Called when initial data is loaded."""
        self.notification_manager.info("Application ready")
    
    def build(self):
        """Build the application UI."""
        # Create screen manager
        self.screen_manager = ScreenManager(transition=SlideTransition())
        
        # Home screen
        home_screen = HomeScreen(name='home')
        self.screen_manager.add_widget(home_screen)
        
        # Sanskrit screen
        sanskrit_screen = SanskritScreen(name='sanskrit')
        self.screen_manager.add_widget(sanskrit_screen)
        
        # Code generation screen
        code_generation_screen = CodeGenerationScreen(name='code_generation')
        self.screen_manager.add_widget(code_generation_screen)
        
        # Instruction screen
        instruction_screen = InstructionScreen(name='instruction')
        self.screen_manager.add_widget(instruction_screen)
        
        # Settings screen
        settings_screen = SettingsScreen(name='settings')
        self.screen_manager.add_widget(settings_screen)
        
        # Repository screen
        repository_screen = RepositoryScreen(name='repository')
        self.screen_manager.add_widget(repository_screen)
        
        # Data comparison screen
        data_comparison_screen = DataComparisonScreen(name='data_comparison')
        self.screen_manager.add_widget(data_comparison_screen)
        
        # Model training screen
        model_training_screen = ModelTrainingScreen(name='model_training')
        self.screen_manager.add_widget(model_training_screen)
        
        # About screen
        about_screen = AboutScreen(name='about')
        self.screen_manager.add_widget(about_screen)
        
        return self.screen_manager
    
    def on_stop(self):
        """Clean up resources when the app is closing."""
        Logger.info("ElAIApp: Cleaning up resources")
    
    def navigate_to(self, screen_name):
        """Navigate to a specific screen."""
        if self.screen_manager:
            self.screen_manager.current = screen_name
    
if __name__ == '__main__':
    ElAIApp().run()