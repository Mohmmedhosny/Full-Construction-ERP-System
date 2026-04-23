import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { projectsAPI, hrAPI, financeAPI, resourcesAPI } from '../services/api';

export default function Dashboard() {
  const [projectStats, setProjectStats] = useState(null);
  const [employeeStats, setEmployeeStats] = useState(null);
  const [invoiceSummary, setInvoiceSummary] = useState(null);
  const [lowStock, setLowStock] = useState([]);
  const [recentProjects, setRecentProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [ps, es, inv, ls, rp] = await Promise.allSettled([
          projectsAPI.getDashboardStats(),
          hrAPI.getEmployeeStats(),
          financeAPI.getInvoiceSummary(),
          resourcesAPI.getLowStock(),
          projectsAPI.getProjects({ page_size: 5 }),
        ]);
        if (ps.status === 'fulfilled') setProjectStats(ps.value.data);
        if (es.status === 'fulfilled') setEmployeeStats(es.value.data);
        if (inv.status === 'fulfilled') setInvoiceSummary(inv.value.data);
        if (ls.status === 'fulfilled') setLowStock(ls.value.data);
        if (rp.status === 'fulfilled') setRecentProjects(rp.value.data.results || rp.value.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  const formatCurrency = (val) =>
    val ? `$${Number(val).toLocaleString('en-US', { minimumFractionDigits: 0 })}` : '$0';

  const statusColor = (status) => {
    const map = { active: 'badge-success', planning: 'badge-info', completed: 'badge-secondary', on_hold: 'badge-warning', cancelled: 'badge-danger' };
    return map[status] || 'badge-secondary';
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <span style={{ color: '#64748b', fontSize: 14 }}>
          {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </span>
      </div>

      {/* Project Stats */}
      <div className="stat-grid">
        <div className="stat-card" style={{ borderTop: '3px solid var(--accent)' }}>
          <div className="stat-label">Total Projects</div>
          <div className="stat-value">{projectStats?.total ?? '—'}</div>
          <div className="stat-sub">Active: {projectStats?.active ?? 0}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--info)' }}>
          <div className="stat-label">Total Budget</div>
          <div className="stat-value" style={{ fontSize: 20 }}>{formatCurrency(projectStats?.total_budget)}</div>
          <div className="stat-sub">Across all projects</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-label">Employees</div>
          <div className="stat-value">{employeeStats?.total ?? '—'}</div>
          <div className="stat-sub">Active: {employeeStats?.active ?? 0}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-label">Outstanding Invoices</div>
          <div className="stat-value" style={{ fontSize: 20 }}>{formatCurrency(invoiceSummary?.total_outstanding)}</div>
          <div className="stat-sub">Total invoiced: {formatCurrency(invoiceSummary?.total_invoiced)}</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>
        {/* Recent Projects */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Projects</h3>
            <Link to="/projects" className="btn btn-sm btn-secondary">View All</Link>
          </div>
          {recentProjects.length === 0 ? (
            <div className="empty-state">No projects yet</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Project</th>
                  <th>Status</th>
                  <th>Progress</th>
                  <th>Budget</th>
                </tr>
              </thead>
              <tbody>
                {recentProjects.slice(0, 5).map(p => (
                  <tr key={p.id}>
                    <td>
                      <Link to={`/projects/${p.id}`} style={{ fontWeight: 500, color: 'var(--primary)' }}>
                        {p.name}
                      </Link>
                      <div style={{ fontSize: 12, color: '#94a3b8' }}>{p.code}</div>
                    </td>
                    <td><span className={`badge ${statusColor(p.status)}`}>{p.status.replace('_', ' ')}</span></td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div className="progress-bar" style={{ width: 80 }}>
                          <div className="progress-bar-fill" style={{ width: `${p.completion_percentage}%` }} />
                        </div>
                        <span style={{ fontSize: 12 }}>{p.completion_percentage}%</span>
                      </div>
                    </td>
                    <td style={{ fontSize: 13 }}>{formatCurrency(p.budget)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Alerts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">⚠️ Low Stock Alerts</h3>
            </div>
            {lowStock.length === 0 ? (
              <div style={{ color: '#64748b', fontSize: 14 }}>All stock levels OK</div>
            ) : (
              <div>
                {lowStock.slice(0, 5).map(m => (
                  <div key={m.id} style={{ padding: '8px 0', borderBottom: '1px solid var(--border)', fontSize: 14 }}>
                    <div style={{ fontWeight: 500 }}>{m.name}</div>
                    <div style={{ color: 'var(--danger)', fontSize: 12 }}>
                      Stock: {m.current_stock} {m.unit} (min: {m.reorder_level})
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Project Status</h3>
            </div>
            {projectStats && (
              <div>
                {[
                  { label: 'Active', value: projectStats.active, color: 'var(--success)' },
                  { label: 'Planning', value: projectStats.planning, color: 'var(--info)' },
                  { label: 'On Hold', value: projectStats.on_hold, color: 'var(--warning)' },
                  { label: 'Completed', value: projectStats.completed, color: '#94a3b8' },
                ].map(({ label, value, color }) => (
                  <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 14 }}>
                      <div style={{ width: 10, height: 10, borderRadius: '50%', background: color }} />
                      {label}
                    </div>
                    <strong>{value}</strong>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
