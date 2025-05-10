import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
import os
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime
from pythonCSV import get_data_from_csv
from pathlib import Path

# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from the project root
env_path = BASE_DIR / '.env'
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Verify environment variables are loaded
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
print(f"Loaded email config: Server={SMTP_SERVER}, Port={SMTP_PORT}, Email={SENDER_EMAIL}")

def send_email(recipient, subject="RPE Data Reminder", message="Please fill out your RPE data today", include_graph=False):
    """Send an email with optional graph attachment."""

    # Email Setup using environment variables
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

    # ✅ Added safety check
    if not SENDER_EMAIL or not SENDER_PASSWORD or not SMTP_SERVER:
        print("Email configuration not set in .env file. Skipping email.")
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
