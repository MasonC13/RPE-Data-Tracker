import React from "react";
import MyForm from "./MyForm";

const App = () => {
  return (
    <div className="flex flex-col min-h-screen justify-start items-center">
      <h1 className="title text-4xl font-bold mt-8 mb-8">Rate of Perceived Exertion Form</h1> 
      <div className="flex justify-center items-center w-full max-w-md p-4">
        <MyForm />
      </div>
    </div>
  );
};

export default App;
