#!/usr/bin/env python3
"""
Local development server runner
"""
import os
import sys
from config import Config

def check_environment():
    """Check if environment is properly set up"""
    print("Checking environment setup...")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("⚠️  Warning: Virtual environment not detected")
        print("Consider activating virtual environment: source venv/bin/activate")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found")
        print("Please run: python setup_local.py")
        return False
    
    # Check email configuration
    if not Config.validate_email_config():
        print("❌ Error: Email configuration incomplete")
        return False
    
    # Check required directories
    required_dirs = ['uploads', 'screenshots', 'templates', 'static']
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"❌ Error: Missing directory: {directory}")
            print("Please run: python setup_local.py")
            return False
    
    print("✅ Environment setup looks good!")
    return True

def run_development_server():
    """Run the development server"""
    if not check_environment():
        print("Please fix the environment issues before running the server")
        return
    
    print("Starting Excel Screenshot Email API...")
    print(f"Server will be available at: http://localhost:{Config.PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        from app import app
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    run_development_server()