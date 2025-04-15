import React from "react";

const ReportPage = () => {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
      <iframe
        src="http://127.0.0.1:4026" // Your Dash app running locally
        title="Trainer Report"
        width="100%"
        height="100%"
        style={{ border: "none" }}
      />
    </div>
  );
};

export default ReportPage;
