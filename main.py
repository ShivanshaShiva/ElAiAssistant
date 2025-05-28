"""
Main application entry point for the System Resource Monitor.
This file initializes the Kivy application and sets up the main UI.
"""

import os
import kivy
kivy.require('2.1.0')  # Replace with your actual Kivy version

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config

# Import our custom widgets
from widgets.dashboard import DashboardWidget
from widgets.cpu_widget import CPUWidget
from widgets.memory_widget import MemoryWidget
from widgets.disk_widget import DiskWidget
from widgets.network_widget import NetworkWidget
from widgets.system_info_widget import SystemInfoWidget
from widgets.history_widget import HistoryWidget

# Import monitor and storage modules
from system_monitor import SystemMonitor
from data_storage import DataStorage

# Set app to be resizable and set initial size
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class MainTabbedPanel(TabbedPanel):
    """Main tabbed panel that contains all the different monitoring views."""
    
    def __init__(self, monitor, storage, **kwargs):
        super(MainTabbedPanel, self).__init__(**kwargs)
        self.monitor = monitor
        self.storage = storage
        
        # Set tabbed panel properties
        self.do_default_tab = False
        self.tab_pos = 'top_mid'
        self.tab_width = 150
        
        # Add the dashboard tab (overview of all metrics)
        dashboard = DashboardWidget(monitor=self.monitor, storage=self.storage)
        self.add_widget(dashboard)
        
        # Add individual monitoring tabs
        self.add_widget(CPUWidget(monitor=self.monitor, storage=self.storage))
        self.add_widget(MemoryWidget(monitor=self.monitor, storage=self.storage))
        self.add_widget(DiskWidget(monitor=self.monitor, storage=self.storage))
        self.add_widget(NetworkWidget(monitor=self.monitor, storage=self.storage))
        self.add_widget(SystemInfoWidget(monitor=self.monitor))
        self.add_widget(HistoryWidget(storage=self.storage))


class SystemMonitorApp(App):
    """Main application class for the System Resource Monitor."""
    
    def build(self):
        """Build the application UI."""
        # Initialize the system monitor and data storage
        self.monitor = SystemMonitor()
        self.storage = DataStorage()
        
        # Create the root layout
        root = BoxLayout(orientation='vertical')
        
        # Add a title bar
        title_bar = BoxLayout(
            size_hint=(1, 0.1),
            padding=[10, 5],
            orientation='horizontal'
        )
        title_bar.add_widget(Label(
            text='System Resource Monitor',
            font_size='20sp',
            halign='left',
            valign='middle',
            size_hint=(0.7, 1)
        ))
        launch_button = Button(text='ElAiAssitant', size_hint=(0.3, 1), on_press=self.launch_ElAiAss)
        title_bar.add_widget(launch_button)
        
        # Create the main tabbed panel
        self.tabbed_panel = MainTabbedPanel(
            monitor=self.monitor,
            storage=self.storage,
            size_hint=(1, 0.9)
        )
        
        # Add widgets to the root layout
        root.add_widget(title_bar)
        root.add_widget(self.tabbed_panel)
        
        # Schedule periodic updates (every second)
        Clock.schedule_interval(self.update_data, 1)
        
        return root
    
    def update_data(self, dt):
        """Update the system data periodically."""
        # Collect new data
        self.monitor.update()
        # Store the data for historical tracking
        self.storage.store_data(self.monitor.get_all_data())
        # Trigger UI updates
        for tab in self.tabbed_panel.tab_list:
            if hasattr(tab.content, 'update_display'):
                tab.content.update_display()
    
    def launch_ElAiAss(self, *args):
        from kivy_app.main import ElAiApp
        self.stop()
        ElAiApp().run()

    def on_stop(self):
        self.storage.close()


def launch_system_monitor():
    # Run the application
    SystemMonitorApp().run()
