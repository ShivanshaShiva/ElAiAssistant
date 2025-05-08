"""
Memory Widget Module.
This module contains the widget that displays detailed memory information.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.properties import ObjectProperty

from utils import format_bytes


class MemoryWidget(TabbedPanelItem):
    """Widget that displays detailed memory information."""
    
    def __init__(self, monitor, storage, **kwargs):
        super(MemoryWidget, self).__init__(**kwargs)
        self.text = 'Memory'
        self.monitor = monitor
        self.storage = storage
        self.content = MemoryContent(monitor=monitor, storage=storage)


class MemoryContent(BoxLayout):
    """Content for the memory tab."""
    
    monitor = ObjectProperty(None)
    storage = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(MemoryContent, self).__init__(**kwargs)
        self.memory_history = []
        
        # Initialize the display with current data
        self.update_display()
    
    def update_display(self):
        """Update the memory usage display."""
        # Get memory data
        memory_data = self.monitor.get_memory_data()
        memory_percent = memory_data['percent']
        memory_used = memory_data['used']
        memory_available = memory_data['available']
        memory_total = memory_data['total']
        
        # Update the memory usage labels
        self.ids.memory_percent.text = f"{memory_percent:.1f}%"
        self.ids.memory_used.text = f"Used: {format_bytes(memory_used)}"
        self.ids.memory_available.text = f"Available: {format_bytes(memory_available)}"
        self.ids.memory_total.text = f"Total: {format_bytes(memory_total)}"
        
        # Update the memory pie chart
        self._update_pie_chart(memory_used, memory_available)
        
        # Update the memory history graph
        self._update_history_graph()
    
    def _update_pie_chart(self, used, available):
        """Update the memory usage pie chart."""
        with self.ids.memory_pie_chart.canvas:
            self.ids.memory_pie_chart.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.memory_pie_chart.pos, size=self.ids.memory_pie_chart.size)
            
            # Calculate the center and radius for the pie chart
            cx = self.ids.memory_pie_chart.center_x
            cy = self.ids.memory_pie_chart.center_y
            radius = min(self.ids.memory_pie_chart.width, self.ids.memory_pie_chart.height) * 0.4
            
            # Calculate the angle for the used portion
            total = used + available
            used_angle = 360 * (used / total) if total > 0 else 0
            
            # Draw the available portion (green)
            Color(0.2, 0.7, 0.2)
            Ellipse(pos=(cx - radius, cy - radius), size=(radius * 2, radius * 2))
            
            # Draw the used portion (red)
            Color(0.7, 0.2, 0.2)
            Ellipse(pos=(cx - radius, cy - radius), size=(radius * 2, radius * 2), 
                  angle_start=0, angle_end=used_angle)
            
            # Draw a white circle in the center to create a donut chart
            Color(0.2, 0.2, 0.2)
            inner_radius = radius * 0.7
            Ellipse(pos=(cx - inner_radius, cy - inner_radius), 
                  size=(inner_radius * 2, inner_radius * 2))
            
            # Add text labels
            Color(1, 1, 1)
            # We would add text here, but we're already using labels in the UI
    
    def _update_history_graph(self):
        """Update the memory usage history graph."""
        # Get memory history data from storage
        memory_history_data = self.storage.get_history('memory_percent', hours=1, limit=120)
        
        # Extract only the values (not timestamps)
        self.memory_history = [value for _, value in memory_history_data]
        
        # Draw the memory history graph
        with self.ids.memory_history_graph.canvas:
            self.ids.memory_history_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.memory_history_graph.pos, size=self.ids.memory_history_graph.size)
            
            # Draw horizontal grid lines (at 25%, 50%, 75%)
            Color(0.3, 0.3, 0.3)
            for percent in [25, 50, 75]:
                y = self.ids.memory_history_graph.y + (percent / 100.0) * self.ids.memory_history_graph.height
                Line(points=[self.ids.memory_history_graph.x, y, 
                            self.ids.memory_history_graph.x + self.ids.memory_history_graph.width, y], 
                    width=1)
            
            # Draw the memory history line
            if self.memory_history:
                Color(0.2, 0.2, 0.7)
                
                points = []
                w = self.ids.memory_history_graph.width
                h = self.ids.memory_history_graph.height
                x_step = w / (len(self.memory_history) - 1) if len(self.memory_history) > 1 else w
                
                for i, value in enumerate(self.memory_history):
                    x = self.ids.memory_history_graph.x + i * x_step
                    y = self.ids.memory_history_graph.y + (value / 100.0) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
