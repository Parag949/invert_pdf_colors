#!/usr/bin/env python3
"""
Invert PDF Colors - Flask Web Application

A web-based tool to invert PDF colors by converting pages to images,
inverting them, and recombining to a PDF.

Run: python app.py
Then open: http://localhost:5000
"""
import sys
from pathlib import Path

# Ensure local 'src' is on sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil

from invert_pdf_colors.pipeline.process_pipeline import run_pipeline
from invert_pdf_colors.logger import get_logger

logger = get_logger()

app = Flask(__name__)
app.secret_key = os.urandom(24)
# No max file size limit
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Log CPU info on startup
cpu_count = os.cpu_count() or 1
logger.info(f"Starting Flask app with {cpu_count} CPU cores available")
logger.info(f"Multicore processing: Image inversion={cpu_count} processes, PDF extraction={min(32, cpu_count*2)} threads")

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Only PDF files are allowed', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get user parameters
        dpi_extract = int(request.form.get('dpi_extract', 200))
        dpi_output = int(request.form.get('dpi_output', 300))
        
        # Create temp directory for this operation
        temp_dir = Path(tempfile.mkdtemp(prefix='invert_pdf_'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = temp_dir / filename
        file.save(input_path)
        
        # Set output path
        output_filename = f"inverted_{filename}"
        output_path = temp_dir / output_filename
        work_dir = temp_dir / "work"
        
        logger.info(f"Processing {filename} with DPI extract={dpi_extract}, output={dpi_output}")
        
        # Run the pipeline
        run_pipeline(
            input_pdf=input_path,
            work_dir=work_dir,
            output_pdf=output_path,
            dpi_extract=dpi_extract,
            dpi_output=(dpi_output, dpi_output)
        )
        
        # Save output to uploads folder for serving
        final_output = app.config['UPLOAD_FOLDER'] / output_filename
        shutil.copy(output_path, final_output)
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        
        logger.info(f"Processing complete for {filename}")
        return render_template('success.html', filename=output_filename)
        
    except Exception as e:
        logger.exception("Error processing PDF")
        flash(f'Error processing PDF: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = app.config['UPLOAD_FOLDER'] / secure_filename(filename)
        if file_path.exists():
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.exception("Error downloading file")
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
