import React, { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import axiosInstance from "../utils/axiosInstance";

const Header = () => {
  let { user, logoutUser, userDetails } = useContext(AuthContext);

  return (
    <div>
      <Link to="/">Home</Link>
      <span> | </span>
      {user ? (
        <p onClick={logoutUser}>Logout</p>
      ) : (
        <Link to="/login">Login</Link>
      )}
      {user && <p> Hello {user.name}</p>}
      {userDetails && <p> Name: {userDetails.name}</p>}
      {userDetails && <p> Email: {userDetails.email}</p>}
      {userDetails && <p> Mobile: {userDetails.phone}</p>}
    </div>
  );
};

export default Header;
