"""
Configuration file for Excel Screenshot Email API
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'production') == 'development'
    
    # Email configuration
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SENDER_NAME = os.getenv('SENDER_NAME', 'Excel Screenshot Service')
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    SCREENSHOT_FOLDER = 'screenshots'
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Application settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    @staticmethod
    def validate_email_config():
        """Validate email configuration"""
        if not Config.SENDER_EMAIL or not Config.SENDER_PASSWORD:
            print("Warning: Email configuration incomplete")
            print("Please set SENDER_EMAIL and SENDER_PASSWORD in .env file")
            return False
        return True