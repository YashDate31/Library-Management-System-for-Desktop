#!/usr/bin/env python3
"""
Batch Email Service with Threading
Sends emails in parallel batches to prevent UI freezing
"""

import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time
from queue import Queue
from datetime import datetime
import os

class EmailBatchService:
    """Handles batch email sending with progress tracking"""
    
    def __init__(self, max_workers=5, batch_size=10):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.email_queue = Queue()
        self.results = []
        self.progress_callback = None
        self.is_cancelled = False
        
    def send_batch_emails(self, email_list, email_config, progress_callback=None):
        """
        Send emails in batches with progress tracking
        
        Args:
            email_list: List of dicts with 'to', 'subject', 'body', 'attachment' keys
            email_config: Dict with SMTP settings
            progress_callback: Function to call with progress updates
        
        Returns:
            Dict with success/failure statistics
        """
        self.progress_callback = progress_callback
        self.results = []
        self.is_cancelled = False
        
        # Add all emails to queue
        for email in email_list:
            self.email_queue.put(email)
        
        total_emails = len(email_list)
        sent_count = 0
        failed_count = 0
        
        # Process in batches
        while not self.email_queue.empty() and not self.is_cancelled:
            batch = []
            
            # Get batch
            for _ in range(min(self.batch_size, self.email_queue.qsize())):
                try:
                    batch.append(self.email_queue.get_nowait())
                except:
                    break
            
            if not batch:
                break
            
            # Send batch using thread pool
            threads = []
            for email_data in batch[:self.max_workers]:
                thread = threading.Thread(
                    target=self._send_single_email,
                    args=(email_data, email_config)
                )
                thread.daemon = True
                thread.start()
                threads.append(thread)
            
            # Wait for batch to complete
            for thread in threads:
                thread.join(timeout=30)  # 30 second timeout per thread
            
            # Update progress
            sent_count += len(batch)
            progress = (sent_count / total_emails) * 100
            
            if self.progress_callback:
                self.progress_callback(sent_count, total_emails, progress)
            
            # Small delay between batches
            time.sleep(0.5)
        
        # Calculate statistics
        success_count = sum(1 for r in self.results if r['success'])
        failed_count = len(self.results) - success_count
        
        return {
            'total': total_emails,
            'sent': success_count,
            'failed': failed_count,
            'cancelled': self.is_cancelled,
            'details': self.results
        }
    
    def _send_single_email(self, email_data, email_config):
        """Send a single email"""
        result = {
            'to': email_data.get('to', ''),
            'subject': email_data.get('subject', ''),
            'success': False,
            'error': None,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config.get('from_email', '')
            msg['To'] = email_data['to']
            msg['Subject'] = email_data['subject']
            
            # Add body
            msg.attach(MIMEText(email_data['body'], 'html'))
            
            # Add attachment if present
            if email_data.get('attachment'):
                attachment_path = email_data['attachment']
                if os.path.exists(attachment_path):
                    with open(attachment_path, 'rb') as f:
                        attachment = MIMEApplication(f.read())
                        attachment.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=os.path.basename(attachment_path)
                        )
                        msg.attach(attachment)
            
            # Send email with timeout
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'], timeout=10) as server:
                server.starttls()
                server.login(email_config['from_email'], email_config['password'])
                server.send_message(msg)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        self.results.append(result)
        return result
    
    def cancel(self):
        """Cancel ongoing email sending"""
        self.is_cancelled = True


def send_overdue_emails_async(students_data, email_config, progress_callback=None):
    """
    Convenience function to send overdue emails
    
    Args:
        students_data: List of dicts with student info and overdue details
        email_config: SMTP configuration
        progress_callback: Function to call with progress (sent, total, percentage)
    
    Returns:
        Statistics dictionary
    """
    service = EmailBatchService(max_workers=5, batch_size=10)
    
    # Prepare email list
    email_list = []
    for student in students_data:
        email_list.append({
            'to': student['email'],
            'subject': f"Overdue Book Reminder - {student['name']}",
            'body': generate_overdue_email_body(student),
            'attachment': None
        })
    
    # Send in background thread
    def send_thread():
        return service.send_batch_emails(email_list, email_config, progress_callback)
    
    thread = threading.Thread(target=send_thread, daemon=True)
    thread.start()
    
    return service  # Return service to allow cancellation


def generate_overdue_email_body(student_data):
    """Generate HTML email body for overdue notice"""
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .header {{ background-color: #003366; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .book-list {{ background-color: #f5f5f5; padding: 15px; margin: 10px 0; }}
            .footer {{ background-color: #f0f0f0; padding: 10px; text-align: center; font-size: 12px; }}
            .fine {{ color: #d9534f; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>INSTITUTE OF AERONAUTICAL ENGINEERING</h2>
            <p>Library Management System</p>
        </div>
        <div class="content">
            <p>Dear {student_data['name']},</p>
            <p>This is a reminder that you have overdue book(s) from our library:</p>
            <div class="book-list">
                <p><strong>Book ID:</strong> {student_data.get('book_id', 'N/A')}</p>
                <p><strong>Title:</strong> {student_data.get('book_title', 'N/A')}</p>
                <p><strong>Due Date:</strong> {student_data.get('due_date', 'N/A')}</p>
                <p><strong>Days Overdue:</strong> {student_data.get('days_overdue', 0)}</p>
                <p class="fine"><strong>Fine Amount:</strong> ₹{student_data.get('fine', 0)}</p>
            </div>
            <p>Please return the book(s) at your earliest convenience to avoid additional fines.</p>
            <p>For any queries, please contact the library administration.</p>
        </div>
        <div class="footer">
            <p>IARE Library | Dundigal, Hyderabad - 500043</p>
            <p>This is an automated email. Please do not reply.</p>
        </div>
    </body>
    </html>
    """
