"""
Notification Manager Module.
This module handles displaying notifications to the user.
"""

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout

class Notification(BoxLayout):
    """A notification widget that appears and disappears."""
    
    text = StringProperty('')
    color = ObjectProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        """Initialize the notification."""
        super(Notification, self).__init__(**kwargs)
        
        # Set up properties
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        self.height = dp(50)
        self.width = dp(300)
        self.opacity = 0  # Start invisible
        self.pos_hint = {'center_x': 0.5, 'top': 0.95}
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(5)
        
        # Background
        from kivy.graphics import Color, RoundedRectangle
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 0.9)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10),])
        
        self.bind(pos=self._update_background, size=self._update_background)
        
        # Message label
        self.label = Label(
            text=self.text,
            color=self.color,
            size_hint=(0.9, 1),
            text_size=(dp(270), None),
            valign='middle',
            halign='left'
        )
        
        # Close button
        self.close_button = Button(
            text='✕',
            size_hint=(0.1, 1),
            background_normal='',
            background_color=(0.3, 0.3, 0.3, 0),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.close_button.bind(on_press=self.dismiss)
        
        # Add widgets
        self.add_widget(self.label)
        self.add_widget(self.close_button)
        
        # Bind properties
        self.bind(text=self._update_text)
        self.bind(color=self._update_color)
    
    def _update_background(self, instance, value):
        """Update the background rectangle."""
        self.background.pos = self.pos
        self.background.size = self.size
    
    def _update_text(self, instance, value):
        """Update the notification text."""
        self.label.text = value
    
    def _update_color(self, instance, value):
        """Update the notification color."""
        self.label.color = value
    
    def show(self, duration=3):
        """Show the notification."""
        # Create fade-in animation
        anim = Animation(opacity=1, duration=0.3)
        
        # Schedule automatic dismissal
        if duration > 0:
            Clock.schedule_once(self.dismiss, duration)
            
        # Start animation
        anim.start(self)
        
    def dismiss(self, instance=None):
        """Immediately dismiss the notification."""
        # Cancel any scheduled dismissal
        Clock.unschedule(self.dismiss)
        
        # Create fade-out animation
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=self.remove_from_parent)
        
        # Start animation
        anim.start(self)
    
    def remove_from_parent(self, instance=None, value=None):
        """Remove the notification from its parent."""
        if self.parent:
            self.parent.remove_widget(self)


class NotificationManager:
    """Manages and displays notifications."""
    
    def __init__(self):
        """Initialize the notification manager."""
        self.notifications = []
        self.root = None
    
    def set_root(self, root):
        """Set the root widget to attach notifications to."""
        self.root = root
    
    def _get_app(self):
        """Get the current app instance."""
        return App.get_running_app()
    
    def _show_notification(self, text, color, duration=3):
        """
        Display a notification.
        
        Args:
            text (str): Notification text
            color (list): Text color as [r, g, b, a]
            duration (float): Display duration in seconds
        """
        # Create the notification widget
        notification = Notification(text=text, color=color)
        
        # Get app window 
        app = self._get_app()
        if app and hasattr(app, 'screen_manager'):
            # Current screen is a good container for notifications
            current_screen = app.screen_manager.current_screen
            
            # Check if the screen has a notification overlay
            notification_overlay = None
            for child in current_screen.children:
                if isinstance(child, FloatLayout) and getattr(child, 'is_notification_overlay', False):
                    notification_overlay = child
                    break
            
            # Create notification overlay if it doesn't exist
            if not notification_overlay:
                notification_overlay = FloatLayout()
                notification_overlay.is_notification_overlay = True
                current_screen.add_widget(notification_overlay)
            
            # Add notification to overlay
            notification_overlay.add_widget(notification)
            
            # Show the notification
            notification.show(duration)
            
            # Store notification reference
            self.notifications.append(notification)
        
    def info(self, text, duration=3):
        """Show an info notification."""
        self._show_notification(text, [0.9, 0.9, 1, 1], duration)
    
    def success(self, text, duration=3):
        """Show a success notification."""
        self._show_notification(text, [0.5, 1, 0.5, 1], duration)
    
    def warning(self, text, duration=3):
        """Show a warning notification."""
        self._show_notification(text, [1, 0.8, 0.3, 1], duration)
    
    def error(self, text, duration=4):
        """Show an error notification."""
        self._show_notification(text, [1, 0.5, 0.5, 1], duration)