import { useEffect, useState } from "react";
import authFetch from "../services/authFetch";
import "./Subjects.css";

function Subjects() {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingSubject, setEditingSubject] = useState(null);
  const [subjectName, setSubjectName] = useState("");
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const response = await authFetch("/subjects");

      if (!response.ok) {
        throw new Error("Failed to fetch subjects");
      }

      const data = await response.json();
      setSubjects(data.subjects || []);
    } catch (error) {
      console.error("Subjects error:", error);
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const openCreateModal = () => {
    setEditingSubject(null);
    setSubjectName("");
    setShowModal(true);
    setMessage("");
  };

  const openEditModal = (subject) => {
    setEditingSubject(subject);
    setSubjectName(subject.name);
    setShowModal(true);
    setMessage("");
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingSubject(null);
    setSubjectName("");
    setMessage("");
  };

  const handleSave = async () => {
    const trimmed = subjectName.trim();

    if (!trimmed) {
      setMessage("Subject name cannot be empty");
      return;
    }

    setSaving(true);
    setMessage("");

    try {
      const url = editingSubject
        ? `/subjects/${editingSubject.id}`
        : "/subjects/";

      const method = editingSubject ? "PUT" : "POST";

      const response = await authFetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: trimmed }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to save subject");
      }

      closeModal();
      await fetchSubjects();
    } catch (error) {
      console.error("Save subject error:", error);
      setMessage(error.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (subject) => {
    const confirmed = window.confirm(
      `Delete "${subject.name}"? Documents in this subject will become unassigned.`
    );

    if (!confirmed) {
      return;
    }

    try {
      const response = await authFetch(`/subjects/${subject.id}`, {
        method: "DELETE",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to delete subject");
      }

      await fetchSubjects();
    } catch (error) {
      console.error("Delete subject error:", error);
      setMessage(error.message);
    }
  };

  if (loading) {
    return <div className="subjects-loading">Loading subjects...</div>;
  }

  return (
    <div className="subjects-page">

      <div className="subjects-header">
        <div>
          <h1>Subjects</h1>
          <p>Organize your documents by subject</p>
        </div>

        <button className="add-subject-button" onClick={openCreateModal}>
          + Add Subject
        </button>
      </div>

      {message && !showModal && (
        <div className="subjects-message">{message}</div>
      )}

      {subjects.length === 0 ? (
        <div className="subjects-empty">
          <div className="empty-subject-icon">📂</div>
          <h2>No subjects yet</h2>
          <p>Create subjects to organize your documents.</p>
          <button className="add-subject-button" onClick={openCreateModal}>
            + Create Your First Subject
          </button>
        </div>
      ) : (
        <div className="subjects-grid">
          {subjects.map((subject) => (
            <div className="subject-card" key={subject.id}>
              <div className="subject-card-header">
                <div className="subject-icon">📁</div>
                <div className="subject-actions">
                  <button
                    className="edit-button"
                    onClick={() => openEditModal(subject)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-button"
                    onClick={() => handleDelete(subject)}
                  >
                    Delete
                  </button>
                </div>
              </div>
              <h3>{subject.name}</h3>
              <p className="subject-doc-count">
                {subject.document_count} document
                {subject.document_count !== 1 ? "s" : ""}
              </p>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editingSubject ? "Edit Subject" : "New Subject"}</h2>

            {message && <div className="modal-error">{message}</div>}

            <label htmlFor="subject-name">Subject Name</label>
            <input
              id="subject-name"
              type="text"
              value={subjectName}
              onChange={(e) => setSubjectName(e.target.value)}
              placeholder="e.g. Mathematics, Physics, History"
              disabled={saving}
              autoFocus
            />

            <div className="modal-actions">
              <button
                className="modal-cancel-button"
                onClick={closeModal}
                disabled={saving}
              >
                Cancel
              </button>
              <button
                className="modal-save-button"
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? "Saving..." : editingSubject ? "Save Changes" : "Create"}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default Subjects;
