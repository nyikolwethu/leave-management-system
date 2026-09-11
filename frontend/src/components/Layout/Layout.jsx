import React from "react";
import Navbar from "../Navbar/Navbar";
import "./Layout.css";

const Layout = ({ children }) => (
  <div className="layout">
    <Navbar />
    <main>{children}</main>
  </div>
);

export default Layout;
