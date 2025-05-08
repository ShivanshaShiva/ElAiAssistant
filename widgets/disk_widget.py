"""
Disk Widget Module.
This module contains the widget that displays detailed disk information.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty

from utils import format_bytes, format_bytes_speed


class DiskWidget(TabbedPanelItem):
    """Widget that displays detailed disk information."""
    
    def __init__(self, monitor, storage, **kwargs):
        super(DiskWidget, self).__init__(**kwargs)
        self.text = 'Disk'
        self.monitor = monitor
        self.storage = storage
        self.content = DiskContent(monitor=monitor, storage=storage)


class DiskContent(BoxLayout):
    """Content for the disk tab."""
    
    monitor = ObjectProperty(None)
    storage = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(DiskContent, self).__init__(**kwargs)
        self.disk_history = {'read': [], 'write': []}
        
        # Initialize the display with current data
        self.update_display()
    
    def update_display(self):
        """Update the disk usage display."""
        # Get disk data
        disk_data = self.monitor.get_disk_data()
        disk_percent = disk_data['percent']
        disk_used = disk_data['used']
        disk_free = disk_data['free']
        disk_total = disk_data['total']
        disk_read_bytes = disk_data['read_bytes']
        disk_write_bytes = disk_data['write_bytes']
        disk_read_count = disk_data['read_count']
        disk_write_count = disk_data['write_count']
        
        # Update the disk usage labels
        self.ids.disk_percent.text = f"{disk_percent:.1f}%"
        self.ids.disk_used.text = f"Used: {format_bytes(disk_used)}"
        self.ids.disk_free.text = f"Free: {format_bytes(disk_free)}"
        self.ids.disk_total.text = f"Total: {format_bytes(disk_total)}"
        
        # Update the disk I/O labels
        self.ids.disk_read_bytes.text = format_bytes_speed(disk_read_bytes)
        self.ids.disk_write_bytes.text = format_bytes_speed(disk_write_bytes)
        self.ids.disk_read_count.text = f"{disk_read_count:,}"
        self.ids.disk_write_count.text = f"{disk_write_count:,}"
        
        # Update the disk I/O history graph
        self._update_history_graph()
    
    def _update_history_graph(self):
        """Update the disk I/O history graph."""
        # Get disk I/O history data from storage
        read_history_data = self.storage.get_history('disk_read_bytes', hours=1, limit=120)
        write_history_data = self.storage.get_history('disk_write_bytes', hours=1, limit=120)
        
        # Extract only the values (not timestamps)
        self.disk_history['read'] = [value for _, value in read_history_data]
        self.disk_history['write'] = [value for _, value in write_history_data]
        
        # Make sure both lists have the same length
        min_length = min(len(self.disk_history['read']), len(self.disk_history['write']))
        self.disk_history['read'] = self.disk_history['read'][:min_length]
        self.disk_history['write'] = self.disk_history['write'][:min_length]
        
        # Draw the disk I/O history graph
        with self.ids.disk_history_graph.canvas:
            self.ids.disk_history_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.disk_history_graph.pos, size=self.ids.disk_history_graph.size)
            
            # Find max value for scaling
            max_value = 1.0  # Avoid division by zero
            for read_val in self.disk_history['read']:
                max_value = max(max_value, read_val)
            for write_val in self.disk_history['write']:
                max_value = max(max_value, write_val)
            
            # Draw horizontal grid lines
            Color(0.3, 0.3, 0.3)
            for i in range(1, 4):
                y = self.ids.disk_history_graph.y + (i / 4.0) * self.ids.disk_history_graph.height
                Line(points=[self.ids.disk_history_graph.x, y, 
                            self.ids.disk_history_graph.x + self.ids.disk_history_graph.width, y], 
                    width=1)
            
            # Draw the read history line (green)
            if self.disk_history['read']:
                Color(0.2, 0.7, 0.2)
                
                points = []
                w = self.ids.disk_history_graph.width
                h = self.ids.disk_history_graph.height
                x_step = w / (len(self.disk_history['read']) - 1) if len(self.disk_history['read']) > 1 else w
                
                for i, value in enumerate(self.disk_history['read']):
                    x = self.ids.disk_history_graph.x + i * x_step
                    y = self.ids.disk_history_graph.y + (value / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
            
            # Draw the write history line (red)
            if self.disk_history['write']:
                Color(0.7, 0.2, 0.2)
                
                points = []
                w = self.ids.disk_history_graph.width
                h = self.ids.disk_history_graph.height
                x_step = w / (len(self.disk_history['write']) - 1) if len(self.disk_history['write']) > 1 else w
                
                for i, value in enumerate(self.disk_history['write']):
                    x = self.ids.disk_history_graph.x + i * x_step
                    y = self.ids.disk_history_graph.y + (value / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
