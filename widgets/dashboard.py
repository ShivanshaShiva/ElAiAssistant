"""
Dashboard Widget Module.
This module contains the widget that displays an overview of all system resources.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty

from utils import format_bytes, format_bytes_speed


class DashboardWidget(TabbedPanelItem):
    """Widget that displays an overview of all system metrics."""
    
    def __init__(self, monitor, storage, **kwargs):
        super(DashboardWidget, self).__init__(**kwargs)
        self.text = 'Dashboard'
        self.monitor = monitor
        self.storage = storage
        self.content = DashboardContent(monitor=monitor, storage=storage)


class DashboardContent(BoxLayout):
    """Content for the dashboard tab."""
    
    monitor = ObjectProperty(None)
    storage = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(DashboardContent, self).__init__(**kwargs)
        self.cpu_history = []
        self.memory_history = []
        self.disk_history = []
        self.network_history = []
        
        # Initialize the dashboard with current data
        self.update_display()
    
    def update_display(self):
        """Update all displayed metrics."""
        self._update_cpu()
        self._update_memory()
        self._update_disk()
        self._update_network()
    
    def _update_cpu(self):
        """Update the CPU usage display."""
        # Get CPU data
        cpu_data = self.monitor.get_cpu_data()
        cpu_percent = cpu_data['percent']
        
        # Update the percentage label
        self.ids.cpu_percent.text = f"{cpu_percent:.1f}%"
        
        # Update the CPU graph
        self.cpu_history.append(cpu_percent)
        if len(self.cpu_history) > 60:  # Keep last 60 seconds
            self.cpu_history.pop(0)
        
        # Draw the CPU graph
        with self.ids.cpu_graph.canvas:
            self.ids.cpu_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.cpu_graph.pos, size=self.ids.cpu_graph.size)
            
            # Draw graph
            if self.cpu_history:
                Color(0.2, 0.7, 0.2)
                
                points = []
                w = self.ids.cpu_graph.width
                h = self.ids.cpu_graph.height
                x_step = w / (len(self.cpu_history) - 1) if len(self.cpu_history) > 1 else w
                
                for i, value in enumerate(self.cpu_history):
                    x = self.ids.cpu_graph.x + i * x_step
                    y = self.ids.cpu_graph.y + (value / 100.0) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
    
    def _update_memory(self):
        """Update the memory usage display."""
        # Get memory data
        memory_data = self.monitor.get_memory_data()
        memory_percent = memory_data['percent']
        
        # Update the percentage label
        self.ids.memory_percent.text = f"{memory_percent:.1f}%"
        
        # Update the memory graph
        self.memory_history.append(memory_percent)
        if len(self.memory_history) > 60:  # Keep last 60 seconds
            self.memory_history.pop(0)
        
        # Draw the memory graph
        with self.ids.memory_graph.canvas:
            self.ids.memory_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.memory_graph.pos, size=self.ids.memory_graph.size)
            
            # Draw graph
            if self.memory_history:
                Color(0.2, 0.2, 0.7)
                
                points = []
                w = self.ids.memory_graph.width
                h = self.ids.memory_graph.height
                x_step = w / (len(self.memory_history) - 1) if len(self.memory_history) > 1 else w
                
                for i, value in enumerate(self.memory_history):
                    x = self.ids.memory_graph.x + i * x_step
                    y = self.ids.memory_graph.y + (value / 100.0) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
    
    def _update_disk(self):
        """Update the disk usage display."""
        # Get disk data
        disk_data = self.monitor.get_disk_data()
        disk_percent = disk_data['percent']
        disk_read = disk_data['read_bytes']
        disk_write = disk_data['write_bytes']
        
        # Update the percentage and I/O labels
        self.ids.disk_percent.text = f"{disk_percent:.1f}%"
        self.ids.disk_io.text = f"Read: {format_bytes_speed(disk_read)} | Write: {format_bytes_speed(disk_write)}"
        
        # Update the disk graph (show disk I/O rather than usage percentage)
        self.disk_history.append((disk_read, disk_write))
        if len(self.disk_history) > 60:  # Keep last 60 seconds
            self.disk_history.pop(0)
        
        # Draw the disk graph
        with self.ids.disk_graph.canvas:
            self.ids.disk_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.disk_graph.pos, size=self.ids.disk_graph.size)
            
            # Find max value for scaling
            max_value = 1.0  # Avoid division by zero
            for read, write in self.disk_history:
                max_value = max(max_value, read, write)
            
            # Draw read graph
            if self.disk_history:
                # Read line (green)
                Color(0.2, 0.7, 0.2)
                
                points = []
                w = self.ids.disk_graph.width
                h = self.ids.disk_graph.height
                x_step = w / (len(self.disk_history) - 1) if len(self.disk_history) > 1 else w
                
                for i, (read, _) in enumerate(self.disk_history):
                    x = self.ids.disk_graph.x + i * x_step
                    y = self.ids.disk_graph.y + (read / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
                
                # Write line (red)
                Color(0.7, 0.2, 0.2)
                
                points = []
                for i, (_, write) in enumerate(self.disk_history):
                    x = self.ids.disk_graph.x + i * x_step
                    y = self.ids.disk_graph.y + (write / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
    
    def _update_network(self):
        """Update the network activity display."""
        # Get network data
        network_data = self.monitor.get_network_data()
        sent_speed = network_data['sent_speed']
        recv_speed = network_data['recv_speed']
        
        # Update the network speed label
        self.ids.network_speed.text = f"Up: {format_bytes_speed(sent_speed)} | Down: {format_bytes_speed(recv_speed)}"
        
        # Update the network graph
        self.network_history.append((sent_speed, recv_speed))
        if len(self.network_history) > 60:  # Keep last 60 seconds
            self.network_history.pop(0)
        
        # Draw the network graph
        with self.ids.network_graph.canvas:
            self.ids.network_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.network_graph.pos, size=self.ids.network_graph.size)
            
            # Find max value for scaling
            max_value = 1.0  # Avoid division by zero
            for sent, recv in self.network_history:
                max_value = max(max_value, sent, recv)
            
            # Draw network graph
            if self.network_history:
                # Upload line (orange)
                Color(0.9, 0.6, 0.2)
                
                points = []
                w = self.ids.network_graph.width
                h = self.ids.network_graph.height
                x_step = w / (len(self.network_history) - 1) if len(self.network_history) > 1 else w
                
                for i, (sent, _) in enumerate(self.network_history):
                    x = self.ids.network_graph.x + i * x_step
                    y = self.ids.network_graph.y + (sent / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
                
                # Download line (blue)
                Color(0.2, 0.6, 0.9)
                
                points = []
                for i, (_, recv) in enumerate(self.network_history):
                    x = self.ids.network_graph.x + i * x_step
                    y = self.ids.network_graph.y + (recv / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
