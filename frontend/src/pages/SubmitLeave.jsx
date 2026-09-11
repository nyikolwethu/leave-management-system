import React, { useState } from "react";
import Layout from "../components/Layout/Layout";
import api from "../services/api"; // we'll build this next

const SubmitLeave = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/leave", {
        startDate,
        endDate,
        reason,
      });
      setMessage("Leave request submitted successfully!");
    } catch (error) {
      console.error(error);
      setMessage("Error submitting leave request.");
    }
  };

  return (
    <Layout>
      <h1>Submit Leave Request</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <br />
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <br />
        <label>
          Reason:
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
      <p>{message}</p>
    </Layout>
  );
};

export default SubmitLeave;
