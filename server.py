from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CSV_FILE = "responses.csv"

# Ensure the CSV file exists with the correct headers
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Email", "Intensity Level", "Session Type"])
    df.to_csv(CSV_FILE, index=False)

@app.route("/submit", methods=["POST"])
def submit_form():
    data = request.json  # Receive JSON data from React
    df = pd.DataFrame([data])  # Convert to DataFrame
    df.to_csv(CSV_FILE, mode="a", header=False, index=False)  # Append to CSV
    return jsonify({"message": "Data saved successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
    