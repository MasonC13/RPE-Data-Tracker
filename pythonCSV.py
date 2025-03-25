import json
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load Credentials
with open("credentials.json", "r") as file:
    creds_data = json.load(file)

# Google Sheets API Setup
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
client = gspread.authorize(creds)       

sheet_id = "1W-wT-2nBcXROuThRrMFK6rTLljDC02aJ6kqL8iDlitE"  
workbook = client.open_by_key(sheet_id)     
worksheet = workbook.worksheet("RPE Sheet")  

data = worksheet.get_all_records()  
df = pd.DataFrame(data)  

# Email Setup (Loaded from JSON)
SMTP_SERVER = creds_data["email_settings"]["smtp_server"]
SMTP_PORT = creds_data["email_settings"]["smtp_port"]
SENDER_EMAIL = creds_data["email_settings"]["sender_email"]
SENDER_PASSWORD = creds_data["email_settings"]["sender_password"]

def send_email(recipient):
    """Function to send an email to a recipient."""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = "RPE Data"  # Placeholder subject
        msg.attach(MIMEText("Please fill out your RPE data today", "plain"))  # Empty message for now

        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        print(f"Email sent to {recipient}")

        server.quit()
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")

# Send emails to all users
for email in df["Email"].dropna().unique():  # Ensure no empty emails
    send_email(email)
