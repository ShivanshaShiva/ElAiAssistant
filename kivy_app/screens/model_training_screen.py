"""
Model Training Screen Module.
This module contains the screen for training AI models.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

class ModelTrainingScreen(Screen):
    """Screen for training AI models."""
    
    def on_enter(self, *args):
        """Actions to perform when screen is entered."""
        app = App.get_running_app()
        
        # Create content if not already created
        if not self.children:
            self.create_content()
    
    def create_content(self):
        """Create the screen content."""
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        back_button = Button(
            text='Back',
            size_hint=(0.2, 1),
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        title_label = Label(
            text='Model Training',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        back_button.bind(on_press=lambda x: self._go_back())
        
        header.add_widget(back_button)
        header.add_widget(title_label)
        
        # Placeholder content
        placeholder = Label(
            text='Model Training\nFeature coming soon!',
            size_hint=(1, 0.9),
            font_size=dp(20)
        )
        
        # Add all elements to the main layout
        layout.add_widget(header)
        layout.add_widget(placeholder)
        
        # Add to screen
        self.add_widget(layout)
    
    def _go_back(self):
        """Return to the home screen."""
        app = App.get_running_app()
        app.navigate_to('home')