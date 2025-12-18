# Study Materials Feature - Changes Summary

## Overview
Changed the Study Materials system from **Google Drive links** to **direct file uploads** through the software.

## What Changed

### 1. **Backend (student_portal.py)**
- **File Upload Support**: Added multipart/form-data handling for file uploads
- **File Storage**: Files are saved in `Web-Extension/uploads/study_materials/` directory
- **Allowed File Types**: pdf, doc, docx, ppt, pptx, txt, jpg, jpeg, png, zip, rar
- **Database Schema Updated**:
  - Removed: `drive_link` column
  - Added: `filename`, `original_filename`, `file_size` columns
- **New Endpoints**:
  - POST `/api/admin/study-materials` - Upload file with multipart/form-data
  - GET `/api/study-materials/<id>/download` - Download file

### 2. **Desktop App (main.py)**
- **File Selection**: Replaced text input for "Google Drive Link" with file picker button
- **Upload Method**: Changed from JSON (urllib) to multipart/form-data (requests library)
- **UI Updates**:
  - Added "📁 Browse" button for file selection
  - Shows selected filename before upload
  - Removed "Copy Link" button (no longer applicable)
- **New Function**: `_browse_study_material_file()` - Opens file dialog

### 3. **Student Portal Frontend (StudyMaterials.jsx)**
- **Download Links**: Changed from external Google Drive links to internal download endpoint
- **Download URL**: Now uses `/api/study-materials/${material.id}/download`
- **Download Behavior**: Files download directly instead of opening in new tab

### 4. **Dependencies (requirements.txt)**
- Added: `requests` library for multipart file upload in desktop app

## How It Works Now

### For Teachers (Desktop App):
1. Open "Study Materials" tab in Portal section
2. Fill in title, description, year, and category
3. Click "📁 Browse" to select a file from your computer
4. Click "Upload" - file is uploaded to server
5. File appears in the materials list immediately

### For Students (Web Portal):
1. Navigate to "Study Materials" page
2. Browse materials by year filter
3. Click "Download" button on any material
4. File downloads directly to their device

## File Storage

- **Location**: `LibraryApp/Web-Extension/uploads/study_materials/`
- **Naming**: Files are saved with timestamp prefix (e.g., `1234567890_notes.pdf`)
- **Soft Delete**: When deleted, files are marked as inactive but not removed from disk
- **File Size**: Tracked in database for future reference

## Migration Notes

- **Old Data**: Existing materials with `drive_link` will need manual migration
- **Database**: Run migration to update schema (handled automatically on first run)
- **Storage Impact**: Direct uploads require more disk space than links
- **Recommended**: Start fresh with new uploads after update

## Benefits

✅ No need for Google Drive account or link sharing  
✅ Everything managed within the software  
✅ Faster downloads for students (local server)  
✅ No external dependencies  
✅ Better control over content  
✅ Works offline (no internet needed for downloads)

## Considerations

⚠️ Increased storage usage (files stored locally)  
⚠️ File size limits (can be configured in backend)  
⚠️ Backup responsibility shifts to you (no cloud backup)  
⚠️ Network speed affects upload time for large files

## Technical Details

### File Upload Flow:
1. User selects file in desktop app
2. File is sent as multipart/form-data to Flask backend
3. Backend validates file type using `allowed_file()` function
4. File is saved with unique timestamp-prefixed name
5. Metadata stored in database (filename, size, upload date)
6. Frontend fetches list and displays materials
7. Students click download → file served via Flask's `send_file()`

### Security:
- Filename sanitization using `secure_filename()`
- File type validation (only allowed extensions)
- Files served through controlled endpoint
- No direct access to upload directory

---

**Date**: January 2025  
**Status**: ✅ Complete and Tested
