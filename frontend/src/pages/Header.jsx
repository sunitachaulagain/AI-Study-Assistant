import { useEffect, useState } from "react";
import authFetch from "../services/authFetch";
import "./Header.css";

function Header() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await authFetch("/auth/me");
        if (response.ok) {
          const data = await response.json();
          setUser(data);
        }
      } catch (error) {
        console.error("Header user fetch error:", error);
      }
    };
    fetchUser();
  }, []);

  return (
    <header className="app-header">
      <div className="header-left">
        <span className="header-logo">🎓</span>
        <h1>AI Study Assistant</h1>
      </div>
      <div className="header-right">
        {user && (
          <div className="header-user">
            <div className="header-avatar">
              {user.email?.charAt(0).toUpperCase()}
            </div>
            <span>{user.email}</span>
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
