import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import authFetch from "../services/authFetch";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState({
    questions_asked: 0,
    quizzes_completed: 0,
    study_progress: 0,
    subject_stats: [],
    unassigned_documents: 0,
    unassigned_chunks: 0,
  });
  const [flashcards, setFlashcards] = useState([]);
  const [flippedCard, setFlippedCard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Get current user first
      const userResponse = await authFetch("/auth/me");

      if (!userResponse.ok) {
        throw new Error("Failed to fetch user");
      }

      const userData = await userResponse.json();
      setUser(userData);

      // Fetch documents, stats in parallel
      const [documentsResponse, statsResponse] = await Promise.all([
        authFetch("/documents"),
        authFetch("/dashboard/stats"),
      ]);

      if (documentsResponse.ok) {
        const documentsData = await documentsResponse.json();
        setDocuments(documentsData.documents || []);
      }

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats({
          questions_asked: statsData.questions_asked || 0,
          quizzes_completed: statsData.quizzes_completed || 0,
          study_progress: statsData.study_progress || 0,
          subject_stats: statsData.subject_stats || [],
          unassigned_documents: statsData.unassigned_documents || 0,
          unassigned_chunks: statsData.unassigned_chunks || 0,
        });
      }

      setLoading(false);

      // Load flashcards separately after dashboard renders (non-blocking)
      try {
        const flashcardsResponse = await authFetch("/flashcards/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            topic: "",
            subject_id: null,
            number_of_cards: 3,
          }),
        });

        if (flashcardsResponse.ok) {
          const flashcardsData = await flashcardsResponse.json();
          setFlashcards(flashcardsData.cards || []);
        }
      } catch (flashcardError) {
        console.error("Flashcards preview error:", flashcardError);
      }

    } catch (error) {
      console.error("Dashboard error:", error);
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

        {/* Subject Breakdown */}
        {stats.subject_stats.length > 0 && (
          <div className="dashboard-card subject-breakdown-card">

            <div className="card-header">

              <div>
                <h2>Documents by Subject</h2>
                <p>Your study material distribution</p>
              </div>

              <button
                className="view-all"
                onClick={() => navigate("/subjects")}
              >
                Manage
              </button>

            </div>

            <div className="subject-breakdown-list">

              {stats.subject_stats.map((subject) => (
                <div className="subject-breakdown-item" key={subject.subject_id}>
                  <div className="subject-breakdown-info">
                    <span className="subject-breakdown-name">{subject.subject_name}</span>
                    <span className="subject-breakdown-count">
                      {subject.document_count} doc{subject.document_count !== 1 ? "s" : ""}
                      {" · "}
                      {subject.chunk_count} chunk{subject.chunk_count !== 1 ? "s" : ""}
                    </span>
                  </div>
                  <div className="subject-breakdown-bar">
                    <div
                      className="subject-breakdown-fill"
                      style={{
                        width: `${Math.min(
                          (subject.document_count / Math.max(documents.length, 1)) * 100,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>
                </div>
              ))}

              {stats.unassigned_documents > 0 && (
                <div className="subject-breakdown-item">
                  <div className="subject-breakdown-info">
                    <span className="subject-breakdown-name unassigned">Unassigned</span>
                    <span className="subject-breakdown-count">
                      {stats.unassigned_documents} doc{stats.unassigned_documents !== 1 ? "s" : ""}
                      {" · "}
                      {stats.unassigned_chunks} chunk{stats.unassigned_chunks !== 1 ? "s" : ""}
                    </span>
                  </div>
                  <div className="subject-breakdown-bar">
                    <div
                      className="subject-breakdown-fill unassigned-fill"
                      style={{
                        width: `${Math.min(
                          (stats.unassigned_documents / Math.max(documents.length, 1)) * 100,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>
                </div>
              )}

            </div>

          </div>
        )}

        {/* Flashcards Preview */}
        {flashcards.length > 0 && (
          <div className="dashboard-card flashcards-preview-card">

            <div className="card-header">

              <div>
                <h2>Quick Flashcards</h2>

                <p>
                  Click a card to flip it
                </p>
              </div>

              <button
                className="view-all"
                onClick={() =>
                  navigate("/flashcards")
                }
              >
                View All
              </button>

            </div>

            <div className="flashcards-preview-grid">

              {flashcards.map(
                (card, index) => (
                  <div
                    className={`mini-flashcard ${
                      flippedCard === index
                        ? "flipped"
                        : ""
                    }`}
                    key={index}
                    onClick={() =>
                      setFlippedCard(
                        flippedCard === index
                          ? null
                          : index
                      )
                    }
                  >
                    <div className="mini-flashcard-inner">
                      <div className="mini-flashcard-front">
                        <div className="mini-flashcard-label">
                          Q
                        </div>
                        <p>{card.front}</p>
                      </div>
                      <div className="mini-flashcard-back">
                        <div className="mini-flashcard-label">
                          A
                        </div>
                        <p>{card.back}</p>
                      </div>
                    </div>
                  </div>
                )
              )}

            </div>

          </div>
        )}

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
                  navigate("/documents")
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
                    navigate("/documents")
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
                  navigate("/documents")
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
                  navigate("/chat")
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
                  navigate("/quiz")
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
                  navigate("/study-plan")
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

              <button
                className="action-button"
                onClick={() =>
                  navigate("/flashcards")
                }
              >

                <span>🃏</span>

                <div>
                  <strong>Flashcards</strong>

                  <small>
                    Boost your memorization
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