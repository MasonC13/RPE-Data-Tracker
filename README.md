# Truman State University RPE Tracker

A full-stack application for tracking Rate of Perceived Exertion (RPE) data for Truman State University athletics. This tool helps athletes submit their workout RPE scores and provides coaches with visualization dashboards to monitor team performance.

## 📋 Overview

This application allows:
- **Athletes** to submit their RPE (Rate of Perceived Exertion) data after workouts
- **Coaches/Trainers** to view aggregated RPE data with interactive visualizations
- **Password protection** for the coaching staff dashboard
- **Data manipulation** through CSV storage
- **Email notifications** for athletes and coaches
- **PDF report generation** for coaching staff

## 🔧 Technologies

### Frontend
- **React.js** - Component-based UI library for building the user interface
- **React Router DOM** - For navigation between different views/pages
- **React Hook Form** - Form validation and submission handling
- **Custom CSS** - Styling with Truman State University brand colors

### Backend
- **Python Flask** - Web server framework handling REST API endpoints and serving the dashboard
- **Pandas** - Data manipulation and analysis for RPE data
- **Dash** - Interactive visualization framework built on Plotly
- **Plotly Express & Graph Objects** - Creating interactive charts and visualizations
- **ReportLab** - PDF generation for coach reports
- **SMTP Library** - Email notifications via `smtplib` and MIME components
- **NumPy** - Numerical operations on RPE data
- **Dash Bootstrap Components** - UI components for dashboard styling

## 💾 Data Storage

The application uses a CSV-based database system for data persistence. This approach provides:

- Simple yet effective data storage without requiring a database server setup
- Easy portability - the entire database can be viewed in spreadsheet applications
- Straightforward backup and version control
- Direct integration with pandas for data analysis

The database structure includes:
- Base columns: Email, Last 4 Digits, Last Name, First Name, Position, Summer Attendance
- Dynamic date columns: Each date gets its own column with RPE values for that day

## 🚀 Features

- **Modern, responsive UI** with Truman State University branding
- **Role-based access** (athlete vs. coach/trainer)
- **Password-protected** coach dashboard
- **Real-time data processing** for RPE scores
- **Interactive visualizations** including:
  - Team-wide average RPE trends
  - Position-based analysis
  - Individual athlete performance tracking
  - Week-over-week change metrics
- **Email notifications** for athletes and coaches
- **PDF report generation** with:
  - Team overview statistics
  - Position analysis
  - Acute:Chronic workload ratio monitoring for injury prevention
  - Customized branding with Truman State University colors

## 📦 Installation

### Prerequisites
- Node.js and npm
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/truman-rpe-tracker.git
cd truman-rpe-tracker
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Install backend dependencies:
```bash
cd ../backend
pip install -r requirements.txt
```

4. Create a `credentials.json` file for email functionality:
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
5. Create a new file named responses.csv in the backend directory:
```csv
Add the following header row to set up the database structure:

Email, Last 4 Digits, Last Name, First Name, Position, Summer Attendance
```

## 🏃‍♂️ Running the Application

### Start the backend server:
```bash
cd backend
python main.py
```
The server will start on http://127.0.0.1:4025.

### Start the frontend development server:
```bash
cd frontend
npm start
```
The application will open in your browser at http://localhost:3000.

## 📁 Project Structure

```
truman-rpe-tracker/
│
├── frontend/                  # React frontend application
│   ├── public/                # Static files
│   ├── src/                   # Source files
│   │   ├── App.jsx            # Main application component
│   │   ├── HomePage.jsx       # Landing page with role selection
│   │   ├── MyForm.jsx         # Athlete RPE submission form
│   │   ├── ReportPage.jsx     # Coach dashboard wrapper
│   │   └── index.css          # Global styles with Truman colors
│   └── ...
│
├── backend/                   # Flask server and Dash application
│   ├── main.py                # Combined Flask/Dash server
│   ├── emailNotif.py          # Email notification functionality
│   ├── coachReport.py         # Coach report generation with ReportLab
│   ├── pythonCSV.py           # CSV data processing utilities
│   ├── credentials.json       # Email configuration (create this file)
│   └── responses.csv          # Data storage file
│
└── README.md                  # Project documentation
```

## 🔐 Authentication

The coach/trainer dashboard is protected with a password. The default password is set in the HomePage component:

```javascript
const COACH_PASSWORD = "Your Password Here"; // Change this to your secure password
```

## 📊 Dashboard

The coaching dashboard includes several interactive visualizations:

- Average RPE by position
- RPE trends over time
- Week-over-week changes
- Individual athlete performance analysis

Coaches can filter data by position, date ranges, and specific athletes.

## 🔄 Data Flow

1. Athletes submit RPE data through the form
2. Data is stored in a CSV file on the server
3. The dashboard reads from the CSV and generates visualizations
4. Coaches can access the visualizations through the protected dashboard
5. Email notifications can be sent to remind athletes to submit data
6. PDF reports can be generated and emailed to coaching staff

## 📧 Email System

The application includes an email notification system that can:
- Send reminders to athletes to complete their RPE submissions
- Send PDF reports to coaches with team performance metrics
- Include visualizations of RPE trends
- Track email delivery success/failure

To use this functionality, create a `credentials.json` file with your SMTP server details.

## 📑 PDF Reports

Coaches can generate comprehensive PDF reports with:
- Team overview statistics
- Position-by-position analysis
- Athletes with high acute:chronic workload ratios (injury risk monitoring)
- Truman State University branding and styling

## 🛠️ Customization

- Update Truman State University colors in `index.css`
- Modify the dashboard layout in `main.py`
- Change the coach password in `HomePage.jsx`
- Customize email templates in `emailNotif.py`
- Adjust PDF report layout in `coachReport.py`

## 📝 License

[MIT License](LICENSE)

## 👨‍💻 Authors

This project was developed by:

- **[Mason Crim]** - *Backend Developer* - [GitHub Profile URL]
- **[Nadine Thomas]** - *Frontend Developer* - [GitHub Profile URL]
- **[Kacie Myers]** - *Frontend Developer* - [GitHub Profile URL]
- **[Grace Lovell]** - *Data Visualization* - [GitHub Profile URL]

---

Developed for Truman State University Athletics Department
