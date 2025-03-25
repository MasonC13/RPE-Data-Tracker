import React from "react";
import { useForm } from "react-hook-form";

const MyForm = () => {
    const {
        register, 
        handleSubmit,
        formstate: { errors },

    } = useForm();

    const onSubmit = (data) => {
        console.log(data); 
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="p-4 border rounded-lg">
            <div>
                <label>Name:</label>
                <input
                    {...register("name", { required: "Name is required "})}
                    className="border p-2 rounded-md w-full"
                />
                {errors.name && <p className="text-red-500">{errors.name.message}</p>}
            </div>

            <div>
                <label>Email:</label>
                <input
                    {...register("email", {
                        required: "Email is required",
                        pattern: { value: /\S+@\S+.\S+/, message: "Invalid email" }, 
                    })}
                    className="border p-2 rounded-md w-full"
                />
                {errors.email && <p className="text-red-500">{errors.email.message}</p>}
            </div>

            <div>
                <label>Intensity Level:</label>
                <input
                    {...register("intensity level", {
                        required: "Intensity Level is required",
                        min: { value: 1, message: "Input must be at least 1" },
                        max: { value: 10, message: "Input must not be more than 10"}, 
                    })}
                    className="border p-2 rounded-md w-full"
                />
                {errors.email && <p className="text-red-500">{errors.email.message}</p>}
            </div>

            <button type="submit" className="bg-blue-500 text-white p-2 rounded-md mt-4">
                Submit
            </button>
        </form>
    );
};

export default MyForm;