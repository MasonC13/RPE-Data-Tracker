import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
import json
import plotly.express as px
from datetime import datetime
from pythonCSV import get_data_from_csv

def send_email(recipient, subject="RPE Data Reminder", message="Please fill out your RPE data today", include_graph=False):
    """Send an email with optional graph attachment."""
    
    with open("credentials.json", "r") as file:
        creds_data = json.load(file)
    
    # Email Setup using credentials.json
    try:
        SMTP_SERVER = creds_data["email_settings"]["smtp_server"]
        SMTP_PORT = creds_data["email_settings"]["smtp_port"]
        SENDER_EMAIL = creds_data["email_settings"]["sender_email"]
        SENDER_PASSWORD = creds_data["email_settings"]["sender_password"]
    except KeyError as e:
        print(f"Missing key in email settings: {e}")
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        SENDER_EMAIL = ""
        SENDER_PASSWORD = ""

    # ✅ Added safety check
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Email or password is not set in credentials.json. Skipping email.")
        return False

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        if include_graph:
            df, _, df_position_daily_avg = get_data_from_csv()
            fig = px.line(df_position_daily_avg, x='Date', y='Value', color='Position', title="Position Group Average Change Over Time")
            img_bytes = io.BytesIO()
            fig.write_image(img_bytes, format="png")
            img_bytes.seek(0)

            img = MIMEImage(img_bytes.read())
            img.add_header('Content-ID', '<graph>')
            img.add_header('Content-Disposition', 'attachment', filename="rpe_trends.png")
            msg.attach(img)

            html_content = f"""
            <html>
              <body>
                <p>{message}</p>
                <p>Here's your current RPE data visualization:</p>
                <img src="cid:graph" alt="RPE Trends">
              </body>
            </html>
            """
            msg.attach(MIMEText(html_content, "html"))

        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        print(f"Email sent to {recipient}")
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")
        return False
