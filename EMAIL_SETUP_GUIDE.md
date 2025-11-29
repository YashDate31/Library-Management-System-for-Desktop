# 📧 Email Setup Guide - Library Management System

## New Feature: Automatic Overdue Letter Email Sending

When you double-click on an overdue student in the Records tab, the system will now:
1. Generate the overdue letter Word document
2. **Automatically send it to the student's email** (if email is enabled and student has email)
3. Save the document to your chosen location

---

## How to Set Up Email Sending

### Step 1: Configure Gmail App Password

1. **Enable 2-Step Verification** on your Gmail account:
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or "Other")
   - Click "Generate"
   - Copy the 16-character password (it will look like: `xxxx xxxx xxxx xxxx`)

### Step 2: Configure Email in the App

1. Click the **📧 Email** button in the top-right header of the app
2. Check **"Enable automatic email sending"**
3. Fill in:
   - **SMTP Server**: `smtp.gmail.com` (default)
   - **SMTP Port**: `587` (default)
   - **Your Gmail Address**: `your.email@gmail.com`
   - **Gmail App Password**: Paste the 16-character password from Step 1
4. Click **💾 Save Settings**

---

## How It Works

### When Email is Enabled:
1. Double-click an overdue student
2. The system:
   - Generates the Word document
   - **Sends it automatically to the student's email** (if student has email address)
   - Saves the document locally
   - Shows success message with email status

### When Email is Not Enabled:
1. Double-click an overdue student
2. The system:
   - Generates the Word document
   - Saves it locally only
   - Shows a tip to enable email

---

## Important Notes

✅ **Student Email Required**: Make sure students have email addresses in their records. Add/edit email in the Students tab.

✅ **Gmail Security**: Use App Password, NOT your regular Gmail password. This is more secure.

✅ **Internet Required**: Email sending requires active internet connection.

✅ **Email Status**: After sending, you'll see whether the email was sent successfully or if there was an error.

---

## Troubleshooting

### "Authentication failed" Error
- Double-check your Gmail address and App Password
- Make sure you're using the App Password, not your regular password
- Verify 2-Step Verification is enabled

### "Student email address is not available"
- Add the student's email address in the Students tab
- Edit the student record and fill in the Email field

### Email Not Sending
- Check your internet connection
- Make sure "Enable automatic email sending" is checked
- Verify email settings are saved correctly

---

## Security Notes

🔒 Email settings are stored locally in `email_settings.json` next to your app
🔒 Your password is stored in plain text locally - keep your computer secure
🔒 Consider using a dedicated Gmail account for the library system

---

## Questions?

Contact the developer:
- **Name**: Yash Vijay Date
- **Enrollment**: 24210270230
- **Branch**: Computer Engineering
- **Year**: 2nd Year
