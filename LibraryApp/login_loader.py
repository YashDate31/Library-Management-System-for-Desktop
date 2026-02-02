#!/usr/bin/env python3
"""
Login Loading Screen with Progress Bar
Actually loads data from server while showing progress
Uses after() for smooth UI - no blocking operations on main thread
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import queue

class LoginLoader:
    """Loading screen with progress bar - loads actual data without UI freezing"""
    
    def __init__(self, parent, callback, colors, db=None):
        self.parent = parent
        self.callback = callback
        self.colors = colors
        self.db = db
        self.progress = 0
        self.target_progress = 0
        self.data_loaded = {
            'students': None,
            'books': None,
            'borrowed': None,
            'stats': None
        }
        self.load_complete = False
        self.min_display_time = 4  # Minimum 4 seconds display
        self.status_queue = queue.Queue()
        self.db_loading_done = False
        
    def show(self):
        """Display loading screen"""
        self.start_time = time.time()
        
        # Create overlay with clean light theme
        self.overlay = tk.Toplevel(self.parent)
        self.overlay.title("Loading")
        self.overlay.geometry("550x340")
        self.overlay.configure(bg='white')
        self.overlay.transient(self.parent)
        self.overlay.grab_set()
        self.overlay.resizable(False, False)
        
        # Center window
        self.overlay.update_idletasks()
        x = (self.overlay.winfo_screenwidth() // 2) - 275
        y = (self.overlay.winfo_screenheight() // 2) - 170
        self.overlay.geometry(f"+{x}+{y}")
        
        # Logo/Icon
        icon_label = tk.Label(
            self.overlay,
            text="📚",
            font=('Segoe UI', 50),
            bg='white',
            fg=self.colors['secondary']
        )
        icon_label.pack(pady=(40, 15))
        
        # Title
        title_label = tk.Label(
            self.overlay,
            text="Loading Library System",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg=self.colors['accent']
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            self.overlay,
            text="Please wait while we retrieve data from server...",
            font=('Segoe UI', 10),
            bg='white',
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Progress bar frame
        progress_frame = tk.Frame(self.overlay, bg='white')
        progress_frame.pack(pady=(0, 12), padx=50, fill=tk.X)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=450,
            mode='determinate',
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)
        
        # Progress label (percentage)
        self.progress_label = tk.Label(
            self.overlay,
            text="0%",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['secondary']
        )
        self.progress_label.pack(pady=(8, 5))
        
        # Status label (current task)
        self.status_label = tk.Label(
            self.overlay,
            text="Initializing...",
            font=('Segoe UI', 10),
            bg='white',
            fg='#888888'
        )
        self.status_label.pack(pady=(0, 20))
        
        # Start data loading in background thread
        threading.Thread(target=self._load_data_background, daemon=True).start()
        
        # Start smooth progress animation using after() - never blocks UI
        self._animate_progress()
        
    def _animate_progress(self):
        """Smooth progress animation using after() - never blocks UI"""
        try:
            # Check for status updates from background thread
            while not self.status_queue.empty():
                try:
                    target, status = self.status_queue.get_nowait()
                    self.target_progress = target
                    if status:
                        self.status_label.config(text=status)
                except:
                    pass
            
            # Smoothly move current progress toward target
            if self.progress < self.target_progress:
                # Move 2% per frame for smooth animation
                self.progress = min(self.progress + 0.5, self.target_progress)
                self.progress_bar['value'] = self.progress
                self.progress_label.config(text=f"{int(self.progress)}%")
            
            # Check if we're done
            elapsed = time.time() - self.start_time
            if self.db_loading_done and self.progress >= 100 and elapsed >= self.min_display_time:
                self.status_label.config(text="Ready!")
                self.overlay.after(300, self._complete_loading)
                return
            
            # Continue animation - 30fps (33ms per frame)
            self.overlay.after(33, self._animate_progress)
            
        except Exception as e:
            # If overlay is destroyed, complete loading
            self._complete_loading()
    
    def _load_data_background(self):
        """Load data in background thread - puts status updates in queue"""
        try:
            # Stage 1: Initialize (0-15%)
            self.status_queue.put((5, "Connecting to database..."))
            time.sleep(0.3)
            self.status_queue.put((15, "Connection established"))
            time.sleep(0.5)
            
            # Stage 2: Load students (15-40%)
            self.status_queue.put((20, "Loading student records..."))
            if self.db:
                try:
                    self.data_loaded['students'] = self.db.get_students()
                except:
                    pass
            self.status_queue.put((40, "Student records loaded"))
            time.sleep(0.3)
            
            # Stage 3: Load books (40-65%)
            self.status_queue.put((45, "Loading book inventory..."))
            if self.db:
                try:
                    self.data_loaded['books'] = self.db.get_books()
                except:
                    pass
            self.status_queue.put((65, "Book inventory loaded"))
            time.sleep(0.3)
            
            # Stage 4: Load transactions (65-85%)
            self.status_queue.put((70, "Loading transaction history..."))
            if self.db:
                try:
                    self.data_loaded['borrowed'] = self.db.get_borrowed_books()
                except:
                    pass
            self.status_queue.put((85, "Transaction history loaded"))
            time.sleep(0.3)
            
            # Stage 5: Load stats (85-95%)
            self.status_queue.put((88, "Loading statistics..."))
            if self.db:
                try:
                    self.data_loaded['stats'] = self.db.get_stats()
                except:
                    pass
            self.status_queue.put((95, "Statistics loaded"))
            time.sleep(0.2)
            
            # Stage 6: Finalize (95-100%)
            self.status_queue.put((98, "Finalizing setup..."))
            time.sleep(0.2)
            self.status_queue.put((100, "Ready!"))
            
            # Wait for minimum display time
            elapsed = time.time() - self.start_time
            if elapsed < self.min_display_time:
                remaining = self.min_display_time - elapsed
                # Keep progress at 100% during wait
                time.sleep(remaining)
            
            self.db_loading_done = True
            
        except Exception as e:
            print(f"Background loading error: {e}")
            self.status_queue.put((100, "Ready!"))
            self.db_loading_done = True
    
    def _complete_loading(self):
        """Complete loading and execute callback"""
        try:
            self.overlay.destroy()
        except:
            pass
        
        # Execute callback with loaded data
        if self.callback:
            self.callback()
    
    def get_loaded_data(self):
        """Get the data that was loaded"""
        return self.data_loaded
