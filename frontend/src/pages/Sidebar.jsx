import "./Sidebar.css";

function Sidebar({ currentPage, onNavigate }) {
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    window.location.reload();
  };

  return (
    <aside className="sidebar">

      <div className="logo">
        <h2>AI Study Assistant</h2>
        <span>Learn smarter with AI</span>
      </div>

      <nav className="sidebar-nav">

        <button
          className={`nav-item ${currentPage === "dashboard" ? "active" : ""}`}
          onClick={() => onNavigate("dashboard")}
        >
          <span>🏠</span>
          Dashboard
        </button>

        <button
          className={`nav-item ${currentPage === "documents" ? "active" : ""}`}
          onClick={() => onNavigate("documents")}
        >
          <span>📚</span>
          Documents
        </button>

        <button
          className={`nav-item ${currentPage === "chat" ? "active" : ""}`}
          onClick={() => onNavigate("chat")}
        >
          <span>💬</span>
          AI Chat
        </button>

        <button
          className={`nav-item ${currentPage === "quiz" ? "active" : ""}`}
          onClick={() => onNavigate("quiz")}
        >
          <span>📝</span>
          Quiz
        </button>

        <button
          className={`nav-item ${currentPage === "study-plan" ? "active" : ""}`}
          onClick={() => onNavigate("study-plan")}
        >
          <span>📅</span>
          Study Plan
        </button>

      </nav>

      <div className="sidebar-bottom">

        <button
          className={`nav-item ${currentPage === "settings" ? "active" : ""}`}
          onClick={() => onNavigate("settings")}
        >
          <span>⚙️</span>
          Settings
        </button>

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
