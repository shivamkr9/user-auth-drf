import "./App.css";
import { Routes, Route } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Header from "./components/Header";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <Header />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<PrivateRoute />}>
            <Route path="/" exact element={<HomePage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </div>
  );
}

export default App;
