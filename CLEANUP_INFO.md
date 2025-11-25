# Automatic Cleanup Feature

## Overview

The Flask app now automatically cleans up temporary files whenever a new instance starts. This prevents disk space waste from old processing runs.

## What Gets Cleaned Up

### 1. Upload Folder (`uploads/`)
- All processed PDF files from previous sessions
- These are the final output files that users download
- Location: `/home/parag/Desktop/invert-pdf-color/uploads/`

### 2. System Temp Directories
- Temporary processing directories created by previous runs
- Pattern: `invert_pdf_*` in system temp folder
- Location: `/tmp/invert_pdf_*` (Linux/Mac) or `C:\Temp\invert_pdf_*` (Windows)
- Contains:
  - Original uploaded PDF
  - Extracted page images
  - Inverted images
  - Work directories

## How It Works

### Cleanup Function
```python
def cleanup_temp_files():
    """Clean up temporary files on startup"""
    # 1. Clean uploads folder
    # 2. Clean system temp directories
    # 3. Log all cleanup operations
```

### Execution
- Runs automatically on Flask app startup
- Executes before the web server starts accepting requests
- Logs all cleanup operations to `logs/app.log`

### Example Log Output
```
[INFO] Cleaned up old upload: inverted_document.pdf
[INFO] Cleaned up old upload: inverted_report.pdf
[INFO] Cleaned up old temp directory: invert_pdf_abc123
[INFO] Cleaned up old temp directory: invert_pdf_xyz789
[INFO] Startup cleanup complete
```

## Benefits

✅ **Automatic** - No manual intervention needed  
✅ **Safe** - Only removes files created by this app  
✅ **Fresh Start** - Each session starts with a clean slate  
✅ **Disk Space** - Prevents accumulation of old files  
✅ **No Data Loss** - Users download files before they're cleaned  

## During-Processing Cleanup

Temporary files are also cleaned up **after each processing operation**:

1. User uploads PDF → Temp directory created
2. Processing runs → Files created in temp directory
3. Output copied to uploads folder
4. **Temp directory deleted immediately**
5. User downloads file from uploads folder

On next app restart:
6. **Uploads folder cleaned** (old downloads removed)

## File Lifecycle

```
Upload PDF
   ↓
Create temp dir (/tmp/invert_pdf_XXXXX/)
   ↓
Process (extract → invert → build)
   ↓
Copy to uploads/ folder
   ↓
Delete temp dir ✓ (immediate)
   ↓
User downloads from uploads/
   ↓
[App Restart]
   ↓
Clean uploads/ folder ✓ (startup)
```

## Customization

If you want to keep uploaded files between sessions, comment out this section in `app.py`:

```python
# In cleanup_temp_files():
# Comment out to keep uploads:
# for file in uploads_dir.iterdir():
#     if file.is_file():
#         file.unlink()
```

## Disk Space Management

Typical space usage per PDF:
- **Small PDF (10 pages, 200 DPI)**: ~50MB temp space
- **Large PDF (100 pages, 300 DPI)**: ~500MB temp space

Without cleanup:
- Multiple processing runs accumulate
- Disk space fills up over time

With cleanup:
- Only current session files exist
- Maximum disk usage = single operation

## Logging

All cleanup operations are logged:
- Location: `logs/app.log`
- Level: INFO
- Includes: Filenames, directory names, errors (if any)

To view cleanup logs:
```bash
grep "Cleaned up" logs/app.log
```

## Error Handling

If cleanup fails for a file/directory:
- Warning logged (not error)
- App continues to start normally
- Common causes:
  - File in use by another process
  - Permission denied
  - File already deleted

Example warning:
```
[WARNING] Could not remove invert_pdf_abc123: [Errno 13] Permission denied
```

## Manual Cleanup

If needed, manually clean up:

```bash
# Clean uploads
rm -rf uploads/*

# Clean system temp
rm -rf /tmp/invert_pdf_*
```

## Summary

🧹 **Automatic cleanup on startup** keeps your disk clean  
🚀 **No performance impact** - cleanup runs before requests  
📝 **Fully logged** - all operations tracked  
🛡️ **Safe** - only removes app-generated files  

Your PDF inverter now maintains itself! 🎉
