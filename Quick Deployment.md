# Quick Deployment to VS Code & Laptop

## 🚀 Step-by-Step Guide

### 1. Download All Files
Copy these files from Replit to your laptop:

**Core Files:**
- `app.py` - Main application
- `main.py` - Entry point  
- `excel_processor.py` - Excel processing
- `email_sender.py` - Email functionality
- `templates/index.html` - Web interface
- `static/style.css` - Styling

**Setup Files (I created these for you):**
- `setup_local.py` - Automated setup script
- `config.py` - Configuration management
- `run_local.py` - Development server runner
- `DEPLOYMENT_GUIDE.md` - Detailed guide

### 2. One-Command Setup
```bash
# Navigate to your project folder
cd excel-screenshot-api

# Run the automated setup
python setup_local.py

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browser for screenshots
playwright install chromium
```

### 3. Configure Email
Edit the `.env` file created by setup:
```
SENDER_EMAIL=aia353167@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=Your Name
```

### 4. Run the Application
```bash
# Simple run
python run_local.py

# Or direct run
python main.py
```

### 5. Access Your API
- **Web Interface**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **API Upload**: POST to http://localhost:5000/api/upload

## 🎯 What You Get

✅ **Complete working API** exactly like on Replit
✅ **Web interface** for file uploads  
✅ **REST API** for programmatic access
✅ **Email functionality** with embedded screenshots
✅ **Error handling** and logging
✅ **Configuration management** with .env file
✅ **Development tools** for VS Code

## 📂 Project Structure
```
excel-screenshot-api/
├── app.py                 # Main Flask app
├── main.py                # Entry point
├── excel_processor.py     # Excel processing
├── email_sender.py        # Email functionality
├── config.py              # Configuration
├── setup_local.py         # Setup script
├── run_local.py           # Development runner
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── style.css          # Styling
├── uploads/               # Temporary uploads
└── screenshots/           # Generated screenshots
```

## 🔧 VS Code Setup
1. Open the project folder in VS Code
2. Install Python extension
3. Select your virtual environment as interpreter
4. Press F5 to run with debugging

## 🌐 Making it Accessible
**For local network access:**
- Change host to `0.0.0.0` in config
- Access via `http://your-laptop-ip:5000`

**For internet access:**
- Use ngrok: `ngrok http 5000`
- Deploy to cloud (Heroku, AWS, etc.)

Your Excel Screenshot Email API is now ready for local development and deployment!