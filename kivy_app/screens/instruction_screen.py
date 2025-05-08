"""
Instruction Screen Module.
This module contains the screen for learning new instructions.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.logger import Logger

class InstructionScreen(Screen):
    """Screen for learning new instructions."""
    
    instruction_input = ObjectProperty(None)
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
            text='Instruction Learning',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        back_button.bind(on_press=lambda x: self._go_back())
        
        header.add_widget(back_button)
        header.add_widget(title_label)
        
        # Description
        description = Label(
            text='Teach the assistant by providing instructions',
            size_hint=(1, 0.1),
            halign='left'
        )
        description.bind(size=description.setter('text_size'))
        
        # Instruction input
        instruction_label = Label(
            text='Instruction:',
            size_hint=(1, 0.05),
            halign='left'
        )
        instruction_label.bind(size=instruction_label.setter('text_size'))
        
        self.instruction_input = TextInput(
            hint_text='Enter your instruction...',
            multiline=True,
            size_hint=(1, 0.3)
        )
        
        # Action buttons
        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        learn_button = Button(
            text='Learn Instruction',
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
        
        learn_button.bind(on_press=lambda x: self._learn_instruction())
        clear_button.bind(on_press=lambda x: self._clear_inputs())
        
        buttons_layout.add_widget(learn_button)
        buttons_layout.add_widget(clear_button)
        
        # Results area
        results_label = Label(
            text='Results:',
            size_hint=(1, 0.05),
            halign='left'
        )
        results_label.bind(size=results_label.setter('text_size'))
        
        self.results_label = TextInput(
            hint_text='Learning results will appear here...',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.3)
        )
        
        # Add all elements to the main layout
        layout.add_widget(header)
        layout.add_widget(description)
        layout.add_widget(instruction_label)
        layout.add_widget(self.instruction_input)
        layout.add_widget(buttons_layout)
        layout.add_widget(results_label)
        layout.add_widget(self.results_label)
        
        # Add to screen
        self.add_widget(layout)
    
    def _go_back(self):
        """Return to the home screen."""
        app = App.get_running_app()
        app.navigate_to('home')
    
    def _learn_instruction(self):
        """Learn an instruction."""
        app = App.get_running_app()
        instruction = self.instruction_input.text.strip()
        
        if not instruction:
            app.notification_manager.warning('Please enter an instruction to learn')
            return
        
        # Show learning indicator
        self.results_label.text = 'Learning...'
        
        # Use the Sanskrit NLP module to learn
        def learn_thread():
            try:
                result = app.sanskrit_nlp.learn_grammar_rule(instruction)
                
                # Update UI in the main thread
                def update_ui(dt):
                    if result.get('success'):
                        output = f"Successfully learned rule: {result.get('rule', {}).get('name', '')}\n\n"
                        output += f"Description: {result.get('rule', {}).get('description', '')}\n\n"
                        
                        # Show mappings/examples
                        mappings = result.get('mappings', {})
                        if mappings:
                            output += "Examples:\n"
                            for example, result_text in mappings.items():
                                output += f"- '{example}' -> '{result_text}'\n"
                        
                        self.results_label.text = output
                        app.notification_manager.success('Instruction learned successfully')
                    else:
                        self.results_label.text = f"Error: {result.get('error', 'Unknown error')}"
                        app.notification_manager.error(f"Learning failed: {result.get('error', 'Unknown error')}")
                
                Clock.schedule_once(update_ui, 0)
            
            except Exception as e:
                def show_error(dt):
                    self.results_label.text = f"Error: {str(e)}"
                    app.notification_manager.error(f"Learning failed: {str(e)}")
                
                Clock.schedule_once(show_error, 0)
        
        from threading import Thread
        Thread(target=learn_thread).start()
    
    def _clear_inputs(self):
        """Clear the instruction and results."""
        self.instruction_input.text = ''
        self.results_label.text = ''