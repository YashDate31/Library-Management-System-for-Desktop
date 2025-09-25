import sys
import os
import tkinter as tk

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import the main application
from main import LibraryManagementApp

if __name__ == "__main__":
    print("🚀 Starting Modern Library Management System...")
    print("📍 Working directory:", os.getcwd())
    
    try:
        root = tk.Tk()
        app = LibraryManagementApp(root)
        print("✅ Application initialized successfully!")
        print("🎨 Modern dark theme activated!")
        print("📚 Database connected!")
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")