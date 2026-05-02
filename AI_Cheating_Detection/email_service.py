import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from database import get_db_connection

class EmailService:
    def __init__(self):
        # Email configuration (update these with your SMTP settings)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.enabled = bool(self.smtp_username and self.smtp_password)
    
    def send_alert(self, examiner_id, behaviors, evidence_path):
        """Send email alert to examiner about cheating detection"""
        if not self.enabled:
            print(f"Email service not configured. Would send alert for behaviors: {behaviors}")
            return
        
        # Get examiner email
        conn = get_db_connection()
        examiner = conn.execute('SELECT email, username FROM users WHERE id = ?', (examiner_id,)).fetchone()
        conn.close()
        
        if not examiner:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = examiner['email']
            msg['Subject'] = '🚨 Cheating Detection Alert'
            
            body = f"""
            <html>
            <body>
                <h2>Cheating Detection Alert</h2>
                <p><strong>Detected Behaviors:</strong></p>
                <ul>
            """
            
            for behavior in behaviors:
                body += f"<li>{behavior}</li>"
            
            body += f"""
                </ul>
                <p><strong>Evidence:</strong> {evidence_path}</p>
                <p>Please review the evidence and take appropriate action.</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach evidence if it exists
            if os.path.exists(evidence_path):
                with open(evidence_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(evidence_path)}'
                    )
                    msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Alert email sent to {examiner['email']}")
        except Exception as e:
            print(f"Failed to send email alert: {e}")

