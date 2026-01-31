"""
AutocompleteEntry widget for tkinter
Provides autocomplete functionality with custom data and display callbacks
"""

import tkinter as tk
from tkinter import font as tkfont
import threading


class AutocompleteEntry(tk.Entry):
    """
    Entry widget with autocomplete functionality.
    
    Parameters:
    - data_callback: Function that returns list of suggestions based on current input
    - display_callback: Function that formats the display of each suggestion
    - width: Width of the entry widget
    """
    
    def __init__(self, parent, data_callback=None, display_callback=None, width=30, **kwargs):
        """Initialize the AutocompleteEntry widget."""
        super().__init__(parent, width=width, **kwargs)
        
        self.data_callback = data_callback
        self.display_callback = display_callback
        self.parent = parent
        self.suggestions_window = None
        self.suggestions_listbox = None
        self.suggestions_data = []
        self._debounce_timer = None
        
        # Bind events for autocomplete
        self.bind('<KeyRelease>', self._on_key_release)
        self.bind('<FocusOut>', self._on_focus_out)
        
    def _on_key_release(self, event):
        """Handle key release events to show suggestions."""
        # Don't show suggestions for certain keys
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Tab', 'Shift_L', 'Shift_R', 
                            'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
        
        # Cancel previous debounce timer
        if self._debounce_timer:
            self.after_cancel(self._debounce_timer)
        
        # Schedule suggestion update with debounce
        self._debounce_timer = self.after(200, self._update_suggestions)
    
    def _update_suggestions(self):
        """Update the list of suggestions based on current input."""
        current_value = self.get()
        
        if not current_value or not self.data_callback:
            self._hide_suggestions()
            return
        
        try:
            # Get suggestions from callback
            suggestions = self.data_callback(current_value)
            
            if not suggestions:
                self._hide_suggestions()
                return
            
            self.suggestions_data = suggestions
            self._show_suggestions()
            
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            self._hide_suggestions()
    
    def _show_suggestions(self):
        """Show the suggestions dropdown."""
        if not self.suggestions_data:
            return
        
        # Create suggestions window if it doesn't exist
        if self.suggestions_window is None:
            self.suggestions_window = tk.Toplevel(self.parent)
            self.suggestions_window.wm_overrideredirect(True)
            
            # Create listbox with scrollbar
            frame = tk.Frame(self.suggestions_window)
            frame.pack(fill=tk.BOTH, expand=True)
            
            self.suggestions_listbox = tk.Listbox(
                frame,
                height=min(5, len(self.suggestions_data)),
                width=50
            )
            self.suggestions_listbox.pack(fill=tk.BOTH, expand=True)
            self.suggestions_listbox.bind('<Button-1>', self._on_suggestion_click)
            self.suggestions_listbox.bind('<Return>', self._on_suggestion_select)
        
        # Update listbox items
        self.suggestions_listbox.delete(0, tk.END)
        for suggestion in self.suggestions_data:
            display_text = self.display_callback(suggestion) if self.display_callback else str(suggestion)
            self.suggestions_listbox.insert(tk.END, display_text)
        
        # Position the suggestions window
        self._position_suggestions_window()
    
    def _position_suggestions_window(self):
        """Position the suggestions window below the entry widget."""
        if self.suggestions_window is None:
            return
        
        # Get the position of the entry widget
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        width = self.winfo_width()
        
        self.suggestions_window.geometry(f'{width}x{self.suggestions_listbox.winfo_height()}+{x}+{y}')
    
    def _hide_suggestions(self):
        """Hide the suggestions dropdown."""
        if self.suggestions_window:
            self.suggestions_window.destroy()
            self.suggestions_window = None
            self.suggestions_listbox = None
            self.suggestions_data = []
    
    def _on_suggestion_click(self, event):
        """Handle suggestion selection by mouse click."""
        selection = self.suggestions_listbox.curselection()
        if selection:
            self._select_suggestion(selection[0])
    
    def _on_suggestion_select(self, event):
        """Handle suggestion selection by keyboard."""
        selection = self.suggestions_listbox.curselection()
        if selection:
            self._select_suggestion(selection[0])
    
    def _select_suggestion(self, index):
        """Select a suggestion and update the entry."""
        if 0 <= index < len(self.suggestions_data):
            selected_item = self.suggestions_data[index]
            
            # Set the entry value
            if isinstance(selected_item, dict):
                # If it's a dict, try to get the main identifier
                if 'enrollment_no' in selected_item:
                    self.delete(0, tk.END)
                    self.insert(0, selected_item['enrollment_no'])
                elif 'book_id' in selected_item:
                    self.delete(0, tk.END)
                    self.insert(0, selected_item['book_id'])
                else:
                    # Use display callback if available
                    display_text = self.display_callback(selected_item) if self.display_callback else str(selected_item)
                    self.delete(0, tk.END)
                    self.insert(0, display_text)
            else:
                self.delete(0, tk.END)
                self.insert(0, str(selected_item))
            
            self._hide_suggestions()
    
    def _on_focus_out(self, event):
        """Handle focus out event."""
        # Hide suggestions after a short delay to allow click handling
        self.after(200, self._hide_suggestions)
    
    def get_selected_data(self):
        """Get the currently selected data object (if available)."""
        return self.suggestions_data[0] if self.suggestions_data else None
