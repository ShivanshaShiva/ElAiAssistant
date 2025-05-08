"""
Sanskrit Screen Module.
This module contains the Sanskrit NLP screen for analyzing Sanskrit text.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.logger import Logger

class SanskritScreen(Screen):
    """Screen for Sanskrit text analysis."""
    
    text_input = ObjectProperty(None)
    results_label = ObjectProperty(None)
    
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
            text='Sanskrit NLP',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        back_button.bind(on_press=lambda x: self._go_back())
        
        header.add_widget(back_button)
        header.add_widget(title_label)
        
        # Description
        description = Label(
            text='Enter Sanskrit text for analysis',
            size_hint=(1, 0.05)
        )
        
        # Text input
        self.text_input = TextInput(
            hint_text='Enter Sanskrit text here...',
            multiline=True,
            size_hint=(1, 0.25),
            font_size=dp(18)
        )
        
        # Analysis options
        options_layout = GridLayout(cols=2, size_hint=(1, 0.1), spacing=dp(10))
        
        analysis_label = Label(text='Analysis Type:', halign='right', size_hint=(0.3, 1))
        analysis_spinner = Spinner(
            text='Grammar',
            values=('Grammar', 'Tokenization', 'POS Tagging', 'Semantics'),
            size_hint=(0.7, 1)
        )
        
        options_layout.add_widget(analysis_label)
        options_layout.add_widget(analysis_spinner)
        
        # Action buttons
        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        analyze_button = Button(
            text='Analyze',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        clear_button = Button(
            text='Clear',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.7, 0.3, 0.3, 1)
        )
        
        analyze_button.bind(on_press=lambda x: self._analyze_text(analysis_spinner.text))
        clear_button.bind(on_press=lambda x: self._clear_text())
        
        buttons_layout.add_widget(analyze_button)
        buttons_layout.add_widget(clear_button)
        
        # Results section
        results_box = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        results_header = Label(
            text='Results',
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.2)
        )
        self.results_label = TextInput(
            text='',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.8)
        )
        
        results_box.add_widget(results_header)
        results_box.add_widget(self.results_label)
        
        # Add all sections to main layout
        layout.add_widget(header)
        layout.add_widget(description)
        layout.add_widget(self.text_input)
        layout.add_widget(options_layout)
        layout.add_widget(buttons_layout)
        layout.add_widget(results_box)
        
        # Add to screen
        self.add_widget(layout)
    
    def _go_back(self):
        """Return to the home screen."""
        app = App.get_running_app()
        app.navigate_to('home')
    
    def _analyze_text(self, analysis_type):
        """Analyze the Sanskrit text."""
        app = App.get_running_app()
        text = self.text_input.text.strip()
        
        if not text:
            app.notification_manager.warning('Please enter some text to analyze')
            return
        
        # Analyze based on selected type
        if analysis_type == 'Grammar':
            result = app.sanskrit_nlp.analyze_grammar(text)
            if result['success']:
                output = 'Grammar Analysis:\n'
                for unit in result.get('grammar_units', []):
                    output += f"Token: {unit.get('token')}, Type: {unit.get('type')}\n"
                self.results_label.text = output
            else:
                self.results_label.text = f"Error: {result.get('error', 'Unknown error')}"
                
        elif analysis_type == 'Tokenization':
            tokens = app.sanskrit_nlp.tokenize_text(text)
            self.results_label.text = f"Tokenization Results:\n{', '.join(tokens)}"
            
        elif analysis_type == 'POS Tagging':
            tags = app.sanskrit_nlp.pos_tag(text)
            output = 'POS Tagging Results:\n'
            for token, tag in tags:
                output += f"{token}: {tag}\n"
            self.results_label.text = output
            
        elif analysis_type == 'Semantics':
            result = app.sanskrit_nlp.semantic_analysis(text)
            if result['success']:
                output = 'Semantic Analysis:\n'
                for meaning in result.get('meanings', []):
                    output += f"{meaning.get('text')}: {meaning.get('meaning')}\n"
                self.results_label.text = output
            else:
                self.results_label.text = f"Error: {result.get('error', 'Unknown error')}"
    
    def _clear_text(self):
        """Clear the text input and results."""
        self.text_input.text = ''
        self.results_label.text = ''