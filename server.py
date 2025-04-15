from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

CSV_FILE = "responses.csv"

# Define base headers
BASE_COLUMNS = [
    "Email",
    "Last 4 Digits",
    "Last Name",
    "First Name",
    "Position",
    "Summer Attendance"
]

# Ensure the CSV exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=BASE_COLUMNS)
    df.to_csv(CSV_FILE, index=False)

@app.route("/submit", methods=["POST"])
def submit_form():
    data = request.json
    today_str = datetime.today().strftime("%m/%d/%Y")  # e.g. 4/15/2025

    # Load existing CSV
    df = pd.read_csv(CSV_FILE)

    # Add today's date column if not exists
    if today_str not in df.columns:
        df[today_str] = ""

    # Check if user already exists (by email)
    email = data.get("email")
    user_index = df[df["Email"] == email].index

    if len(user_index) > 0:
        # Update existing row with intensity level
        idx = user_index[0]
        df.at[idx, today_str] = data.get("intensityLevel")  # Store intensity level for today
    else:
        # Create new row with intensity level
        new_row = {
            "Email": data.get("email"),
            "Last 4 Digits": data.get("last4"),
            "Last Name": data.get("lastName"),
            "First Name": data.get("firstName"),
            "Position": data.get("position"),
            "Summer Attendance": data.get("summerAttendance"),
            today_str: data.get("intensityLevel")  # Store intensity level for today
        }

        # Fill missing date columns
        for col in df.columns:
            if col not in new_row:
                new_row[col] = ""

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Reorder columns: base + dates
    date_cols = [col for col in df.columns if col not in BASE_COLUMNS]
    df = df[BASE_COLUMNS + sorted(date_cols, key=lambda x: datetime.strptime(x, "%m/%d/%Y"))]

    df.to_csv(CSV_FILE, index=False)
    return jsonify({"message": "Data saved successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=4025)
