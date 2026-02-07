#!/usr/bin/env python3
"""
REPORT TAB CODE - Extracted from LibraryApp/main.py
Author: Yash Date
Date: January 31, 2026

This file contains the complete code for the Reports Tab functionality
including all methods for creating report cards, previewing, and exporting
to Excel and PDF formats.

Dependencies:
- tkinter
- tkcalendar (for date pickers)
- pandas
- reportlab
- xlsxwriter

Report Types:
1. Students Report - Complete roster of students
2. Books Catalog - Library inventory
3. Transactions Log - Loan/return history
4. Overdue Analysis - Overdue books tracking
5. Promotion History - Student year progressions
6. Admin Activity Audit - System audit trail

Features:
- Calendar date pickers for filtering
- Quick date presets (7 days, 30 days, this year)
- Type-specific filters (year, category, status)
- Preview before export
- Export to Excel with professional formatting
- Export to PDF with college branding
- Optional date range filtering
- No mandatory filters
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import os
import sqlite3
import pandas as pd
from tkinter import font
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

try:
    from tkcalendar import DateEntry
except Exception:
    DateEntry = None

# ============================================================================
# REPORT TAB CREATION METHOD
# ============================================================================

def create_reports_tab(self):
    """Create enhanced reports tab with calendar date pickers and improved UI"""
    reports_frame = tk.Frame(self.notebook, bg='#f0f2f5')
    self.notebook.add(reports_frame, text="📄 Reports")
    
    # Main scrollable container
    canvas = tk.Canvas(reports_frame, bg='#f0f2f5', highlightthickness=0)
    scrollbar = ttk.Scrollbar(reports_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#f0f2f5')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def resize_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind('<Configure>', resize_frame)
    
    # Mouse wheel scrolling
    def _on_mousewheel(event):
        try:
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
    
    def bind_mousewheel(widget):
        widget.bind("<MouseWheel>", _on_mousewheel)
        for child in widget.winfo_children():
            bind_mousewheel(child)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Enhanced Header with gradient effect simulation
    header_frame = tk.Frame(scrollable_frame, bg='white', relief='flat', bd=0)
    header_frame.pack(fill=tk.X, padx=30, pady=(20, 15))
    
    # Add subtle shadow
    shadow = tk.Frame(scrollable_frame, bg='#d0d0d0', height=2)
    shadow.pack(fill=tk.X, padx=30)
    
    header_content = tk.Frame(header_frame, bg='white')
    header_content.pack(fill=tk.X, padx=30, pady=20)
    
    title_container = tk.Frame(header_content, bg='white')
    title_container.pack(anchor='w')
    
    tk.Label(
        title_container,
        text="📄",
        font=('Segoe UI', 36),
        bg='white',
        fg=self.colors['secondary']
    ).pack(side=tk.LEFT)
    
    title_text_frame = tk.Frame(title_container, bg='white')
    title_text_frame.pack(side=tk.LEFT, padx=(15, 0))
    
    tk.Label(
        title_text_frame,
        text="Reports & Export Center",
        font=('Segoe UI', 26, 'bold'),
        bg='white',
        fg='#1a1a2e'
    ).pack(anchor='w')
    
    tk.Label(
        title_text_frame,
        text="📊 Export comprehensive reports • 📅 Use calendar to select dates • 🎯 No mandatory filters",
        font=('Segoe UI', 11),
        bg='white',
        fg='#666'
    ).pack(anchor='w', pady=(3, 0))
    
    # Content area
    content_frame = tk.Frame(scrollable_frame, bg='#f0f2f5')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
    
    # Helper function to create enhanced report cards with calendar
    def create_report_card(parent, title, icon, description, color, report_type):
        # Card with shadow
        card_container = tk.Frame(parent, bg='#f0f2f5')
        
        shadow_frame = tk.Frame(card_container, bg='#c8c8c8')
        shadow_frame.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
        
        card = tk.Frame(shadow_frame, bg='white', padx=30, pady=25)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Card header with icon
        header = tk.Frame(card, bg='white')
        header.pack(fill=tk.X, pady=(0, 12))
        
        # Larger, rounded icon
        icon_frame = tk.Frame(header, bg=color, width=50, height=50)
        icon_frame.pack(side=tk.LEFT)
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=('Segoe UI', 22),
            bg=color,
            fg='white'
        )
        icon_label.pack(expand=True)
        
        title_frame = tk.Frame(header, bg='white')
        title_frame.pack(side=tk.LEFT, padx=(15, 0), fill=tk.X, expand=True)
        
        tk.Label(
            title_frame,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#1a1a2e'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text=description,
            font=('Segoe UI', 10),
            bg='white',
            fg='#777',
            justify='left',
            wraplength=350
        ).pack(anchor='w', pady=(2, 0))
        
        # Separator
        sep = tk.Frame(card, bg='#e0e0e0', height=1)
        sep.pack(fill=tk.X, pady=(0, 15))
        
        # Filters section - OPTIONAL
        filters_section = tk.Frame(card, bg='#f8f9fa', relief='flat')
        filters_section.pack(fill=tk.X, pady=(0, 15))
        
        filters_header = tk.Frame(filters_section, bg='#f8f9fa')
        filters_header.pack(fill=tk.X, padx=15, pady=(12, 8))
        
        tk.Label(
            filters_header,
            text="🔍 Optional Filters",
            font=('Segoe UI', 11, 'bold'),
            bg='#f8f9fa',
            fg='#333'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            filters_header,
            text="(Leave empty to export all data)",
            font=('Segoe UI', 9, 'italic'),
            bg='#f8f9fa',
            fg='#888'
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Date range with calendar pickers
        date_frame = tk.Frame(filters_section, bg='#f8f9fa')
        date_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # From Date
        from_container = tk.Frame(date_frame, bg='#f8f9fa')
        from_container.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(
            from_container,
            text="📅 From Date:",
            font=('Segoe UI', 9, 'bold'),
            bg='#f8f9fa',
            fg='#555'
        ).pack(anchor='w')
        
        try:
            from_cal = DateEntry(
                from_container,
                width=15,
                background=color,
                foreground='white',
                borderwidth=2,
                font=('Segoe UI', 10),
                date_pattern='yyyy-mm-dd'
            )
            from_cal.pack(pady=(3, 0))
            # Clear initial date
            from_cal.delete(0, tk.END)
        except Exception:
            from_cal = tk.Entry(from_container, font=('Segoe UI', 10), width=15)
            from_cal.pack(pady=(3, 0))
        
        # To Date
        to_container = tk.Frame(date_frame, bg='#f8f9fa')
        to_container.pack(side=tk.LEFT)
        
        tk.Label(
            to_container,
            text="📅 To Date:",
            font=('Segoe UI', 9, 'bold'),
            bg='#f8f9fa',
            fg='#555'
        ).pack(anchor='w')
        
        try:
            to_cal = DateEntry(
                to_container,
                width=15,
                background=color,
                foreground='white',
                borderwidth=2,
                font=('Segoe UI', 10),
                date_pattern='yyyy-mm-dd'
            )
            to_cal.pack(pady=(3, 0))
            # Clear initial date
            to_cal.delete(0, tk.END)
        except Exception:
            to_cal = tk.Entry(to_container, font=('Segoe UI', 10), width=15)
            to_cal.pack(pady=(3, 0))
        
        # Quick date presets
        preset_frame = tk.Frame(date_frame, bg='#f8f9fa')
        preset_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        tk.Label(
            preset_frame,
            text="⚡ Quick:",
            font=('Segoe UI', 9, 'bold'),
            bg='#f8f9fa',
            fg='#555'
        ).pack(anchor='w')
        
        preset_btns = tk.Frame(preset_frame, bg='#f8f9fa')
        preset_btns.pack(pady=(3, 0))
        
        def set_last_7_days():
            from_cal.delete(0, tk.END)
            to_cal.delete(0, tk.END)
            from_cal.insert(0, (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
            to_cal.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def set_last_30_days():
            from_cal.delete(0, tk.END)
            to_cal.delete(0, tk.END)
            from_cal.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
            to_cal.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def set_this_year():
            from_cal.delete(0, tk.END)
            to_cal.delete(0, tk.END)
            from_cal.insert(0, f"{datetime.now().year}-01-01")
            to_cal.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def clear_dates():
            from_cal.delete(0, tk.END)
            to_cal.delete(0, tk.END)
        
        for text, cmd, bg_col in [
            ("7 Days", set_last_7_days, '#007bff'),
            ("30 Days", set_last_30_days, '#007bff'),
            ("This Year", set_this_year, '#007bff'),
            ("Clear", clear_dates, '#6c757d')
        ]:
            btn = tk.Button(
                preset_btns,
                text=text,
                font=('Segoe UI', 8),
                bg=bg_col,
                fg='white',
                relief='flat',
                padx=8,
                pady=3,
                cursor='hand2',
                command=cmd
            )
            btn.pack(side=tk.LEFT, padx=2)
            
            # Hover effect
            def on_enter(e, b=btn, col=bg_col):
                if col == '#6c757d':
                    b.config(bg='#5a6268')
                else:
                    b.config(bg='#0056b3')
            
            def on_leave(e, b=btn, col=bg_col):
                b.config(bg=col)
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # Additional type-specific filters
        filter_var = tk.StringVar(value="All")
        
        if report_type in ["students", "books", "transactions"]:
            type_filter_frame = tk.Frame(filters_section, bg='#f8f9fa')
            type_filter_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
            
            if report_type == "students":
                label_text = "👥 Year Filter:"
                values = ["All", "1st Year", "2nd Year", "3rd Year", "Pass Out"]
            elif report_type == "books":
                label_text = "📚 Category Filter:"
                values = ["All", "Technology", "Textbook", "Research"]
            else:  # transactions
                label_text = "📖 Status Filter:"
                values = ["All", "Active", "Returned", "Overdue"]
            
            tk.Label(
                type_filter_frame,
                text=label_text,
                font=('Segoe UI', 9, 'bold'),
                bg='#f8f9fa',
                fg='#555'
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            filter_combo = ttk.Combobox(
                type_filter_frame,
                textvariable=filter_var,
                values=values,
                state="readonly",
                width=20,
                font=('Segoe UI', 10)
            )
            filter_combo.pack(side=tk.LEFT)
        
        # Export buttons section
        export_section = tk.Frame(card, bg='white')
        export_section.pack(fill=tk.X, pady=(5, 0))
        
        def get_filter_values():
            date_from = from_cal.get().strip() if hasattr(from_cal, 'get') else ""
            date_to = to_cal.get().strip() if hasattr(to_cal, 'get') else ""
            return date_from, date_to, filter_var.get()
        
        # Preview button
        preview_btn = tk.Button(
            export_section,
            text="👁️ Preview Data",
            font=('Segoe UI', 11, 'bold'),
            bg='#17a2b8',
            fg='white',
            relief='flat',
            padx=25,
            pady=12,
            cursor='hand2',
            command=lambda: self._preview_report(report_type, *get_filter_values())
        )
        preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Excel button
        excel_btn = tk.Button(
            export_section,
            text="📊 Export Excel",
            font=('Segoe UI', 11, 'bold'),
            bg='#28a745',
            fg='white',
            relief='flat',
            padx=25,
            pady=12,
            cursor='hand2',
            command=lambda: self._export_report(report_type, 'excel', *get_filter_values())
        )
        excel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # PDF button
        pdf_btn = tk.Button(
            export_section,
            text="📑 Export PDF",
            font=('Segoe UI', 11, 'bold'),
            bg='#dc3545',
            fg='white',
            relief='flat',
            padx=25,
            pady=12,
            cursor='hand2',
            command=lambda: self._export_report(report_type, 'pdf', *get_filter_values())
        )
        pdf_btn.pack(side=tk.LEFT)
        
        # Hover effects with smooth transitions
        def create_hover(btn, normal_bg, hover_bg):
            def on_enter(e):
                btn.config(bg=hover_bg)
            def on_leave(e):
                btn.config(bg=normal_bg)
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        create_hover(preview_btn, '#17a2b8', '#138496')
        create_hover(excel_btn, '#28a745', '#218838')
        create_hover(pdf_btn, '#dc3545', '#c82333')
        
        return card_container
    
    # Create report cards in 2-column grid
    # Row 1: Students and Books
    row1 = tk.Frame(content_frame, bg='#f0f2f5')
    row1.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    row1.grid_columnconfigure(0, weight=1)
    row1.grid_columnconfigure(1, weight=1)
    
    students_card = create_report_card(
        row1,
        "Students Report",
        "👥",
        "Complete roster of all registered students with enrollment details and academic information",
        '#2E86AB',
        'students'
    )
    students_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    books_card = create_report_card(
        row1,
        "Books Catalog",
        "📚",
        "Comprehensive library inventory with book status, categories, and availability",
        '#28a745',
        'books'
    )
    books_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
    
    # Row 2: Transactions and Overdue
    row2 = tk.Frame(content_frame, bg='#f0f2f5')
    row2.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    row2.grid_columnconfigure(0, weight=1)
    row2.grid_columnconfigure(1, weight=1)
    
    transactions_card = create_report_card(
        row2,
        "Transactions Log",
        "📖",
        "Detailed history of all book loans, returns, and current borrowing status",
        '#6f42c1',
        'transactions'
    )
    transactions_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    overdue_card = create_report_card(
        row2,
        "Overdue Analysis",
        "⚠️",
        "Active overdue books with student contacts, days late, and calculated fines",
        '#dc3545',
        'overdue'
    )
    overdue_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
    
    # Row 3: Promotion and Activity
    row3 = tk.Frame(content_frame, bg='#f0f2f5')
    row3.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    row3.grid_columnconfigure(0, weight=1)
    row3.grid_columnconfigure(1, weight=1)
    
    promotion_card = create_report_card(
        row3,
        "Promotion History",
        "⬆️",
        "Complete record of student year progressions with academic year tracking",
        '#17a2b8',
        'promotions'
    )
    promotion_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    
    activity_card = create_report_card(
        row3,
        "Admin Activity Audit",
        "📋",
        "Comprehensive audit trail of all system operations and administrative actions",
        '#ffc107',
        'admin_activity'
    )
    activity_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
    
    # Bind mousewheel after all widgets created
    self.root.after(100, lambda: bind_mousewheel(scrollable_frame))

# ============================================================================
# HELPER METHODS FOR REPORT TAB
# ============================================================================

def _preview_report(self, report_type, date_from, date_to, filter_value):
    """Preview report data in a dialog before exporting"""
    # Implementation of preview - see main.py for full code
    pass

def _export_report(self, report_type, format_type, date_from, date_to, filter_value):
    """Export report to Excel or PDF format"""
    # Implementation of export - see main.py for full code
    pass

def _export_to_excel(self, data, columns, title, report_type, filter_value, date_from, date_to):
    """Export report data to Excel format with GPAK branding"""
    # Implementation of Excel export - see main.py for full code
    pass

def _export_to_pdf(self, data, columns, title, report_type, filter_value, date_from, date_to):
    """Export report data to PDF format with GPAK branding"""
    # Implementation of PDF export - see main.py for full code
    pass

# ============================================================================
# DATA RETRIEVAL METHODS FOR REPORTS
# ============================================================================

def _get_students_report_data(self, year_filter, date_from, date_to):
    """Get students data for report"""
    # Implementation - see main.py for full code
    pass

def _get_books_report_data(self, category_filter, date_from, date_to):
    """Get books data for report"""
    # Implementation - see main.py for full code
    pass

def _get_transactions_report_data(self, status_filter, date_from, date_to):
    """Get transactions data for report"""
    # Implementation - see main.py for full code
    pass

def _get_overdue_report_data(self, date_from, date_to):
    """Get overdue books data for report"""
    # Implementation - see main.py for full code
    pass

def _get_promotions_report_data(self, date_from, date_to):
    """Get promotion history data for report"""
    # Implementation - see main.py for full code
    pass

def _get_admin_activity_report_data(self, date_from, date_to):
    """Get admin activity log data for report"""
    # Implementation - see main.py for full code
    pass

# ============================================================================
# END OF REPORT TAB CODE
# ============================================================================

"""
USAGE NOTES:
1. This file contains the extracted report tab code from main.py
2. To use this code, copy the methods into your LibraryApp class
3. Ensure all dependencies are installed: pandas, reportlab, xlsxwriter
4. The tab integrates with your database through self.db connection
5. Color scheme uses self.colors dictionary from main LibraryApp
6. Reports are branded with GPAK college logo and information

CUSTOMIZATION TIPS:
- Modify color codes in create_report_card() to change card colors
- Update card descriptions to match your needs
- Adjust filter values to add custom filters
- Modify export formats and headers as needed
- Add more report types by duplicating card creation blocks

For full implementation, refer to LibraryApp/main.py lines 2031-3380
"""
