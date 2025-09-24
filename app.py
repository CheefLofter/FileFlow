from flask import Flask, Response, render_template, abort, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import humanize
import atexit
import shutil

# Configuration
CONFIG = {
    'SHARED_DIR': 'shared',      # Single directory for all files
    'HOST': '0.0.0.0',          # Server host
    'PORT': 8080,               # Server port
    'ALLOWED_EXTENSIONS': None   # None means allow all; or use set(['pdf', 'txt', etc])
}

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Setup paths
BASE_DIR = os.path.dirname(__file__)
SHARED_FOLDER = os.path.join(BASE_DIR, CONFIG['SHARED_DIR'])

# Ensure directory exists
os.makedirs(SHARED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = CONFIG['ALLOWED_EXTENSIONS']  # None means allow all; adjust if you want to restrict

def allowed_file(filename):
    if ALLOWED_EXTENSIONS is None:
        return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_info(filepath):
    """Get file size and modification time in human readable format"""
    try:
        stats = os.stat(filepath)
        return {
            'size': stats.st_size,
            'size_str': humanize.naturalsize(stats.st_size),
            'modified': humanize.naturaltime(datetime.fromtimestamp(stats.st_mtime))
        }
    except OSError:
        return {'size': 0, 'size_str': '0 B', 'modified': 'unknown'}


@app.route('/')
def home():
    files = []
    files_info = {}
    
    try:
        files = sorted(os.listdir(SHARED_FOLDER))
        for file in files:
            files_info[file] = get_file_info(os.path.join(SHARED_FOLDER, file))
    except FileNotFoundError:
        files = []
    
    return render_template('index.html',
                         files=files,
                         files_info=files_info,
                         upload_dir=CONFIG['SHARED_DIR'])
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('home'))
    
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('home'))
    
    success_count = 0
    error_count = 0
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                save_path = os.path.join(SHARED_FOLDER, filename)
                file.save(save_path)
                success_count += 1
            except Exception as e:
                error_count += 1
                flash(f'Error saving {file.filename}: {str(e)}', 'error')
        else:
            error_count += 1
            flash(f'File type not allowed: {file.filename}', 'error')
    
    if success_count > 0:
        flash(f'Successfully uploaded {success_count} file(s)', 'success')
    if error_count > 0:
        flash(f'Failed to upload {error_count} file(s)', 'error')
        
    return redirect(url_for('home'))

@app.route('/download/<path:filename>')
def download_file(filename):
    safe_name = secure_filename(filename)
    file_path = os.path.join(SHARED_FOLDER, safe_name)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(SHARED_FOLDER, safe_name, as_attachment=True)

@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    safe_name = secure_filename(filename)
    file_path = os.path.join(SHARED_FOLDER, safe_name)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            flash(f'Successfully deleted {filename}', 'success')
        else:
            flash(f'File not found: {filename}', 'error')
    except Exception as e:
        flash(f'Error deleting {filename}: {str(e)}', 'error')
    return redirect(url_for('home'))


def clear_shared_folder():
    try:
        for filename in os.listdir(SHARED_FOLDER):
            file_path = os.path.join(SHARED_FOLDER, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print("Shared directory cleared.")
    except Exception as e:
        print("Error clearing shared directory:", e)

atexit.register(clear_shared_folder)

if __name__ == '__main__':
    app.run(host=CONFIG['HOST'], port=CONFIG['PORT'])
