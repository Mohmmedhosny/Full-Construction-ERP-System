import React, { useState, useEffect } from 'react';
import { procurementAPI } from '../services/api';

export default function Procurement() {
  const [tab, setTab] = useState('vendors');
  const [vendors, setVendors] = useState([]);
  const [purchaseOrders, setPurchaseOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [v, po] = await Promise.all([
          procurementAPI.getVendors(),
          procurementAPI.getPurchaseOrders(),
        ]);
        setVendors(v.data.results || v.data);
        setPurchaseOrders(po.data.results || po.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
  }, []);

  const poStatusColor = {
    draft: 'badge-secondary', pending: 'badge-warning', approved: 'badge-info',
    sent: 'badge-primary', partial: 'badge-warning', received: 'badge-success', cancelled: 'badge-danger',
  };
  const vendorStatusColor = { active: 'badge-success', inactive: 'badge-secondary', blacklisted: 'badge-danger' };
  const fmt = (v) => `$${Number(v || 0).toLocaleString()}`;

  if (loading) return <div className="loading">Loading procurement data...</div>;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">🛒 Procurement</h1>
      </div>

      <div className="stat-grid">
        <div className="stat-card" style={{ borderTop: '3px solid var(--accent)' }}>
          <div className="stat-label">Total Vendors</div>
          <div className="stat-value">{vendors.length}</div>
          <div className="stat-sub">Active: {vendors.filter(v => v.status === 'active').length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--info)' }}>
          <div className="stat-label">Purchase Orders</div>
          <div className="stat-value">{purchaseOrders.length}</div>
          <div className="stat-sub">Pending: {purchaseOrders.filter(p => p.status === 'pending').length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-label">Total PO Value</div>
          <div className="stat-value" style={{ fontSize: 18 }}>{fmt(purchaseOrders.reduce((s, p) => s + parseFloat(p.total_amount || 0), 0))}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-label">Awaiting Delivery</div>
          <div className="stat-value">{purchaseOrders.filter(p => ['approved', 'sent', 'partial'].includes(p.status)).length}</div>
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === 'vendors' ? 'active' : ''}`} onClick={() => setTab('vendors')}>Vendors ({vendors.length})</button>
        <button className={`tab ${tab === 'orders' ? 'active' : ''}`} onClick={() => setTab('orders')}>Purchase Orders ({purchaseOrders.length})</button>
      </div>

      {tab === 'vendors' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Code</th><th>Name</th><th>Category</th><th>Contact</th><th>Email</th><th>Rating</th><th>Status</th></tr>
            </thead>
            <tbody>
              {vendors.length === 0 ? (
                <tr><td colSpan={7}><div className="empty-state">No vendors registered</div></td></tr>
              ) : vendors.map(v => (
                <tr key={v.id}>
                  <td><code style={{ fontSize: 12 }}>{v.code}</code></td>
                  <td style={{ fontWeight: 500 }}>{v.name}</td>
                  <td><span className="badge badge-secondary">{v.category}</span></td>
                  <td style={{ fontSize: 13 }}>{v.contact_person || '—'}</td>
                  <td style={{ fontSize: 13 }}>{v.email || '—'}</td>
                  <td style={{ fontSize: 13 }}>{'⭐'.repeat(Math.round(v.rating))} {v.rating}</td>
                  <td><span className={`badge ${vendorStatusColor[v.status] || 'badge-secondary'}`}>{v.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'orders' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>PO Number</th><th>Project</th><th>Vendor</th><th>Date</th><th>Expected</th><th>Amount</th><th>Status</th></tr>
            </thead>
            <tbody>
              {purchaseOrders.length === 0 ? (
                <tr><td colSpan={7}><div className="empty-state">No purchase orders</div></td></tr>
              ) : purchaseOrders.map(po => (
                <tr key={po.id}>
                  <td style={{ fontWeight: 500 }}>{po.po_number}</td>
                  <td style={{ fontSize: 13 }}>{po.project_code}</td>
                  <td style={{ fontSize: 13 }}>{po.vendor_name}</td>
                  <td style={{ fontSize: 13 }}>{po.date}</td>
                  <td style={{ fontSize: 13 }}>{po.expected_delivery || '—'}</td>
                  <td style={{ fontWeight: 500 }}>{fmt(po.total_amount)}</td>
                  <td><span className={`badge ${poStatusColor[po.status] || 'badge-secondary'}`}>{po.status.replace('_', ' ')}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
