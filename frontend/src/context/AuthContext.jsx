import { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  let [user, setUser] = useState(() =>
    localStorage.getItem("authToken")
      ? jwt_decode(localStorage.getItem("authToken"))
      : null
  );
  let [authToken, setAuthToken] = useState(() =>
    localStorage.getItem("authToken")
      ? JSON.parse(localStorage.getItem("authToken"))
      : null
  );
  let [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  //   Create a login function that will be used to login the user.

  let loginUser = async (e) => {
    e.preventDefault();
    let res = await fetch("http://localhost:8000/api/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: e.target.email.value,
        password: e.target.password.value,
      }),
    });
    let data = await res.json();
    console.log("data:", data);
    console.log(res);
    if (res.status === 200) {
      setUser(jwt_decode(data.access));
      setAuthToken(data);
      localStorage.setItem("authToken", JSON.stringify(data.access));
      localStorage.setItem("refreshToken", JSON.stringify(data.refresh));
      navigate("/");
    } else {
      alert("Invalid credentials");
    }
  };

  // Creating a logout function that will be used to logout the user.

  let logoutUser = () => {
    setUser(null);
    setAuthToken(null);
    localStorage.removeItem("authToken");
    localStorage.removeItem("refreshToken");
    navigate("/login");
  };

  // Create a function that will be used to update the access token.

  let updateToken = async () => {
    let res = await fetch("http://localhost:8000/api/token/refresh/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh: JSON.parse(localStorage?.getItem("refreshToken")),
      }),
    });
    let data = await res.json();
    if (res.status === 200) {
      setUser(jwt_decode(data.access));
      setAuthToken(data);
      localStorage.setItem("authToken", JSON.stringify(data.access));
    } else {
      logoutUser();
    }
    if (loading) {
      setLoading(false);
    }
  };

  //Passing the data to the context provider.
  let contextData = {
    user: user,
    authToken: authToken,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  //calling the updateToken function in eache 9 minutes.
  useEffect(() => {
    if (loading) {
      updateToken();
    }

    let nineMinutes = 9 * 60 * 1000;
    let interval = setInterval(() => {
      if (authToken) {
        updateToken();
      }
    }, nineMinutes);
    return () => clearInterval(interval);
  }, [authToken, loading]);

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
