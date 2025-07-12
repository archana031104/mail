# VS Code & Laptop Deployment Guide

## Prerequisites

1. **Python 3.9+** installed on your laptop (your Python 3.9.6 is perfect!)
2. **VS Code** with Python extension
3. **Git** (optional, for version control)

## Step-by-Step Deployment

### Step 1: Download Project Files

Copy these files from Replit to your laptop:

**Required Files:**
- `app.py` - Main Flask application
- `main.py` - Application entry point
- `excel_processor.py` - Excel processing logic
- `email_sender.py` - Email functionality
- `requirements.txt` - Python dependencies (create this)
- `templates/index.html` - Web interface
- `static/style.css` - Styling

**Required Folders:**
- `uploads/` - For temporary file storage
- `screenshots/` - For generated screenshots

### Step 2: Create Project Structure

```
excel-screenshot-api/
├── app.py
├── main.py
├── excel_processor.py
├── email_sender.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── uploads/
└── screenshots/
```

### Step 3: Install Dependencies

Create `requirements.txt`:
```
Flask==3.0.0
gunicorn==21.2.0
openpyxl==3.1.2
pandas==2.1.4
playwright==1.40.0
xlrd==2.0.1
Werkzeug==3.0.1
```

Install dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 4: Environment Variables

Create `.env` file in your project root:
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=Your Name
SESSION_SECRET=your-secret-key-here
```

**For production, use environment variables or a secure config file.**

### Step 5: Update Code for Local Environment

Create `config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SESSION_SECRET', 'dev-secret-key')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SENDER_NAME = os.getenv('SENDER_NAME', 'Excel Screenshot Service')
```

### Step 6: Update requirements.txt

Add environment variable support:
```
python-dotenv==1.0.0
```

### Step 7: Running the Application

**Development Mode:**
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the application
python main.py
```

**Production Mode:**
```bash
# Using Gunicorn (recommended for production)
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app

# Or using Flask's built-in server
python -m flask run --host=0.0.0.0 --port=5000
```

### Step 8: VS Code Setup

1. **Open project in VS Code**
2. **Install Python extension**
3. **Select Python interpreter** (from your venv)
4. **Create launch.json** for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "env": {
                "FLASK_ENV": "development"
            },
            "args": [],
            "jinja": true
        }
    ]
}
```

### Step 9: Testing the Deployment

1. **Test the API health:**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Test file upload:**
   ```bash
   curl -X POST http://localhost:5000/api/upload \
     -F "file=@test.xlsx" \
     -F "email=test@example.com"
   ```

3. **Access web interface:**
   Open `http://localhost:5000` in your browser

### Step 10: Production Deployment Options

**Option 1: Local Server**
- Use Gunicorn with systemd service
- Configure reverse proxy with nginx

**Option 2: Cloud Deployment**
- Heroku, AWS, Google Cloud, or Azure
- Use Docker for containerization

**Option 3: Network Access**
- Configure firewall to allow port 5000
- Use ngrok for temporary public access

## Security Considerations

1. **Never commit `.env` file to version control**
2. **Use strong secret keys**
3. **Configure HTTPS for production**
4. **Implement rate limiting**
5. **Validate file uploads strictly**

## Troubleshooting

**Common Issues:**
1. **Playwright browser not found**: Run `playwright install chromium`
2. **Permission denied**: Check file permissions for uploads/screenshots folders
3. **Email not sending**: Verify SMTP settings and credentials
4. **Port already in use**: Change port in main.py or kill existing process

**Debug Mode:**
Set `debug=True` in `app.run()` for detailed error messages.