import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { projectsAPI } from '../services/api';

const STATUS_COLORS = {
  active: 'badge-success', planning: 'badge-info', completed: 'badge-secondary',
  on_hold: 'badge-warning', cancelled: 'badge-danger',
};

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [formError, setFormError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ name: '', code: '', location: '', start_date: '', end_date: '', status: 'planning', priority: 'medium', budget: '0' });

  const fetchProjects = async () => {
    try {
      const params = {};
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      const res = await projectsAPI.getProjects(params);
      setProjects(res.data.results || res.data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchProjects(); }, [search, statusFilter]);

  const handleCreate = async (e) => {
    e.preventDefault();
    setFormError('');
    setSubmitting(true);
    try {
      const payload = { ...form, budget: parseFloat(form.budget) || 0 };
      await projectsAPI.createProject(payload);
      setShowModal(false);
      setForm({ name: '', code: '', location: '', start_date: '', end_date: '', status: 'planning', priority: 'medium', budget: '0' });
      fetchProjects();
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const messages = Object.entries(data).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ');
        setFormError(messages);
      } else {
        setFormError('Failed to create project. Please check all fields and try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">🏗️ Projects</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ New Project</button>
      </div>

      <div className="card">
        <div className="search-bar">
          <input className="search-input" placeholder="Search projects..." value={search} onChange={e => setSearch(e.target.value)} />
          <select className="form-control" style={{ width: 160 }} value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
            <option value="">All Statuses</option>
            <option value="planning">Planning</option>
            <option value="active">Active</option>
            <option value="on_hold">On Hold</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
        {loading ? <div className="loading">Loading...</div> : (
          <table>
            <thead>
              <tr>
                <th>Code</th><th>Project Name</th><th>Location</th><th>Status</th>
                <th>Priority</th><th>Start</th><th>End</th><th>Budget</th><th>Progress</th>
              </tr>
            </thead>
            <tbody>
              {projects.length === 0 ? (
                <tr><td colSpan={9}><div className="empty-state">No projects found</div></td></tr>
              ) : projects.map(p => (
                <tr key={p.id}>
                  <td><code style={{ fontSize: 12 }}>{p.code}</code></td>
                  <td>
                    <Link to={`/projects/${p.id}`} style={{ fontWeight: 500, color: 'var(--primary)' }}>{p.name}</Link>
                    {p.client_name && <div style={{ fontSize: 12, color: '#94a3b8' }}>{p.client_name}</div>}
                  </td>
                  <td style={{ fontSize: 13 }}>{p.location || '—'}</td>
                  <td><span className={`badge ${STATUS_COLORS[p.status] || 'badge-secondary'}`}>{p.status.replace('_', ' ')}</span></td>
                  <td><span className={`badge ${p.priority === 'critical' ? 'badge-danger' : p.priority === 'high' ? 'badge-warning' : 'badge-secondary'}`}>{p.priority}</span></td>
                  <td style={{ fontSize: 13 }}>{p.start_date}</td>
                  <td style={{ fontSize: 13 }}>{p.end_date}</td>
                  <td style={{ fontSize: 13 }}>${Number(p.budget).toLocaleString()}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <div className="progress-bar" style={{ width: 60 }}>
                        <div className="progress-bar-fill" style={{ width: `${p.completion_percentage}%` }} />
                      </div>
                      <span style={{ fontSize: 11 }}>{p.completion_percentage}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={e => { if (e.target === e.currentTarget) { setShowModal(false); setFormError(''); } }}>
          <div className="modal">
            <div className="modal-header">
              <h3 className="modal-title">New Project</h3>
              <button className="close-btn" onClick={() => { setShowModal(false); setFormError(''); }}>×</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="modal-body">
                {formError && (
                  <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', color: '#dc2626', padding: '10px 14px', borderRadius: 6, fontSize: 13, marginBottom: 16 }}>
                    {formError}
                  </div>
                )}
                <div className="grid-2">
                  <div className="form-group">
                    <label className="form-label">Project Name *</label>
                    <input className="form-control" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Code *</label>
                    <input className="form-control" value={form.code} onChange={e => setForm({...form, code: e.target.value})} required />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Location</label>
                  <input className="form-control" value={form.location} onChange={e => setForm({...form, location: e.target.value})} />
                </div>
                <div className="grid-2">
                  <div className="form-group">
                    <label className="form-label">Start Date *</label>
                    <input type="date" className="form-control" value={form.start_date} onChange={e => setForm({...form, start_date: e.target.value})} required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">End Date *</label>
                    <input type="date" className="form-control" value={form.end_date} onChange={e => setForm({...form, end_date: e.target.value})} required />
                  </div>
                </div>
                <div className="grid-3">
                  <div className="form-group">
                    <label className="form-label">Status</label>
                    <select className="form-control" value={form.status} onChange={e => setForm({...form, status: e.target.value})}>
                      <option value="planning">Planning</option>
                      <option value="active">Active</option>
                      <option value="on_hold">On Hold</option>
                      <option value="completed">Completed</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Priority</label>
                    <select className="form-control" value={form.priority} onChange={e => setForm({...form, priority: e.target.value})}>
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Budget ($)</label>
                    <input type="number" className="form-control" value={form.budget} onChange={e => setForm({...form, budget: e.target.value})} />
                  </div>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => { setShowModal(false); setFormError(''); }}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={submitting}>{submitting ? 'Creating...' : 'Create Project'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
