"""
About Screen Module.
This module contains the About screen with app information.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.window import Window

class AboutScreen(Screen):
    """Screen with information about the app."""
    
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
            text='About',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        back_button.bind(on_press=lambda x: self._go_back())
        
        header.add_widget(back_button)
        header.add_widget(title_label)
        
        # Content layout (scrollable)
        content = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.9),
            spacing=dp(20)
        )
        content.bind(minimum_height=content.setter('height'))
        
        # App logo
        logo_wrapper = BoxLayout(
            size_hint=(1, None),
            height=dp(100),
            padding=[dp(50), 0]
        )
        logo = Image(
            source='resources/app_icon.png',
            allow_stretch=True,
            size_hint=(None, None),
            size=(dp(100), dp(100))
        )
        logo_wrapper.add_widget(logo)
        
        # App name and version
        app = App.get_running_app()
        app_info = Label(
            text=f'El AI Assistant\nVersion {app.version}',
            font_size=dp(20),
            halign='center',
            valign='middle',
            size_hint=(1, None),
            height=dp(60)
        )
        
        # Description
        description = Label(
            text='El AI Assistant is a powerful tool for AI-powered code generation, '
                 'Sanskrit language processing, repository analysis, and more. '
                 'The app integrates multiple AI models and provides a '
                 'comprehensive suite of features for developers and researchers.',
            size_hint=(1, None),
            height=dp(120),
            text_size=(Window.width - dp(40), None),
            halign='left',
            valign='top'
        )
        description.bind(texture_size=description.setter('size'))
        
        # Features
        features_title = Label(
            text='Key Features:',
            font_size=dp(18),
            bold=True,
            size_hint=(1, None),
            height=dp(40),
            halign='left'
        )
        
        features_list = Label(
            text='• AI Code Generation\n'
                 '• Sanskrit Language Processing\n'
                 '• Repository Analysis\n'
                 '• Instruction Learning\n'
                 '• Model Training\n'
                 '• Data Comparison',
            size_hint=(1, None),
            height=dp(150),
            halign='left',
            valign='top',
            text_size=(Window.width - dp(40), None)
        )
        features_list.bind(texture_size=features_list.setter('size'))
        
        # Credits
        credits = Label(
            text='© 2023-2024 El AI Assistant Team\n'
                 'All rights reserved.',
            size_hint=(1, None),
            height=dp(50),
            halign='center',
            valign='bottom'
        )
        
        # Add all sections to content
        content.add_widget(logo_wrapper)
        content.add_widget(app_info)
        content.add_widget(description)
        content.add_widget(features_title)
        content.add_widget(features_list)
        content.add_widget(credits)
        
        # Add everything to main layout
        layout.add_widget(header)
        layout.add_widget(content)
        
        # Add to screen
        self.add_widget(layout)
    
    def _go_back(self):
        """Return to the home screen."""
        app = App.get_running_app()
        app.navigate_to('home')