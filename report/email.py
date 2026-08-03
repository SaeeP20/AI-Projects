import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def send_report(report_data, recipient: str) -> None:
    """
    Email the CEO report as an HTML dashboard in the message body.
    
    Args:
        report_data: dict with keys 'summary', 'dashboard_file', 'export_file'
                    OR just a string (for backward compatibility)
        recipient: email address to send to
    
    Reads credentials from environment variables:
      export EMAIL_SENDER=you@example.com
      export EMAIL_PASSWORD=your_app_password
    """
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    smtp_server = os.environ.get("EMAIL_SMTP", "smtp.gmail.com")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", 587))
    
    if not sender or not password:
        print("ERROR: EMAIL_SENDER and EMAIL_PASSWORD environment variables not set.")
        print("Email not sent. Please configure credentials and try again.")
        return
    
    # Handle both dict (new format) and string (backward compatibility)
    if isinstance(report_data, dict):
        summary = report_data.get("summary", "")
        dashboard_file = report_data.get("dashboard_file")
        report_url = report_data.get("report_url")
        export_file = report_data.get("export_file")
    else:
        summary = str(report_data)
        dashboard_file = None
        report_url = None
        export_file = None
    
    subject = f"Weekly Business Briefing — {datetime.today().strftime('%d %b %Y')}"

    html_body = f"""
    <html>
      <body style="font-family:Segoe UI, Arial, sans-serif; color:#16324f;">
        <h2>Weekly Business Briefing</h2>
        <p>Your weekly dashboard is ready.</p>
        <p><strong>Summary</strong></p>
        <pre style="white-space:pre-wrap; background:#f4f7fb; padding:12px; border-radius:8px;">{summary}</pre>
    """

    if report_url:
        html_body += f"""
        <p><strong>Power BI report</strong>: <a href=\"{report_url}\">Open dashboard</a></p>
        """

    if dashboard_file and os.path.exists(dashboard_file):
        with open(dashboard_file, "r", encoding="utf-8") as fh:
            dashboard_html = fh.read()
        html_body += f"""
        <p><strong>Dashboard preview</strong></p>
        <div style="border:1px solid #dfe6ee; padding:12px; border-radius:8px; background:white;">
          {dashboard_html}
        </div>
        """

    html_body += """
        <p style="margin-top:16px; color:#6b7a8f;">This is an automated report from the AI Analyst pipeline.</p>
      </body>
    </html>
    """
    
    try:
        # Create email message
        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))
        
        # Attach the dashboard file as an HTML attachment as well
        if dashboard_file and os.path.exists(dashboard_file):
            with open(dashboard_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(dashboard_file)}")
                msg.attach(part)
        
        # Attach Excel file if available
        if export_file and os.path.exists(export_file):
            with open(export_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(export_file)}")
                msg.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(sender, password)
            server.send_message(msg)
        
        print(f"✓ Email sent successfully to {recipient}")
        if dashboard_file:
            print(f"✓ Dashboard attachment: {dashboard_file}")
        if export_file:
            print(f"✓ Excel attachment: {export_file}")
    
    except smtplib.SMTPAuthenticationError:
        print(f"ERROR: Invalid email credentials for {sender}")
    except smtplib.SMTPException as e:
        print(f"ERROR: Failed to send email: {e}")
    except Exception as e:
        print(f"ERROR: Unexpected error while sending email: {e}")
