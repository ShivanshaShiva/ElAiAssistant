"""
System Monitor Module.
This module dynamically switches between psutil-based monitoring and
os/subprocess-based monitoring, ensuring compatibility across platforms.
"""

import os
import platform
import time
from datetime import datetime

# Attempt to import psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemMonitor:
    """System monitor that dynamically selects psutil or fallback implementation."""
    def __init__(self):
        self.cpu_data = {}
        self.memory_data = {}
        self.disk_data = {}
        self.network_data = {}
        self.prev_net_io = None
        self.prev_disk_io = None
        self.prev_time = None
        self.system_info = {}
        
        if PSUTIL_AVAILABLE:
            self._initialize_psutil()
        else:
            self._initialize_fallback()

        self.update()

    def _initialize_psutil(self):
        """Initialize psutil-specific attributes."""
        self.prev_net_io = psutil.net_io_counters()
        self.prev_disk_io = psutil.disk_io_counters()
        self.prev_time = time.time()
        self.system_info = self._get_system_info_psutil()

    def _initialize_fallback(self):
        """Initialize fallback attributes."""
        self.prev_net_io = self._get_network_data_fallback()
        self.prev_disk_io = self._get_disk_data_fallback()
        self.prev_time = time.time()
        self.system_info = self._get_system_info_fallback()

    def update(self):
        """Update all system resource data."""
        if PSUTIL_AVAILABLE:
            self._update_cpu_psutil()
            self._update_memory_psutil()
            self._update_disk_psutil()
            self._update_network_psutil()
        else:
            self._update_cpu_fallback()
            self._update_memory_fallback()
            self._update_disk_fallback()
            self._update_network_fallback()

    # ------------------ Psutil-Based Methods ------------------
    def _update_cpu_psutil(self):
        """Update CPU usage data using psutil."""
        self.cpu_data = {
            'percent': psutil.cpu_percent(interval=0),
            'per_cpu': psutil.cpu_percent(interval=0, percpu=True),
            'count': psutil.cpu_count(logical=True),
            'physical_count': psutil.cpu_count(logical=False)
        }

    def _update_memory_psutil(self):
        """Update memory usage data using psutil."""
        mem = psutil.virtual_memory()
        self.memory_data = {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
            'free': mem.free
        }

    def _update_disk_psutil(self):
        """Update disk usage and I/O data using psutil."""
        disk = psutil.disk_usage('/')
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        time_delta = current_time - self.prev_time

        if time_delta > 0:
            read_delta = current_disk_io.read_bytes - self.prev_disk_io.read_bytes
            write_delta = current_disk_io.write_bytes - self.prev_disk_io.write_bytes
            self.disk_data = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'read_bytes': read_delta / time_delta,
                'write_bytes': write_delta / time_delta
            }

        self.prev_disk_io = current_disk_io
        self.prev_time = current_time

    def _update_network_psutil(self):
        """Update network usage data using psutil."""
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_delta = current_time - self.prev_time

        if time_delta > 0:
            sent_delta = current_net_io.bytes_sent - self.prev_net_io.bytes_sent
            recv_delta = current_net_io.bytes_recv - self.prev_net_io.bytes_recv
            self.network_data = {
                'bytes_sent': current_net_io.bytes_sent,
                'bytes_recv': current_net_io.bytes_recv,
                'sent_speed': sent_delta / time_delta,
                'recv_speed': recv_delta / time_delta
            }

        self.prev_net_io = current_net_io
        self.prev_time = current_time

    def _get_system_info_psutil(self):
        """Get static system information using psutil."""
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
        return info

    # ------------------ Fallback Methods ------------------
    def _update_cpu_fallback(self):
        """Update CPU usage data using fallback."""
        self.cpu_data = {
            'percent': 0,  # Placeholder for CPU percentage
            'per_cpu': [],
            'count': os.cpu_count(),
            'physical_count': os.cpu_count()
        }

    def _update_memory_fallback(self):
        """Update memory usage data using fallback."""
        try:
            with open("/proc/meminfo", "r") as meminfo:
                lines = meminfo.readlines()
                total = int(lines[0].split()[1]) * 1024
                free = int(lines[1].split()[1]) * 1024
                available = int(lines[2].split()[1]) * 1024
                self.memory_data = {
                    'total': total,
                    'available': available,
                    'used': total - free,
                    'free': free,
                    'percent': (total - free) / total * 100
                }
        except Exception as e:
            self.memory_data = {'error': str(e)}

    def _update_disk_fallback(self):
        """Update disk usage data using fallback."""
        try:
            result = os.popen("df /").readlines()[1].split()
            self.disk_data = {
                'total': int(result[1]) * 1024,
                'used': int(result[2]) * 1024,
                'free': int(result[3]) * 1024,
                'percent': int(result[4].strip('%'))
            }
        except Exception as e:
            self.disk_data = {'error': str(e)}

    def _update_network_fallback(self):
        """Update network usage data using fallback."""
        try:
            with open("/proc/net/dev", "r") as net_dev:
                lines = net_dev.readlines()[2:]
                total_received = sum(int(line.split()[1]) for line in lines)
                total_sent = sum(int(line.split()[9]) for line in lines)
                self.network_data = {
                    'bytes_recv': total_received,
                    'bytes_sent': total_sent,
                }
        except Exception as e:
            self.network_data = {'error': str(e)}

    def _get_system_info_fallback(self):
        """Get static system information using fallback."""
        return {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }

    # ------------------ Public Methods ------------------
    def get_cpu_data(self):
        return self.cpu_data

    def get_memory_data(self):
        return self.memory_data

    def get_disk_data(self):
        return self.disk_data

    def get_network_data(self):
        return self.network_data

    def get_system_info(self):
        return self.system_info

    def get_all_data(self):
        """Get all current data in a single dictionary."""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_data(),
            'memory': self.get_memory_data(),
            'disk': self.get_disk_data(),
            'network': self.get_network_data(),
            'system_info': self.get_system_info()
        }