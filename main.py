"""
Main application entry point for the System Resource Monitor.
This file initializes the Kivy application and sets up the main UI.
"""

import kivy
kivy.require('2.1.0')  # Replace with your actual Kivy version

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config

# Set app to be resizable and set initial size
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class NavigationPanel(BoxLayout):
    """Panel for navigating to different functionalities."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Add navigation buttons
        self.add_widget(Button(text="System Monitor", on_press=self.load_system_monitor))
        self.add_widget(Button(text="Sanskrit NLP", on_press=self.load_sanskrit_nlp))
        self.add_widget(Button(text="Code Generation", on_press=self.load_code_generation))
        self.add_widget(Button(text="Repository Analysis", on_press=self.load_repository_analysis))
        self.add_widget(Button(text="Model Training", on_press=self.load_model_training))
        self.add_widget(Button(text="Settings", on_press=self.load_settings))
        self.add_widget(Button(text="About", on_press=self.load_about))

    def load_system_monitor(self, instance):
        """Load the system monitor."""
        print("Navigating to System Monitor...")

    def load_sanskrit_nlp(self, instance):
        """Load Sanskrit NLP tools."""
        print("Navigating to Sanskrit NLP...")

    def load_code_generation(self, instance):
        """Generate code using AI."""
        print("Navigating to Code Generation...")

    def load_repository_analysis(self, instance):
        """Analyze repositories."""
        print("Navigating to Repository Analysis...")

    def load_model_training(self, instance):
        """Train models."""
        print("Navigating to Model Training...")

    def load_settings(self, instance):
        """Load settings."""
        print("Navigating to Settings...")

    def load_about(self, instance):
        """About the app."""
        print("Navigating to About...")

