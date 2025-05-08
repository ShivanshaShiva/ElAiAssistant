"""
Home Screen Module.
This is the main screen of the application.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.logger import Logger

class HomeScreen(Screen):
    """Main home screen of the application."""
    
    def on_enter(self, *args):
        """Actions to perform when screen is entered."""
        # Create content if not already created
        if not self.children:
            self.create_content()
    
    def create_content(self):
        """Create the screen content."""
        app = App.get_running_app()
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Header
        header = BoxLayout(
            size_hint=(1, 0.15),
            spacing=dp(10)
        )
        
        # App logo
        logo = Image(
            source='resources/app_icon.png',
            size_hint=(0.2, 1),
            allow_stretch=True
        )
        
        # App name and version
        title_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 1),
            padding=[0, dp(10)]
        )
        
        title = Label(
            text='El AI Assistant',
            font_size=dp(24),
            bold=True,
            size_hint=(1, 0.6)
        )
        
        version = Label(
            text=f'Version {app.version}',
            font_size=dp(14),
            size_hint=(1, 0.4)
        )
        
        title_box.add_widget(title)
        title_box.add_widget(version)
        
        # Settings and About buttons
        buttons_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1),
            spacing=dp(5)
        )
        
        settings_button = Button(
            text='Settings',
            size_hint=(1, 0.5),
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        
        about_button = Button(
            text='About',
            size_hint=(1, 0.5),
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        
        settings_button.bind(on_press=lambda x: app.navigate_to('settings'))
        about_button.bind(on_press=lambda x: app.navigate_to('about'))
        
        buttons_box.add_widget(settings_button)
        buttons_box.add_widget(about_button)
        
        # Add widgets to header
        header.add_widget(logo)
        header.add_widget(title_box)
        header.add_widget(buttons_box)
        
        # Feature grid
        feature_grid = GridLayout(
            cols=2,
            size_hint=(1, 0.85),
            spacing=dp(15),
            padding=[0, dp(10)]
        )
        
        # Create feature buttons
        features = [
            {'name': 'Sanskrit NLP', 'screen': 'sanskrit', 'icon': '🔤', 'color': (0.2, 0.6, 0.8, 1)},
            {'name': 'Code Generation', 'screen': 'code_generation', 'icon': '💻', 'color': (0.2, 0.7, 0.3, 1)},
            {'name': 'Instruction Learning', 'screen': 'instruction', 'icon': '🧠', 'color': (0.8, 0.4, 0.2, 1)},
            {'name': 'Repository Analysis', 'screen': 'repository', 'icon': '📁', 'color': (0.6, 0.2, 0.6, 1)},
            {'name': 'Data Comparison', 'screen': 'data_comparison', 'icon': '📊', 'color': (0.8, 0.6, 0.2, 1)},
            {'name': 'Model Training', 'screen': 'model_training', 'icon': '⚙️', 'color': (0.5, 0.5, 0.5, 1)}
        ]
        
        for feature in features:
            feature_button = self._create_feature_button(
                name=feature['name'],
                icon=feature['icon'],
                color=feature['color'],
                screen=feature['screen']
            )
            feature_grid.add_widget(feature_button)
        
        # Add all sections to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(feature_grid)
        
        # Add to screen
        self.add_widget(main_layout)
    
    def _create_feature_button(self, name, icon, color, screen):
        """Create a feature button with icon and label."""
        app = App.get_running_app()
        
        button_layout = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10)
        )
        button_layout.background_color = color
        
        # Custom background using canvas
        from kivy.graphics import Color, Rectangle
        with button_layout.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=button_layout.pos, size=button_layout.size)
        
        button_layout.bind(pos=self._update_rect, size=self._update_rect)
        
        # Icon and text
        icon_label = Label(
            text=icon,
            font_size=dp(36),
            size_hint=(1, 0.6)
        )
        
        name_label = Label(
            text=name,
            font_size=dp(18),
            size_hint=(1, 0.4)
        )
        
        button_layout.add_widget(icon_label)
        button_layout.add_widget(name_label)
        
        # Make it clickable
        button = Button(
            background_color=(0, 0, 0, 0),  # Transparent
            on_press=lambda x: app.navigate_to(screen)
        )
        
        # Combine button and layout
        container = BoxLayout()
        container.add_widget(button_layout)
        container.add_widget(button)
        
        return container
    
    def _update_rect(self, instance, value):
        """Update rectangle position and size."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size