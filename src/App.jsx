import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./HomePage";
import MyForm from "./MyForm";
import ReportPage from "./ReportPage";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/form" element={<MyForm />} />
                <Route path="/report" element={<ReportPage />} />
            </Routes>
        </Router>
    );
};

export default App;
