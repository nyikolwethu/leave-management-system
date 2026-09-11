import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);

  // If user exists, show the protected page
  // Otherwise redirect to login
  return user ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
