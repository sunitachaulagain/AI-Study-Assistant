import { useEffect, useState } from "react";
import authFetch from "../services/authFetch";
import "./Documents.css";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState("");
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [uploadSubject, setUploadSubject] = useState("");

  useEffect(() => {
    fetchDocuments();
    fetchSubjects();
  }, []);

  useEffect(() => {
    fetchDocuments();
  }, [selectedSubject]);

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

  // Fetch all documents for the logged-in user
  const fetchDocuments = async () => {
    try {
      let url = "/documents";

      if (selectedSubject) {
        url += `?subject_id=${selectedSubject}`;
      }

      const response = await authFetch(url);

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

    if (uploadSubject) {
      formData.append("subject_id", uploadSubject);
    }

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
      setUploadSubject("");

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

      </div>

      {/* Subject Filter + Upload */}
      <div className="documents-toolbar">

        <div className="subject-filter">
          <label htmlFor="filter-subject">Filter by subject:</label>
          <select
            id="filter-subject"
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
          >
            <option value="">All Subjects</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>

        <div className="upload-area">
          <select
            className="upload-subject-select"
            value={uploadSubject}
            onChange={(e) => setUploadSubject(e.target.value)}
            disabled={uploading}
          >
            <option value="">No subject</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>

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
              {selectedSubject ? "No documents in this subject" : "No documents yet"}
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
                    {document.subject_id
                      ? subjects.find((s) => s.id === document.subject_id)?.name || "Unknown subject"
                      : "No subject"
                    }
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

