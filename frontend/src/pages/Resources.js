import React, { useState, useEffect } from 'react';
import { resourcesAPI } from '../services/api';

export default function Resources() {
  const [tab, setTab] = useState('equipment');
  const [equipment, setEquipment] = useState([]);
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [eq, mat] = await Promise.all([
          resourcesAPI.getEquipment(),
          resourcesAPI.getMaterials(),
        ]);
        setEquipment(eq.data.results || eq.data);
        setMaterials(mat.data.results || mat.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
  }, []);

  const statusColor = { available: 'badge-success', in_use: 'badge-info', maintenance: 'badge-warning', retired: 'badge-secondary', rented: 'badge-primary' };

  if (loading) return <div className="loading">Loading resources...</div>;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">🔧 Resources</h1>
      </div>

      <div className="stat-grid">
        <div className="stat-card" style={{ borderTop: '3px solid var(--accent)' }}>
          <div className="stat-label">Total Equipment</div>
          <div className="stat-value">{equipment.length}</div>
          <div className="stat-sub">Available: {equipment.filter(e => e.status === 'available').length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--info)' }}>
          <div className="stat-label">In Use</div>
          <div className="stat-value">{equipment.filter(e => e.status === 'in_use').length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-label">Materials</div>
          <div className="stat-value">{materials.length}</div>
          <div className="stat-sub">Low stock: {materials.filter(m => parseFloat(m.current_stock) <= parseFloat(m.reorder_level)).length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-label">Maintenance</div>
          <div className="stat-value">{equipment.filter(e => e.status === 'maintenance').length}</div>
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === 'equipment' ? 'active' : ''}`} onClick={() => setTab('equipment')}>Equipment ({equipment.length})</button>
        <button className={`tab ${tab === 'materials' ? 'active' : ''}`} onClick={() => setTab('materials')}>Materials ({materials.length})</button>
      </div>

      {tab === 'equipment' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Code</th><th>Name</th><th>Category</th><th>Status</th><th>Cost/Day</th><th>Location</th><th>Next Maintenance</th></tr>
            </thead>
            <tbody>
              {equipment.length === 0 ? (
                <tr><td colSpan={7}><div className="empty-state">No equipment records</div></td></tr>
              ) : equipment.map(e => (
                <tr key={e.id}>
                  <td><code style={{ fontSize: 12 }}>{e.code}</code></td>
                  <td style={{ fontWeight: 500 }}>{e.name}</td>
                  <td style={{ fontSize: 13 }}>{e.category_name || '—'}</td>
                  <td><span className={`badge ${statusColor[e.status] || 'badge-secondary'}`}>{e.status.replace('_', ' ')}</span></td>
                  <td style={{ fontSize: 13 }}>${Number(e.cost_per_day).toLocaleString()}</td>
                  <td style={{ fontSize: 13 }}>{e.location || '—'}</td>
                  <td style={{ fontSize: 13, color: e.next_maintenance ? 'var(--warning)' : '#94a3b8' }}>{e.next_maintenance || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'materials' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Code</th><th>Name</th><th>Category</th><th>Unit</th><th>Unit Cost</th><th>Stock</th><th>Min Stock</th><th>Status</th></tr>
            </thead>
            <tbody>
              {materials.length === 0 ? (
                <tr><td colSpan={8}><div className="empty-state">No materials records</div></td></tr>
              ) : materials.map(m => {
                const lowStock = parseFloat(m.current_stock) <= parseFloat(m.reorder_level);
                return (
                  <tr key={m.id}>
                    <td><code style={{ fontSize: 12 }}>{m.code}</code></td>
                    <td style={{ fontWeight: 500 }}>{m.name}</td>
                    <td style={{ fontSize: 13 }}>{m.category_name || '—'}</td>
                    <td style={{ fontSize: 13 }}>{m.unit}</td>
                    <td style={{ fontSize: 13 }}>${Number(m.unit_cost).toLocaleString()}</td>
                    <td style={{ fontSize: 13, color: lowStock ? 'var(--danger)' : 'inherit', fontWeight: lowStock ? 600 : 400 }}>{m.current_stock}</td>
                    <td style={{ fontSize: 13 }}>{m.reorder_level}</td>
                    <td><span className={`badge ${lowStock ? 'badge-danger' : 'badge-success'}`}>{lowStock ? 'Low Stock' : 'OK'}</span></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
