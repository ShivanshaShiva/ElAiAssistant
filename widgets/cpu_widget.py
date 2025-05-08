"""
CPU Widget Module.
This module contains the widget that displays detailed CPU information.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty


class CPUWidget(TabbedPanelItem):
    """Widget that displays detailed CPU information."""
    
    def __init__(self, monitor, storage, **kwargs):
        super(CPUWidget, self).__init__(**kwargs)
        self.text = 'CPU'
        self.monitor = monitor
        self.storage = storage
        self.content = CPUContent(monitor=monitor, storage=storage)


class CPUContent(BoxLayout):
    """Content for the CPU tab."""
    
    monitor = ObjectProperty(None)
    storage = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(CPUContent, self).__init__(**kwargs)
        self.cpu_history = []
        self.per_cpu_bars = []
        
        # Initialize with the current CPU count
        cpu_data = self.monitor.get_cpu_data()
        self.cpu_count = cpu_data['count']
        self.physical_count = cpu_data['physical_count']
        
        # Create progress bars for each CPU core
        self._create_per_cpu_bars()
        
        # Initialize the display with current data
        self.update_display()
    
    def _create_per_cpu_bars(self):
        """Create the UI components for each CPU core."""
        self.ids.per_cpu_layout.clear_widgets()
        self.per_cpu_bars = []
        
        for i in range(self.cpu_count):
            # Create a layout for this core
            core_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=30,
                spacing=10
            )
            
            # Create a label for the core number
            core_label = Label(
                text=f"Core {i}:",
                size_hint_x=0.15,
                halign='right',
                valign='middle',
                text_size=(None, None)
            )
            
            # Create a progress bar
            progress_bar = ProgressBar(
                max=100,
                value=0,
                size_hint_x=0.7
            )
            
            # Create a label for the percentage
            percent_label = Label(
                text="0%",
                size_hint_x=0.15,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            
            # Add the widgets to the layout
            core_layout.add_widget(core_label)
            core_layout.add_widget(progress_bar)
            core_layout.add_widget(percent_label)
            
            # Add the layout to the per_cpu_layout
            self.ids.per_cpu_layout.add_widget(core_layout)
            
            # Store a reference to the progress bar and percentage label
            self.per_cpu_bars.append((progress_bar, percent_label))
    
    def update_display(self):
        """Update the CPU usage display."""
        # Get CPU data
        cpu_data = self.monitor.get_cpu_data()
        cpu_percent = cpu_data['percent']
        per_cpu = cpu_data['per_cpu']
        
        # If the CPU count has changed, recreate the per-CPU bars
        if len(per_cpu) != self.cpu_count:
            self.cpu_count = len(per_cpu)
            self._create_per_cpu_bars()
        
        # Update the overall CPU usage
        self.ids.cpu_percent.text = f"Total: {cpu_percent:.1f}%"
        self.ids.cpu_count.text = f"Cores: {self.cpu_count} ({self.physical_count} physical)"
        
        # Update each CPU core's progress bar
        for i, (progress_bar, percent_label) in enumerate(self.per_cpu_bars):
            if i < len(per_cpu):
                progress_bar.value = per_cpu[i]
                percent_label.text = f"{per_cpu[i]:.1f}%"
        
        # Update the CPU history graph
        self._update_history_graph()
    
    def _update_history_graph(self):
        """Update the CPU usage history graph."""
        # Get CPU history data from storage
        cpu_history_data = self.storage.get_history('cpu_percent', hours=1, limit=120)
        
        # Extract only the values (not timestamps)
        self.cpu_history = [value for _, value in cpu_history_data]
        
        # Draw the CPU history graph
        with self.ids.cpu_history_graph.canvas:
            self.ids.cpu_history_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.cpu_history_graph.pos, size=self.ids.cpu_history_graph.size)
            
            # Draw horizontal grid lines (at 25%, 50%, 75%)
            Color(0.3, 0.3, 0.3)
            for percent in [25, 50, 75]:
                y = self.ids.cpu_history_graph.y + (percent / 100.0) * self.ids.cpu_history_graph.height
                Line(points=[self.ids.cpu_history_graph.x, y, 
                            self.ids.cpu_history_graph.x + self.ids.cpu_history_graph.width, y], 
                    width=1)
            
            # Draw the CPU history line
            if self.cpu_history:
                Color(0.2, 0.7, 0.2)
                
                points = []
                w = self.ids.cpu_history_graph.width
                h = self.ids.cpu_history_graph.height
                x_step = w / (len(self.cpu_history) - 1) if len(self.cpu_history) > 1 else w
                
                for i, value in enumerate(self.cpu_history):
                    x = self.ids.cpu_history_graph.x + i * x_step
                    y = self.ids.cpu_history_graph.y + (value / 100.0) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
