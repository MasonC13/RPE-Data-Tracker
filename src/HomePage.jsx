import React, { useState } from "react";
import "./index.css";

const HomePage = () => {
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");
    
    const COACH_PASSWORD = "bulldogs";

    const handleAthleteClick = () => {
        window.location.href = "/form";
    };

    const handleTrainerClick = () => {
        setShowPasswordModal(true);
    };
    
    const handlePasswordSubmit = (e) => {
        e.preventDefault();
        
        if (password === COACH_PASSWORD) {
            setPasswordError("");
            window.location.href = "/report";
        } else {
            setPasswordError("Incorrect password. Please try again.");
        }
    };
    
    const handleCloseModal = (e) => {
        if (e.target === e.currentTarget) {
            setShowPasswordModal(false);
            setPassword("");
            setPasswordError("");
        }
    };

    return (
        <div className="container">
            <header className="header">
                <div className="header-content">
                    <div className="header-text">
                        BULLDOGS ATHLETICS
                    </div>
                </div>
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
        </div>
    );
};

export default HomePage;
