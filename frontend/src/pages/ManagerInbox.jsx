import React, { useEffect, useState } from "react";
import Layout from "../components/Layout/Layout";
import api from "../services/api";

const ManagerInbox = () => {
  const [pending, setPending] = useState([]);

  useEffect(() => {
    const fetchPending = async () => {
      try {
        const response = await api.get("/manager/456/pending");
        setPending(response.data);
      } catch (error) {
        console.error("Error fetching pending requests:", error);
      }
    };
    fetchPending();
  }, []);

  const handleDecision = async (requestId, decision) => {
    try {
      await api.put(`/leave/${requestId}`, { status: decision });
      setPending(pending.filter(req => req.requestId !== requestId));
    } catch (error) {
      console.error("Error updating request:", error);
    }
  };

  return (
    <Layout>
      <h1>Manager Inbox</h1>
      <table>
        <thead>
          <tr>
            <th>Employee</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Reason</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {pending.map((req) => (
            <tr key={req.requestId}>
              <td>{req.employeeName}</td>
              <td>{req.startDate}</td>
              <td>{req.endDate}</td>
              <td>{req.reason}</td>
              <td>
                <button onClick={() => handleDecision(req.requestId, "APPROVED")}>Approve</button>
                <button onClick={() => handleDecision(req.requestId, "REJECTED")}>Reject</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Layout>
  );
};

export default ManagerInbox;
