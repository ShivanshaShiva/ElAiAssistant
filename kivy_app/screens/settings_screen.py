"""
Settings Screen Module.
This screen allows users to configure application settings.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.logger import Logger

from kivy_app.models.model_handler import ModelType

class SettingsScreen(Screen):
    """Settings screen for configuring the application."""
    
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
            text='Settings',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Content in a scrollview
        scroll_view = ScrollView(
            size_hint=(1, 0.9),
            do_scroll_x=False
        )
        
        settings_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint=(1, None)
        )
        settings_layout.bind(minimum_height=settings_layout.setter('height'))
        
        # Sections
        api_keys_section = self._create_api_keys_section()
        model_paths_section = self._create_model_paths_section()
        app_settings_section = self._create_app_settings_section()
        
        # Add sections
        settings_layout.add_widget(api_keys_section)
        settings_layout.add_widget(model_paths_section)
        settings_layout.add_widget(app_settings_section)
        
        # Add the settings layout to the scroll view
        scroll_view.add_widget(settings_layout)
        
        # Add widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(scroll_view)
        
        # Add to screen
        self.add_widget(main_layout)
    
    def _create_api_keys_section(self):
        """Create the API keys settings section."""
        app = App.get_running_app()
        
        section = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(300)
        )
        
        # Section header
        header = Label(
            text='API Keys',
            font_size=dp(18),
            bold=True,
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        header.bind(size=header.setter('text_size'))
        
        # Gemma API key
        gemma_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(80)
        )
        
        gemma_label = Label(
            text='Gemma API Key',
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        
        gemma_input = TextInput(
            text=app.model_handler.get_api_key(ModelType.GEMMA),
            multiline=False,
            password=True,
            hint_text='Enter Gemma API key',
            size_hint=(1, None),
            height=dp(40)
        )
        
        gemma_layout.add_widget(gemma_label)
        gemma_layout.add_widget(gemma_input)
        
        # ChatGPT API key
        chatgpt_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(80)
        )
        
        chatgpt_label = Label(
            text='ChatGPT API Key',
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        
        chatgpt_input = TextInput(
            text=app.model_handler.get_api_key(ModelType.CHATGPT),
            multiline=False,
            password=True,
            hint_text='Enter ChatGPT API key',
            size_hint=(1, None),
            height=dp(40)
        )
        
        chatgpt_layout.add_widget(chatgpt_label)
        chatgpt_layout.add_widget(chatgpt_input)
        
        # Qiskit API key
        qiskit_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(80)
        )
        
        qiskit_label = Label(
            text='IBM Quantum API Key',
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        
        qiskit_input = TextInput(
            text=app.model_handler.get_api_key(ModelType.QISKIT),
            multiline=False,
            password=True,
            hint_text='Enter IBM Quantum API key',
            size_hint=(1, None),
            height=dp(40)
        )
        
        qiskit_layout.add_widget(qiskit_label)
        qiskit_layout.add_widget(qiskit_input)
        
        # Save button
        save_api_keys_button = Button(
            text='Save API Keys',
            size_hint=(0.5, None),
            height=dp(40),
            pos_hint={'center_x': 0.5}
        )
        
        # Store references to inputs
        self.gemma_api_key_input = gemma_input
        self.chatgpt_api_key_input = chatgpt_input
        self.qiskit_api_key_input = qiskit_input
        
        # Bind save button
        save_api_keys_button.bind(on_press=self._on_save_api_keys)
        
        # Add widgets to section
        section.add_widget(header)
        section.add_widget(gemma_layout)
        section.add_widget(chatgpt_layout)
        section.add_widget(qiskit_layout)
        section.add_widget(save_api_keys_button)
        
        return section
    
    def _create_model_paths_section(self):
        """Create the model paths settings section."""
        app = App.get_running_app()
        
        section = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(200)
        )
        
        # Section header
        header = Label(
            text='Local Model Paths',
            font_size=dp(18),
            bold=True,
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        header.bind(size=header.setter('text_size'))
        
        # Gemma model path
        gemma_path_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(40)
        )
        
        gemma_path_label = Label(
            text='Gemma Model Path:',
            size_hint=(0.3, 1),
            halign='left'
        )
        
        gemma_path_input = TextInput(
            text=app.model_handler.get_model_path(ModelType.GEMMA),
            multiline=False,
            hint_text='Path to local Gemma model',
            size_hint=(0.5, 1)
        )
        
        gemma_path_button = Button(
            text='Browse',
            size_hint=(0.2, 1)
        )
        
        gemma_path_layout.add_widget(gemma_path_label)
        gemma_path_layout.add_widget(gemma_path_input)
        gemma_path_layout.add_widget(gemma_path_button)
        
        # Save button
        save_paths_button = Button(
            text='Save Paths',
            size_hint=(0.5, None),
            height=dp(40),
            pos_hint={'center_x': 0.5}
        )
        
        # Store references to inputs
        self.gemma_path_input = gemma_path_input
        
        # Bind buttons
        gemma_path_button.bind(on_press=lambda x: self._browse_for_model_path(ModelType.GEMMA))
        save_paths_button.bind(on_press=self._on_save_model_paths)
        
        # Add widgets to section
        section.add_widget(header)
        section.add_widget(gemma_path_layout)
        section.add_widget(save_paths_button)
        
        return section
    
    def _create_app_settings_section(self):
        """Create the application settings section."""
        section = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(250)
        )
        
        # Section header
        header = Label(
            text='Application Settings',
            font_size=dp(18),
            bold=True,
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        header.bind(size=header.setter('text_size'))
        
        # Settings grid
        settings_grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(150)
        )
        
        # Dark mode setting
        dark_mode_label = Label(
            text='Dark Mode',
            halign='left',
            valign='middle'
        )
        dark_mode_label.bind(size=dark_mode_label.setter('text_size'))
        
        dark_mode_toggle = ToggleButton(
            text='Off',
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        dark_mode_toggle.bind(state=self._on_dark_mode_toggle)
        
        # Auto-save setting
        auto_save_label = Label(
            text='Auto-save',
            halign='left',
            valign='middle'
        )
        auto_save_label.bind(size=auto_save_label.setter('text_size'))
        
        auto_save_toggle = ToggleButton(
            text='Off',
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'center_y': 0.5}
        )
        auto_save_toggle.bind(state=self._on_auto_save_toggle)
        
        # Add to grid
        settings_grid.add_widget(dark_mode_label)
        settings_grid.add_widget(dark_mode_toggle)
        settings_grid.add_widget(auto_save_label)
        settings_grid.add_widget(auto_save_toggle)
        
        # Reset settings button
        reset_button = Button(
            text='Reset to Defaults',
            size_hint=(0.5, None),
            height=dp(40),
            pos_hint={'center_x': 0.5}
        )
        reset_button.bind(on_press=self._on_reset_settings)
        
        # Add widgets to section
        section.add_widget(header)
        section.add_widget(settings_grid)
        section.add_widget(reset_button)
        
        return section
    
    def _on_back_pressed(self, instance):
        """Handle back button press."""
        app = App.get_running_app()
        app.navigate_to('home')
    
    def _on_save_api_keys(self, instance):
        """Handle save API keys button press."""
        app = App.get_running_app()
        
        # Get input values
        gemma_api_key = self.gemma_api_key_input.text.strip()
        chatgpt_api_key = self.chatgpt_api_key_input.text.strip()
        qiskit_api_key = self.qiskit_api_key_input.text.strip()
        
        # Update API keys
        app.model_handler.set_api_key(ModelType.GEMMA, gemma_api_key)
        app.model_handler.set_api_key(ModelType.CHATGPT, chatgpt_api_key)
        app.model_handler.set_api_key(ModelType.QISKIT, qiskit_api_key)
        
        # Show success notification
        app.notification_manager.success("API keys saved successfully")
    
    def _on_save_model_paths(self, instance):
        """Handle save model paths button press."""
        app = App.get_running_app()
        
        # Get input values
        gemma_path = self.gemma_path_input.text.strip()
        
        # Update paths
        app.model_handler.set_model_path(ModelType.GEMMA, gemma_path)
        
        # Show success notification
        app.notification_manager.success("Model paths saved successfully")
    
    def _browse_for_model_path(self, model_type):
        """
        Open file browser to select model path.
        
        Args:
            model_type (ModelType): The model type to set path for
        """
        app = App.get_running_app()
        
        # File filters based on model type
        if model_type == ModelType.GEMMA:
            filters = ['*.gguf', '*.bin']
        else:
            filters = ['*.*']
        
        # Show file selector
        app.file_manager.select_file(
            title=f"Select {model_type.value} model file",
            filters=filters,
            on_selection=lambda path: self._on_model_path_selected(model_type, path)
        )
    
    def _on_model_path_selected(self, model_type, path):
        """
        Handle model path selection.
        
        Args:
            model_type (ModelType): The model type to set path for
            path (str): Selected file path
        """
        app = App.get_running_app()
        
        # Update path input
        if model_type == ModelType.GEMMA:
            self.gemma_path_input.text = path
        
        app.notification_manager.info(f"Selected {model_type.value} model: {path}")
    
    def _on_dark_mode_toggle(self, instance, value):
        """Handle dark mode toggle."""
        # Update toggle button text
        instance.text = 'On' if value == 'down' else 'Off'
        
        # TODO: Implement dark mode theme switching
        # This would change the app's color scheme
    
    def _on_auto_save_toggle(self, instance, value):
        """Handle auto-save toggle."""
        # Update toggle button text
        instance.text = 'On' if value == 'down' else 'Off'
        
        # TODO: Implement auto-save setting
    
    def _on_reset_settings(self, instance):
        """Handle reset settings button press."""
        app = App.get_running_app()
        
        # Reset settings (placeholder)
        # This would reset all settings to default values
        
        # For now, just show notification
        app.notification_manager.info("Settings reset to defaults")