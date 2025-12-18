# 📚 Study Materials System - User Guide

## Overview
The Study Materials system allows teachers to share educational resources with students through Google Drive links, keeping the software lightweight while providing easy access to notes, PYQs, and study materials.

---

## 🎯 Key Features

### For Teachers (Desktop App)
- **Upload Study Materials** - Share Google Drive links for notes, PYQs, syllabi
- **Organize by Year** - Categorize materials for 1st, 2nd, or 3rd year students
- **Category Tags** - Label materials as Notes, PYQ, Study Material, Syllabus, or Other
- **Manage Materials** - View, delete, and copy links easily
- **Space Efficient** - Only stores links, not files (saves ~99% storage)

### For Students (Web Portal)
- **Browse Materials** - View all available study resources
- **Filter by Year** - See materials relevant to your year
- **Direct Downloads** - One-click access to Google Drive resources
- **Category Badges** - Visual indicators for material type
- **Mobile Friendly** - Responsive design for phones and tablets

---

## 📖 How to Use (Teacher - Desktop App)

### Step 1: Access Study Materials Tab
1. Open the Library Management System desktop app
2. Log in with your admin credentials (`gpa` / `gpa123`)
3. Click on the **📱 Portal** tab
4. Navigate to the **📚 Study Materials** sub-tab

### Step 2: Upload Material to Google Drive
1. First, upload your file (notes/PYQ/etc.) to **Google Drive**
2. Right-click the file → **Get Link**
3. Set sharing to **"Anyone with the link can view"**
4. Copy the Google Drive share link

### Step 3: Add Material to System
1. In the Upload Form (left side):
   - **Title**: Enter a descriptive name (e.g., "Data Structures Unit 1 Notes")
   - **Description**: Add details (optional)
   - **Google Drive Link**: Paste the link from Step 2
   - **Year**: Select 1st, 2nd, or 3rd year
   - **Category**: Choose Notes, PYQ, Study Material, Syllabus, or Other
2. Click **📤 Upload Material**
3. Material appears in the list immediately!

### Step 4: Manage Materials
- **View All**: See all uploaded materials in the right panel
- **Delete**: Select material → Click **🗑️ Delete**
- **Copy Link**: Select material → Click **🔗 Copy Link**
- **Refresh**: Click **🔄 Refresh** to reload the list

---

## 📱 How to Use (Student - Web Portal)

### Access Study Materials
1. Log in to the Student Portal (enrollment number as username)
2. Click **📚 Study Materials** in the left sidebar
3. Browse available materials

### Filter by Year
- Use the dropdown at top-right to filter:
  - **All Years** - Show everything
  - **1st Year** - First year materials only
  - **2nd Year** - Second year materials only
  - **3rd Year** - Third year materials only

### Download Materials
1. Find the material you need
2. Click the **Download** button
3. You'll be taken directly to Google Drive
4. Download the file from there

---

## 💡 Best Practices

### For Teachers
✅ **Use Descriptive Titles** - "Computer Networks - Unit 3 Notes (2024)"
✅ **Add Context** - Brief description helps students know what to expect
✅ **Organize by Year** - Correctly tag materials for the right year
✅ **Use Shared Drive** - Consider using a dedicated Google Drive folder
✅ **Check Links** - Test links before uploading to ensure they work
✅ **Regular Cleanup** - Remove outdated materials to keep list clean

### For Students
✅ **Download Promptly** - Materials may be updated or removed
✅ **Organize Locally** - Create folders on your device by subject/year
✅ **Check Regularly** - New materials are added throughout the semester
✅ **Verify Downloads** - Ensure files download correctly

---

## 🔧 Technical Details

### Storage Optimization
- **Files NOT stored in software** - Only Google Drive links saved
- **Minimal Database Impact** - ~100 bytes per material entry
- **Scalable** - Can handle thousands of materials without performance issues
- **10-15 Year Longevity** - Software won't bloat over time

### Database Schema
```sql
study_materials table:
- id (Primary Key)
- title (Text)
- description (Text)
- drive_link (Google Drive URL)
- branch (Default: "Computer")
- year (1st/2nd/3rd)
- category (Notes/PYQ/Study Material/etc.)
- uploaded_by (Admin name)
- upload_date (Timestamp)
- active (1/0 for soft delete)
```

### API Endpoints
- `GET /api/study-materials` - List materials (with year filter)
- `POST /api/admin/study-materials` - Add new material
- `DELETE /api/admin/study-materials/:id` - Delete material
- `PUT /api/admin/study-materials/:id` - Update material

---

## ❓ Troubleshooting

### "Failed to upload material"
- ✅ Check if Student Portal is running
- ✅ Verify Google Drive link is shareable
- ✅ Ensure all required fields are filled

### "Cannot access download link"
- ✅ Verify link sharing is set to "Anyone with link"
- ✅ Check if link hasn't expired
- ✅ Try opening in incognito/private window

### "Materials not showing"
- ✅ Click Refresh button
- ✅ Check year filter isn't hiding materials
- ✅ Verify materials are marked as active

---

## 🎓 Tips for Students

### Organize Your Downloads
Create a folder structure like:
```
Computer Engineering/
  ├── 1st Year/
  │   ├── C Programming/
  │   │   ├── Notes/
  │   │   └── PYQs/
  │   └── Mathematics/
  └── 2nd Year/
      └── Data Structures/
```

### Study Smart
- Download materials as soon as they're uploaded
- Review regularly, don't wait for exams
- Create your own notes alongside downloaded materials
- Share feedback with teachers if links are broken

---

## 📞 Support
If you encounter issues:
1. Contact your library administrator
2. Check if Student Portal server is running
3. Verify your internet connection for Google Drive access

---

**Version**: 5.0 FINAL  
**Last Updated**: December 2025  
**Developer**: Yash Vijay Date  
**Institution**: Government Polytechnic, Awasari (Kh.)
