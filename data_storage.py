"""
Data Storage Module.
This module handles the storage and retrieval of historical system resource data using SQLite.
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta


class DataStorage:
    """Stores and retrieves historical system resource data."""
    
    def __init__(self, db_path='system_monitor.db'):
        """Initialize the data storage with an SQLite database."""
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create the necessary tables if they don't exist."""
        # Create a table for the system metrics
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                disk_read_bytes REAL,
                disk_write_bytes REAL,
                network_sent_speed REAL,
                network_recv_speed REAL,
                data_json TEXT
            )
        ''')
        self.connection.commit()
    
    def store_data(self, data):
        """Store the current system data in the database."""
        # Extract key metrics for quick access
        timestamp = data['timestamp']
        cpu_percent = data['cpu']['percent']
        memory_percent = data['memory']['percent']
        disk_percent = data['disk']['percent']
        disk_read_bytes = data['disk']['read_bytes']
        disk_write_bytes = data['disk']['write_bytes']
        network_sent_speed = data['network']['sent_speed']
        network_recv_speed = data['network']['recv_speed']
        
        # Store the full data as JSON for future use
        data_json = json.dumps(data)
        
        # Insert the data into the database
        self.cursor.execute('''
            INSERT INTO system_metrics (
                timestamp, cpu_percent, memory_percent, disk_percent,
                disk_read_bytes, disk_write_bytes, network_sent_speed,
                network_recv_speed, data_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp, cpu_percent, memory_percent, disk_percent,
            disk_read_bytes, disk_write_bytes, network_sent_speed,
            network_recv_speed, data_json
        ))
        self.connection.commit()
        
        # Clean up old data (keep only the last 24 hours by default)
        self._cleanup_old_data()
    
    def _cleanup_old_data(self, hours=24):
        """Remove data older than the specified number of hours."""
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        self.cursor.execute('''
            DELETE FROM system_metrics
            WHERE timestamp < ?
        ''', (cutoff_time,))
        self.connection.commit()
    
    def get_history(self, metric, hours=1, limit=60):
        """
        Get historical data for a specific metric.
        
        Args:
            metric (str): The metric to retrieve ('cpu_percent', 'memory_percent', etc.)
            hours (int): Number of hours of history to retrieve
            limit (int): Maximum number of data points to return
            
        Returns:
            list: List of (timestamp, value) tuples
        """
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        if metric in ['cpu_percent', 'memory_percent', 'disk_percent',
                      'disk_read_bytes', 'disk_write_bytes',
                      'network_sent_speed', 'network_recv_speed']:
            # Direct database columns
            self.cursor.execute(f'''
                SELECT timestamp, {metric}
                FROM system_metrics
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (cutoff_time, limit))
            
            return [(row[0], row[1]) for row in self.cursor.fetchall()]
        else:
            # For metrics stored in the JSON data
            self.cursor.execute('''
                SELECT timestamp, data_json
                FROM system_metrics
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (cutoff_time, limit))
            
            result = []
            for row in self.cursor.fetchall():
                timestamp = row[0]
                data = json.loads(row[1])
                
                # Extract the requested metric from the JSON data
                # This assumes the metric is in the format 'category.name'
                if '.' in metric:
                    category, name = metric.split('.', 1)
                    if category in data and name in data[category]:
                        result.append((timestamp, data[category][name]))
            
            return result
    
    def get_recent_data(self):
        """Get the most recent data point."""
        self.cursor.execute('''
            SELECT data_json
            FROM system_metrics
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        
        row = self.cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    # Simple test for the DataStorage class
    storage = DataStorage()
    
    # Example data
    test_data = {
        'timestamp': datetime.now().isoformat(),
        'cpu': {'percent': 25.5, 'per_cpu': [20.0, 30.0, 25.0, 27.0]},
        'memory': {'percent': 45.2, 'used': 4000000000, 'total': 8000000000},
        'disk': {'percent': 65.7, 'read_bytes': 1024, 'write_bytes': 2048},
        'network': {'sent_speed': 1024, 'recv_speed': 2048}
    }
    
    # Store test data
    storage.store_data(test_data)
    
    # Test retrieval
    print("CPU history:", storage.get_history('cpu_percent', hours=1, limit=5))
    
    # Close connection
    storage.close()
