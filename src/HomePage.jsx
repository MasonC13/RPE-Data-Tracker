import React, { useState } from "react";
import "./index.css";
import userManualPDF from './assets/rpe-user-manual.pdf';

const HomePage = () => {
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [showHelpModal, setShowHelpModal] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");

    const handleAthleteClick = () => {
        window.location.href = "/form";
    };

    const handleTrainerClick = () => {
        setShowPasswordModal(true);
    };
    
    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('/api/authenticate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password }),
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (data.success) {
                window.location.href = "/report";
            } else {
                setPasswordError(data.message || "Incorrect password. Please try again.");
            }
        } catch (error) {
            setPasswordError("Network error. Please try again.");
        }
    };
    
    const handleCloseModal = (e) => {
        if (e.target === e.currentTarget) {
            setShowPasswordModal(false);
            setPassword("");
            setPasswordError("");
        }
    };

    const handleHelpClick = () => {
        setShowHelpModal(true);
    };

    const handleCloseHelpModal = (e) => {
        if (e.target === e.currentTarget) {
            setShowHelpModal(false);
        }
    };

    const downloadUserManual = () => {
        window.open(userManualPDF, '_blank');
    };

    return (
        <div className="container">
            <header className="header">
                <div className="header-content">
                    <div className="header-text">
                        BULLDOGS ATHLETICS
                    </div>
                </div>
                <button 
                    onClick={handleHelpClick} 
                    className="help-button"
                    title="Help"
                >
                    {/* Large question mark icon without outer circle */}
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 17L12 17.01" strokeWidth="2" strokeLinecap="round" />
                        <path d="M12 14C12 11 15 11.5 15 9C15 7.5 13.5 6 12 6C10.5 6 9 7.5 9 9" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                </button>
            </header>
            
            <div className="main-content">
                <h1 className="title">
                    Truman State University
                </h1>
                <h2 className="subtitle">
                    Rate of Perceived Exertion
                </h2>
                
                <div className="card">
                    <h3 className="card-title">
                        Please select your role:
                    </h3>
                    
                    <div className="button-group">
                        <button
                            onClick={handleAthleteClick}
                            className="button button-primary"
                        >
                            <svg className="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                            </svg>
                            I am an athlete
                        </button>
                        
                        <button
                            onClick={handleTrainerClick}
                            className="button button-secondary"
                        >
                            <svg className="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                            </svg>
                            I am a trainer/coach
                        </button>
                    </div>
                </div>
            </div>
            
            <footer className="footer">
                <div className="footer-text">
                    <svg className="footer-icon" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd"></path>
                    </svg>
                    Truman State University Athletics
                    <span style={{ margin: '0 0.5rem' }}>•</span>
                    {new Date().getFullYear()}
                </div>
            </footer>
            
            {showPasswordModal && (
                <div 
                    className="modal-overlay"
                    onClick={handleCloseModal}
                >
                    <div 
                        className="modal-content"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h3 className="modal-title">
                            Coach/Trainer Access
                        </h3>
                        
                        <p className="modal-text">
                            Please enter your password to access the dashboard.
                        </p>
                        
                        <form onSubmit={handlePasswordSubmit}>
                            <div>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter password"
                                    className="input"
                                    autoFocus
                                />
                                {passwordError && (
                                    <p className="error-message">
                                        {passwordError}
                                    </p>
                                )}
                            </div>
                            
                            <div className="button-group-horizontal">
                                <button
                                    type="button"
                                    onClick={() => {
                                        setShowPasswordModal(false);
                                        setPassword("");
                                        setPasswordError("");
                                    }}
                                    className="button-cancel"
                                >
                                    Cancel
                                </button>
                                
                                <button
                                    type="submit"
                                    className="button-submit"
                                >
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {showHelpModal && (
                <div 
                    className="modal-overlay"
                    onClick={handleCloseHelpModal}
                >
                    <div 
                        className="modal-content help-modal"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h3 className="modal-title">
                            Help Resources
                        </h3>
                        
                        <div className="help-content">
                            <div className="help-section">
                                <h4 className="help-subtitle">User Manual</h4>
                                <p className="help-text">
                                    The comprehensive user manual provides detailed instructions 
                                    for both athletes and coaches on how to use the RPE Tracker.
                                </p>
                                <button
                                    onClick={downloadUserManual}
                                    className="help-download-button"
                                >
                                    <svg className="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    Download User Manual
                                </button>
                            </div>

                            <div className="help-section">
                                <h4 className="help-subtitle">Contact Support</h4>
                                <p className="help-text">
                                    For further assistance, contact the development team:
                                </p>
                                <p className="help-contact">
                                    Email: rpereminder@gmail.com
                                </p>
                            </div>
                        </div>
                        
                        <div className="button-group-horizontal">
                            <button
                                type="button"
                                onClick={() => setShowHelpModal(false)}
                                className="button-submit"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HomePage;
