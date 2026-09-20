import { useState, useEffect } from "react";
import authFetch from "../services/authFetch";
import "./Chat.css";

function Chat() {
  const [messages, setMessages] = useState(() => {
    const saved = sessionStorage.getItem("chat_messages");
    return saved ? JSON.parse(saved) : [];
  });
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState("");

  useEffect(() => {
    sessionStorage.setItem("chat_messages", JSON.stringify(messages));
  }, [messages]);

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const response = await authFetch("/subjects");
      if (!response.ok) return;
      const data = await response.json();
      setSubjects(data.subjects || []);
    } catch (error) {
      console.error("Subjects error:", error);
    }
  };

  const handleSend = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage,
    ]);

    setQuestion("");
    setError("");
    setLoading(true);

    try {
      const body = { question: trimmedQuestion };

      if (selectedSubject) {
        body.subject_id = parseInt(selectedSubject);
      }

      const response = await authFetch(
        "/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to get an answer."
        );
      }

      const aiMessage = {
        role: "assistant",
        content:
          data.answer || "I couldn't generate an answer.",
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        aiMessage,
      ]);
    } catch (error) {
      console.error("Chat error:", error);
      setError(error.message);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't process your question.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    sessionStorage.removeItem("chat_messages");
    setError("");
  };

  return (
    <div className="chat-page">

      {/* Header */}
      <div className="chat-header">

        <div>
          <h1>AI Study Assistant</h1>

          <p>
            Ask questions and learn from your study materials.
          </p>
        </div>

        {messages.length > 0 && (
          <button
            className="clear-chat-button"
            onClick={handleClearChat}
          >
            Clear Chat
          </button>
        )}

      </div>

      {/* Subject Filter */}
      {subjects.length > 0 && (
        <div className="chat-subject-filter">
          <label htmlFor="chat-subject">Scope:</label>
          <select
            id="chat-subject"
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
          >
            <option value="">All documents</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
      )}

      {/* Chat container */}
      <div className="chat-container">

        {/* Empty state */}
        {messages.length === 0 && (
          <div className="chat-empty">

            <div className="chat-empty-icon">
              🤖
            </div>

            <h2>
              How can I help you study?
            </h2>

            <p>
              Ask a question about your study materials.
            </p>

            <div className="example-questions">

              <button
                onClick={() =>
                  setQuestion(
                    "What are the main topics in my study materials?"
                  )
                }
              >
                What are the main topics in my study materials?
              </button>

              <button
                onClick={() =>
                  setQuestion(
                    "Explain this topic in simple terms."
                  )
                }
              >
                Explain this topic in simple terms.
              </button>

              <button
                onClick={() =>
                  setQuestion(
                    "Give me some important questions to study."
                  )
                }
              >
                Give me some important questions to study.
              </button>

            </div>

          </div>
        )}

        {/* Messages */}
        {messages.length > 0 && (
          <div className="messages">

            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${
                  message.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >

                <div className="message-avatar">
                  {message.role === "user"
                    ? "👤"
                    : "🤖"}
                </div>

                <div className="message-content">
                  <div className="message-role">
                    {message.role === "user"
                      ? "You"
                      : "AI Assistant"}
                  </div>

                  <div className="message-text">
                    {message.content}
                  </div>
                </div>

              </div>
            ))}

            {/* Loading */}
            {loading && (
              <div className="message assistant-message">

                <div className="message-avatar">
                  🤖
                </div>

                <div className="message-content">

                  <div className="message-role">
                    AI Assistant
                  </div>

                  <div className="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>

                </div>

              </div>
            )}

          </div>
        )}

      </div>

      {/* Error */}
      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}

      {/* Input */}
      <div className="chat-input-container">

        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask your study question..."
          rows="1"
          disabled={loading}
        />

        <button
          className="send-button"
          onClick={handleSend}
          disabled={!question.trim() || loading}
        >
          {loading ? "..." : "Send"}
        </button>

      </div>

      <p className="chat-hint">
        Press Enter to send • Shift + Enter for a new line
      </p>

    </div>
  );
}

export default Chat;