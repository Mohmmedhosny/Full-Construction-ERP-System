import React, { useState, useEffect } from 'react';
import { documentsAPI } from '../services/api';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchDocs = async () => {
    try {
      const params = {};
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      const res = await documentsAPI.getDocuments(params);
      setDocuments(res.data.results || res.data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchDocs(); }, [search, statusFilter]);

  const statusColor = {
    draft: 'badge-secondary', review: 'badge-warning', approved: 'badge-success',
    superseded: 'badge-info', archived: 'badge-secondary',
  };

  const formatSize = (bytes) => {
    if (!bytes) return '—';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">📄 Documents</h1>
      </div>

      <div className="stat-grid">
        <div className="stat-card" style={{ borderTop: '3px solid var(--accent)' }}>
          <div className="stat-label">Total Documents</div>
          <div className="stat-value">{documents.length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-label">Approved</div>
          <div className="stat-value">{documents.filter(d => d.status === 'approved').length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-label">Under Review</div>
          <div className="stat-value">{documents.filter(d => d.status === 'review').length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--secondary)' }}>
          <div className="stat-label">Drafts</div>
          <div className="stat-value">{documents.filter(d => d.status === 'draft').length}</div>
        </div>
      </div>

      <div className="card">
        <div className="search-bar">
          <input className="search-input" placeholder="Search documents..." value={search} onChange={e => setSearch(e.target.value)} />
          <select className="form-control" style={{ width: 180 }} value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
            <option value="">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="review">Under Review</option>
            <option value="approved">Approved</option>
            <option value="superseded">Superseded</option>
            <option value="archived">Archived</option>
          </select>
        </div>
        {loading ? <div className="loading">Loading...</div> : (
          <table>
            <thead>
              <tr><th>Doc #</th><th>Name</th><th>Project</th><th>Category</th><th>Version</th><th>Size</th><th>Tags</th><th>Status</th><th>Date</th></tr>
            </thead>
            <tbody>
              {documents.length === 0 ? (
                <tr><td colSpan={9}><div className="empty-state">No documents found</div></td></tr>
              ) : documents.map(d => (
                <tr key={d.id}>
                  <td style={{ fontSize: 12 }}>{d.document_number || '—'}</td>
                  <td style={{ fontWeight: 500 }}>{d.name}</td>
                  <td style={{ fontSize: 13 }}>{d.project_code}</td>
                  <td style={{ fontSize: 13 }}>{d.category_name || '—'}</td>
                  <td><span className="badge badge-secondary">v{d.version}</span></td>
                  <td style={{ fontSize: 12 }}>{formatSize(d.file_size)}</td>
                  <td style={{ fontSize: 12, color: '#64748b' }}>{d.tags || '—'}</td>
                  <td><span className={`badge ${statusColor[d.status] || 'badge-secondary'}`}>{d.status.replace('_', ' ')}</span></td>
                  <td style={{ fontSize: 12 }}>{new Date(d.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
