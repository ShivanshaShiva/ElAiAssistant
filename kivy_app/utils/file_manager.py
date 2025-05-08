"""
File Manager Module.
This module is responsible for handling file operations such as opening, saving, and browsing files.
"""

import os
import tempfile
import shutil
from datetime import datetime
from typing import Callable, List, Optional, Union

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.logger import Logger


class FileManager:
    """Manages file operations for the application."""
    
    def __init__(self):
        """Initialize the file manager."""
        self.default_dir = self._get_default_directory()
        self.temp_dir = self._get_temp_directory()
        
        # Create temp directory if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)
    
    def _get_default_directory(self) -> str:
        """
        Get the default directory for file operations.
        
        Returns:
            str: Path to the default directory
        """
        # Try to use Downloads directory if on Android
        try:
            from android.storage import primary_external_storage_path
            downloads_dir = os.path.join(primary_external_storage_path(), 'Download')
            if os.path.exists(downloads_dir):
                return downloads_dir
        except (ImportError, Exception):
            pass
        
        # Fallback to the app's directory for non-Android platforms
        return os.path.dirname(os.path.abspath(__file__))
    
    def _get_temp_directory(self) -> str:
        """
        Get the temporary directory for file operations.
        
        Returns:
            str: Path to the temp directory
        """
        try:
            # Try to use app-specific directory on Android
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'temp')
        except (ImportError, Exception):
            # Fallback to system temp directory for non-Android platforms
            return os.path.join(tempfile.gettempdir(), 'elai_assistant')
    
    def select_file(self, 
                   title: str = "Select File", 
                   filters: List[str] = None, 
                   initial_path: str = None,
                   on_selection: Callable[[Optional[str]], None] = None,
                   mode: str = 'open') -> None:
        """
        Open a file selection dialog.
        
        Args:
            title (str): Title of the dialog
            filters (List[str]): List of file extensions to filter (e.g., ['*.txt', '*.py'])
            initial_path (str): Initial directory to open
            on_selection (Callable): Callback function to call with selected file path
            mode (str): 'open' or 'save'
        """
        if not initial_path:
            initial_path = self.default_dir
        
        # Create file chooser dialog
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        file_chooser = FileChooserListView(
            path=initial_path,
            filters=filters,
            dirselect=(mode == 'dir')
        )
        
        buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        cancel_btn = Button(text='Cancel')
        select_btn = Button(text='Select' if mode == 'open' else 'Save')
        
        # Bind events
        file_chooser.bind(on_submit=lambda instance, selection, touch: self._on_file_selected(selection[0], on_selection) if selection else None)
        cancel_btn.bind(on_release=lambda instance: popup.dismiss())
        select_btn.bind(on_release=lambda instance: self._on_file_selected(file_chooser.selection[0], on_selection, popup) if file_chooser.selection else None)
        
        buttons.add_widget(cancel_btn)
        buttons.add_widget(select_btn)
        
        content.add_widget(Label(text=title, size_hint_y=None, height=dp(30)))
        content.add_widget(file_chooser)
        content.add_widget(buttons)
        
        # Create and open popup
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    def _on_file_selected(self, path: str, callback: Callable[[str], None], popup: Popup = None) -> None:
        """
        Handle file selection.
        
        Args:
            path (str): Selected file path
            callback (Callable): Callback function to call with selected file path
            popup (Popup): Popup to dismiss
        """
        if popup:
            popup.dismiss()
        
        if callback:
            callback(path)
    
    def create_temp_file(self, content: str, prefix: str = "temp_", suffix: str = ".txt") -> Optional[str]:
        """
        Create a temporary file with the given content.
        
        Args:
            content (str): Content to write to the file
            prefix (str): Prefix for the temp filename
            suffix (str): Suffix for the temp filename (file extension)
            
        Returns:
            str: Path to the created temporary file or None if failed
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{prefix}{timestamp}{suffix}"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Write content to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return filepath
        except Exception as e:
            Logger.error(f"FileManager: Failed to create temp file: {e}")
            return None
    
    def read_file(self, filepath: str) -> Optional[str]:
        """
        Read and return the content of a file.
        
        Args:
            filepath (str): Path to the file to read
            
        Returns:
            str: Content of the file or None if failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            Logger.error(f"FileManager: Failed to read file {filepath}: {e}")
            return None
    
    def save_file(self, filepath: str, content: str) -> bool:
        """
        Save content to a file.
        
        Args:
            filepath (str): Path to save the file
            content (str): Content to write to the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                
            # Write content to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return True
        except Exception as e:
            Logger.error(f"FileManager: Failed to save file {filepath}: {e}")
            return False
    
    def list_directory(self, dirpath: str, filter_pattern: str = None) -> List[str]:
        """
        List files in a directory, optionally filtered by a pattern.
        
        Args:
            dirpath (str): Directory path to list
            filter_pattern (str): Optional glob pattern to filter files
            
        Returns:
            List[str]: List of file paths in the directory
        """
        try:
            import glob
            
            if filter_pattern:
                return glob.glob(os.path.join(dirpath, filter_pattern))
            else:
                return [os.path.join(dirpath, f) for f in os.listdir(dirpath) 
                        if not f.startswith('.')]  # Skip hidden files
        except Exception as e:
            Logger.error(f"FileManager: Failed to list directory {dirpath}: {e}")
            return []
    
    def delete_file(self, filepath: str) -> bool:
        """
        Delete a file.
        
        Args:
            filepath (str): Path to the file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(filepath):
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                else:
                    os.remove(filepath)
                return True
            return False
        except Exception as e:
            Logger.error(f"FileManager: Failed to delete file {filepath}: {e}")
            return False
    
    def get_documents_dir(self) -> str:
        """
        Get the documents directory on the device.
        
        Returns:
            str: Path to the documents directory
        """
        try:
            # Try to use Android-specific storage
            from android.storage import primary_external_storage_path
            return os.path.join(primary_external_storage_path(), 'Documents')
        except (ImportError, Exception):
            # Fallback for non-Android platforms
            return os.path.expanduser("~/Documents")
    
    def get_downloads_dir(self) -> str:
        """
        Get the downloads directory on the device.
        
        Returns:
            str: Path to the downloads directory
        """
        try:
            # Try to use Android-specific storage
            from android.storage import primary_external_storage_path
            return os.path.join(primary_external_storage_path(), 'Download')
        except (ImportError, Exception):
            # Fallback for non-Android platforms
            return os.path.expanduser("~/Downloads")
    
    def get_app_dir(self) -> str:
        """
        Get the application's storage directory.
        
        Returns:
            str: Path to the app's storage directory
        """
        try:
            # Try to use Android-specific app storage
            from android.storage import app_storage_path
            return app_storage_path()
        except (ImportError, Exception):
            # Fallback for non-Android platforms
            app = App.get_running_app()
            if app:
                return app.user_data_dir
            return os.path.dirname(os.path.abspath(__file__))
    
    def clean_temp_files(self, days_old: int = 7) -> int:
        """
        Clean temporary files older than the specified number of days.
        
        Args:
            days_old (int): Files older than this many days will be deleted
            
        Returns:
            int: Number of files deleted
        """
        import time
        from datetime import datetime, timedelta
        
        cutoff_time = time.time() - (days_old * 86400)  # 86400 seconds in a day
        count = 0
        
        try:
            if os.path.exists(self.temp_dir):
                for filename in os.listdir(self.temp_dir):
                    filepath = os.path.join(self.temp_dir, filename)
                    if os.path.isfile(filepath):
                        mtime = os.path.getmtime(filepath)
                        if mtime < cutoff_time:
                            os.remove(filepath)
                            count += 1
            
            return count
        except Exception as e:
            Logger.error(f"FileManager: Failed to clean temp files: {e}")
            return 0