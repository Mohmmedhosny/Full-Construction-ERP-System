import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { projectsAPI } from '../services/api';

export default function ProjectDetail() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    projectsAPI.getProject(id).then(res => {
      setProject(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading">Loading project...</div>;
  if (!project) return <div className="empty-state">Project not found</div>;

  const statusColor = {
    active: 'badge-success', planning: 'badge-info', completed: 'badge-secondary',
    on_hold: 'badge-warning', cancelled: 'badge-danger',
  };

  const taskStatusColor = {
    todo: 'badge-secondary', in_progress: 'badge-info', review: 'badge-warning',
    completed: 'badge-success', blocked: 'badge-danger',
  };

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Link to="/projects" style={{ color: '#64748b', fontSize: 14 }}>← Projects</Link>
      </div>
      <div className="page-header">
        <div>
          <h1 className="page-title">{project.name}</h1>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginTop: 6 }}>
            <code style={{ fontSize: 13, background: 'var(--light)', padding: '2px 8px', borderRadius: 4 }}>{project.code}</code>
            <span className={`badge ${statusColor[project.status] || 'badge-secondary'}`}>{project.status.replace('_', ' ')}</span>
            <span className={`badge ${project.priority === 'critical' ? 'badge-danger' : 'badge-warning'}`}>{project.priority}</span>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        {[
          { label: 'Budget', value: `$${Number(project.budget).toLocaleString()}` },
          { label: 'Start Date', value: project.start_date },
          { label: 'End Date', value: project.end_date },
          { label: 'Progress', value: `${project.completion_percentage}%` },
        ].map(({ label, value }) => (
          <div key={label} className="card" style={{ padding: '16px' }}>
            <div style={{ fontSize: 12, color: '#64748b', marginBottom: 4 }}>{label}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: 'var(--primary)' }}>{value}</div>
          </div>
        ))}
      </div>

      <div className="tabs">
        {['overview', 'phases', 'milestones'].map(tab => (
          <button key={tab} className={`tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {activeTab === 'overview' && (
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: 16 }}>Project Details</h3>
          <div className="grid-2">
            <div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 12, color: '#64748b' }}>Description</div>
                <div style={{ fontSize: 14 }}>{project.description || 'No description'}</div>
              </div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 12, color: '#64748b' }}>Location</div>
                <div style={{ fontSize: 14 }}>{project.location || '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: 12, color: '#64748b' }}>Client</div>
                <div style={{ fontSize: 14 }}>{project.client_detail?.name || '—'}</div>
              </div>
            </div>
            <div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 12, color: '#64748b' }}>Project Manager</div>
                <div style={{ fontSize: 14 }}>{project.project_manager_detail ? `${project.project_manager_detail.first_name} ${project.project_manager_detail.last_name}`.trim() || project.project_manager_detail.username : '—'}</div>
              </div>
              <div>
                <div style={{ fontSize: 12, color: '#64748b', marginBottom: 6 }}>Completion</div>
                <div className="progress-bar" style={{ height: 12 }}>
                  <div className="progress-bar-fill" style={{ width: `${project.completion_percentage}%` }} />
                </div>
                <div style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>{project.completion_percentage}% complete</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'phases' && (
        <div>
          {project.phases?.length === 0 ? (
            <div className="empty-state">No phases defined</div>
          ) : project.phases?.map(phase => (
            <div key={phase.id} className="card" style={{ marginBottom: 16 }}>
              <div className="card-header">
                <div>
                  <h3 className="card-title">{phase.name}</h3>
                  <div style={{ fontSize: 13, color: '#64748b' }}>{phase.start_date} → {phase.end_date}</div>
                </div>
                <span className={`badge ${taskStatusColor[phase.status] || 'badge-secondary'}`}>{phase.status.replace('_', ' ')}</span>
              </div>
              <div style={{ fontSize: 13, color: '#64748b' }}>Tasks: {phase.task_count} | Progress: {phase.completion_percentage}%</div>
              <div className="progress-bar" style={{ marginTop: 8 }}>
                <div className="progress-bar-fill" style={{ width: `${phase.completion_percentage}%` }} />
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'milestones' && (
        <div className="card">
          {project.milestones?.length === 0 ? (
            <div className="empty-state">No milestones defined</div>
          ) : (
            <table>
              <thead><tr><th>Milestone</th><th>Date</th><th>Status</th><th>Description</th></tr></thead>
              <tbody>
                {project.milestones?.map(m => (
                  <tr key={m.id}>
                    <td style={{ fontWeight: 500 }}>{m.name}</td>
                    <td style={{ fontSize: 13 }}>{m.date}</td>
                    <td><span className={`badge ${m.status === 'achieved' ? 'badge-success' : m.status === 'missed' ? 'badge-danger' : m.status === 'at_risk' ? 'badge-warning' : 'badge-info'}`}>{m.status.replace('_', ' ')}</span></td>
                    <td style={{ fontSize: 13 }}>{m.description || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
