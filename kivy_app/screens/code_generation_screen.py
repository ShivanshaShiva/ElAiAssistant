"""
Code Generation Screen Module.
This module contains the code generation screen.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.logger import Logger

class CodeGenerationScreen(Screen):
    """Screen for AI code generation."""
    
    prompt_input = ObjectProperty(None)
    code_output = ObjectProperty(None)
    
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
            text='Code Generation',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        back_button.bind(on_press=lambda x: self._go_back())
        
        header.add_widget(back_button)
        header.add_widget(title_label)
        
        # Description
        description = Label(
            text='Enter a description of what you need, and AI will generate code for you.',
            size_hint=(1, 0.1),
            halign='left'
        )
        description.bind(size=description.setter('text_size'))
        
        # Model selection
        model_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        model_label = Label(
            text='Model:',
            size_hint=(0.3, 1)
        )
        
        model_spinner = Spinner(
            text='ChatGPT',
            values=('ChatGPT', 'Gemma'),
            size_hint=(0.7, 1)
        )
        
        model_layout.add_widget(model_label)
        model_layout.add_widget(model_spinner)
        
        # Prompt input
        prompt_label = Label(
            text='Description:',
            size_hint=(1, 0.05),
            halign='left'
        )
        prompt_label.bind(size=prompt_label.setter('text_size'))
        
        self.prompt_input = TextInput(
            hint_text='Describe what code you need...',
            multiline=True,
            size_hint=(1, 0.2)
        )
        
        # Action buttons
        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        generate_button = Button(
            text='Generate Code',
            size_hint=(0.7, 1),
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        
        clear_button = Button(
            text='Clear',
            size_hint=(0.3, 1),
            background_normal='',
            background_color=(0.7, 0.3, 0.3, 1)
        )
        
        generate_button.bind(on_press=lambda x: self._generate_code(model_spinner.text))
        clear_button.bind(on_press=lambda x: self._clear_inputs())
        
        buttons_layout.add_widget(generate_button)
        buttons_layout.add_widget(clear_button)
        
        # Code output
        output_label = Label(
            text='Generated Code:',
            size_hint=(1, 0.05),
            halign='left'
        )
        output_label.bind(size=output_label.setter('text_size'))
        
        self.code_output = TextInput(
            hint_text='Generated code will appear here...',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.3)
        )
        
        # Add all elements to the main layout
        layout.add_widget(header)
        layout.add_widget(description)
        layout.add_widget(model_layout)
        layout.add_widget(prompt_label)
        layout.add_widget(self.prompt_input)
        layout.add_widget(buttons_layout)
        layout.add_widget(output_label)
        layout.add_widget(self.code_output)
        
        # Add to screen
        self.add_widget(layout)
    
    def _go_back(self):
        """Return to the home screen."""
        app = App.get_running_app()
        app.navigate_to('home')
    
    def _generate_code(self, model_name):
        """Generate code using the selected model."""
        app = App.get_running_app()
        prompt = self.prompt_input.text.strip()
        
        if not prompt:
            app.notification_manager.warning('Please enter a description of what code you need')
            return
        
        # Select model type
        if model_name == 'ChatGPT':
            from kivy_app.models.model_handler import ModelType
            model_type = ModelType.CHATGPT
        else:  # Gemma
            from kivy_app.models.model_handler import ModelType
            model_type = ModelType.GEMMA
        
        # Check if model is ready
        status_info = app.model_handler.get_status(model_type)
        if status_info.get('status') != 'ready':
            app.notification_manager.error(f'Model {model_name} is not ready. Please check Settings.')
            return
        
        # Show generating indicator
        self.code_output.text = 'Generating code...'
        
        # Enhance prompt for code generation
        code_prompt = f"Generate code for: {prompt}\nPlease provide only the code without explanations."
        
        # Use a background thread to avoid blocking the UI
        def generate_code_thread():
            try:
                # Generate text
                result = app.model_handler.generate_text(model_type, code_prompt)
                
                # Update UI in the main thread
                def update_ui(dt):
                    if result.get('success'):
                        self.code_output.text = result.get('text', '')
                    else:
                        self.code_output.text = f"Error: {result.get('error', 'Unknown error')}"
                        app.notification_manager.error(f"Code generation failed: {result.get('error', 'Unknown error')}")
                
                Clock.schedule_once(update_ui, 0)
            
            except Exception as e:
                def show_error(dt):
                    self.code_output.text = f"Error: {str(e)}"
                    app.notification_manager.error(f"Code generation failed: {str(e)}")
                
                Clock.schedule_once(show_error, 0)
        
        from threading import Thread
        Thread(target=generate_code_thread).start()
    
    def _clear_inputs(self):
        """Clear the prompt and output."""
        self.prompt_input.text = ''
        self.code_output.text = ''