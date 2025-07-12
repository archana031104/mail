#!/usr/bin/env python3
"""
Setup script for local deployment of Excel Screenshot Email API
"""

import os
import sys
import subprocess
import shutil

def create_project_structure():
    """Create necessary directories"""
    directories = ['uploads', 'screenshots', 'templates', 'static']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory exists: {directory}")

def create_env_file():
    """Create .env file template"""
    env_content = """# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=Your Name

# Application Configuration
SESSION_SECRET=your-secret-key-here
FLASK_ENV=development
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("Created .env file - please update with your credentials")
    else:
        print(".env file already exists")

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = """Flask==2.3.3
gunicorn==21.2.0
openpyxl==3.1.2
pandas==1.5.3
numpy==1.24.3
playwright==1.39.0
xlrd==2.0.1
Werkzeug==2.3.7
python-dotenv==1.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("Created requirements.txt")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
env/
ENV/

# Temporary files
uploads/*
!uploads/.gitkeep
screenshots/*
!screenshots/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("Created .gitignore")

def create_gitkeep_files():
    """Create .gitkeep files for empty directories"""
    for directory in ['uploads', 'screenshots']:
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write(f"# This directory stores {directory} temporarily\n")
            print(f"Created {gitkeep_path}")

def main():
    """Main setup function"""
    print("Setting up Excel Screenshot Email API for local development...")
    print("=" * 60)
    
    create_project_structure()
    create_env_file()
    create_requirements_file()
    create_gitignore()
    create_gitkeep_files()
    
    print("\n" + "=" * 60)
    print("Setup complete! Next steps:")
    print("1. Create virtual environment: python -m venv venv")
    print("2. Activate virtual environment:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - macOS/Linux: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Install Playwright browsers: playwright install chromium")
    print("5. Update .env file with your email credentials")
    print("6. Run the application: python main.py")
    print("7. Access the web interface at: http://localhost:5000")

if __name__ == "__main__":
    main()