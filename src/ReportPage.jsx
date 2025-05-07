import React from "react";

const ReportPage = () => {
  return (
    <div className="report-container">
      <header className="report-header">
        <div className="report-header-content">
          <div className="report-header-left">
            <a href="/" className="report-back-link">
              <svg className="report-back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              Back
            </a>
            <h1 className="report-title">Truman State University</h1>
          </div>
          <div className="report-date">
            {new Date().toLocaleDateString()}
          </div>
        </div>
      </header>
      
      <main className="report-main">
        <div className="report-dashboard-container">
          <div className="report-dashboard-header">
            <h2 className="report-dashboard-title">RPE Analytics Dashboard</h2>
            <p className="report-dashboard-subtitle">Interactive reporting tool for trainers and coaches</p>
          </div>
          
          <div className="report-iframe-container">
            <iframe
              src="/dashboard/" 
              title="Trainer Report"
              className="report-iframe"
            />
          </div>
        </div>
      </main>
      
      <footer className="report-footer">
        <div className="report-footer-text">
          &copy; {new Date().getFullYear()} Truman State University Athletics
        </div>
      </footer>
    </div>
  );
};

export default ReportPage;
