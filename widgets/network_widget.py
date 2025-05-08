"""
Network Widget Module.
This module contains the widget that displays detailed network information.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty

from utils import format_bytes, format_bytes_speed


class NetworkWidget(TabbedPanelItem):
    """Widget that displays detailed network information."""
    
    def __init__(self, monitor, storage, **kwargs):
        super(NetworkWidget, self).__init__(**kwargs)
        self.text = 'Network'
        self.monitor = monitor
        self.storage = storage
        self.content = NetworkContent(monitor=monitor, storage=storage)


class NetworkContent(BoxLayout):
    """Content for the network tab."""
    
    monitor = ObjectProperty(None)
    storage = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(NetworkContent, self).__init__(**kwargs)
        self.network_history = {'sent': [], 'recv': []}
        
        # Initialize the display with current data
        self.update_display()
    
    def update_display(self):
        """Update the network activity display."""
        # Get network data
        network_data = self.monitor.get_network_data()
        bytes_sent = network_data['bytes_sent']
        bytes_recv = network_data['bytes_recv']
        packets_sent = network_data['packets_sent']
        packets_recv = network_data['packets_recv']
        sent_speed = network_data['sent_speed']
        recv_speed = network_data['recv_speed']
        
        # Update the network activity labels
        self.ids.network_sent_speed.text = f"Upload: {format_bytes_speed(sent_speed)}"
        self.ids.network_recv_speed.text = f"Download: {format_bytes_speed(recv_speed)}"
        self.ids.network_bytes_sent.text = format_bytes(bytes_sent)
        self.ids.network_bytes_recv.text = format_bytes(bytes_recv)
        self.ids.network_packets_sent.text = f"{packets_sent:,}"
        self.ids.network_packets_recv.text = f"{packets_recv:,}"
        
        # Update the network history graph
        self._update_history_graph()
    
    def _update_history_graph(self):
        """Update the network activity history graph."""
        # Get network history data from storage
        sent_history_data = self.storage.get_history('network_sent_speed', hours=1, limit=120)
        recv_history_data = self.storage.get_history('network_recv_speed', hours=1, limit=120)
        
        # Extract only the values (not timestamps)
        self.network_history['sent'] = [value for _, value in sent_history_data]
        self.network_history['recv'] = [value for _, value in recv_history_data]
        
        # Make sure both lists have the same length
        min_length = min(len(self.network_history['sent']), len(self.network_history['recv']))
        self.network_history['sent'] = self.network_history['sent'][:min_length]
        self.network_history['recv'] = self.network_history['recv'][:min_length]
        
        # Draw the network history graph
        with self.ids.network_history_graph.canvas:
            self.ids.network_history_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.network_history_graph.pos, size=self.ids.network_history_graph.size)
            
            # Find max value for scaling
            max_value = 1.0  # Avoid division by zero
            for sent_val in self.network_history['sent']:
                max_value = max(max_value, sent_val)
            for recv_val in self.network_history['recv']:
                max_value = max(max_value, recv_val)
            
            # Draw horizontal grid lines
            Color(0.3, 0.3, 0.3)
            for i in range(1, 4):
                y = self.ids.network_history_graph.y + (i / 4.0) * self.ids.network_history_graph.height
                Line(points=[self.ids.network_history_graph.x, y, 
                            self.ids.network_history_graph.x + self.ids.network_history_graph.width, y], 
                    width=1)
            
            # Draw the sent history line (orange)
            if self.network_history['sent']:
                Color(0.9, 0.6, 0.2)
                
                points = []
                w = self.ids.network_history_graph.width
                h = self.ids.network_history_graph.height
                x_step = w / (len(self.network_history['sent']) - 1) if len(self.network_history['sent']) > 1 else w
                
                for i, value in enumerate(self.network_history['sent']):
                    x = self.ids.network_history_graph.x + i * x_step
                    y = self.ids.network_history_graph.y + (value / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
            
            # Draw the recv history line (blue)
            if self.network_history['recv']:
                Color(0.2, 0.6, 0.9)
                
                points = []
                w = self.ids.network_history_graph.width
                h = self.ids.network_history_graph.height
                x_step = w / (len(self.network_history['recv']) - 1) if len(self.network_history['recv']) > 1 else w
                
                for i, value in enumerate(self.network_history['recv']):
                    x = self.ids.network_history_graph.x + i * x_step
                    y = self.ids.network_history_graph.y + (value / max_value) * h
                    points.extend([x, y])
                
                if len(points) >= 4:  # Need at least 2 points (4 coordinates)
                    Line(points=points, width=1.5)
