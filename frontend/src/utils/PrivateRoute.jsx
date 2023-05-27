import React, { useContext } from "react";
import { Outlet, Navigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const PrivateRoute = ({ component: component, ...rest }) => {
  let { user } = useContext(AuthContext);
  console.log("PrivateRoute");
  return user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
