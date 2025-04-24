# Truman State University RPE Tracker

A full-stack application for tracking Rate of Perceived Exertion (RPE) data for Truman State University athletics.

---

## 👨‍💻 Authors

Developed for **Truman State University Athletics** by:

- [Mason Crim](https://github.com/MasonC13) – Lead Developer & API Architect
- [Nadine Thomas](https://github.com/Nadine-Thomas) – Frontend Engineer & UI/UX Designer
- [Kacie Myers](https://github.com/kaciemyers23) – QA Engineer & Technical Documentation  
- [Grace Lovell](https://github.com/grace-lovell) – Server Integration Engineer & Technical Documentation

---

## 📋 Overview

This application allows:
- **Athletes** to submit their RPE (Rate of Perceived Exertion) data after workouts  
- **Coaches/Trainers** to view aggregated RPE data with interactive visualizations  
- **Password protection** for the coaching staff dashboard  
- **Data manipulation** through CSV storage  
- **Email notifications** for athletes and coaches  
- **PDF report generation** for coaching staff  

---

## 🔧 Technologies

### Frontend
- **React.js** – Component-based UI library for the interface  
- **React Router DOM** – For navigation between pages  
- **React Hook Form** – Form validation and submission  
- **Custom CSS** – Styling with Truman State University brand colors  

### Backend
- **Python Flask** – Web server handling API routes and serving the dashboard  
- **Pandas** – Data analysis and manipulation  
- **NumPy** – Numerical operations on RPE data  
- **Dash** – Interactive dashboard built on Plotly  
- **Plotly Express & Graph Objects** – Graph visualizations  
- **Dash Bootstrap Components** – Dashboard UI styling  
- **ReportLab** – PDF report generation  
- **SMTP (smtplib)** – Sending email notifications  

---

## 💾 Data Storage

The application uses a simple CSV file for data storage:  
- Easy to manage and edit  
- Readable with Excel or spreadsheet tools  
- Integrates with pandas for backend processing  

CSV header:  
```
Email, Last 4 Digits, Last Name, First Name, Position, Summer Attendance
```  
New columns are automatically added for each new date with RPE entries.  

---

## 🚀 Features

- Athlete RPE submission form  
- Coach dashboard with password protection  
- Interactive team and individual RPE visualizations  
- Real-time data processing  
- Email notifications to athletes  
- PDF report generation for coaches  
- Role-based UI for athlete vs coach  

---

## 📦 Installation

### Prerequisites
- Node.js and npm (for frontend)  
- Python 3.8+ and pip (for backend)  

---

### 🔧 Setup

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/truman-rpe-tracker.git  
cd truman-rpe-tracker
```

2. **Install frontend dependencies**  
```bash
npm install
```

3. **Create `requirements.txt` file**  
This file should contain:  
```txt
Flask
pandas
numpy
dash
plotly
dash-bootstrap-components
reportlab
```

4. **Install backend dependencies**  
```bash
pip install -r requirements.txt
```

5. **Download Google credentials**  
Download your credentials JSON file from the Google Cloud Console (APIs & Services → Credentials).  
Save it as `credentials.json` in the project root.

6. **Add your SMTP settings**  
Open `credentials.json` and add your email configuration under an `"email_settings"` key:  
```json
{
  "email_settings": {
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "sender_email": "your-email@example.com",
    "sender_password": "your-password"
  }
}
```

7. **Create the initial CSV data file**  
```csv
Email, Last 4 Digits, Last Name, First Name, Position, Summer Attendance
```

---

## 🏃‍♂️ Running the Application

### 1. Start the backend server  
```bash
python main.py
```
Runs on [http://127.0.0.1:4025](http://127.0.0.1:4025)

### 2. Start the React frontend  
```bash
npm start
```
Opens on [http://localhost:3000](http://localhost:3000)

---

## 📁 Project Structure

```
truman-rpe-tracker/
│
├── public/                   # Static files for React
├── src/                      # React source files
│   ├── App.jsx               # Main app component
│   ├── HomePage.jsx          # Role selection (athlete or coach)
│   ├── MyForm.jsx            # Athlete RPE submission form
│   ├── ReportPage.jsx        # Coach dashboard
│   └── index.css             # Global styles
│
├── main.py                   # Flask + Dash server
├── emailNotif.py             # Email functionality
├── coachReport.py            # PDF generation using ReportLab
├── pythonCSV.py              # CSV utilities
├── credentials.json          # Email credentials (downloaded from Google Cloud Console)
├── responses.csv             # CSV-based RPE database
└── README.md                 # This file
```

---

## 🔐 Authentication

The coach dashboard is protected by a hardcoded password in `HomePage.jsx`.  
```js
const COACH_PASSWORD = "Your Password Here"; // Update this securely
```

---

## 📊 Dashboard Features

The dashboard includes:  
- Team average RPE trends  
- Position-based RPE comparisons  
- Individual athlete tracking  
- Weekly changes in workload  
- PDF export of visual reports  

---

## 📧 Email System

The backend can send:  
- Athlete reminder emails  
- PDF reports to coaching staff  
- Visual charts embedded in emails (optional)  

Email credentials are stored securely in `credentials.json`.  

---

## 📑 PDF Reports

PDF reports include:  
- Team and position statistics  
- Individual workload tracking  
- Acute:Chronic workload ratio alerts   

---
