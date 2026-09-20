import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import authFetch from "../services/authFetch";
import "./Flashcards.css";

function Flashcards() {
  const navigate = useNavigate();
  const [cards, setCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [historyLoaded, setHistoryLoaded] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await authFetch("/flashcards/history");
      if (!response.ok) return;
      const data = await response.json();
      if (data.cards && data.cards.length > 0) {
        setCards(data.cards);
      }
      setHistoryLoaded(true);
    } catch (error) {
      console.error("History error:", error);
      setHistoryLoaded(true);
    }
  };

  const handleFlip = () => {
    setFlipped((prev) => !prev);
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
      setFlipped(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setFlipped(false);
    }
  };

  const handleKeyDown = (e) => {
    if (cards.length === 0) return;

    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      handleFlip();
    } else if (e.key === "ArrowLeft") {
      handlePrevious();
    } else if (e.key === "ArrowRight") {
      handleNext();
    }
  };

  return (
    <div
      className="flashcards-page"
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {/* Header */}
      <div className="flashcards-header">
        <div className="flashcards-title-section">
          <div className="flashcards-title-icon">🃏</div>
          <div>
            <h1>Flashcards</h1>
            <p>
              Review your chat conversations as flashcards.
            </p>
          </div>
        </div>
      </div>

      {/* Flashcard Viewer */}
      {cards.length === 0 && (
        <div className="flashcards-start-container">
          <div className="flashcards-start-card">
            <div className="flashcards-large-icon">🃏</div>
            <h2>Flashcards</h2>
            <p>
              {historyLoaded
                ? "No flashcards yet. Start a chat to create flashcards from your conversations!"
                : "Loading flashcards..."}
            </p>

            <button
              className="generate-flashcards-button"
              onClick={() => navigate("/chat")}
            >
              Start Chatting
            </button>
          </div>
        </div>
      )}

      {/* Flashcard Viewer */}
      {cards.length > 0 && (
        <div className="flashcards-content">
          {/* Progress */}
          <div className="flashcards-progress-card">
            <div>
              <strong>Flashcard Progress</strong>
              <span>
                {currentIndex + 1} / {cards.length}
              </span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${
                    ((currentIndex + 1) / cards.length) *
                    100
                  }%`,
                }}
              ></div>
            </div>
          </div>

          {/* Card */}
          <div className="flashcard-viewer">
            <button
              className="nav-arrow nav-arrow-left"
              onClick={handlePrevious}
              disabled={currentIndex === 0}
            >
              ‹
            </button>

            <div
              className={`flashcard ${
                flipped ? "flipped" : ""
              }`}
              onClick={handleFlip}
            >
              <div className="flashcard-inner">
                <div className="flashcard-front">
                  <div className="flashcard-label">
                    Question
                  </div>
                  <p>{cards[currentIndex].front}</p>
                  <span className="flashcard-hint">
                    Click to reveal answer
                  </span>
                </div>
                <div className="flashcard-back">
                  <div className="flashcard-label">
                    Answer
                  </div>
                  <p>{cards[currentIndex].back}</p>
                  <span className="flashcard-hint">
                    Click to see question
                  </span>
                </div>
              </div>
            </div>

            <button
              className="nav-arrow nav-arrow-right"
              onClick={handleNext}
              disabled={
                currentIndex === cards.length - 1
              }
            >
              ›
            </button>
          </div>

          {/* Keyboard hint */}
          <p className="flashcards-keyboard-hint">
            Use ← → arrows to navigate, Space or Enter to
            flip
          </p>

          {/* Actions */}
          <div className="flashcards-actions">
            <button
              className="secondary-flashcards-button"
              onClick={() => navigate("/chat")}
            >
              Chat to Create More
            </button>

            <button
              className="generate-flashcards-button"
              onClick={() => navigate("/dashboard")}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Flashcards;
