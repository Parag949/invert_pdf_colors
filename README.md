# invert-pdf-color

A Flask web application to invert PDF colors by converting pages to images, inverting them, and recombining to a PDF.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py
# Or: ./run.sh

# 3. Open browser
# Visit: http://localhost:5000
```

That's it! Upload a PDF, click process, and download your inverted PDF.

## Project structure

```
root/
├── app.py                     # Flask web application (main entry point)
├── run.sh                     # Quick startup script
├── requirements.txt           # Python dependencies
├── setup.py                   # Package metadata
├── src/
│   └── invert_pdf_colors/
│       ├── __init__.py
│       ├── exception.py       # Custom exceptions
│       ├── logger.py          # Logging configuration
│       ├── utils.py           # Utility functions
│       ├── components/        # Core processing components (parallel optimized)
│       │   ├── images_to_pdf.py
│       │   ├── invert_images.py
│       │   └── pdf_to_images.py
│       └── pipeline/          # Processing pipeline
│           └── process_pipeline.py
├── templates/                 # HTML templates for web UI
│   ├── index.html
│   └── home.html
├── logs/                      # Log files (auto-created)
└── uploads/                   # Temporary storage for web uploads (auto-created)
```

## Requirements

- Python 3.8+
- ImageMagick and Ghostscript installed on your system (required by `wand` for PDF rendering)

### System Dependencies (Linux)

```bash
sudo apt-get update
sudo apt-get install -y imagemagick ghostscript
```

**Important**: ImageMagick policy must allow PDF read. If you see `not authorized` errors, edit `/etc/ImageMagick-6/policy.xml` (or IM7 path) and change the PDF policy from `none` to `read|write`:

```xml
<policy domain="coder" rights="read|write" pattern="PDF" />
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

Or if using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Start the Flask web application:

```bash
python app.py
```

Then open your browser to:
- **http://localhost:5000** (or http://127.0.0.1:5000)

### Features:
- 📤 **Drag & drop PDF upload** - Simply drag your PDF or click to browse
- ⚙️ **Adjustable DPI settings** - Control quality for extraction and output
- 📊 **Progress indicator** - Real-time feedback during processing
- 💾 **Automatic download** - Get your inverted PDF immediately
- 🎨 **Modern UI** - Clean, responsive interface
- 📝 **Comprehensive logging** - All operations logged to `logs/app.log`
- 🧹 **Automatic cleanup** - Removes temporary files on startup

## How It Works

1. **PDF to Images**: Extracts each page of the PDF as a high-resolution image using Wand (ImageMagick) with **parallel thread processing**
2. **Color Inversion**: Inverts the colors of each image using Pillow with **multiprocessing for maximum CPU utilization**
3. **Images to PDF**: Combines all inverted images back into a single PDF with **parallel image loading**

### Performance Optimizations

- ⚡ **Multi-core Processing**: Uses all available CPU cores for image inversion
- 🚀 **Parallel Extraction**: Multiple threads extract PDF pages simultaneously
- 📦 **Concurrent Loading**: Images loaded in parallel when building output PDF
- 🎯 **Optimized Workers**: Automatically scales to your CPU count

## Logs

Application logs are written to `logs/app.log` with rotation enabled.

## Performance Notes

- **No file size limit** - Process any size PDF
- Processing time depends on PDF size and DPI settings
- Lower DPI = faster processing, smaller file size
- Higher DPI = better quality, larger file size
- Recommended settings: Extract DPI 200, Output DPI 300

### Speed Improvements

- **Multi-page PDFs**: Up to **N×** faster (where N = CPU cores)
- **Image inversion**: Utilizes **all CPU cores** via multiprocessing
- **PDF extraction**: Parallel thread processing for I/O operations
- **Automatic scaling**: Adjusts worker count to your hardware

Example: 50-page PDF on 8-core CPU → ~8× faster inversion!

## Troubleshooting

**ModuleNotFoundError: No module named 'flask'**
- Activate your virtual environment or install Flask: `pip install Flask`

**wand.exceptions.PolicyError: not authorized**
- Edit ImageMagick policy as described in System Dependencies section

**Memory issues with large PDFs**
- Reduce DPI settings (try 150 for extract, 200 for output)
- Process smaller batches of pages

## Development

To set up for development:

```bash
git clone <repository-url>
cd invert-pdf-color
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The application will be available at http://localhost:5000