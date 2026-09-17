import { useEffect, useState } from "react";
import authFetch from "../services/authFetch";
import "./Documents.css";

function Documents({ onNavigate }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Fetch all documents for the logged-in user
  const fetchDocuments = async () => {
    try {
      const response = await authFetch("/documents");

      if (!response.ok) {
        throw new Error("Failed to fetch documents");
      }

      const data = await response.json();

      setDocuments(data.documents || []);
    } catch (error) {
      console.error("Documents error:", error);
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Upload PDF
  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setMessage("Only PDF files are supported.");
      event.target.value = "";
      return;
    }

    setUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await authFetch(
        "/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setMessage("Document uploaded successfully!");

      await fetchDocuments();
    } catch (error) {
      console.error("Upload error:", error);
      setMessage(error.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  // Delete document
  const handleDelete = async (documentId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmed) {
      return;
    }

    try {
      const response = await authFetch(
        `/documents/${documentId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to delete document"
        );
      }

      setMessage("Document deleted successfully!");

      await fetchDocuments();
    } catch (error) {
      console.error("Delete error:", error);
      setMessage(error.message);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="documents-loading">
        Loading documents...
      </div>
    );
  }

  return (
    <div className="documents-page">

      {/* Header */}
      <div className="documents-header">

        <div>
          <h1>My Documents</h1>

          <p>
            Manage your study materials
          </p>
        </div>

        {/* Upload button */}
        <label className="upload-button">
          {uploading
            ? "Uploading..."
            : "+ Upload Document"}

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleUpload}
            disabled={uploading}
            hidden
          />
        </label>

      </div>


      {/* Upload / Delete Message */}
      {message && (
        <div className="upload-message">
          {message}
        </div>
      )}


      {/* Documents Card */}
      <div className="documents-card">

        {documents.length === 0 ? (

          /* Empty State */
          <div className="documents-empty">

            <div className="empty-document-icon">
              📚
            </div>

            <h2>
              No documents yet
            </h2>

            <p>
              Upload your study materials to start learning with AI.
            </p>

            <label className="upload-button">
              {uploading
                ? "Uploading..."
                : "Upload Your First Document"}

              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleUpload}
                disabled={uploading}
                hidden
              />
            </label>

          </div>

        ) : (

          /* Document List */
          <div className="document-list">

            {documents.map((document) => (

              <div
                className="document-item"
                key={document.id}
              >

                <div className="document-icon">
                  📄
                </div>

                <div className="document-info">

                  <h3>
                    {document.title}
                  </h3>

                  <p>
                    Document ID: {document.id}
                  </p>

                </div>

                <button
                  className="delete-button"
                  onClick={() => handleDelete(document.id)}
                >
                  Delete
                </button>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  );
}

export default Documents;

