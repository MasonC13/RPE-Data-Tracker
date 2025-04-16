# Truman State University RPE Tracker

A full-stack application for tracking Rate of Perceived Exertion (RPE) data for Truman State University athletics. This tool helps athletes submit their workout RPE scores and provides coaches with visualization dashboards to monitor team performance.

## 📋 Overview

This application allows:
- **Athletes** to submit their RPE (Rate of Perceived Exertion) data after workouts
- **Coaches/Trainers** to view aggregated RPE data with interactive visualizations
- **Password protection** for the coaching staff dashboard
- **Data persistence** through CSV storage

## 🔧 Technologies

### Frontend
- React.js
- React Router for navigation
- Custom CSS styling with Truman State University branding

### Backend
- Python Flask server
- Dash for interactive data visualizations
- Pandas for data processing
- CSV file storage

## 🏗️ Architecture

The application follows a client-server architecture:

1. **React Frontend** - Handles user interface and form submission
2. **Flask Backend** - Processes data and serves the dashboard
   - `/submit` endpoint receives RPE form submissions
   - `/dashboard` serves the interactive Dash visualization application

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
│   │   └── ...
│   └── ...
│
├── backend/                   # Flask server and Dash application
│   ├── main.py               # Combined Flask/Dash server
│   ├── emailNotif.py         # Email notification functionality
│   ├── coachReport.py        # Coach report generation
│   └── ...
│
└── README.md                  # Project documentation
```

## 🔐 Authentication

The coach/trainer dashboard is protected with a password. The default password is set in the HomePage component:

```javascript
const COACH_PASSWORD = "bulldogs2025"; // Change this to your secure password
```

For improved security in production, consider implementing server-side password validation.

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

## 💾 Data Storage

Data is stored in a CSV file (`responses.csv`) with the following structure:
- Base columns: Email, Last 4 Digits, Last Name, First Name, Position, Summer Attendance
- Dynamic date columns: Each date gets its own column with RPE values for that date

## 🛠️ Customization

- Update Truman State University colors in `index.css`
- Modify the dashboard layout in `main.py`
- Change the coach password in `HomePage.jsx`

## 📝 License

[MIT License](LICENSE)

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please contact [your-email@truman.edu](mailto:your-email@truman.edu).

---

Developed for Truman State University Athletics Department
