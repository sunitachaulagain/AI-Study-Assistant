import { NavLink, useNavigate } from "react-router-dom";
import "./Sidebar.css";

function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <aside className="sidebar">

      <nav className="sidebar-nav">

        <NavLink
          to="/dashboard"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>🏠</span>
          Dashboard
        </NavLink>

        <NavLink
          to="/documents"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>📚</span>
          Documents
        </NavLink>

        <NavLink
          to="/subjects"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>📂</span>
          Subjects
        </NavLink>

        <NavLink
          to="/chat"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>💬</span>
          AI Chat
        </NavLink>

        <NavLink
          to="/quiz"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>📝</span>
          Quiz
        </NavLink>

        <NavLink
          to="/flashcards"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>🃏</span>
          Flashcards
        </NavLink>

        <NavLink
          to="/study-plan"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>📅</span>
          Study Plan
        </NavLink>

      </nav>

      <div className="sidebar-bottom">

        <NavLink
          to="/settings"
          className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
        >
          <span>⚙️</span>
          Settings
        </NavLink>

        <button
          className="nav-item logout"
          onClick={handleLogout}
        >
          <span>🚪</span>
          Logout
        </button>

      </div>

    </aside>
  );
}

export default Sidebar;
