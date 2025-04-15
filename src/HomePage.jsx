import React from "react";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
    const navigate = useNavigate();

    const handleAthleteClick = () => {
        navigate("/form");
    };

    const handleTrainerClick = () => {
        navigate("/report");
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            <h1 style={{ fontSize: '3rem', fontWeight: 'bold', textAlign: 'center', marginTop: '32px' }}>
                Truman State University
                <br />
                Rate of Perceived Exertion
            </h1>
    
            <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '32px' }}>
                    <button
                        onClick={handleAthleteClick}
                        style={{
                            backgroundColor: '#00B2E3',
                            color: 'white',
                            padding: '20px 40px',
                            borderRadius: '10px',
                            width: '300px',
                            fontSize: '1.25rem',
                            fontWeight: 'bold'
                        }}
                    >
                        I am an athlete
                    </button>
                    <button
                        onClick={handleTrainerClick}
                        style={{
                            backgroundColor: '#00B2E3',
                            color: 'white',
                            padding: '20px 40px',
                            borderRadius: '10px',
                            width: '300px',
                            fontSize: '1.25rem',
                            fontWeight: 'bold'
                        }}
                    >
                        I am a trainer/coach
                    </button>
                </div>
            </div>
        </div>
    );    
    
};

export default HomePage;
