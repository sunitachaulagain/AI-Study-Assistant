import { useEffect, useState } from "react";
import authFetch from "../services/authFetch";
import "./Dashboard.css";

function Dashboard({ onNavigate }) {
  const [user, setUser] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState({
    questions_asked: 0,
    quizzes_completed: 0,
    study_progress: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Get current user
      const userResponse = await authFetch("/auth/me");

      if (!userResponse.ok) {
        throw new Error("Failed to fetch user");
      }

      const userData = await userResponse.json();

      setUser(userData);

      // Get documents
      const documentsResponse = await authFetch("/documents");

      if (!documentsResponse.ok) {
        throw new Error("Failed to fetch documents");
      }

      const documentsData =
        await documentsResponse.json();

      setDocuments(
        documentsData.documents || []
      );

      // Get dashboard statistics
      const statsResponse = await authFetch("/dashboard/stats");

      if (!statsResponse.ok) {
        throw new Error(
          "Failed to fetch dashboard statistics"
        );
      }

      const statsData =
        await statsResponse.json();

      setStats({
        questions_asked:
          statsData.questions_asked || 0,

        quizzes_completed:
          statsData.quizzes_completed || 0,

        study_progress:
          statsData.study_progress || 0,
      });

    } catch (error) {
      console.error(
        "Dashboard error:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        Loading dashboard...
      </div>
    );
  }

  return (
    <div className="dashboard">

      {/* Main Content */}
      <main className="main-content">

        {/* Header */}
        <div className="dashboard-header">

          <div>
            <h1>Welcome back!</h1>

            <p>
              Here's what's happening with your studies.
            </p>
          </div>

          {user && (
            <div className="user-profile">

              <div>
                <strong>{user.email}</strong>
                <span>Student</span>
              </div>

              <div className="avatar">
                {user.email?.charAt(0).toUpperCase()}
              </div>

            </div>
          )}

        </div>

        {/* Statistics */}
        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              📚
            </div>

            <div>
              <span>Total Documents</span>
              <h2>{documents.length}</h2>
            </div>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              💬
            </div>

            <div>
              <span>Questions Asked</span>
              <h2>{stats.questions_asked}</h2>
            </div>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              📝
            </div>

            <div>
              <span>Quizzes Completed</span>
              <h2>{stats.quizzes_completed}</h2>
            </div>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              📊
            </div>

            <div>
              <span>Study Progress</span>
              <h2>{stats.study_progress}%</h2>
            </div>

          </div>

        </div>

        {/* Dashboard Content */}
        <div className="dashboard-grid">

          {/* Recent Documents */}
          <div className="dashboard-card">

            <div className="card-header">

              <div>
                <h2>Recent Documents</h2>

                <p>
                  Your recently uploaded study materials
                </p>
              </div>

              <button
                className="view-all"
                onClick={() =>
                  onNavigate("documents")
                }
              >
                View All
              </button>

            </div>

            {documents.length === 0 ? (

              <div className="empty-documents">

                <div className="empty-icon">
                  📚
                </div>

                <h3>No documents uploaded yet</h3>

                <p>
                  Upload your study materials to start
                  learning with AI.
                </p>

                <button
                  className="primary-button"
                  onClick={() =>
                    onNavigate("documents")
                  }
                >
                  Upload Document
                </button>

              </div>

            ) : (

              <div className="document-list">

                {documents
                  .slice(0, 5)
                  .map((document) => (

                    <div
                      className="document-item"
                      key={document.id}
                    >

                      <div className="document-icon">
                        📄
                      </div>

                      <div>
                        <h3>{document.title}</h3>

                        <p>
                          Document ID: {document.id}
                        </p>
                      </div>

                    </div>

                  ))}

              </div>

            )}

          </div>

          {/* Quick Actions */}
          <div className="dashboard-card">

            <div className="card-header">

              <div>
                <h2>Quick Actions</h2>

                <p>
                  Start learning
                </p>
              </div>

            </div>

            <div className="quick-actions">

              <button
                className="action-button"
                onClick={() =>
                  onNavigate("documents")
                }
              >

                <span>📤</span>

                <div>
                  <strong>Upload Document</strong>

                  <small>
                    Add study materials
                  </small>
                </div>

              </button>

              <button
                className="action-button"
                onClick={() =>
                  onNavigate("chat")
                }
              >

                <span>💬</span>

                <div>
                  <strong>Ask AI</strong>

                  <small>
                    Ask questions about your notes
                  </small>
                </div>

              </button>

              <button
                className="action-button"
                onClick={() =>
                  onNavigate("quiz")
                }
              >

                <span>📝</span>

                <div>
                  <strong>Take a Quiz</strong>

                  <small>
                    Test your knowledge
                  </small>
                </div>

              </button>

              <button
                className="action-button"
                onClick={() =>
                  onNavigate("study-plan")
                }
              >

                <span>📅</span>

                <div>
                  <strong>Study Plan</strong>

                  <small>
                    Organize your learning
                  </small>
                </div>

              </button>

            </div>

          </div>

        </div>

      </main>

    </div>
  );
}

export default Dashboard;