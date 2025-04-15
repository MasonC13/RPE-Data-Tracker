import React, { useState } from "react";
import { useForm } from "react-hook-form";

const MyForm = () => {
    const {
        register, 
        handleSubmit,
        formState: { errors },
    } = useForm();

    const [submitted, setSubmitted] = useState(false);

    const onSubmit = async (data) => {
        try {
            const response = await fetch("http://127.0.0.1:4025/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
    
            if (response.ok) {
                setSubmitted(true);
            } else {
                console.error("Error saving data");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };

    if (submitted) {
        return <div className="p-4 text-center text-lg font-bold">Thank you for your response!</div>;
    }

    return (
        <div className="form-container">
        <div className="p-4 border rounded-lg max-w-xl mx-auto">
            <h1 className="text-3xl font-bold mb-6 text-center">Rate of Perceived Exertion Form</h1>
            <form onSubmit={handleSubmit(onSubmit)}>
                {/* Email */}
                <div className="mb-6">
                    <label className="block mb-2">Email:</label>
                    <input
                        {...register("email", { required: "Email is required", pattern: { value: /\S+@\S+\.\S+/, message: "Invalid email" }})}
                        className="border p-2 rounded-md w-full"
                    />
                    {errors.email && <p className="text-red-500">{errors.email.message}</p>}
                </div>

                {/* Last 4 Digits */}
                <div className="mb-6">
                    <label className="block mb-2">Last 4 Digits (Phone):</label>
                    <input
                        {...register("last4", { required: "Last 4 digits are required", pattern: { value: /^\d{4}$/, message: "Must be 4 digits" }})}
                        className="border p-2 rounded-md w-full"
                    />
                    {errors.last4 && <p className="text-red-500">{errors.last4.message}</p>}
                </div>

                {/* First Name */}
                <div className="mb-6">
                    <label className="block mb-2">First Name:</label>
                    <input
                        {...register("firstName", { required: "First name is required" })}
                        className="border p-2 rounded-md w-full"
                    />
                    {errors.firstName && <p className="text-red-500">{errors.firstName.message}</p>}
                </div>

                {/* Last Name */}
                <div className="mb-6">
                    <label className="block mb-2">Last Name:</label>
                    <input
                        {...register("lastName", { required: "Last name is required" })}
                        className="border p-2 rounded-md w-full"
                    />
                    {errors.lastName && <p className="text-red-500">{errors.lastName.message}</p>}
                </div>

                {/* Position */}
                <div className="mb-6">
                    <label className="block mb-2">Position:</label>
                    <select
                        defaultValue=""
                        {...register("position", { required: "Position is required" })}
                        className="border p-2 rounded-md w-full"
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
                    {errors.position && <p className="text-red-500">{errors.position.message}</p>}
                </div>

                {/* Summer Attendance */}
                <div className="mb-6">
                    <label className="block mb-2">Summer Attendance:</label>
                    <select
                        defaultValue=""
                        {...register("summerAttendance", { required: "Please select yes or no" })}
                        className="border p-2 rounded-md w-full"
                    >
                        <option value="" disabled>Select option</option>
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                    </select>
                    {errors.summerAttendance && <p className="text-red-500">{errors.summerAttendance.message}</p>}
                </div>

                {/* Intensity Level */}
                <div className="mb-6">
                    <label className="block mb-2">Intensity Level (1-10):</label>
                    <select
                        {...register("intensityLevel", { required: "Please select an intensity level" })}
                        defaultValue=""
                        className="border p-2 rounded-md w-full"
                    >
                         <option value="" disabled>Select intensity level</option>
                         {[...Array(10)].map((_, index) => (
                         <option key={index} value={index + 1}>{index + 1}</option>
                         ))}
                    </select>
                    {errors.intensityLevel && <p className="text-red-500">{errors.intensityLevel.message}</p>}
                </div>

                <button type="submit">
                    Submit
                </button>
            </form>
        </div>
        </div>
    );
};

export default MyForm;
