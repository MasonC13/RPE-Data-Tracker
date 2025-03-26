import React, { useState } from "react";
import { useForm } from "react-hook-form";

const MyForm = () => {
    const {
        register, 
        handleSubmit,
        formState: { errors },
    } = useForm();

    const [submitted, setSubmitted] = useState(false);

    const onSubmit = (data) => {
        console.log(data); 
        setSubmitted(true);
    };

    if (submitted) {
        return <div className="p-4 text-center text-lg font-bold">Thank you for your response!</div>;
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="p-4 border rounded-lg">
            <div className="mb-6">
                <label className="block mb-2">Name:</label>
                <input
                    {...register("name", { required: "Name is required "})}
                    className="border p-2 rounded-md w-full"
                />
                {errors.name && <p className="text-red-500">{errors.name.message}</p>}
            </div>

            <div className="mb-6">
                <label className="block mb-2">Email:</label>
                <input
                    {...register("email", {
                        required: "Email is required",
                        pattern: { value: /\S+@\S+\.\S+/, message: "Invalid email" }, 
                    })}
                    className="border p-2 rounded-md w-full"
                />
                {errors.email && <p className="text-red-500">{errors.email.message}</p>}
            </div>

            <div className="mb-6">
                <label className="block mb-2">Intensity Level:</label>
                <select
                    defaultValue=""
                    {...register("intensityLevel", { required: "Intensity Level is required" })}
                    className="border p-2 rounded-md w-full"
                >
                    <option value="" disabled>Select intensity</option>
                    {[...Array(10).keys()].map((num) => (
                        <option key={num + 1} value={num + 1}>{num + 1}</option>
                    ))}
                </select>
                {errors.intensityLevel && <p className="text-red-500">{errors.intensityLevel.message}</p>}
            </div>

            <div className="mb-6">
                <label className="block mb-2">What type of session did you just complete?</label>
                <select
                    defaultValue=""
                    {...register("sessionType", { required: "Session type is required" })}
                    className="border p-2 rounded-md w-full"
                >
                    <option value="" disabled>Select session type</option>
                    <option value="practice">Practice</option>
                    <option value="weights/conditioning">Weights/Conditioning</option>
                </select>
                {errors.sessionType && <p className="text-red-500">{errors.sessionType.message}</p>}
            </div>

            <button type="submit" className="bg-blue-500 text-white p-2 rounded-md mt-4">
                Submit
            </button>
        </form>
    );
};

export default MyForm;
