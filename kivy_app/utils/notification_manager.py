"""
Notification Manager Module.
This module is responsible for displaying and managing notifications to the user.
"""

import time
from functools import partial
from typing import Optional, Callable, Dict, List

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import (
    StringProperty, NumericProperty, ColorProperty, 
    BooleanProperty, ObjectProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.logger import Logger


class Notification(BoxLayout):
    """A notification widget that can be used to display messages to the user."""
    
    text = StringProperty("")
    icon = StringProperty("")
    duration = NumericProperty(3)  # Seconds to show notification
    background_color = ColorProperty([0.3, 0.3, 0.3, 0.9])
    text_color = ColorProperty([1, 1, 1, 1])
    dismissable = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super(Notification, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        self.spacing = dp(10)
        self.size_hint = (None, None)
        self.height = dp(50)
        self.width = Window.width - dp(40)
        self.opacity = 0
        self.pos_hint = {'center_x': 0.5, 'top': 0}
        
        # Auto-position based on window size
        Window.bind(on_resize=self._on_window_resize)
        
        # Auto-dismiss after duration
        if self.duration > 0:
            Clock.schedule_once(self.dismiss, self.duration)
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the notification UI."""
        # Message label
        self.message_label = Label(
            text=self.text,
            color=self.text_color,
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            shorten=True,
            markup=True
        )
        self.message_label.bind(size=self.message_label.setter('text_size'))
        
        # Close button (if dismissable)
        if self.dismissable:
            self.close_button = Button(
                text='×',
                size_hint=(None, 1),
                width=dp(30),
                background_normal='',
                background_color=(0.5, 0.5, 0.5, 0)
            )
            self.close_button.bind(on_release=self.dismiss)
        
        # Add widgets
        self.add_widget(self.message_label)
        if self.dismissable:
            self.add_widget(self.close_button)
    
    def _on_window_resize(self, instance, width, height):
        """Handle window resize."""
        self.width = width - dp(40)
    
    def show(self, pos_hint=None):
        """
        Show the notification.
        
        Args:
            pos_hint (dict): Optional position hint to override default
        """
        if pos_hint:
            self.pos_hint = pos_hint
            
        # Animation to show
        anim = Animation(opacity=1, pos_hint={'center_x': 0.5, 'top': 0.98}, duration=0.3)
        anim.bind(on_complete=self._on_show_complete)
        anim.start(self)
        
        return self
    
    def dismiss(self, *args):
        """Dismiss the notification."""
        # Animation to hide
        anim = Animation(opacity=0, pos_hint={'center_x': 0.5, 'top': 1.1}, duration=0.3)
        anim.bind(on_complete=self._on_dismiss_complete)
        anim.start(self)
        
        return self
    
    def _on_show_complete(self, *args):
        """Called when show animation completes."""
        pass
    
    def _on_dismiss_complete(self, *args):
        """Called when dismiss animation completes."""
        # Remove from parent
        if self.parent:
            self.parent.remove_widget(self)


class NotificationManager:
    """Manages notifications throughout the application."""
    
    def __init__(self):
        """Initialize the notification manager."""
        self.app = None  # Will be set when used in the app
        self.notification_overlay = None
        self.active_notifications = []
        self.notification_history = []
    
    def _ensure_overlay(self):
        """
        Ensure that the notification overlay exists.
        Creates it if it doesn't exist yet.
        """
        if not self.notification_overlay:
            # Create overlay
            self.notification_overlay = FloatLayout()
            self.notification_overlay.is_notification_overlay = True
            
            # Add to root window
            Window.add_widget(self.notification_overlay)
    
    def show(self, message: str, 
             type_: str = 'info', 
             duration: float = 3, 
             callback: Optional[Callable] = None,
             dismissable: bool = True) -> Notification:
        """
        Show a notification to the user.
        
        Args:
            message (str): The message to display
            type_ (str): Type of notification ('info', 'success', 'warning', 'error')
            duration (float): Time in seconds to show the notification (0 for no auto-dismiss)
            callback (callable): Optional callback to call when notification is dismissed
            dismissable (bool): Whether the notification can be dismissed by the user
            
        Returns:
            Notification: The created notification object
        """
        self._ensure_overlay()
        
        # Get colors based on type
        colors = {
            'info': ([0.2, 0.6, 0.8, 0.95], [1, 1, 1, 1]),
            'success': ([0.2, 0.8, 0.2, 0.95], [1, 1, 1, 1]),
            'warning': ([0.9, 0.6, 0.1, 0.95], [1, 1, 1, 1]),
            'error': ([0.8, 0.2, 0.2, 0.95], [1, 1, 1, 1])
        }
        bg_color, text_color = colors.get(type_, colors['info'])
        
        # Create notification
        notification = Notification(
            text=message,
            background_color=bg_color,
            text_color=text_color,
            duration=duration,
            dismissable=dismissable
        )
        
        # Add to overlay
        self.notification_overlay.add_widget(notification)
        
        # Record in history and active list
        self.notification_history.append({
            'message': message,
            'type': type_,
            'timestamp': time.time()
        })
        self.active_notifications.append(notification)
        
        # Show notification
        notification.show()
        
        # Bind to dismissal if callback provided
        if callback:
            def on_dismiss(*args):
                callback()
                # Remove from active notifications
                if notification in self.active_notifications:
                    self.active_notifications.remove(notification)
            
            # Schedule callback after dismiss animation
            Clock.schedule_once(lambda dt: Clock.schedule_once(on_dismiss, 0.35), duration)
        else:
            # Schedule removal from active list
            def on_dismiss(dt):
                if notification in self.active_notifications:
                    self.active_notifications.remove(notification)
            
            Clock.schedule_once(lambda dt: Clock.schedule_once(on_dismiss, 0.35), duration)
        
        return notification
    
    def info(self, message: str, 
             duration: float = 3, 
             callback: Optional[Callable] = None,
             dismissable: bool = True) -> Notification:
        """Show an info notification."""
        return self.show(message, 'info', duration, callback, dismissable)
    
    def success(self, message: str, 
                duration: float = 3, 
                callback: Optional[Callable] = None,
                dismissable: bool = True) -> Notification:
        """Show a success notification."""
        return self.show(message, 'success', duration, callback, dismissable)
    
    def warning(self, message: str, 
                duration: float = 3, 
                callback: Optional[Callable] = None,
                dismissable: bool = True) -> Notification:
        """Show a warning notification."""
        return self.show(message, 'warning', duration, callback, dismissable)
    
    def error(self, message: str, 
              duration: float = 5, 
              callback: Optional[Callable] = None,
              dismissable: bool = True) -> Notification:
        """Show an error notification."""
        return self.show(message, 'error', duration, callback, dismissable)
    
    def clear_all(self):
        """Dismiss all active notifications."""
        for notification in self.active_notifications[:]:
            notification.dismiss()
        self.active_notifications = []
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Get the notification history.
        
        Args:
            limit (int): Maximum number of history items to return
            
        Returns:
            List[Dict]: List of notification history items
        """
        return self.notification_history[-limit:] if self.notification_history else []