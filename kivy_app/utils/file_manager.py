"""
File Manager Module.
This module handles file selection and management operations.
"""

import os
import shutil
import tempfile
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.logger import Logger

class FileSelector(BoxLayout):
    """A file selector widget with file browser and action buttons."""
    
    def __init__(self, title="Select a file", filters=None, start_dir=None, 
                 on_selection=None, on_cancel=None, **kwargs):
        """
        Initialize the file selector.
        
        Args:
            title (str): Title for the file selector popup
            filters (list): List of file filters (e.g., ['*.txt', '*.py'])
            start_dir (str): Starting directory path
            on_selection (callable): Callback when file is selected
            on_cancel (callable): Callback when selection is cancelled
        """
        super(FileSelector, self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        
        # Set properties
        self.title = title
        self.on_selection = on_selection
        self.on_cancel = on_cancel
        
        # Get start directory
        if not start_dir or not os.path.exists(start_dir):
            start_dir = os.path.expanduser('~')
        
        # Create file chooser
        self.file_chooser = FileChooserListView(
            path=start_dir,
            filters=filters,
            dirselect=False
        )
        
        # Create buttons
        button_layout = BoxLayout(
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )
        
        self.cancel_button = Button(
            text='Cancel',
            size_hint=(0.5, 1)
        )
        
        self.select_button = Button(
            text='Select',
            size_hint=(0.5, 1),
            disabled=True
        )
        
        # Bind events
        self.file_chooser.bind(selection=self._on_file_chooser_selection)
        self.cancel_button.bind(on_press=self._on_cancel)
        self.select_button.bind(on_press=self._on_select)
        
        # Add widgets
        button_layout.add_widget(self.cancel_button)
        button_layout.add_widget(self.select_button)
        
        self.add_widget(self.file_chooser)
        self.add_widget(button_layout)
    
    def _on_file_chooser_selection(self, instance, selection):
        """Handle file selection change."""
        self.select_button.disabled = not bool(selection)
    
    def _on_cancel(self, instance):
        """Handle cancel button press."""
        if self.on_cancel:
            self.on_cancel()
    
    def _on_select(self, instance):
        """Handle select button press."""
        selection = self.file_chooser.selection
        if selection and self.on_selection:
            self.on_selection(selection[0])


class FileManager:
    """Manages file operations and selection dialogs."""
    
    def __init__(self):
        """Initialize the file manager."""
        self.temp_dir = tempfile.mkdtemp(prefix='elai_')
        Logger.info(f"FileManager: Created temp directory at {self.temp_dir}")
    
    def select_file(self, title="Select a file", filters=None, start_dir=None, 
                    on_selection=None, on_cancel=None):
        """
        Show a file selection dialog.
        
        Args:
            title (str): Title for the file selector popup
            filters (list): List of file filters (e.g., ['*.txt', '*.py'])
            start_dir (str): Starting directory path
            on_selection (callable): Callback when file is selected
            on_cancel (callable): Callback when selection is cancelled
        """
        content = FileSelector(
            title=title,
            filters=filters,
            start_dir=start_dir,
            on_selection=self._on_file_selected,
            on_cancel=self._on_selection_cancel
        )
        
        # Store callbacks
        self._on_file_selected_callback = on_selection
        self._on_selection_cancel_callback = on_cancel
        
        # Create popup
        self.popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        # Show popup
        self.popup.open()
    
    def _on_file_selected(self, file_path):
        """Handle file selection from popup."""
        Logger.info(f"FileManager: Selected file {file_path}")
        
        # Dismiss popup
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
            self.popup = None
        
        # Call user callback
        if hasattr(self, '_on_file_selected_callback') and self._on_file_selected_callback:
            self._on_file_selected_callback(file_path)
    
    def _on_selection_cancel(self):
        """Handle selection cancellation."""
        Logger.info("FileManager: File selection cancelled")
        
        # Dismiss popup
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
            self.popup = None
        
        # Call user callback
        if hasattr(self, '_on_selection_cancel_callback') and self._on_selection_cancel_callback:
            self._on_selection_cancel_callback()
    
    def create_temp_file(self, content="", prefix="file_", suffix=".txt"):
        """
        Create a temporary file with the given content.
        
        Args:
            content (str): Content to write to the file
            prefix (str): Prefix for the temporary file name
            suffix (str): Suffix (extension) for the temporary file name
            
        Returns:
            str: Path to the created temporary file
        """
        try:
            # Create a temporary file
            fd, temp_file_path = tempfile.mkstemp(
                suffix=suffix,
                prefix=prefix,
                dir=self.temp_dir,
                text=True
            )
            
            # Write content
            with os.fdopen(fd, 'w') as f:
                f.write(content)
            
            Logger.info(f"FileManager: Created temp file at {temp_file_path}")
            return temp_file_path
        
        except Exception as e:
            Logger.error(f"FileManager: Error creating temp file: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files and directory."""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                Logger.info(f"FileManager: Removed temp directory {self.temp_dir}")
        except Exception as e:
            Logger.error(f"FileManager: Error cleaning up temp directory: {e}")
    
    def get_file_extension(self, file_path):
        """
        Get the extension of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: File extension (with leading dot) or empty string
        """
        return os.path.splitext(file_path)[1]
    
    def copy_file(self, source_path, destination_path):
        """
        Copy a file from source to destination.
        
        Args:
            source_path (str): Path to the source file
            destination_path (str): Path to the destination
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            shutil.copy2(source_path, destination_path)
            Logger.info(f"FileManager: Copied {source_path} to {destination_path}")
            return True
        except Exception as e:
            Logger.error(f"FileManager: Error copying file: {e}")
            return False
    
    def read_file(self, file_path):
        """
        Read the content of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: File content or None if error
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            Logger.error(f"FileManager: Error reading file {file_path}: {e}")
            return None
    
    def write_file(self, file_path, content):
        """
        Write content to a file.
        
        Args:
            file_path (str): Path to the file
            content (str): Content to write
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            dir_path = os.path.dirname(file_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path)
            
            # Write content
            with open(file_path, 'w') as f:
                f.write(content)
            
            Logger.info(f"FileManager: Wrote content to {file_path}")
            return True
        except Exception as e:
            Logger.error(f"FileManager: Error writing to file {file_path}: {e}")
            return False