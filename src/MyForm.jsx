import React, { useState } from "react";
import { useForm } from "react-hook-form";

const MyForm = () => {
    const {
        register, 
        handleSubmit,
        formState: { errors },
    } = useForm();

    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const onSubmit = async (data) => {
        setLoading(true);
        setError("");
        try {
            const response = await fetch("http://127.0.0.1:4025/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
    
            if (response.ok) {
                setSubmitted(true);
            } else {
                setError("Failed to save your response. Please try again.");
            }
        } catch (error) {
            setError("Network error. Please check your connection and try again.");
            console.error("Error:", error);
        } finally {
            setLoading(false);
        }
    };

    const formContainerStyle = {
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        background: 'linear-gradient(to bottom, var(--truman-purple), var(--truman-light-blue))',
        padding: '1rem'
    };

    const formWrapperStyle = {
        maxWidth: '600px',
        width: '100%',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        flex: 1
    };

    const headerStyle = {
        display: 'flex',
        alignItems: 'center',
        marginBottom: '1.5rem'
    };

    const backLinkStyle = {
        color: '#a0c4ff',
        display: 'flex',
        alignItems: 'center',
        textDecoration: 'none',
        fontSize: '0.875rem'
    };

    const dateStyle = {
        color: 'var(--truman-white)',
        fontSize: '0.875rem',
        marginLeft: 'auto'
    };

    const formCardStyle = {
        backgroundColor: 'var(--truman-white)',
        borderRadius: '12px',
        overflow: 'hidden',
        boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)'
    };

    const formHeaderStyle = {
        backgroundColor: 'var(--truman-purple)',
        padding: '1.5rem',
        textAlign: 'center'
    };

    const formTitleStyle = {
        fontSize: '1.75rem',
        fontWeight: 'bold',
        color: 'var(--truman-white)',
        margin: 0
    };

    const formSubtitleStyle = {
        fontSize: '0.875rem',
        color: '#a0c4ff',
        marginTop: '0.25rem'
    };

    const formBodyStyle = {
        padding: '1.5rem'
    };

    const fieldGroupStyle = {
        display: 'grid',
        gridTemplateColumns: '1fr',
        gap: '1.5rem',
        marginBottom: '1.5rem'
    };

    const fieldStyle = {
        marginBottom: '1.5rem'
    };
    
    const labelStyle = {
        display: 'block',
        fontSize: '0.875rem',
        fontWeight: '500',
        color: '#4a5568',
        marginBottom: '0.5rem'
    };
    
    const inputStyle = {
        width: '100%',
        padding: '0.75rem',
        border: '1px solid #cbd5e0',
        borderRadius: '0.375rem',
        fontSize: '1rem',
        color: '#2d3748',
        backgroundColor: '#fff',
        outline: 'none'
    };
    
    const errorStyle = {
        color: '#e53e3e',
        fontSize: '0.75rem',
        marginTop: '0.25rem'
    };
    
    const buttonStyle = {
        width: '100%',
        padding: '0.75rem 1rem',
        backgroundColor: 'var(--truman-purple)',
        color: 'white',
        border: 'none',
        borderRadius: '0.375rem',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        background: 'linear-gradient(to right, var(--truman-purple), var(--truman-light-blue))'
    };
    
    const loadingButtonStyle = {
        ...buttonStyle,
        opacity: 0.7,
        cursor: 'not-allowed'
    };
    
    const footerStyle = {
        textAlign: 'center',
        color: '#a0c4ff',
        fontSize: '0.75rem',
        marginTop: '1rem',
        padding: '1rem 0'
    };

    const errorMsgStyle = {
        backgroundColor: '#fff5f5',
        border: '1px solid #fed7d7',
        color: '#c53030',
        padding: '0.75rem',
        borderRadius: '0.375rem',
        marginBottom: '1.5rem',
        fontSize: '0.875rem'
    };

    const intensityGradientStyle = {
        height: '8px',
        borderRadius: '4px',
        background: 'linear-gradient(to right, #10b981, #fbbf24, #ef4444)',
        marginTop: '0.75rem'
    };
    
    const intensityLabelsStyle = {
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '0.75rem',
        color: '#4a5568',
        marginTop: '0.25rem'
    };

    const infoTextStyle = {
        textAlign: 'center',
        fontSize: '0.75rem',
        color: '#718096',
        marginTop: '0.5rem'
    };

    if (submitted) {
        return (
            <div style={formContainerStyle}>
                <div style={{...formWrapperStyle, justifyContent: 'center'}}>
                    <div style={{
                        backgroundColor: 'var(--truman-white)',
                        borderRadius: '12px',
                        padding: '2rem',
                        textAlign: 'center',
                        maxWidth: '400px',
                        width: '100%',
                        margin: '0 auto',
                        boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)'
                    }}>
                        <div style={{
                            width: '64px',
                            height: '64px',
                            borderRadius: '50%',
                            backgroundColor: '#e6fffa',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            margin: '0 auto 1rem auto'
                        }}>
                            <svg style={{ width: '32px', height: '32px', color: '#38b2ac' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--truman-purple)', marginBottom: '0.5rem' }}>Thank You!</h2>
                        <p style={{ color: '#4a5568', marginBottom: '1.5rem' }}>Your RPE response has been submitted successfully.</p>
                        <div style={{ fontSize: '0.875rem', color: '#718096', marginBottom: '1.5rem' }}>
                            Submitted on: {new Date().toLocaleDateString()}
                        </div>
                        <a 
                            href="/"
                            style={{
                                display: 'inline-block',
                                padding: '0.75rem 1.5rem',
                                backgroundColor: 'var(--truman-purple)',
                                color: 'white',
                                borderRadius: '0.375rem',
                                textDecoration: 'none',
                                fontWeight: '500',
                                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
                            }}
                        >
                            Return Home
                        </a>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div style={formContainerStyle} className="form-container">
            <div style={formWrapperStyle}>
                <div style={headerStyle}>
                    <a href="/" style={backLinkStyle}>
                        <svg style={{ width: '1.25rem', height: '1.25rem', marginRight: '0.25rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                        </svg>
                        Back
                    </a>
                    <div style={dateStyle}>
                        Today: {new Date().toLocaleDateString()}
                    </div>
                </div>
                
                <div style={formCardStyle}>
                    <div style={formHeaderStyle}>
                        <h1 style={formTitleStyle}>
                            Rate of Perceived Exertion
                        </h1>
                        <div style={formSubtitleStyle}>
                            Truman State University Athletics
                        </div>
                    </div>
                    
                    <form onSubmit={handleSubmit(onSubmit)} style={formBodyStyle}>
                        {error && (
                            <div style={errorMsgStyle}>
                                {error}
                            </div>
                        )}
                    
                        <div style={{...fieldGroupStyle, '@media (min-width: 768px)': { gridTemplateColumns: '1fr 1fr' }}}>
                            {/* First Name */}
                            <div style={fieldStyle}>
                                <label style={labelStyle}>First Name</label>
                                <input
                                    {...register("firstName", { required: "First name is required" })}
                                    style={inputStyle}
                                    placeholder="Your first name"
                                />
                                {errors.firstName && <p style={errorStyle}>{errors.firstName.message}</p>}
                            </div>

                            {/* Last Name */}
                            <div style={fieldStyle}>
                                <label style={labelStyle}>Last Name</label>
                                <input
                                    {...register("lastName", { required: "Last name is required" })}
                                    style={inputStyle}
                                    placeholder="Your last name"
                                />
                                {errors.lastName && <p style={errorStyle}>{errors.lastName.message}</p>}
                            </div>
                            
                            {/* Email */}
                            <div style={fieldStyle}>
                                <label style={labelStyle}>Email Address</label>
                                <input
                                    {...register("email", { 
                                        required: "Email is required", 
                                        pattern: { 
                                            value: /\S+@\S+\.\S+/, 
                                            message: "Please enter a valid email" 
                                        }
                                    })}
                                    style={inputStyle}
                                    placeholder="your.email@example.com"
                                    type="email"
                                />
                                {errors.email && <p style={errorStyle}>{errors.email.message}</p>}
                            </div>

                            {/* Last 4 Digits */}
                            <div style={fieldStyle}>
                                <label style={labelStyle}>Last 4 Digits (Phone)</label>
                                <input
                                    {...register("last4", { 
                                        required: "Last 4 digits are required", 
                                        pattern: { 
                                            value: /^\d{4}$/, 
                                            message: "Must be exactly 4 digits" 
                                        }
                                    })}
                                    style={inputStyle}
                                    placeholder="1234"
                                    maxLength={4}
                                    type="text"
                                    inputMode="numeric"
                                />
                                {errors.last4 && <p style={errorStyle}>{errors.last4.message}</p>}
                            </div>
                        </div>

                        <div style={{...fieldGroupStyle, '@media (min-width: 768px)': { gridTemplateColumns: '1fr 1fr' }}}>
                            {/* Position */}
                            <div style={fieldStyle}>
                                <label style={labelStyle}>Position</label>
                                <select
                                    defaultValue=""
                                    {...register("position", { required: "Position is required" })}
                                    style={inputStyle}
                                >
                                    <option value="" disabled>Select position</option>
                                    <option value="DB">DB</option>
                                    <option value="DL">DL</option>
                                    <option value="KPS">KPS</option>
                                    <option value="LB">LB</option>
                                    <option value="OL">OL</option>
                                    <option value="QB">QB</option>
                                    <option value="RB">RB</option>
                                    <option value="TE">TE</option>
                                    <option value="WR">WR</option>
                                </select>
                                {errors.position && <p style={errorStyle}>{errors.position.message}</p>}
                            </div>

                            {/* Summer Attendance */}
                            <div style={fieldStyle}>
                                <label style={labelStyle}>Summer Attendance</label>
                                <select
                                    defaultValue=""
                                    {...register("summerAttendance", { required: "Please select yes or no" })}
                                    style={inputStyle}
                                >
                                    <option value="" disabled>Select option</option>
                                    <option value="yes">Yes</option>
                                    <option value="no">No</option>
                                </select>
                                {errors.summerAttendance && <p style={errorStyle}>{errors.summerAttendance.message}</p>}
                            </div>
                        </div>

                        {/* Intensity Level - Full width with explanations */}
                        <div style={fieldStyle}>
                            <label style={labelStyle}>Intensity Level (1-10)</label>
                            <select
                                {...register("intensityLevel", { required: "Please select an intensity level" })}
                                defaultValue=""
                                style={inputStyle}
                            >
                                <option value="" disabled>Select intensity level</option>
                                <option value="1">1 - Very, very easy</option>
                                <option value="2">2 - Very easy</option>
                                <option value="3">3 - Easy</option>
                                <option value="4">4 - Somewhat easy</option>
                                <option value="5">5 - Moderate</option>
                                <option value="6">6 - Somewhat hard</option>
                                <option value="7">7 - Hard</option>
                                <option value="8">8 - Very hard</option>
                                <option value="9">9 - Very, very hard</option>
                                <option value="10">10 - Maximum effort</option>
                            </select>
                            {errors.intensityLevel && 
                                <p style={errorStyle}>{errors.intensityLevel.message}</p>
                            }
                            <div style={intensityGradientStyle}></div>
                            <div style={intensityLabelsStyle}>
                                <span>Easy</span>
                                <span>Moderate</span>
                                <span>Hard</span>
                                <span>Max</span>
                            </div>
                        </div>

                        <div style={{ marginTop: '1.5rem' }}>
                            <button 
                                type="submit"
                                disabled={loading}
                                style={loading ? loadingButtonStyle : buttonStyle}
                            >
                                {loading ? (
                                    <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                        <svg style={{ 
                                            width: '1.25rem', 
                                            height: '1.25rem',
                                            marginRight: '0.75rem',
                                            animation: 'spin 1s linear infinite'
                                        }} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle style={{ opacity: 0.25 }} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path style={{ opacity: 0.75 }} fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Submitting...
                                    </span>
                                ) : (
                                    'Submit Response'
                                )}
                            </button>
                        </div>
                        
                        <div style={infoTextStyle}>
                            Your response will be recorded for {new Date().toLocaleDateString()}
                        </div>
                    </form>
                </div>
                
                <div style={footerStyle}>
                    &copy; {new Date().getFullYear()} Truman State University Athletics
                </div>
            </div>
        </div>
    );
};

export default MyForm;
