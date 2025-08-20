// ProtectedRoute.js
import React from "react";
import { Navigate } from "react-router-dom";

// Development-only version: always allow access
const ProtectedRoute = ({ children }) => {
  return children;
};

export default ProtectedRoute;

/* 
// Original logic — use this in production
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
};
*/
