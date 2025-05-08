"""
Sanskrit Screen Module.
This screen provides Sanskrit language processing capabilities.
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

class SanskritScreen(Screen):
    """Screen for Sanskrit language processing."""
    
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
            text='Sanskrit NLP',
            font_size=dp(24),
            bold=True,
            size_hint=(0.8, 1)
        )
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Content in a tab-like structure
        tab_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.9)
        )
        
        # Tabs buttons
        tabs_buttons = BoxLayout(
            size_hint=(1, 0.08),
            spacing=dp(2)
        )
        
        transliterate_button = Button(
            text='Transliterate',
            background_normal='',
            background_color=(0.3, 0.5, 0.9, 1)
        )
        
        tokenize_button = Button(
            text='Tokenize',
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        
        sandhi_button = Button(
            text='Sandhi Analysis',
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        
        learn_button = Button(
            text='Learn Rules',
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 1)
        )
        
        # Bind tab buttons
        transliterate_button.bind(on_press=lambda x: self._switch_tab('transliterate'))
        tokenize_button.bind(on_press=lambda x: self._switch_tab('tokenize'))
        sandhi_button.bind(on_press=lambda x: self._switch_tab('sandhi'))
        learn_button.bind(on_press=lambda x: self._switch_tab('learn'))
        
        tabs_buttons.add_widget(transliterate_button)
        tabs_buttons.add_widget(tokenize_button)
        tabs_buttons.add_widget(sandhi_button)
        tabs_buttons.add_widget(learn_button)
        
        # Tab content layout
        self.tab_content = BoxLayout(
            size_hint=(1, 0.92)
        )
        
        # Store button references
        self.tab_buttons = {
            'transliterate': transliterate_button,
            'tokenize': tokenize_button,
            'sandhi': sandhi_button,
            'learn': learn_button
        }
        
        # Add tabs and content to tab layout
        tab_layout.add_widget(tabs_buttons)
        tab_layout.add_widget(self.tab_content)
        
        # Add header and tab layout to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(tab_layout)
        
        # Add main layout to screen
        self.add_widget(main_layout)
        
        # Initially show transliterate tab
        self._switch_tab('transliterate')
    
    def _switch_tab(self, tab_name):
        """
        Switch to a specific tab.
        
        Args:
            tab_name (str): Name of the tab to switch to
        """
        # Reset all tab buttons to default color
        for button in self.tab_buttons.values():
            button.background_color = (0.3, 0.3, 0.3, 1)
        
        # Highlight the active tab
        self.tab_buttons[tab_name].background_color = (0.3, 0.5, 0.9, 1)
        
        # Clear current content
        self.tab_content.clear_widgets()
        
        # Add new content based on selected tab
        if tab_name == 'transliterate':
            self.tab_content.add_widget(self._create_transliterate_tab())
        elif tab_name == 'tokenize':
            self.tab_content.add_widget(self._create_tokenize_tab())
        elif tab_name == 'sandhi':
            self.tab_content.add_widget(self._create_sandhi_tab())
        elif tab_name == 'learn':
            self.tab_content.add_widget(self._create_learn_tab())
    
    def _create_transliterate_tab(self):
        """Create the transliterate tab content."""
        tab = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # Explanation
        explanation = Label(
            text='Convert Sanskrit text between different writing systems',
            size_hint=(1, 0.1),
            halign='left',
            valign='top'
        )
        explanation.bind(size=explanation.setter('text_size'))
        
        # Input section
        input_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        input_header = Label(
            text='Input Text:',
            size_hint=(1, 0.2),
            halign='left'
        )
        input_header.bind(size=input_header.setter('text_size'))
        
        # Text input
        self.transliterate_input = TextInput(
            hint_text='Enter Sanskrit text to transliterate',
            size_hint=(1, 0.6),
            multiline=True
        )
        
        # Scheme selection
        schemes_layout = BoxLayout(
            size_hint=(1, 0.2),
            spacing=dp(10)
        )
        
        from_label = Label(
            text='From:',
            size_hint=(0.15, 1)
        )
        
        self.from_scheme = Spinner(
            text='IAST',
            values=('IAST', 'Devanagari', 'Harvard-Kyoto'),
            size_hint=(0.35, 1)
        )
        
        to_label = Label(
            text='To:',
            size_hint=(0.15, 1)
        )
        
        self.to_scheme = Spinner(
            text='Devanagari',
            values=('IAST', 'Devanagari', 'Harvard-Kyoto'),
            size_hint=(0.35, 1)
        )
        
        schemes_layout.add_widget(from_label)
        schemes_layout.add_widget(self.from_scheme)
        schemes_layout.add_widget(to_label)
        schemes_layout.add_widget(self.to_scheme)
        
        input_section.add_widget(input_header)
        input_section.add_widget(self.transliterate_input)
        input_section.add_widget(schemes_layout)
        
        # Transliterate button
        transliterate_button = Button(
            text='Transliterate',
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5}
        )
        transliterate_button.bind(on_press=self._on_transliterate)
        
        # Result section
        result_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        result_header = Label(
            text='Result:',
            size_hint=(1, 0.2),
            halign='left'
        )
        result_header.bind(size=result_header.setter('text_size'))
        
        # Result display
        self.transliterate_result = TextInput(
            readonly=True,
            size_hint=(1, 0.8)
        )
        
        result_section.add_widget(result_header)
        result_section.add_widget(self.transliterate_result)
        
        # Add sections to tab
        tab.add_widget(explanation)
        tab.add_widget(input_section)
        tab.add_widget(transliterate_button)
        tab.add_widget(result_section)
        
        return tab
    
    def _create_tokenize_tab(self):
        """Create the tokenize tab content."""
        tab = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # Explanation
        explanation = Label(
            text='Break Sanskrit text into words and morphemes',
            size_hint=(1, 0.1),
            halign='left',
            valign='top'
        )
        explanation.bind(size=explanation.setter('text_size'))
        
        # Input section
        input_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        input_header = Label(
            text='Input Text:',
            size_hint=(1, 0.2),
            halign='left'
        )
        input_header.bind(size=input_header.setter('text_size'))
        
        # Text input
        self.tokenize_input = TextInput(
            hint_text='Enter Sanskrit text to tokenize',
            size_hint=(1, 0.8),
            multiline=True
        )
        
        input_section.add_widget(input_header)
        input_section.add_widget(self.tokenize_input)
        
        # Tokenize button
        tokenize_button = Button(
            text='Tokenize',
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5}
        )
        tokenize_button.bind(on_press=self._on_tokenize)
        
        # Result section
        result_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        result_header = Label(
            text='Tokens:',
            size_hint=(1, 0.2),
            halign='left'
        )
        result_header.bind(size=result_header.setter('text_size'))
        
        # Result display
        self.tokenize_result = TextInput(
            readonly=True,
            size_hint=(1, 0.8)
        )
        
        result_section.add_widget(result_header)
        result_section.add_widget(self.tokenize_result)
        
        # Add sections to tab
        tab.add_widget(explanation)
        tab.add_widget(input_section)
        tab.add_widget(tokenize_button)
        tab.add_widget(result_section)
        
        return tab
    
    def _create_sandhi_tab(self):
        """Create the sandhi analysis tab content."""
        tab = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # Explanation
        explanation = Label(
            text='Analyze sandhi (phonological fusion) in Sanskrit text',
            size_hint=(1, 0.1),
            halign='left',
            valign='top'
        )
        explanation.bind(size=explanation.setter('text_size'))
        
        # Input section
        input_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        input_header = Label(
            text='Input Text:',
            size_hint=(1, 0.2),
            halign='left'
        )
        input_header.bind(size=input_header.setter('text_size'))
        
        # Text input
        self.sandhi_input = TextInput(
            hint_text='Enter Sanskrit text to analyze sandhi',
            size_hint=(1, 0.8),
            multiline=True
        )
        
        input_section.add_widget(input_header)
        input_section.add_widget(self.sandhi_input)
        
        # Analyze button
        analyze_button = Button(
            text='Analyze Sandhi',
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5}
        )
        analyze_button.bind(on_press=self._on_analyze_sandhi)
        
        # Result section
        result_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=dp(5)
        )
        
        result_header = Label(
            text='Sandhi Analysis:',
            size_hint=(1, 0.2),
            halign='left'
        )
        result_header.bind(size=result_header.setter('text_size'))
        
        # Result display in a scrollview
        result_scroll = ScrollView(
            size_hint=(1, 0.8)
        )
        
        self.sandhi_result = TextInput(
            readonly=True,
            size_hint=(1, None)
        )
        self.sandhi_result.bind(minimum_height=self.sandhi_result.setter('height'))
        
        result_scroll.add_widget(self.sandhi_result)
        result_section.add_widget(result_header)
        result_section.add_widget(result_scroll)
        
        # Add sections to tab
        tab.add_widget(explanation)
        tab.add_widget(input_section)
        tab.add_widget(analyze_button)
        tab.add_widget(result_section)
        
        return tab
    
    def _create_learn_tab(self):
        """Create the learn grammar rules tab content."""
        tab = BoxLayout(
            orientation='vertical',
            spacing=dp(10)
        )
        
        # Explanation
        explanation = Label(
            text='Teach the system new Sanskrit grammar rules',
            size_hint=(1, 0.1),
            halign='left',
            valign='top'
        )
        explanation.bind(size=explanation.setter('text_size'))
        
        # Input section
        input_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.4),
            spacing=dp(5)
        )
        
        input_header = Label(
            text='Rule Description:',
            size_hint=(1, 0.2),
            halign='left'
        )
        input_header.bind(size=input_header.setter('text_size'))
        
        # Text input
        self.learn_input = TextInput(
            hint_text='Describe a Sanskrit grammar rule (e.g., "When a ends with a and b starts with i, a+b becomes ai")',
            size_hint=(1, 0.8),
            multiline=True
        )
        
        input_section.add_widget(input_header)
        input_section.add_widget(self.learn_input)
        
        # Learn button
        learn_button = Button(
            text='Add Rule',
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5}
        )
        learn_button.bind(on_press=self._on_learn_rule)
        
        # Existing rules section
        rules_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            spacing=dp(5)
        )
        
        rules_header = Label(
            text='Existing Rules:',
            size_hint=(1, 0.2),
            halign='left'
        )
        rules_header.bind(size=rules_header.setter('text_size'))
        
        # Rules display in a scrollview
        rules_scroll = ScrollView(
            size_hint=(1, 0.8)
        )
        
        self.rules_display = TextInput(
            readonly=True,
            size_hint=(1, None)
        )
        self.rules_display.bind(minimum_height=self.rules_display.setter('height'))
        
        rules_scroll.add_widget(self.rules_display)
        rules_section.add_widget(rules_header)
        rules_section.add_widget(rules_scroll)
        
        # Add sections to tab
        tab.add_widget(explanation)
        tab.add_widget(input_section)
        tab.add_widget(learn_button)
        tab.add_widget(rules_section)
        
        # Load existing rules when tab is created
        self._load_existing_rules()
        
        return tab
    
    def _on_back_pressed(self, instance):
        """Handle back button press."""
        app = App.get_running_app()
        app.navigate_to('home')
    
    def _on_transliterate(self, instance):
        """Handle transliterate button press."""
        app = App.get_running_app()
        
        text = self.transliterate_input.text.strip()
        if not text:
            app.notification_manager.warning("Please enter text to transliterate")
            return
        
        # Get selected schemes
        from_scheme = self.from_scheme.text.lower()
        to_scheme = self.to_scheme.text.lower()
        
        # Convert scheme names to match SanskritNLP implementation
        scheme_map = {
            'iast': 'iast',
            'devanagari': 'devanagari',
            'harvard-kyoto': 'hk'
        }
        
        from_scheme = scheme_map.get(from_scheme, 'iast')
        to_scheme = scheme_map.get(to_scheme, 'devanagari')
        
        # Perform transliteration
        result = app.sanskrit_nlp.transliterate(text, from_scheme, to_scheme)
        
        if result['success']:
            self.transliterate_result.text = result['text']
        else:
            app.notification_manager.error(f"Transliteration failed: {result.get('error', 'Unknown error')}")
    
    def _on_tokenize(self, instance):
        """Handle tokenize button press."""
        app = App.get_running_app()
        
        text = self.tokenize_input.text.strip()
        if not text:
            app.notification_manager.warning("Please enter text to tokenize")
            return
        
        # Perform tokenization
        result = app.sanskrit_nlp.tokenize(text)
        
        if result['success']:
            # Format tokens for display
            tokens = result['tokens']
            self.tokenize_result.text = '\n'.join([f"{i+1}. {token}" for i, token in enumerate(tokens)])
        else:
            app.notification_manager.error(f"Tokenization failed: {result.get('error', 'Unknown error')}")
    
    def _on_analyze_sandhi(self, instance):
        """Handle analyze sandhi button press."""
        app = App.get_running_app()
        
        text = self.sandhi_input.text.strip()
        if not text:
            app.notification_manager.warning("Please enter text to analyze")
            return
        
        # Perform sandhi analysis
        result = app.sanskrit_nlp.analyze_sandhi(text)
        
        if result['success']:
            # Format analysis for display
            analysis = result['analysis']
            if analysis:
                display_text = []
                for i, item in enumerate(analysis):
                    display_text.append(f"Sandhi {i+1}:")
                    display_text.append(f"  Word 1: {item.get('word1', '')}")
                    display_text.append(f"  Word 2: {item.get('word2', '')}")
                    display_text.append(f"  Combined: {item.get('combined', '')}")
                    display_text.append(f"  Type: {item.get('type', '')}")
                    display_text.append("")
                
                self.sandhi_result.text = '\n'.join(display_text)
            else:
                self.sandhi_result.text = "No sandhi combinations detected in the text."
        else:
            app.notification_manager.error(f"Sandhi analysis failed: {result.get('error', 'Unknown error')}")
    
    def _on_learn_rule(self, instance):
        """Handle learn rule button press."""
        app = App.get_running_app()
        
        instruction = self.learn_input.text.strip()
        if not instruction:
            app.notification_manager.warning("Please enter a rule description")
            return
        
        # Add the rule
        result = app.sanskrit_nlp.learn_grammar_rule(instruction)
        
        if result['success']:
            app.notification_manager.success("Grammar rule added successfully")
            self.learn_input.text = ""  # Clear input
            
            # Reload rules
            self._load_existing_rules()
        else:
            app.notification_manager.error(f"Failed to add rule: {result.get('error', 'Unknown error')}")
    
    def _load_existing_rules(self):
        """Load and display existing grammar rules."""
        app = App.get_running_app()
        
        # Get existing rules
        rules = app.sanskrit_nlp.get_grammar_rules()
        
        if rules:
            display_text = []
            for rule in rules:
                display_text.append(f"Rule {rule.get('id', '')}:")
                display_text.append(f"  Description: {rule.get('description', '')}")
                if 'pattern' in rule and 'replacement' in rule:
                    display_text.append(f"  Pattern: {rule.get('pattern', '')}")
                    display_text.append(f"  Replacement: {rule.get('replacement', '')}")
                display_text.append(f"  Created: {rule.get('created_at', '')}")
                display_text.append("")
            
            self.rules_display.text = '\n'.join(display_text)
        else:
            self.rules_display.text = "No grammar rules have been added yet."