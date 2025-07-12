import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

logger = logging.getLogger(__name__)


class EmailSender:

    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.sender_name = os.getenv('SENDER_NAME', 'Excel Screenshot Service')

        # Validate required configuration
        if not self.sender_email or not self.sender_password:
            logger.warning(
                "Email configuration incomplete: SENDER_EMAIL and SENDER_PASSWORD must be set"
            )
            # Don't raise error to allow app to start, just log warning

    def send_email_with_screenshot(self, recipient_email, screenshot_path,
                                   original_filename):
        """
        Send email with screenshot embedded in the body
        """
        try:
            # Create message
            msg = MIMEMultipart('related')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"Excel Screenshot: {original_filename}"

            # Create HTML body with embedded image
            html_body = f"""
            <html>
            <head></head>
            <body>
                <h2>Excel File Screenshot</h2>
                <p>Hello,</p>
                <p>Please find below the screenshot of the Excel file content for: <strong>{original_filename}</strong></p>
                <br>
                <img src="cid:screenshot" alt="Excel Screenshot" style="max-width: 100%; height: auto; border: 1px solid #ddd;">
                <br><br>
                
            </body>
            </html>
            """

            # Attach HTML body
            msg.attach(MIMEText(html_body, 'html'))

            # Read and attach screenshot
            with open(screenshot_path, 'rb') as f:
                img_data = f.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<screenshot>')
                msg.attach(img)

            # Send email with better error handling
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)

                text = msg.as_string()
                server.sendmail(self.sender_email, recipient_email, text)

            logger.info(f"Email sent successfully to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def test_email_configuration(self):
        """
        Test email configuration
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)

            logger.info("Email configuration test successful")
            return True

        except Exception as e:
            logger.error(f"Email configuration test failed: {e}")
            return False
