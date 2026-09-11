import React, { useEffect, useState, useContext } from "react";
import Layout from "../components/Layout/Layout";
import api from "../services/api";
import { AuthContext } from "../context/AuthContext";

const MyRequests = () => {
  const [requests, setRequests] = useState([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        // Assuming user.username is the employee ID or email
        const response = await api.get(`/employee/${user?.username}/requests`);
        setRequests(response.data);
      } catch (error) {
        console.error("Error fetching my requests:", error);
      }
    };
    if (user) {
      fetchRequests();
    }
  }, [user]);

  return (
    <Layout>
      <h1>My Leave Requests</h1>
      {requests.length === 0 ? (
        <p>No leave requests found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Reason</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((req) => (
              <tr key={req.requestId}>
                <td>{req.startDate}</td>
                <td>{req.endDate}</td>
                <td>{req.reason}</td>
                <td>{req.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
};

export default MyRequests;
