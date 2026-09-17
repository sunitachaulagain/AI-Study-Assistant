import { useState } from "react";
import api from "../services/api";

function Register({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await api.post("/auth/register", {
        email,
        password,
      });

      setSuccess("Account created successfully! You can now sign in.");

      setEmail("");
      setPassword("");
    } catch (error) {
      if (error.response) {
        setError(
          error.response.data.detail || "Registration failed."
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

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">🎓</div>

        <h1>AI Study Assistant</h1>

        <p className="auth-subtitle">
          Create your account and start learning.
        </p>

        <form onSubmit={handleRegister}>
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
            <label>Password</label>

            <input
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          {success && (
            <p className="auth-success">{success}</p>
          )}

          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account?{" "}
          <button
            type="button"
            className="link-button"
            onClick={onLogin}
          >
            Sign in
          </button>
        </p>
      </div>
    </div>
  );
}

export default Register;