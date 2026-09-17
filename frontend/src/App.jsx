import { useState, useEffect } from "react";
import Login from "./pages/login";
import Register from "./pages/Register";
import Sidebar from "./pages/Sidebar";
import Dashboard from "./pages/Dashboard";
import Documents from "./pages/Documents";
import Chat from "./pages/Chat";
import Quiz  from "./pages/Quiz";
import StudyPlan from "./pages/StudyPlan";
import api from "./services/api";

import "./App.css";

function App() {
  const [page, setPage] = useState(() => {
    const token = localStorage.getItem("access_token");
    return token ? "dashboard" : "login";
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      api
        .get("/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => setPage("dashboard"))
        .catch(() => {
          localStorage.removeItem("access_token");
          setPage("login");
        });
    }
  }, []);

  const handleLoginSuccess = () => {
    setPage("dashboard");
  };

  const isAuthPage = page === "login" || page === "register";

  return (
    <>
      {page === "login" && (
        <Login
          onRegister={() => setPage("register")}
          onLoginSuccess={handleLoginSuccess}
        />
      )}

      {page === "register" && (
        <Register
          onLogin={() => setPage("login")}
        />
      )}

      {!isAuthPage && (
        <div className="app-layout">
          <Sidebar currentPage={page} onNavigate={setPage} />

          {page === "dashboard" && (
            <Dashboard onNavigate={setPage} />
          )}

          {page === "documents" && (
            <Documents onNavigate={setPage} />
          )}

          {page === "chat" && (
            <Chat onNavigate={setPage} />
          )}

          {page === "quiz" && (
            <Quiz onNavigate={setPage} />
          )}

          {page === "study-plan" && (
            <StudyPlan onNavigate={setPage} />
          )}
        </div>
      )}
    </>
  );
}

export default App;