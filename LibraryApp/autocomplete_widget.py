#!/usr/bin/env python3
"""
Autocomplete Widget for Student and Book Suggestions
Shows dropdown with suggestions as user types
"""

import tkinter as tk
from tkinter import ttk

class AutocompleteEntry:
    """Entry widget with autocomplete dropdown"""
    
    def __init__(self, parent, data_callback, display_callback=None, width=30):
        """
        Args:
            parent: Parent widget
            data_callback: Function that returns list of suggestions based on query
            display_callback: Function to format display text (optional)
            width: Width of entry widget
        """
        self.parent = parent
        self.data_callback = data_callback
        self.display_callback = display_callback or (lambda x: str(x))
        self.suggestions = []
        self.dropdown = None
        
        # Create entry widget
        self.entry = tk.Entry(parent, font=('Segoe UI', 12), width=width, relief='solid', bd=2)
        
        # Bind events
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.entry.bind('<Down>', self._on_down_arrow)
        self.entry.bind('<Up>', self._on_up_arrow)
        self.entry.bind('<Return>', self._on_return)
        self.entry.bind('<Escape>', self._close_dropdown)
        self.entry.bind('<FocusOut>', lambda e: self._schedule_close())
        
    def _on_key_release(self, event):
        """Handle key release - show suggestions"""
        # Ignore navigation keys
        if event.keysym in ('Up', 'Down', 'Return', 'Escape', 'Left', 'Right', 'Home', 'End'):
            return
        
        query = self.entry.get().strip()
        
        # Close dropdown if query too short
        if len(query) < 1:
            self._close_dropdown(None)
            return
        
        # Get suggestions
        self.suggestions = self.data_callback(query)
        
        if self.suggestions:
            self._show_dropdown()
        else:
            self._close_dropdown(None)
    
    def _show_dropdown(self):
        """Show dropdown with suggestions"""
        # Close existing dropdown
        if self.dropdown:
            try:
                self.dropdown.destroy()
            except:
                pass
        
        # Create dropdown
        self.dropdown = tk.Toplevel(self.entry)
        self.dropdown.wm_overrideredirect(True)
        self.dropdown.wm_attributes('-topmost', True)  # Keep on top
        
        # Position dropdown below entry
        self.entry.update_idletasks()
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        width = max(self.entry.winfo_width(), 350)  # Minimum width
        self.dropdown.geometry(f"{width}x180+{x}+{y}")
        
        # Create listbox
        listbox_frame = tk.Frame(self.dropdown, relief='solid', bd=1, bg='white')
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            listbox_frame,
            font=('Segoe UI', 10),
            bg='white',
            fg='#333',
            selectbackground='#2E86AB',
            selectforeground='white',
            yscrollcommand=scrollbar.set,
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Populate suggestions
        for item in self.suggestions[:10]:  # Limit to 10 items
            display_text = self.display_callback(item)
            self.listbox.insert(tk.END, display_text)
        
        # Bind selection - single click and double click
        self.listbox.bind('<ButtonRelease-1>', self._on_click_select)
        self.listbox.bind('<Double-Button-1>', self._on_select)
        self.listbox.bind('<Return>', self._on_select)
        
        # Select first item
        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
    
    def _on_click_select(self, event=None):
        """Handle single click - select item after short delay"""
        if self.listbox:
            self.entry.after(50, self._on_select)
    
    def _on_select(self, event=None):
        """Handle item selection"""
        if not self.listbox:
            return
        
        try:
            selection = self.listbox.curselection()
            if selection:
                idx = selection[0]
                selected_item = self.suggestions[idx]
                
                # Get the actual value (first part before space or hyphen)
                display_text = self.display_callback(selected_item)
                # Extract ID/enrollment (first word)
                value = display_text.split()[0] if display_text else ""
                
                # Set entry value
                self.entry.delete(0, tk.END)
                self.entry.insert(0, value)
                
                # Trigger KeyRelease event to update details
                self.entry.event_generate('<KeyRelease>')
        except Exception as e:
            print(f"Selection error: {e}")
        finally:
            self._close_dropdown(None)
    
    def _on_down_arrow(self, event):
        """Navigate down in listbox"""
        if self.dropdown and self.listbox:
            current = self.listbox.curselection()
            if current:
                idx = current[0]
                if idx < self.listbox.size() - 1:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(idx + 1)
                    self.listbox.activate(idx + 1)
                    self.listbox.see(idx + 1)
            return 'break'
    
    def _on_up_arrow(self, event):
        """Navigate up in listbox"""
        if self.dropdown and self.listbox:
            current = self.listbox.curselection()
            if current:
                idx = current[0]
                if idx > 0:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(idx - 1)
                    self.listbox.activate(idx - 1)
                    self.listbox.see(idx - 1)
            return 'break'
    
    def _on_return(self, event):
        """Select current item on Enter"""
        if self.dropdown and self.listbox:
            self._on_select()
            return 'break'
    
    def _close_dropdown(self, event):
        """Close dropdown"""
        if self.dropdown:
            try:
                self.dropdown.destroy()
                self.dropdown = None
                self.listbox = None
            except:
                pass
    
    def _schedule_close(self):
        """Schedule dropdown close (after small delay to allow clicks)"""
        self.entry.after(200, lambda: self._close_dropdown(None))
    
    def get(self):
        """Get entry value"""
        return self.entry.get()
    
    def delete(self, start, end):
        """Delete entry content"""
        self.entry.delete(start, end)
    
    def insert(self, index, string):
        """Insert into entry"""
        self.entry.insert(index, string)
    
    def pack(self, **kwargs):
        """Pack entry"""
        self.entry.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid entry"""
        self.entry.grid(**kwargs)
    
    def focus(self):
        """Focus entry"""
        self.entry.focus()
    
    def bind(self, event, callback):
        """Bind event to entry"""
        self.entry.bind(event, callback)
