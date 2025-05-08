"""
Code Generation Screen Module.
This screen provides code generation capabilities using AI models.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.logger import Logger

from kivy_app.models.model_handler import ModelType

class CodeGenerationScreen(Screen):
    """Screen for code generation using AI models."""
    
    def on_enter(self, *args):
        """Actions to perform when screen is entered."""
        # Create content if not already created
        if not self.children:
            self.create_content()
    
    def create_content(self):
        """Create the screen content."""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Header with back button
        header = BoxLayout(
            size_hint=(1, 0.1),
            spacing=dp(10)
        )
        
        back_button = Button(
            text='Back',
            size_hint=(0.2, 1),
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        back_button.bind(on_press=self._on_back_pressed)
        
        title = Label(
            text='Code Generation',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Main content
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.9),
            spacing=dp(15)
        )
        
        # Model selection
        model_section = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),
            spacing=dp(10)
        )
        
        model_label = Label(
            text='Model:',
            size_hint=(0.15, 1)
        )
        
        self.model_spinner = Spinner(
            text='ChatGPT',
            values=('ChatGPT', 'Gemma'),
            size_hint=(0.35, 1)
        )
        
        language_label = Label(
            text='Language:',
            size_hint=(0.15, 1)
        )
        
        self.language_spinner = Spinner(
            text='Python',
            values=('Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust', 'PHP', 'Swift', 'Kotlin', 'C#'),
            size_hint=(0.35, 1)
        )
        
        model_section.add_widget(model_label)
        model_section.add_widget(self.model_spinner)
        model_section.add_widget(language_label)
        model_section.add_widget(self.language_spinner)
        
        # Prompt section
        prompt_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            spacing=dp(5)
        )
        
        prompt_header = Label(
            text='Prompt:',
            size_hint=(1, 0.15),
            halign='left'
        )
        prompt_header.bind(size=prompt_header.setter('text_size'))
        
        # Prompt text input
        self.prompt_input = TextInput(
            hint_text='Describe the code you want to generate (e.g., "Create a function to sort a list of dictionaries by a specific key")',
            size_hint=(1, 0.85),
            multiline=True
        )
        
        prompt_section.add_widget(prompt_header)
        prompt_section.add_widget(self.prompt_input)
        
        # Action buttons
        button_section = BoxLayout(
            size_hint=(1, 0.1),
            spacing=dp(10)
        )
        
        generate_button = Button(
            text='Generate Code',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        
        clear_button = Button(
            text='Clear',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.7, 0.3, 0.3, 1)
        )
        
        # Bind buttons
        generate_button.bind(on_press=self._on_generate_code)
        clear_button.bind(on_press=self._on_clear)
        
        button_section.add_widget(generate_button)
        button_section.add_widget(clear_button)
        
        # Generated code section
        code_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.42),
            spacing=dp(5)
        )
        
        code_header = Label(
            text='Generated Code:',
            size_hint=(1, 0.1),
            halign='left'
        )
        code_header.bind(size=code_header.setter('text_size'))
        
        # Code output in a scrollview
        code_scroll = ScrollView(
            size_hint=(1, 0.8)
        )
        
        self.code_output = TextInput(
            readonly=True,
            font_name='monospace',
            size_hint=(1, None),
            height=dp(400)
        )
        
        code_scroll.add_widget(self.code_output)
        
        # Action buttons for generated code
        code_buttons = BoxLayout(
            size_hint=(1, 0.1),
            spacing=dp(10)
        )
        
        copy_button = Button(
            text='Copy to Clipboard',
            size_hint=(0.5, 1)
        )
        
        save_button = Button(
            text='Save to File',
            size_hint=(0.5, 1)
        )
        
        # Bind buttons
        copy_button.bind(on_press=self._on_copy_to_clipboard)
        save_button.bind(on_press=self._on_save_to_file)
        
        code_buttons.add_widget(copy_button)
        code_buttons.add_widget(save_button)
        
        code_section.add_widget(code_header)
        code_section.add_widget(code_scroll)
        code_section.add_widget(code_buttons)
        
        # Add sections to content layout
        content_layout.add_widget(model_section)
        content_layout.add_widget(prompt_section)
        content_layout.add_widget(button_section)
        content_layout.add_widget(code_section)
        
        # Add widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(content_layout)
        
        # Add main layout to screen
        self.add_widget(main_layout)
    
    def _on_back_pressed(self, instance):
        """Handle back button press."""
        app = App.get_running_app()
        app.navigate_to('home')
    
    def _on_generate_code(self, instance):
        """Handle generate code button press."""
        app = App.get_running_app()
        
        prompt = self.prompt_input.text.strip()
        if not prompt:
            app.notification_manager.warning("Please enter a prompt for code generation")
            return
        
        # Get selected model and language
        model_name = self.model_spinner.text
        language = self.language_spinner.text
        
        # Map model name to ModelType
        model_type = None
        if model_name == 'ChatGPT':
            model_type = ModelType.CHATGPT
        elif model_name == 'Gemma':
            model_type = ModelType.GEMMA
        
        if not model_type:
            app.notification_manager.error("Invalid model selected")
            return
        
        # Build complete prompt with language
        complete_prompt = f"Generate {language} code for: {prompt}\n\nPlease provide only the code with appropriate comments, no explanations."
        
        # Show loading message
        app.notification_manager.info(f"Generating code using {model_name}...")
        self.code_output.text = "Generating code, please wait..."
        
        # Generate code using the selected model
        result = app.model_handler.generate_text(model_type, complete_prompt)
        
        if result.get('success', False):
            generated_text = result.get('text', '')
            
            # Extract code block if present (assuming markdown format from AI)
            import re
            code_block_pattern = r'```(?:\w+)?\n([\s\S]+?)\n```'
            code_blocks = re.findall(code_block_pattern, generated_text)
            
            if code_blocks:
                # Use the first code block found
                self.code_output.text = code_blocks[0].strip()
            else:
                # Use the full output if no code blocks found
                self.code_output.text = generated_text.strip()
                
            app.notification_manager.success("Code generated successfully")
        else:
            error = result.get('error', 'Unknown error')
            self.code_output.text = f"Error generating code: {error}"
            app.notification_manager.error(f"Failed to generate code: {error}")
    
    def _on_clear(self, instance):
        """Handle clear button press."""
        self.prompt_input.text = ""
        self.code_output.text = ""
    
    def _on_copy_to_clipboard(self, instance):
        """Handle copy to clipboard button press."""
        app = App.get_running_app()
        
        if not self.code_output.text.strip():
            app.notification_manager.warning("No code to copy")
            return
        
        # Copy to clipboard
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.code_output.text)
        
        app.notification_manager.success("Code copied to clipboard")
    
    def _on_save_to_file(self, instance):
        """Handle save to file button press."""
        app = App.get_running_app()
        
        code = self.code_output.text.strip()
        if not code:
            app.notification_manager.warning("No code to save")
            return
        
        # Map language to file extension
        language = self.language_spinner.text
        extensions = {
            'Python': '.py',
            'JavaScript': '.js',
            'Java': '.java',
            'C++': '.cpp',
            'Go': '.go',
            'Rust': '.rs',
            'PHP': '.php',
            'Swift': '.swift',
            'Kotlin': '.kt',
            'C#': '.cs'
        }
        
        extension = extensions.get(language, '.txt')
        
        # Create temporary file with the generated code
        temp_file = app.file_manager.create_temp_file(
            content=code,
            prefix="generated_code_",
            suffix=extension
        )
        
        if temp_file:
            app.notification_manager.success(f"Code saved to: {temp_file}")
            
            # Ask user where to save the file permanently
            app.file_manager.select_file(
                title=f"Save {language} Code",
                filters=[f"*{extension}"],
                on_selection=lambda path: self._on_save_location_selected(temp_file, path)
            )
        else:
            app.notification_manager.error("Failed to save code to file")