"""
System Monitor Module.
This module is responsible for collecting system resource data using psutil.
"""

import os
import platform
import psutil
import time
from datetime import datetime

class SystemMonitor:
    """Collects and provides system resource usage data."""
    
    def __init__(self):
        """Initialize the system monitor with empty data."""
        self.cpu_data = {
            'percent': 0,
            'per_cpu': [],
            'count': psutil.cpu_count(logical=True),
            'physical_count': psutil.cpu_count(logical=False)
        }
        
        self.memory_data = {
            'total': 0,
            'available': 0,
            'percent': 0,
            'used': 0,
            'free': 0
        }
        
        self.disk_data = {
            'total': 0,
            'used': 0,
            'free': 0,
            'percent': 0,
            'read_count': 0,
            'write_count': 0,
            'read_bytes': 0,
            'write_bytes': 0
        }
        
        self.network_data = {
            'bytes_sent': 0,
            'bytes_recv': 0,
            'packets_sent': 0,
            'packets_recv': 0,
            'sent_speed': 0,  # Bytes per second
            'recv_speed': 0   # Bytes per second
        }
        
        self.prev_net_io = psutil.net_io_counters()
        self.prev_disk_io = psutil.disk_io_counters()
        self.prev_time = time.time()
        
        # System information (static data, only collected once)
        self.system_info = self._get_system_info()
        
        # Perform initial update
        self.update()
    
    def update(self):
        """Update all system resource data."""
        self._update_cpu()
        self._update_memory()
        self._update_disk()
        self._update_network()
    
    def _update_cpu(self):
        """Update CPU usage data."""
        self.cpu_data['percent'] = psutil.cpu_percent(interval=0)
        self.cpu_data['per_cpu'] = psutil.cpu_percent(interval=0, percpu=True)
    
    def _update_memory(self):
        """Update memory usage data."""
        mem = psutil.virtual_memory()
        self.memory_data['total'] = mem.total
        self.memory_data['available'] = mem.available
        self.memory_data['percent'] = mem.percent
        self.memory_data['used'] = mem.used
        self.memory_data['free'] = mem.free
    
    def _update_disk(self):
        """Update disk usage and I/O data."""
        # Get disk usage
        disk = psutil.disk_usage('/')
        self.disk_data['total'] = disk.total
        self.disk_data['used'] = disk.used
        self.disk_data['free'] = disk.free
        self.disk_data['percent'] = disk.percent
        
        # Get disk I/O statistics
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        time_delta = current_time - self.prev_time
        
        if time_delta > 0:
            # Calculate I/O rates
            read_delta = current_disk_io.read_bytes - self.prev_disk_io.read_bytes
            write_delta = current_disk_io.write_bytes - self.prev_disk_io.write_bytes
            
            self.disk_data['read_count'] = current_disk_io.read_count
            self.disk_data['write_count'] = current_disk_io.write_count
            self.disk_data['read_bytes'] = read_delta / time_delta  # Bytes per second
            self.disk_data['write_bytes'] = write_delta / time_delta  # Bytes per second
        
        self.prev_disk_io = current_disk_io
    
    def _update_network(self):
        """Update network usage data."""
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_delta = current_time - self.prev_time
        
        if time_delta > 0:
            # Calculate network rates
            sent_delta = current_net_io.bytes_sent - self.prev_net_io.bytes_sent
            recv_delta = current_net_io.bytes_recv - self.prev_net_io.bytes_recv
            
            self.network_data['bytes_sent'] = current_net_io.bytes_sent
            self.network_data['bytes_recv'] = current_net_io.bytes_recv
            self.network_data['packets_sent'] = current_net_io.packets_sent
            self.network_data['packets_recv'] = current_net_io.packets_recv
            self.network_data['sent_speed'] = sent_delta / time_delta  # Bytes per second
            self.network_data['recv_speed'] = recv_delta / time_delta  # Bytes per second
        
        self.prev_net_io = current_net_io
        self.prev_time = current_time
    
    def _get_system_info(self):
        """Get static system information."""
        try:
            # Basic system information
            info = {
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            # CPU information
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                info['cpu_freq_current'] = cpu_freq.current
                if hasattr(cpu_freq, 'min'):
                    info['cpu_freq_min'] = cpu_freq.min
                if hasattr(cpu_freq, 'max'):
                    info['cpu_freq_max'] = cpu_freq.max
            
            # Memory information
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            info['total_memory'] = mem.total
            info['total_swap'] = swap.total
            
            # Disk information
            disk_partitions = []
            for partition in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_partitions.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'percent': usage.percent
                    })
                except (PermissionError, OSError):
                    # Skip partitions that cannot be accessed
                    continue
            
            info['disk_partitions'] = disk_partitions
            
            # Network information
            network_interfaces = []
            for name, stats in psutil.net_if_stats().items():
                network_interfaces.append({
                    'name': name,
                    'isup': stats.isup,
                    'speed': getattr(stats, 'speed', 0),
                    'mtu': stats.mtu
                })
            
            info['network_interfaces'] = network_interfaces
            
            return info
        
        except Exception as e:
            # In case of error, return basic information
            return {
                'error': str(e),
                'system': platform.system(),
                'node': platform.node(),
                'processor': platform.processor()
            }
    
    def get_cpu_data(self):
        """Get the current CPU data."""
        return self.cpu_data
    
    def get_memory_data(self):
        """Get the current memory data."""
        return self.memory_data
    
    def get_disk_data(self):
        """Get the current disk data."""
        return self.disk_data
    
    def get_network_data(self):
        """Get the current network data."""
        return self.network_data
    
    def get_system_info(self):
        """Get system information."""
        return self.system_info
    
    def get_all_data(self):
        """Get all current data in a single dictionary."""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_data(),
            'memory': self.get_memory_data(),
            'disk': self.get_disk_data(),
            'network': self.get_network_data()
        }
