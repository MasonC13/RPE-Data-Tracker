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

    const onSubmit = async (formData) => {
        setLoading(true);
        setError("");

        const fullData = {
            ...formData,
            email: `${formData.emailPrefix}@truman.edu`
        };

        try {
            const response = await fetch("http://127.0.0.1:4025/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(fullData),
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

    if (submitted) {
        return (
            <div className="form-container">
                <div className="form-wrapper success-container">
                    <div className="success-card">
                        <div className="success-icon">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                        <h2 className="success-title">Thank You!</h2>
                        <p className="success-message">Your RPE response has been submitted successfully.</p>
                        <div className="success-date">
                            Submitted on: {new Date().toLocaleDateString()}
                        </div>
                        <a href="/" className="success-button">
                            Return Home
                        </a>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="form-container">
            <div className="form-wrapper">
                <div className="form-header">
                    <a href="/" className="back-link">
                        <svg className="back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                        </svg>
                        Back
                    </a>
                    <div className="form-date">
                        Today: {new Date().toLocaleDateString()}
                    </div>
                </div>

                <div className="form-card">
                    <div className="form-card-header">
                        <h1 className="form-title">
                            Rate of Perceived Exertion
                        </h1>
                        <div className="form-subtitle">
                            Truman State University Athletics
                        </div>
                    </div>

                    <form onSubmit={handleSubmit(onSubmit)} className="form-body">
                        {error && (
                            <div className="error-message">
                                {error}
                            </div>
                        )}

                        <div className="field-group">
                            {/* Email field with @truman.edu suffix */}
                            <div className="field">
                                <label className="field-label">Truman Email Address</label>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <input
                                        {...register("emailPrefix", {
                                            required: "Email is required",
                                            pattern: {
                                                value: /^[a-zA-Z0-9._%+-]+$/,
                                                message: "Invalid format before @truman.edu"
                                            }
                                        })}
                                        className="field-input"
                                        placeholder="jsmith"
                                        type="text"
                                        style={{ flex: 1 }}
                                    />
                                    <span style={{
                                        marginLeft: '8px',
                                        color: '#555',
                                        fontWeight: 'bold',
                                        whiteSpace: 'nowrap'
                                    }}>
                                        @truman.edu
                                    </span>
                                </div>
                                {errors.emailPrefix && <p className="field-error">{errors.emailPrefix.message}</p>}
                            </div>

                            {/* RPE selection */}
                            <div className="field">
                                <label className="field-label">Intensity Level (1-10)</label>
                                <select
                                    {...register("intensityLevel", { required: "Please select an intensity level" })}
                                    defaultValue=""
                                    className="field-input"
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
                                {errors.intensityLevel && <p className="field-error">{errors.intensityLevel.message}</p>}
                                <div className="intensity-gradient"></div>
                                <div className="intensity-labels">
                                    <span>Easy</span>
                                    <span>Moderate</span>
                                    <span>Hard</span>
                                    <span>Max</span>
                                </div>
                            </div>
                        </div>

                        <div style={{ marginTop: '1.5rem' }}>
                            <button
                                type="submit"
                                disabled={loading}
                                className="form-button"
                            >
                                {loading ? (
                                    <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                        <svg className="loading-spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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

                        <div className="info-text">
                            Your response will be recorded for {new Date().toLocaleDateString()}
                        </div>
                    </form>
                </div>

                <div className="form-footer">
                    &copy; {new Date().getFullYear()} Truman State University Athletics
                </div>
            </div>
        </div>
    );
};

export default MyForm;


