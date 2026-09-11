import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";

const Navbar = () => {
  // Replace these placeholders with your actual Cognito values
  const domainPrefix = "leave-mgmt-auth"; // your Cognito domain prefix
  const region = "us-east-1"; // your AWS region
  const clientId = "YOUR_APP_CLIENT_ID"; // Cognito App Client ID
  const redirectUri = "http://localhost:5173/"; // or Amplify app URL

  const loginUrl = `https://${domainPrefix}.auth.${region}.amazoncognito.com/login?client_id=${clientId}&response_type=code&scope=email+openid+profile&redirect_uri=${redirectUri}`;
  const logoutUrl = `https://${domainPrefix}.auth.${region}.amazoncognito.com/logout?client_id=${clientId}&logout_uri=${redirectUri}`;

  return (
    <nav className="navbar">
      <h2 className="logo">Leave Management</h2>
      <ul className="nav-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/submit-leave">Submit Leave</Link></li>
        <li><Link to="/my-requests">My Requests</Link></li>
        <li><Link to="/manager-inbox">Manager Inbox</Link></li>
        <li>
          <a href={loginUrl} className="login-btn">Login</a>
        </li>
        <li>
          <a href={logoutUrl} className="logout-btn">Logout</a>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
