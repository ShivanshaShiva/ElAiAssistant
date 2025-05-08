"""
Utility Functions.
This module contains helper functions used throughout the application.
"""

def format_bytes(bytes_value):
    """
    Format byte value into a human-readable string.
    
    Args:
        bytes_value (int): The value in bytes to format
        
    Returns:
        str: Human-readable string representation
    """
    if bytes_value < 0:
        return "0 B"
    
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    suffix_index = 0
    while bytes_value >= 1024 and suffix_index < len(suffixes) - 1:
        bytes_value /= 1024
        suffix_index += 1
    
    if suffix_index == 0:
        return f"{bytes_value:.0f} {suffixes[suffix_index]}"
    else:
        return f"{bytes_value:.2f} {suffixes[suffix_index]}"


def format_bytes_speed(bytes_per_second):
    """
    Format bytes per second value into a human-readable string.
    
    Args:
        bytes_per_second (float): The value in bytes per second to format
        
    Returns:
        str: Human-readable string representation
    """
    formatted_bytes = format_bytes(bytes_per_second)
    return f"{formatted_bytes}/s"
