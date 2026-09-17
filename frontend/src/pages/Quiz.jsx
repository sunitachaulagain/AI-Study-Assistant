import { useState } from "react";
import authFetch from "../services/authFetch";
import "./Quiz.css";

function Quiz({ onNavigate }) {
  const [topic, setTopic] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [completionRecorded, setCompletionRecorded] =
    useState(false);

  const generateQuiz = async () => {
    setLoading(true);
    setError("");
    setQuestions([]);
    setAnswers({});
    setSubmitted(false);
    setCompletionRecorded(false);

    try {
      const response = await authFetch(
        "/quiz/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            topic: topic.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to generate quiz."
        );
      }

      if (
        !data.questions ||
        data.questions.length === 0
      ) {
        throw new Error(
          "No quiz questions could be generated from your study materials."
        );
      }

      setQuestions(data.questions);

    } catch (error) {
      console.error(
        "Quiz error:",
        error
      );

      setError(error.message);

    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (
    questionIndex,
    optionIndex
  ) => {

    if (submitted) {
      return;
    }

    setAnswers(
      (previousAnswers) => ({
        ...previousAnswers,
        [questionIndex]: optionIndex,
      })
    );

    setError("");
  };

  const calculateScore = () => {

    let score = 0;

    questions.forEach(
      (question, index) => {

        if (
          answers[index] ===
          question.correct_answer
        ) {
          score++;
        }

      }
    );

    return score;
  };

  const recordQuizCompletion = async (
    score
  ) => {

    if (completionRecorded) {
      return;
    }

    try {

      const response = await authFetch(
        "/quiz/complete",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            score: score,
            total_questions: questions.length,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to record quiz completion."
        );
      }

      setCompletionRecorded(true);

    } catch (error) {

      console.error(
        "Quiz completion error:",
        error
      );

      setError(
        "Quiz submitted, but the completion could not be recorded."
      );
    }
  };

  const handleSubmit = async () => {

    if (
      Object.keys(answers).length !==
      questions.length
    ) {
      setError(
        "Please answer all questions before submitting the quiz."
      );

      return;
    }

    setError("");

    const score = calculateScore();

    setSubmitted(true);

    await recordQuizCompletion(score);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const getScoreMessage = () => {

    const score = calculateScore();

    const percentage =
      (score / questions.length) * 100;

    if (percentage === 100) {
      return "Perfect score! Excellent work.";
    }

    if (percentage >= 75) {
      return "Great job! You have a strong understanding of the material.";
    }

    if (percentage >= 50) {
      return "Good effort! Review the explanations and keep practicing.";
    }

    return "Keep practicing. Reviewing your study materials will help.";
  };

  const handleRetry = () => {

    setQuestions([]);
    setAnswers({});
    setSubmitted(false);
    setError("");
    setCompletionRecorded(false);
  };

  return (
    <div className="quiz-page">

      {/* Header */}
      <div className="quiz-header">

        <div className="quiz-title-section">

          <div className="quiz-title-icon">
            🧠
          </div>

          <div>
            <h1>AI Quiz Generator</h1>

            <p>
              Test your knowledge using your study materials.
            </p>
          </div>

        </div>

      </div>

      {/* Error */}
      {error && (
        <div className="quiz-error">
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Quiz Generator */}
      {questions.length === 0 && (
        <div className="quiz-start-container">

          <div className="quiz-start-card">

            <div className="quiz-large-icon">
              🧠
            </div>

            <h2>Generate a Quiz</h2>

            <p>
              Create multiple-choice questions from
              your uploaded study materials.
            </p>

            <div className="quiz-input-group">

              <label htmlFor="topic">
                Topic
              </label>

              <input
                id="topic"
                type="text"
                value={topic}
                onChange={(event) =>
                  setTopic(event.target.value)
                }
                placeholder="e.g. Data Visualization"
                disabled={loading}
              />

              <small>
                Leave this empty to generate a quiz
                from your general study materials.
              </small>

            </div>

            <button
              className="generate-quiz-button"
              onClick={generateQuiz}
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="quiz-spinner"></span>
                  Generating Quiz...
                </>
              ) : (
                <>
                  ✨ Generate Quiz
                </>
              )}

            </button>

            {loading && (
              <p className="quiz-loading-text">
                The AI is reading your study materials
                and creating questions. This may take
                a little time.
              </p>
            )}

          </div>

        </div>
      )}

      {/* Quiz */}
      {questions.length > 0 && (
        <div className="quiz-content">

          {/* Score */}
          {submitted && (
            <div className="quiz-score-card">

              <div className="score-icon">
                🏆
              </div>

              <div className="score-content">

                <p className="score-label">
                  Your Score
                </p>

                <div className="score-number">

                  {calculateScore()}

                  <span>
                    / {questions.length}
                  </span>

                </div>

                <p className="score-message">
                  {getScoreMessage()}
                </p>

              </div>

            </div>
          )}

          {/* Progress */}
          {!submitted && (
            <div className="quiz-progress-card">

              <div>

                <strong>
                  Quiz Progress
                </strong>

                <span>
                  {Object.keys(answers).length}
                  {" / "}
                  {questions.length} answered
                </span>

              </div>

              <div className="progress-bar">

                <div
                  className="progress-fill"
                  style={{
                    width: `${
                      (
                        Object.keys(answers).length /
                        questions.length
                      ) * 100
                    }%`,
                  }}
                ></div>

              </div>

            </div>
          )}

          {/* Questions */}
          {questions.map(
            (question, questionIndex) => (

              <div
                className="question-card"
                key={questionIndex}
              >

                <div className="question-header">

                  <span className="question-number">
                    Question {questionIndex + 1}
                  </span>

                  {submitted && (
                    <span
                      className={
                        answers[questionIndex] ===
                        question.correct_answer
                          ? "question-result correct-result"
                          : "question-result incorrect-result"
                      }
                    >

                      {answers[questionIndex] ===
                      question.correct_answer
                        ? "✓ Correct"
                        : "✕ Incorrect"}

                    </span>
                  )}

                </div>

                <h2>
                  {question.question}
                </h2>

                <div className="quiz-options">

                  {question.options.map(
                    (option, optionIndex) => {

                      const selected =
                        answers[questionIndex] ===
                        optionIndex;

                      const correct =
                        question.correct_answer ===
                        optionIndex;

                      let optionClass =
                        "quiz-option";

                      if (selected) {
                        optionClass +=
                          " selected";
                      }

                      if (
                        submitted &&
                        correct
                      ) {
                        optionClass +=
                          " correct";
                      }

                      if (
                        submitted &&
                        selected &&
                        !correct
                      ) {
                        optionClass +=
                          " incorrect";
                      }

                      return (
                        <button
                          key={optionIndex}
                          className={optionClass}
                          onClick={() =>
                            handleAnswer(
                              questionIndex,
                              optionIndex
                            )
                          }
                          disabled={submitted}
                        >

                          <span className="option-letter">
                            {String.fromCharCode(
                              65 + optionIndex
                            )}
                          </span>

                          <span className="option-text">
                            {option}
                          </span>

                          {submitted &&
                            correct && (
                              <span className="option-status">
                                ✓
                              </span>
                            )}

                          {submitted &&
                            selected &&
                            !correct && (
                              <span className="option-status">
                                ✕
                              </span>
                            )}

                        </button>
                      );
                    }
                  )}

                </div>

                {/* Explanation */}
                {submitted && (
                  <div className="explanation">

                    <div className="explanation-title">
                      💡 Explanation
                    </div>

                    <p>
                      {question.explanation}
                    </p>

                  </div>
                )}

              </div>

            )
          )}

          {/* Bottom Actions */}
          <div className="quiz-actions">

            {!submitted ? (

              <button
                className="submit-quiz-button"
                onClick={handleSubmit}
              >
                Submit Quiz
              </button>

            ) : (

              <>

                <button
                  className="secondary-quiz-button"
                  onClick={handleRetry}
                >
                  ← Generate Another Quiz
                </button>

                <button
                  className="submit-quiz-button"
                  onClick={() =>
                    onNavigate("dashboard")
                  }
                >
                  Back to Dashboard
                </button>

              </>

            )}

          </div>

        </div>
      )}

    </div>
  );
}

export default Quiz;