import tkinter as tk
from tkinter import ttk

class StudentsTabHandler:
    def create_students_tab(self):
        """Create students management tab with search, actions, and student list"""
        students_frame = tk.Frame(self.notebook, bg=self.colors['primary'])
        self.notebook.add(students_frame, text="👥 Students")
        
        # Top frame for search and actions
        top_frame = tk.Frame(students_frame, bg=self.colors['primary'])
        top_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Search frame (left side)
        search_frame = tk.LabelFrame(
            top_frame,
            text="🔍 Search & Filter Students",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Search controls
        search_controls = tk.Frame(search_frame, bg=self.colors['primary'])
        search_controls.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_controls, text="Search:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        search_entry = tk.Entry(search_controls, textvariable=self.student_search_var, font=('Segoe UI', 10), width=25)
        search_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(search_controls, text="Year:", bg=self.colors['primary'], fg=self.colors['accent'], font=('Segoe UI', 10)).pack(side=tk.LEFT)
        year_combo = ttk.Combobox(search_controls, textvariable=self.student_year_filter, values=["All", "1st", "2nd", "3rd", "4th"], state="readonly", width=10)
        year_combo.pack(side=tk.LEFT, padx=5)
        year_combo.bind('<<ComboboxSelected>>', lambda e: self.search_students())
        
        # Actions frame (right side)
        actions_frame = tk.LabelFrame(
            top_frame,
            text="⚡ Actions",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        actions_frame.pack(side=tk.RIGHT)
        
        # Action buttons
        buttons_frame = tk.Frame(actions_frame, bg=self.colors['primary'])
        buttons_frame.pack(padx=10, pady=10)
        
        # Add Student button
        add_student_btn = tk.Button(
            buttons_frame,
            text="➕ Add Student",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.show_add_student_dialog,
            cursor='hand2'
        )
        add_student_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Import Excel button
        import_students_btn = tk.Button(
            buttons_frame,
            text="📥 Import Excel",
            font=('Segoe UI', 10, 'bold'),
            bg='#6f42c1',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.import_students_from_excel,
            cursor='hand2'
        )
        import_students_btn.pack(side=tk.LEFT, padx=5)
        
        # Students list frame
        students_list_frame = tk.LabelFrame(
            students_frame,
            text="📋 Students List",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['accent'],
            padx=10,
            pady=10
        )
        students_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Students treeview with scrollbars
        columns = ('Enrollment No', 'Name', 'Email', 'Phone', 'Year')
        self.students_tree = ttk.Treeview(students_list_frame, columns=columns, show='headings', height=15)
        
        # Configure column headings and widths
        col_widths = {'Enrollment No': 120, 'Name': 150, 'Email': 180, 'Phone': 120, 'Year': 80}
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=col_widths[col])
        
        # Create scrollbars
        students_v_scrollbar = ttk.Scrollbar(students_list_frame, orient=tk.VERTICAL, command=self.students_tree.yview)
        students_h_scrollbar = ttk.Scrollbar(students_list_frame, orient=tk.HORIZONTAL, command=self.students_tree.xview)
        
        # Configure scrollbars
        self.students_tree.configure(yscrollcommand=students_v_scrollbar.set, xscrollcommand=students_h_scrollbar.set)
        
        # Pack everything
        self.students_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        students_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        students_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind search function
        search_entry.bind('<KeyRelease>', lambda e: self.search_students())