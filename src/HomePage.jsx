import React, { useState } from "react";

const HomePage = () => {
    const [showPasswordModal, setShowPasswordModal] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordError, setPasswordError] = useState("");
    
    // Replace with your actual password
    const COACH_PASSWORD = "bulldogs";

    // For athlete access - no password required
    const handleAthleteClick = () => {
        window.location.href = "/form";
    };

    // For coach/trainer access - requires password
    const handleTrainerClick = () => {
        setShowPasswordModal(true);
    };
    
    // Verify password and navigate if correct
    const handlePasswordSubmit = (e) => {
        e.preventDefault();
        
        if (password === COACH_PASSWORD) {
            // Password is correct
            setPasswordError("");
            window.location.href = "/report";
        } else {
            // Password is incorrect
            setPasswordError("Incorrect password. Please try again.");
        }
    };
    
    // Close the modal when clicking outside
    const handleCloseModal = (e) => {
        if (e.target === e.currentTarget) {
            setShowPasswordModal(false);
            setPassword("");
            setPasswordError("");
        }
    };

    return (
        <div style={{ 
            display: 'flex', 
            flexDirection: 'column', 
            height: '100vh',
            background: 'linear-gradient(to bottom, var(--truman-purple), var(--truman-light-blue))'
        }}>
            <header style={{ padding: '1rem' }}>
                <div style={{ 
                    background: 'rgba(255, 255, 255, 0.1)', 
                    backdropFilter: 'blur(8px)',
                    padding: '0.5rem 1rem',
                    borderRadius: '8px',
                    display: 'inline-block'
                }}>
                    <div style={{ color: '#a0c4ff', fontSize: '0.875rem', fontWeight: '500' }}>
                        BULLDOGS ATHLETICS
                    </div>
                </div>
            </header>
            
            <div style={{ 
                flex: 1, 
                display: 'flex', 
                flexDirection: 'column',
                justifyContent: 'center', 
                alignItems: 'center',
                padding: '0 1rem'
            }}>
                <h1 style={{ 
                    fontSize: '2.5rem', 
                    fontWeight: 'bold', 
                    textAlign: 'center', 
                    color: 'var(--truman-white)',
                    marginBottom: '0.5rem'
                }}>
                    Truman State University
                </h1>
                <h2 style={{ 
                    fontSize: '1.75rem', 
                    fontWeight: '600', 
                    textAlign: 'center', 
                    color: '#a0c4ff',
                    marginBottom: '3rem'
                }}>
                    Rate of Perceived Exertion
                </h2>
                
                <div style={{ 
                    background: 'rgba(255, 255, 255, 0.1)', 
                    backdropFilter: 'blur(8px)',
                    padding: '2rem',
                    borderRadius: '12px',
                    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.2)',
                    width: '100%',
                    maxWidth: '400px'
                }}>
                    <h3 style={{ 
                        fontSize: '1.25rem', 
                        fontWeight: '500', 
                        textAlign: 'center', 
                        color: 'var(--truman-white)',
                        marginBottom: '1.5rem'
                    }}>
                        Please select your role:
                    </h3>
                    
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        <button
                            onClick={handleAthleteClick}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                background: 'linear-gradient(to right, #2563eb, #60a5fa)',
                                color: 'white',
                                padding: '1rem',
                                borderRadius: '8px',
                                width: '100%',
                                fontSize: '1.125rem',
                                fontWeight: 'bold',
                                border: '1px solid rgba(255, 255, 255, 0.2)',
                                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease'
                            }}
                        >
                            <svg style={{ width: '1.5rem', height: '1.5rem', marginRight: '0.75rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                            </svg>
                            I am an athlete
                        </button>
                        
                        <button
                            onClick={handleTrainerClick}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                background: 'linear-gradient(to right, var(--truman-purple), #8b5cf6)',
                                color: 'white',
                                padding: '1rem',
                                borderRadius: '8px',
                                width: '100%',
                                fontSize: '1.125rem',
                                fontWeight: 'bold',
                                border: '1px solid rgba(255, 255, 255, 0.2)',
                                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease'
                            }}
                        >
                            <svg style={{ width: '1.5rem', height: '1.5rem', marginRight: '0.75rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                            </svg>
                            I am a trainer/coach
                        </button>
                    </div>
                </div>
            </div>
            
            <footer style={{ padding: '1.5rem', textAlign: 'center' }}>
                <div style={{ color: '#a0c4ff', fontSize: '0.875rem' }}>
                    <svg style={{ display: 'inline-block', width: '1rem', height: '1rem', marginRight: '0.25rem', verticalAlign: 'middle' }} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd"></path>
                    </svg>
                    Truman State University Athletics
                    <span style={{ margin: '0 0.5rem' }}>•</span>
                    {new Date().getFullYear()}
                </div>
            </footer>
            
            {/* Password Modal */}
            {showPasswordModal && (
                <div 
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        backgroundColor: 'rgba(0, 0, 0, 0.5)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        zIndex: 1000
                    }}
                    onClick={handleCloseModal}
                >
                    <div 
                        style={{
                            backgroundColor: 'white',
                            padding: '2rem',
                            borderRadius: '8px',
                            width: '90%',
                            maxWidth: '400px',
                            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                        }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h3 style={{
                            fontSize: '1.25rem',
                            fontWeight: 'bold',
                            color: 'var(--truman-purple)',
                            marginBottom: '1rem',
                            textAlign: 'center'
                        }}>
                            Coach/Trainer Access
                        </h3>
                        
                        <p style={{
                            fontSize: '0.875rem',
                            color: '#4b5563',
                            marginBottom: '1.5rem',
                            textAlign: 'center'
                        }}>
                            Please enter your password to access the dashboard.
                        </p>
                        
                        <form onSubmit={handlePasswordSubmit}>
                            <div style={{ marginBottom: '1rem' }}>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter password"
                                    style={{
                                        width: '100%',
                                        padding: '0.75rem',
                                        borderRadius: '4px',
                                        border: '1px solid #d1d5db',
                                        fontSize: '1rem'
                                    }}
                                    autoFocus
                                />
                                {passwordError && (
                                    <p style={{
                                        color: '#ef4444',
                                        fontSize: '0.875rem',
                                        marginTop: '0.5rem'
                                    }}>
                                        {passwordError}
                                    </p>
                                )}
                            </div>
                            
                            <div style={{
                                display: 'flex',
                                justifyContent: 'space-between'
                            }}>
                                <button
                                    type="button"
                                    onClick={() => {
                                        setShowPasswordModal(false);
                                        setPassword("");
                                        setPasswordError("");
                                    }}
                                    style={{
                                        padding: '0.5rem 1rem',
                                        backgroundColor: '#f3f4f6',
                                        color: '#4b5563',
                                        borderRadius: '4px',
                                        border: 'none',
                                        fontSize: '0.875rem',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Cancel
                                </button>
                                
                                <button
                                    type="submit"
                                    style={{
                                        padding: '0.5rem 1rem',
                                        backgroundColor: 'var(--truman-purple)',
                                        color: 'white',
                                        borderRadius: '4px',
                                        border: 'none',
                                        fontSize: '0.875rem',
                                        cursor: 'pointer'
                                    }}
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
  
