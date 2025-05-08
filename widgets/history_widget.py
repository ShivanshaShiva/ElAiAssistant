"""
History Widget Module.
This module contains the widget that displays historical data for various metrics.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from datetime import datetime
from utils import format_bytes_speed


class HistoryWidget(TabbedPanelItem):
    """Widget that displays historical data for various metrics."""
    
    def __init__(self, storage, **kwargs):
        super(HistoryWidget, self).__init__(**kwargs)
        self.text = 'History'
        self.storage = storage
        self.content = HistoryContent(storage=storage)


class HistoryContent(BoxLayout):
    """Content for the history tab."""
    
    storage = ObjectProperty(None)
    current_metric = StringProperty('cpu_percent')
    time_period_hours = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super(HistoryContent, self).__init__(**kwargs)
        self.history_data = []
        
        # Initialize the display with current data
        self.update_display()
    
    def update_display(self):
        """Update the historical data display."""
        self._load_history_data()
        self._update_graph()
    
    def _load_history_data(self):
        """Load historical data for the current metric."""
        # Map the display metric to the actual database metric
        metric_map = {
            'cpu_percent': 'cpu_percent',
            'memory_percent': 'memory_percent',
            'disk_percent': 'disk_percent',
            'disk_io': 'disk_read_bytes',  # We'll load both read and write below
            'network': 'network_sent_speed'  # We'll load both sent and recv below
        }
        
        # Load the appropriate data based on the current metric
        if self.current_metric in ['disk_io', 'network']:
            # For disk I/O and network, we need two metrics
            if self.current_metric == 'disk_io':
                read_data = self.storage.get_history('disk_read_bytes', 
                                                   hours=self.time_period_hours, 
                                                   limit=500)
                write_data = self.storage.get_history('disk_write_bytes', 
                                                    hours=self.time_period_hours, 
                                                    limit=500)
                self.history_data = {
                    'primary': read_data,
                    'secondary': write_data,
                    'primary_label': 'Read',
                    'secondary_label': 'Write',
                    'primary_color': (0.2, 0.7, 0.2),  # Green
                    'secondary_color': (0.7, 0.2, 0.2),  # Red
                    'format_func': format_bytes_speed
                }
            else:  # network
                sent_data = self.storage.get_history('network_sent_speed', 
                                                   hours=self.time_period_hours, 
                                                   limit=500)
                recv_data = self.storage.get_history('network_recv_speed', 
                                                   hours=self.time_period_hours, 
                                                   limit=500)
                self.history_data = {
                    'primary': recv_data,
                    'secondary': sent_data,
                    'primary_label': 'Download',
                    'secondary_label': 'Upload',
                    'primary_color': (0.2, 0.6, 0.9),  # Blue
                    'secondary_color': (0.9, 0.6, 0.2),  # Orange
                    'format_func': format_bytes_speed
                }
        else:
            # For single metrics (CPU, memory, disk usage)
            data = self.storage.get_history(metric_map[self.current_metric], 
                                          hours=self.time_period_hours, 
                                          limit=500)
            
            # Determine color and formatting based on metric
            if self.current_metric == 'cpu_percent':
                color = (0.2, 0.7, 0.2)  # Green
                format_func = lambda x: f"{x:.1f}%"
            elif self.current_metric == 'memory_percent':
                color = (0.2, 0.2, 0.7)  # Blue
                format_func = lambda x: f"{x:.1f}%"
            else:  # disk_percent
                color = (0.7, 0.7, 0.2)  # Yellow
                format_func = lambda x: f"{x:.1f}%"
            
            self.history_data = {
                'primary': data,
                'primary_label': self._get_metric_label(),
                'primary_color': color,
                'format_func': format_func
            }
        
        # Update the graph title
        self.ids.history_title.text = f"{self._get_metric_label()} History ({self.time_period_hours} hour{'s' if self.time_period_hours > 1 else ''})"
    
    def _update_graph(self):
        """Update the history graph with the loaded data."""
        with self.ids.history_graph.canvas:
            self.ids.history_graph.canvas.clear()
            
            # Draw background
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=self.ids.history_graph.pos, size=self.ids.history_graph.size)
            
            # Draw grid lines
            self._draw_grid()
            
            # Check if we have data to display
            if not self.history_data or 'primary' not in self.history_data or not self.history_data['primary']:
                # No data, draw empty state
                return
            
            # Determine if we're dealing with a dual metric (disk I/O or network)
            is_dual_metric = 'secondary' in self.history_data and self.history_data['secondary']
            
            # Find max value for scaling
            if is_dual_metric:
                max_value = 1.0  # Avoid division by zero
                for _, value in self.history_data['primary']:
                    max_value = max(max_value, value)
                for _, value in self.history_data['secondary']:
                    max_value = max(max_value, value)
            else:
                max_value = 1.0  # Avoid division by zero
                if self.current_metric in ['cpu_percent', 'memory_percent', 'disk_percent']:
                    max_value = 100.0  # Percentage metrics
                else:
                    for _, value in self.history_data['primary']:
                        max_value = max(max_value, value)
            
            # Draw the primary metric line
            self._draw_metric_line(
                self.history_data['primary'],
                self.history_data['primary_color'],
                max_value
            )
            
            # Draw the secondary metric line if available
            if is_dual_metric:
                self._draw_metric_line(
                    self.history_data['secondary'],
                    self.history_data['secondary_color'],
                    max_value
                )
    
    def _draw_grid(self):
        """Draw grid lines on the graph."""
        # Draw vertical grid lines (time divisions)
        Color(0.3, 0.3, 0.3)
        w = self.ids.history_graph.width
        h = self.ids.history_graph.height
        
        # Draw 4 horizontal lines (at 20%, 40%, 60%, 80%)
        for i in range(1, 5):
            y = self.ids.history_graph.y + (i / 5.0) * h
            Line(points=[self.ids.history_graph.x, y, 
                        self.ids.history_graph.x + w, y], 
                width=1)
        
        # Draw 5 vertical lines
        for i in range(1, 6):
            x = self.ids.history_graph.x + (i / 6.0) * w
            Line(points=[x, self.ids.history_graph.y, 
                        x, self.ids.history_graph.y + h], 
                width=1)
    
    def _draw_metric_line(self, data, color_tuple, max_value):
        """Draw a line for a specific metric on the graph."""
        if not data:
            return
        
        Color(*color_tuple)
        
        points = []
        w = self.ids.history_graph.width
        h = self.ids.history_graph.height
        
        # Reverse the data to go from oldest to newest (left to right)
        reversed_data = list(reversed(data))
        
        x_step = w / (len(reversed_data) - 1) if len(reversed_data) > 1 else w
        
        for i, (_, value) in enumerate(reversed_data):
            x = self.ids.history_graph.x + i * x_step
            y = self.ids.history_graph.y + (value / max_value) * h
            points.extend([x, y])
        
        if len(points) >= 4:  # Need at least 2 points (4 coordinates)
            Line(points=points, width=1.5)
    
    def update_time_period(self, period_text):
        """Update the time period for historical data."""
        # Map the spinner text to hours
        period_map = {
            '30 minutes': 0.5,
            '1 hour': 1,
            '3 hours': 3,
            '6 hours': 6,
            '12 hours': 12,
            '24 hours': 24
        }
        
        self.time_period_hours = period_map.get(period_text, 1)
        self.update_display()
    
    def show_metric(self, metric):
        """Change the displayed metric."""
        self.current_metric = metric
        self.update_display()
    
    def _get_metric_label(self):
        """Get a human-readable label for the current metric."""
        labels = {
            'cpu_percent': 'CPU Usage',
            'memory_percent': 'Memory Usage',
            'disk_percent': 'Disk Usage',
            'disk_io': 'Disk I/O',
            'network': 'Network Activity'
        }
        return labels.get(self.current_metric, self.current_metric)
