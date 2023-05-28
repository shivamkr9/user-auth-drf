import React from "react";
import axios from "axios";
import jwt_decode from "jwt-decode";
import dayjs from "dayjs";

const baseURL = "http://localhost:8000";

let authToken = localStorage.getItem("authToken")
  ? JSON.parse(localStorage.getItem("authToken"))
  : null;

const axiosInstance = axios.create({
  baseURL: baseURL,
  //   timeout: 5000,
  headers: {
    Authorization: authToken ? `Bearer ${authToken}` : null,
    "Content-Type": "application/json",
    accept: "application/json",
  },
});

// console.log("axiosInstance", axiosInstance);

axiosInstance.interceptors.request.use(async (req) => {
  if (!authToken) {
    authToken = localStorage.getItem("authToken")
      ? JSON.parse(localStorage.getItem("authToken"))
      : null;
    console.log("authToken", authToken);
    const refreshToken = localStorage.getItem("refreshToken")
      ? JSON.parse(localStorage.getItem("refreshToken"))
      : null;
    if (!refreshToken) {
      //   window.location.href = "/login";
    }
    req.headers.Authorization = `Bearer ${authToken}` ? authToken : null;
  }

  const user = jwt_decode(authToken);
  const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
  //   if (!refreshToken) return req;
  if (!isExpired) return req;
  const response = await axios.post(`${baseURL}/api/token/refresh/`, {
    refresh: authToken.refresh,
  });
  console.log("response", response);
  localStorage.setItem("authToken", JSON.stringify(response.data));
  req.headers.Authorization = `Bearer ${response.data.access}`;
  console.log("isExpired", isExpired);
  return req;
});

export default axiosInstance;
