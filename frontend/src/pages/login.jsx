import { useState } from "react";
import api from "../services/api";

function Login({ onRegister, onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      const token = response.data.access_token;

      localStorage.setItem("access_token", token);

      console.log("Login successful");

      onLoginSuccess();
    } catch (error) {
      if (error.response) {
        setError(
          error.response.data.detail || "Invalid email or password."
        );
      } else {
        setError(
          "Could not connect to the server. Make sure FastAPI is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = () => {
    console.log("Forgot password clicked");
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">🎓</div>

        <h1>AI Study Assistant</h1>

        <p className="auth-subtitle">
          Welcome back! Sign in to continue studying.
        </p>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <div className="password-label">
              <label>Password</label>

              <button
                type="button"
                className="forgot-button"
                onClick={handleForgotPassword}
              >
                Forgot password?
              </button>
            </div>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p className="auth-switch">
          Don't have an account?{" "}
          <button
            type="button"
            className="link-button"
            onClick={onRegister}
          >
            Create account
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;