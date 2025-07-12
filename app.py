import os
import logging
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from excel_processor import ExcelProcessor
from email_sender import EmailSender
import tempfile
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
SCREENSHOT_FOLDER = 'screenshots'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SCREENSHOT_FOLDER'] = SCREENSHOT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

# Initialize processors
excel_processor = ExcelProcessor()
try:
    email_sender = EmailSender()
    logger.info("Email sender initialized successfully")
except Exception as e:
    logger.warning(f"Email sender initialization incomplete: {e}")
    email_sender = EmailSender()  # Initialize anyway to allow configuration later

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        recipient_email = request.form.get('email', '').strip()
        
        # Validate inputs
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not recipient_email:
            flash('Email address is required', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Only .xlsx and .xls files are allowed.', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        logger.info(f"File uploaded: {filepath}")
        
        # Process Excel file and take screenshot
        screenshot_path = excel_processor.process_excel_and_screenshot(filepath)
        
        if not screenshot_path:
            flash('Failed to process Excel file or take screenshot', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        # Send email with embedded screenshot
        if email_sender:
            success = email_sender.send_email_with_screenshot(
                recipient_email, 
                screenshot_path, 
                filename
            )
        else:
            logger.error("Email sender not initialized - check email configuration")
            success = False
        
        # Cleanup files
        try:
            os.remove(filepath)
            os.remove(screenshot_path)
        except OSError as e:
            logger.warning(f"Failed to cleanup files: {e}")
        
        if success:
            flash('Excel file processed and email sent successfully!', 'success')
        else:
            flash('Failed to send email. Please check the email configuration.', 'error')
            
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        flash(f'An error occurred while processing the file: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API endpoint for file upload"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        recipient_email = request.form.get('email', '').strip()
        
        # Validate inputs
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not recipient_email:
            return jsonify({'error': 'Email address is required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only .xlsx and .xls files are allowed.'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        logger.info(f"File uploaded via API: {filepath}")
        
        # Process Excel file and take screenshot
        screenshot_path = excel_processor.process_excel_and_screenshot(filepath)
        
        if not screenshot_path:
            return jsonify({'error': 'Failed to process Excel file or take screenshot'}), 500
        
        logger.info(f"Screenshot saved via API: {screenshot_path}")
        
        # Send email with embedded screenshot
        if email_sender:
            success = email_sender.send_email_with_screenshot(
                recipient_email, 
                screenshot_path, 
                filename
            )
        else:
            logger.error("Email sender not initialized - check email configuration")
            success = False
        
        # Cleanup files
        try:
            os.remove(filepath)
            os.remove(screenshot_path)
        except OSError as e:
            logger.warning(f"Failed to cleanup files: {e}")
        
        if success:
            return jsonify({
                'message': 'Excel file processed and email sent successfully!',
                'filename': filename,
                'recipient': recipient_email
            }), 200
        else:
            return jsonify({'error': 'Failed to send email. Please check email configuration.'}), 500
            
    except Exception as e:
        logger.error(f"API error processing file: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Excel Screenshot Email API',
        'version': '1.0.0'
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
