import React, { useContext } from "react";
import { Outlet, Navigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const PrivateRoute = ({ component: component, ...rest }) => {
  let { user } = useContext(AuthContext);
  let accessToken = localStorage.getItem("authToken")
    ? JSON.parse(localStorage.getItem("authToken"))
    : null;
  console.log("PrivateRoute");
  return accessToken ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
