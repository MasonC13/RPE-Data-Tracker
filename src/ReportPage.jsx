import React from "react";

const ReportPage = () => {
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    background: 'linear-gradient(to bottom, var(--truman-purple), var(--truman-light-blue))'
  };

  const headerStyle = {
    backgroundColor: 'var(--truman-purple)',
    padding: '1rem',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
  };

  const headerContentStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0 1rem'
  };

  const titleStyle = {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: 'var(--truman-white)',
    margin: 0
  };

  const backLinkStyle = {
    display: 'flex',
    alignItems: 'center',
    color: '#a0c4ff',
    textDecoration: 'none',
    marginRight: '2rem',
    fontSize: '0.875rem'
  };

  const headerLeftStyle = {
    display: 'flex',
    alignItems: 'center'
  };

  const dateStyle = {
    color: '#a0c4ff',
    fontSize: '0.875rem'
  };

  const mainStyle = {
    flex: 1,
    padding: '1rem'
  };

  const dashboardContainerStyle = {
    backgroundColor: 'var(--truman-white)',
    borderRadius: '0.75rem',
    overflow: 'hidden',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
    height: '100%'
  };

  const dashboardHeaderStyle = {
    background: 'linear-gradient(to right, var(--truman-purple), var(--truman-light-blue))',
    padding: '1rem 1.5rem',
    color: 'var(--truman-white)'
  };

  const dashboardTitleStyle = {
    fontSize: '1.25rem',
    fontWeight: '600',
    margin: 0
  };

  const dashboardSubtitleStyle = {
    fontSize: '0.875rem',
    color: '#a0c4ff',
    marginTop: '0.25rem'
  };

  const iframeContainerStyle = {
    height: 'calc(100vh - 12rem)',
    overflow: 'hidden'
  };

  const iframeStyle = {
    width: '100%',
    height: '100%',
    border: 'none',
    borderRadius: '0 0 0.75rem 0.75rem'
  };

  const footerStyle = {
    backgroundColor: 'var(--truman-purple)',
    padding: '0.75rem',
    textAlign: 'center'
  };
  
  const footerTextStyle = {
    color: '#a0c4ff',
    fontSize: '0.875rem'
  };

  return (
    <div style={containerStyle}>
      <header style={headerStyle}>
        <div style={headerContentStyle}>
          <div style={headerLeftStyle}>
            <a href="/" style={backLinkStyle}>
              <svg style={{ width: '1.25rem', height: '1.25rem', marginRight: '0.25rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              Back
            </a>
            <h1 style={titleStyle}>Truman State University</h1>
          </div>
          <div style={dateStyle}>
            {new Date().toLocaleDateString()}
          </div>
        </div>
      </header>
      
      <main style={mainStyle}>
        <div style={dashboardContainerStyle}>
          <div style={dashboardHeaderStyle}>
            <h2 style={dashboardTitleStyle}>RPE Analytics Dashboard</h2>
            <p style={dashboardSubtitleStyle}>Interactive reporting tool for trainers and coaches</p>
          </div>
          
          <div style={iframeContainerStyle}>
            <iframe
              src="http://127.0.0.1:4025/dashboard/" 
              title="Trainer Report"
              style={iframeStyle}
            />
          </div>
        </div>
      </main>
      
      <footer style={footerStyle}>
        <div style={footerTextStyle}>
          &copy; {new Date().getFullYear()} Truman State University Athletics
        </div>
      </footer>
    </div>
  );
};

export default ReportPage;
