import { useState, useEffect } from "react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import authFetch from "../services/authFetch";
import "./StudyPlan.css";

const PIE_COLORS = ["#f59e0b", "#3b82f6", "#22c55e"];
const BAR_COLORS = ["#7c3aed", "#6366f1", "#3b82f6", "#22c55e", "#f59e0b", "#ef4444"];

function StudyPlan() {
  const [plans, setPlans] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("plans");
  const [showForm, setShowForm] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    subject: "",
    due_date: "",
    priority: "medium",
    estimated_hours: 1,
  });

  const [filterStatus, setFilterStatus] = useState("all");
  const [filterSubject, setFilterSubject] = useState("all");

  useEffect(() => {
    fetchPlans();
    fetchStats();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await authFetch("/study-plans/");
      if (response.ok) {
        const data = await response.json();
        setPlans(data);
      }
    } catch (error) {
      console.error("Failed to fetch plans:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await authFetch("/study-plans/stats");
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error("Failed to fetch stats:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const url = editingPlan
      ? `/study-plans/${editingPlan.id}`
      : `/study-plans/`;

    const method = editingPlan ? "PUT" : "POST";

    try {
      const response = await authFetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (response.ok) {
        resetForm();
        fetchPlans();
        fetchStats();
      }
    } catch (error) {
      console.error("Failed to save plan:", error);
    }
  };

  const handleDelete = async (planId) => {
    if (!window.confirm("Delete this study plan?")) return;

    try {
      const response = await authFetch(
        `/study-plans/${planId}`,
        { method: "DELETE" }
      );

      if (response.ok) {
        fetchPlans();
        fetchStats();
      }
    } catch (error) {
      console.error("Failed to delete plan:", error);
    }
  };

  const handleStatusChange = async (planId, newStatus) => {
    try {
      const response = await authFetch(
        `/study-plans/${planId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: newStatus }),
        }
      );

      if (response.ok) {
        fetchPlans();
        fetchStats();
      }
    } catch (error) {
      console.error("Failed to update status:", error);
    }
  };

  const handleEdit = (plan) => {
    setEditingPlan(plan);
    setForm({
      title: plan.title,
      description: plan.description || "",
      subject: plan.subject,
      due_date: plan.due_date,
      priority: plan.priority,
      estimated_hours: plan.estimated_hours,
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setForm({
      title: "",
      description: "",
      subject: "",
      due_date: "",
      priority: "medium",
      estimated_hours: 1,
    });
    setEditingPlan(null);
    setShowForm(false);
  };

  const getFilteredPlans = () => {
    return plans.filter((plan) => {
      if (filterStatus !== "all" && plan.status !== filterStatus) return false;
      if (filterSubject !== "all" && plan.subject !== filterSubject) return false;
      return true;
    });
  };

  const getSubjects = () => {
    const subjects = [...new Set(plans.map((p) => p.subject))];
    return subjects.sort();
  };

  const isOverdue = (dueDate) => {
    return new Date(dueDate) < new Date() && dueDate;
  };

  const getPieData = () => {
    if (!stats) return [];
    return [
      { name: "Pending", value: stats.status_counts.pending },
      { name: "In Progress", value: stats.status_counts.in_progress },
      { name: "Completed", value: stats.status_counts.completed },
    ].filter((d) => d.value > 0);
  };

  const getBarData = () => {
    if (!stats) return [];
    return Object.entries(stats.subject_counts).map(([subject, count]) => ({
      subject,
      count,
    }));
  };

  if (loading) {
    return <div className="loading">Loading study plans...</div>;
  }

  return (
    <div className="study-plan">
      <main className="sp-main-content">
        <div className="sp-header">
          <div>
            <h1>Study Plans</h1>
            <p>Organize your learning schedule and track progress.</p>
          </div>
          <button
            className="sp-add-button"
            onClick={() => {
              resetForm();
              setShowForm(true);
            }}
          >
            + New Plan
          </button>
        </div>

        {/* Tabs */}
        <div className="sp-tabs">
          <button
            className={`sp-tab ${activeTab === "plans" ? "active" : ""}`}
            onClick={() => setActiveTab("plans")}
          >
            My Plans
          </button>
          <button
            className={`sp-tab ${activeTab === "reports" ? "active" : ""}`}
            onClick={() => setActiveTab("reports")}
          >
            Reports
          </button>
        </div>

        {/* Plans Tab */}
        {activeTab === "plans" && (
          <div className="sp-plans-section">
            {/* Filters */}
            <div className="sp-filters">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="sp-filter-select"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>

              <select
                value={filterSubject}
                onChange={(e) => setFilterSubject(e.target.value)}
                className="sp-filter-select"
              >
                <option value="all">All Subjects</option>
                {getSubjects().map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>

              <span className="sp-plan-count">
                {getFilteredPlans().length} plan
                {getFilteredPlans().length !== 1 ? "s" : ""}
              </span>
            </div>

            {/* Plan List */}
            {getFilteredPlans().length === 0 ? (
              <div className="sp-empty">
                <div className="sp-empty-icon">📅</div>
                <h3>No study plans yet</h3>
                <p>Create your first study plan to get started.</p>
                <button
                  className="sp-primary-button"
                  onClick={() => setShowForm(true)}
                >
                  Create Plan
                </button>
              </div>
            ) : (
              <div className="sp-plan-list">
                {getFilteredPlans().map((plan) => (
                  <div
                    key={plan.id}
                    className={`sp-plan-card ${plan.status} ${isOverdue(plan.due_date) && plan.status !== "completed" ? "overdue" : ""}`}
                  >
                    <div className="sp-plan-top">
                      <div className="sp-plan-info">
                        <h3>{plan.title}</h3>
                        {plan.description && (
                          <p className="sp-plan-desc">{plan.description}</p>
                        )}
                      </div>
                      <span
                        className={`sp-priority-badge ${plan.priority}`}
                      >
                        {plan.priority}
                      </span>
                    </div>

                    <div className="sp-plan-meta">
                      <span className="sp-meta-item">
                        <span className="sp-meta-icon">📚</span>
                        {plan.subject}
                      </span>
                      <span className="sp-meta-item">
                        <span className="sp-meta-icon">📅</span>
                        {plan.due_date}
                        {isOverdue(plan.due_date) &&
                          plan.status !== "completed" && (
                            <span className="sp-overdue-label">Overdue</span>
                          )}
                      </span>
                      <span className="sp-meta-item">
                        <span className="sp-meta-icon">⏱️</span>
                        {plan.estimated_hours}h
                      </span>
                    </div>

                    <div className="sp-plan-actions">
                      <div className="sp-status-buttons">
                        {["pending", "in_progress", "completed"].map((s) => (
                          <button
                            key={s}
                            className={`sp-status-btn ${plan.status === s ? "active" : ""} ${s}`}
                            onClick={() => handleStatusChange(plan.id, s)}
                          >
                            {s === "in_progress"
                              ? "In Progress"
                              : s.charAt(0).toUpperCase() + s.slice(1)}
                          </button>
                        ))}
                      </div>
                      <div className="sp-action-buttons">
                        <button
                          className="sp-edit-btn"
                          onClick={() => handleEdit(plan)}
                        >
                          Edit
                        </button>
                        <button
                          className="sp-delete-btn"
                          onClick={() => handleDelete(plan.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Reports Tab */}
        {activeTab === "reports" && (
          <div className="sp-reports-section">
            {/* Summary Cards */}
            <div className="sp-stats-grid">
              <div className="sp-stat-card">
                <div className="sp-stat-icon total">📊</div>
                <div>
                  <span>Total Plans</span>
                  <h2>{stats?.total || 0}</h2>
                </div>
              </div>
              <div className="sp-stat-card">
                <div className="sp-stat-icon completed">✅</div>
                <div>
                  <span>Completed</span>
                  <h2>{stats?.status_counts.completed || 0}</h2>
                </div>
              </div>
              <div className="sp-stat-card">
                <div className="sp-stat-icon pending">⏳</div>
                <div>
                  <span>Pending</span>
                  <h2>{stats?.status_counts.pending || 0}</h2>
                </div>
              </div>
              <div className="sp-stat-card">
                <div className="sp-stat-icon hours">⏱️</div>
                <div>
                  <span>Total Hours</span>
                  <h2>{stats?.total_estimated_hours || 0}h</h2>
                </div>
              </div>
            </div>

            {/* Charts */}
            <div className="sp-charts-grid">
              {/* Pie Chart - Status Breakdown */}
              <div className="sp-chart-card">
                <div className="sp-card-header">
                  <h2>Completion Status</h2>
                  <p>Plan status distribution</p>
                </div>
                {getPieData().length > 0 ? (
                  <div className="sp-chart-container">
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={getPieData()}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={100}
                          paddingAngle={5}
                          dataKey="value"
                          label={({ name, percent }) =>
                            `${name} ${(percent * 100).toFixed(0)}%`
                          }
                        >
                          {getPieData().map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={PIE_COLORS[index % PIE_COLORS.length]}
                            />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <div className="sp-no-data">No data available</div>
                )}
              </div>

              {/* Bar Chart - Plans by Subject */}
              <div className="sp-chart-card">
                <div className="sp-card-header">
                  <h2>Plans by Subject</h2>
                  <p>Number of plans per subject</p>
                </div>
                {getBarData().length > 0 ? (
                  <div className="sp-chart-container">
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={getBarData()}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis
                          dataKey="subject"
                          tick={{ fontSize: 12, fill: "#6b7280" }}
                        />
                        <YAxis
                          allowDecimals={false}
                          tick={{ fontSize: 12, fill: "#6b7280" }}
                        />
                        <Tooltip
                          contentStyle={{
                            borderRadius: "8px",
                            border: "1px solid #e5e7eb",
                          }}
                        />
                        <Bar
                          dataKey="count"
                          name="Plans"
                          radius={[4, 4, 0, 0]}
                        >
                          {getBarData().map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={BAR_COLORS[index % BAR_COLORS.length]}
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <div className="sp-no-data">No data available</div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Add/Edit Form Modal */}
        {showForm && (
          <div className="sp-modal-overlay" onClick={resetForm}>
            <div
              className="sp-modal"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="sp-modal-header">
                <h2>{editingPlan ? "Edit Plan" : "New Study Plan"}</h2>
                <button className="sp-close-btn" onClick={resetForm}>
                  ×
                </button>
              </div>

              <form onSubmit={handleSubmit} className="sp-form">
                <div className="sp-form-group">
                  <label>Title *</label>
                  <input
                    type="text"
                    placeholder="e.g. Review Chapter 5"
                    value={form.title}
                    onChange={(e) =>
                      setForm({ ...form, title: e.target.value })
                    }
                    required
                  />
                </div>

                <div className="sp-form-group">
                  <label>Description</label>
                  <textarea
                    placeholder="Optional notes about this study plan..."
                    value={form.description}
                    onChange={(e) =>
                      setForm({ ...form, description: e.target.value })
                    }
                    rows={3}
                  />
                </div>

                <div className="sp-form-row">
                  <div className="sp-form-group">
                    <label>Subject *</label>
                    <input
                      type="text"
                      placeholder="e.g. Mathematics"
                      value={form.subject}
                      onChange={(e) =>
                        setForm({ ...form, subject: e.target.value })
                      }
                      required
                    />
                  </div>

                  <div className="sp-form-group">
                    <label>Due Date *</label>
                    <input
                      type="date"
                      value={form.due_date}
                      onChange={(e) =>
                        setForm({ ...form, due_date: e.target.value })
                      }
                      required
                    />
                  </div>
                </div>

                <div className="sp-form-row">
                  <div className="sp-form-group">
                    <label>Priority</label>
                    <select
                      value={form.priority}
                      onChange={(e) =>
                        setForm({ ...form, priority: e.target.value })
                      }
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>

                  <div className="sp-form-group">
                    <label>Estimated Hours</label>
                    <input
                      type="number"
                      min="0.5"
                      step="0.5"
                      value={form.estimated_hours}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          estimated_hours: parseFloat(e.target.value) || 1,
                        })
                      }
                    />
                  </div>
                </div>

                <div className="sp-form-actions">
                  <button
                    type="button"
                    className="sp-cancel-button"
                    onClick={resetForm}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="sp-submit-button">
                    {editingPlan ? "Update Plan" : "Create Plan"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default StudyPlan;
