import React, { useState, useEffect } from 'react';
import { financeAPI } from '../services/api';

export default function Finance() {
  const [tab, setTab] = useState('invoices');
  const [invoices, setInvoices] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [inv, exp, sum] = await Promise.all([
          financeAPI.getInvoices(),
          financeAPI.getExpenses(),
          financeAPI.getInvoiceSummary(),
        ]);
        setInvoices(inv.data.results || inv.data);
        setExpenses(exp.data.results || exp.data);
        setSummary(sum.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
  }, []);

  const fmt = (v) => `$${Number(v || 0).toLocaleString()}`;
  const statusColor = {
    draft: 'badge-secondary', sent: 'badge-info', partial: 'badge-warning',
    paid: 'badge-success', overdue: 'badge-danger', cancelled: 'badge-secondary',
  };
  const expStatusColor = { pending: 'badge-warning', approved: 'badge-success', rejected: 'badge-danger', paid: 'badge-info' };

  if (loading) return <div className="loading">Loading finance data...</div>;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">💰 Finance</h1>
      </div>

      <div className="stat-grid">
        <div className="stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-label">Total Invoiced</div>
          <div className="stat-value" style={{ fontSize: 20 }}>{fmt(summary?.total_invoiced)}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--info)' }}>
          <div className="stat-label">Total Collected</div>
          <div className="stat-value" style={{ fontSize: 20 }}>{fmt(summary?.total_paid)}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--danger)' }}>
          <div className="stat-label">Outstanding</div>
          <div className="stat-value" style={{ fontSize: 20 }}>{fmt(summary?.total_outstanding)}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-label">Total Expenses</div>
          <div className="stat-value" style={{ fontSize: 20 }}>{fmt(expenses.reduce((s, e) => s + parseFloat(e.amount || 0), 0))}</div>
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === 'invoices' ? 'active' : ''}`} onClick={() => setTab('invoices')}>Invoices ({invoices.length})</button>
        <button className={`tab ${tab === 'expenses' ? 'active' : ''}`} onClick={() => setTab('expenses')}>Expenses ({expenses.length})</button>
      </div>

      {tab === 'invoices' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Invoice #</th><th>Project</th><th>Type</th><th>Date</th><th>Due</th><th>Total</th><th>Paid</th><th>Balance</th><th>Status</th></tr>
            </thead>
            <tbody>
              {invoices.length === 0 ? (
                <tr><td colSpan={9}><div className="empty-state">No invoices yet</div></td></tr>
              ) : invoices.map(inv => (
                <tr key={inv.id}>
                  <td style={{ fontWeight: 500 }}>{inv.invoice_number}</td>
                  <td style={{ fontSize: 13 }}>{inv.project_code}</td>
                  <td><span className="badge badge-secondary">{inv.invoice_type}</span></td>
                  <td style={{ fontSize: 13 }}>{inv.date}</td>
                  <td style={{ fontSize: 13 }}>{inv.due_date}</td>
                  <td style={{ fontSize: 13 }}>{fmt(inv.total_amount)}</td>
                  <td style={{ fontSize: 13 }}>{fmt(inv.paid_amount)}</td>
                  <td style={{ fontSize: 13, fontWeight: 600, color: parseFloat(inv.balance_due) > 0 ? 'var(--danger)' : 'var(--success)' }}>{fmt(inv.balance_due)}</td>
                  <td><span className={`badge ${statusColor[inv.status] || 'badge-secondary'}`}>{inv.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'expenses' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Project</th><th>Category</th><th>Description</th><th>Amount</th><th>Date</th><th>Status</th></tr>
            </thead>
            <tbody>
              {expenses.length === 0 ? (
                <tr><td colSpan={6}><div className="empty-state">No expenses recorded</div></td></tr>
              ) : expenses.map(exp => (
                <tr key={exp.id}>
                  <td style={{ fontSize: 13 }}>{exp.project_code}</td>
                  <td><span className="badge badge-secondary">{exp.category}</span></td>
                  <td style={{ fontSize: 13 }}>{exp.description}</td>
                  <td style={{ fontWeight: 500 }}>{fmt(exp.amount)}</td>
                  <td style={{ fontSize: 13 }}>{exp.date}</td>
                  <td><span className={`badge ${expStatusColor[exp.status] || 'badge-secondary'}`}>{exp.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
