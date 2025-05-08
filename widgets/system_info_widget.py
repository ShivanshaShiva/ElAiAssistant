"""
System Info Widget Module.
This module contains the widget that displays detailed system information.
"""

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from utils import format_bytes


class SystemInfoWidget(TabbedPanelItem):
    """Widget that displays detailed system information."""
    
    def __init__(self, monitor, **kwargs):
        super(SystemInfoWidget, self).__init__(**kwargs)
        self.text = 'System Info'
        self.monitor = monitor
        self.content = SystemInfoContent(monitor=monitor)


class SystemInfoContent(BoxLayout):
    """Content for the system info tab."""
    
    monitor = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(SystemInfoContent, self).__init__(**kwargs)
        
        # Fill the system info grid with data
        self._populate_system_info()
    
    def _populate_system_info(self):
        """Populate the system info grid with all available system information."""
        # Get the system info
        info = self.monitor.get_system_info()
        
        # Clear any existing widgets
        self.ids.system_info_grid.clear_widgets()
        
        # Add basic system information
        self._add_section_header("System Information")
        self._add_info_row("Operating System", f"{info.get('system', 'Unknown')}")
        self._add_info_row("Computer Name", f"{info.get('node', 'Unknown')}")
        self._add_info_row("OS Release", f"{info.get('release', 'Unknown')}")
        self._add_info_row("OS Version", f"{info.get('version', 'Unknown')}")
        self._add_info_row("Machine Type", f"{info.get('machine', 'Unknown')}")
        self._add_info_row("Processor", f"{info.get('processor', 'Unknown')}")
        self._add_info_row("Python Version", f"{info.get('python_version', 'Unknown')}")
        self._add_info_row("Boot Time", f"{info.get('boot_time', 'Unknown')}")
        
        # Add CPU information
        self._add_section_header("CPU Information")
        self._add_info_row("CPU Count", f"{self.monitor.get_cpu_data()['count']}")
        self._add_info_row("Physical CPUs", f"{self.monitor.get_cpu_data()['physical_count']}")
        
        if 'cpu_freq_current' in info:
            self._add_info_row("CPU Frequency", f"{info.get('cpu_freq_current', 0):.1f} MHz")
        
        if 'cpu_freq_min' in info and 'cpu_freq_max' in info:
            self._add_info_row("CPU Freq Range", 
                              f"{info.get('cpu_freq_min', 0):.1f} - {info.get('cpu_freq_max', 0):.1f} MHz")
        
        # Add memory information
        self._add_section_header("Memory Information")
        self._add_info_row("Total RAM", format_bytes(info.get('total_memory', 0)))
        self._add_info_row("Total Swap", format_bytes(info.get('total_swap', 0)))
        
        # Add disk partition information
        self._add_section_header("Disk Partitions")
        disk_partitions = info.get('disk_partitions', [])
        
        for partition in disk_partitions:
            device = partition.get('device', 'Unknown')
            mountpoint = partition.get('mountpoint', 'Unknown')
            fstype = partition.get('fstype', 'Unknown')
            total = partition.get('total', 0)
            percent = partition.get('percent', 0)
            
            self._add_info_row(f"{device} ({fstype})", 
                              f"Mount: {mountpoint}, Total: {format_bytes(total)}, Used: {percent:.1f}%")
        
        # Add network interface information
        self._add_section_header("Network Interfaces")
        network_interfaces = info.get('network_interfaces', [])
        
        for interface in network_interfaces:
            name = interface.get('name', 'Unknown')
            is_up = "Up" if interface.get('isup', False) else "Down"
            speed = interface.get('speed', 0)
            mtu = interface.get('mtu', 0)
            
            self._add_info_row(name, f"Status: {is_up}, Speed: {speed} Mbps, MTU: {mtu}")
    
    def _add_section_header(self, title):
        """Add a section header to the grid."""
        header = Label(
            text=title,
            font_size='18sp',
            bold=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=40,
            text_size=(None, None)
        )
        # Add empty label for the second column
        empty = Label(text="")
        
        self.ids.system_info_grid.add_widget(header)
        self.ids.system_info_grid.add_widget(empty)
    
    def _add_info_row(self, label_text, value_text):
        """Add an information row to the grid."""
        label = Label(
            text=label_text,
            halign='right',
            valign='middle',
            padding=[0, 0, 10, 0],
            text_size=(None, None)
        )
        
        value = Label(
            text=value_text,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        
        self.ids.system_info_grid.add_widget(label)
        self.ids.system_info_grid.add_widget(value)
