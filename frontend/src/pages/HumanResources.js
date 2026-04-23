import React, { useState, useEffect } from 'react';
import { hrAPI } from '../services/api';

export default function HumanResources() {
  const [tab, setTab] = useState('employees');
  const [employees, setEmployees] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [emp, att, lv, st] = await Promise.all([
          hrAPI.getEmployees(),
          hrAPI.getTodayAttendance(),
          hrAPI.getLeaveRequests(),
          hrAPI.getEmployeeStats(),
        ]);
        setEmployees(emp.data.results || emp.data);
        setAttendance(att.data.results || att.data);
        setLeaveRequests(lv.data.results || lv.data);
        setStats(st.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
  }, []);

  const empStatusColor = { active: 'badge-success', inactive: 'badge-secondary', on_leave: 'badge-warning', terminated: 'badge-danger' };
  const leaveStatusColor = { pending: 'badge-warning', approved: 'badge-success', rejected: 'badge-danger', cancelled: 'badge-secondary' };
  const attStatusColor = { present: 'badge-success', absent: 'badge-danger', half_day: 'badge-warning', on_leave: 'badge-info' };

  if (loading) return <div className="loading">Loading HR data...</div>;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">👥 Human Resources</h1>
      </div>

      <div className="stat-grid">
        <div className="stat-card" style={{ borderTop: '3px solid var(--accent)' }}>
          <div className="stat-label">Total Employees</div>
          <div className="stat-value">{stats?.total ?? '—'}</div>
          <div className="stat-sub">Active: {stats?.active ?? 0}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--info)' }}>
          <div className="stat-label">Today Present</div>
          <div className="stat-value">{attendance.filter(a => a.status === 'present').length}</div>
          <div className="stat-sub">Total checked: {attendance.length}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--warning)' }}>
          <div className="stat-label">On Leave</div>
          <div className="stat-value">{stats?.on_leave ?? '—'}</div>
        </div>
        <div className="stat-card" style={{ borderTop: '3px solid var(--success)' }}>
          <div className="stat-label">Pending Leave Requests</div>
          <div className="stat-value">{leaveRequests.filter(l => l.status === 'pending').length}</div>
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === 'employees' ? 'active' : ''}`} onClick={() => setTab('employees')}>Employees ({employees.length})</button>
        <button className={`tab ${tab === 'attendance' ? 'active' : ''}`} onClick={() => setTab('attendance')}>Today's Attendance ({attendance.length})</button>
        <button className={`tab ${tab === 'leaves' ? 'active' : ''}`} onClick={() => setTab('leaves')}>Leave Requests ({leaveRequests.length})</button>
      </div>

      {tab === 'employees' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>ID</th><th>Name</th><th>Department</th><th>Job Title</th><th>Type</th><th>Hire Date</th><th>Status</th></tr>
            </thead>
            <tbody>
              {employees.length === 0 ? (
                <tr><td colSpan={7}><div className="empty-state">No employees found</div></td></tr>
              ) : employees.map(e => (
                <tr key={e.id}>
                  <td><code style={{ fontSize: 12 }}>{e.employee_id}</code></td>
                  <td style={{ fontWeight: 500 }}>{e.full_name}</td>
                  <td style={{ fontSize: 13 }}>{e.department_name || '—'}</td>
                  <td style={{ fontSize: 13 }}>{e.job_title_name || '—'}</td>
                  <td><span className="badge badge-secondary">{e.employment_type.replace('_', ' ')}</span></td>
                  <td style={{ fontSize: 13 }}>{e.hire_date}</td>
                  <td><span className={`badge ${empStatusColor[e.status] || 'badge-secondary'}`}>{e.status.replace('_', ' ')}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'attendance' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Employee ID</th><th>Name</th><th>Check In</th><th>Check Out</th><th>Status</th><th>Overtime</th></tr>
            </thead>
            <tbody>
              {attendance.length === 0 ? (
                <tr><td colSpan={6}><div className="empty-state">No attendance records for today</div></td></tr>
              ) : attendance.map(a => (
                <tr key={a.id}>
                  <td style={{ fontSize: 13 }}>{a.employee_id}</td>
                  <td style={{ fontWeight: 500 }}>{a.employee_name}</td>
                  <td style={{ fontSize: 13 }}>{a.check_in || '—'}</td>
                  <td style={{ fontSize: 13 }}>{a.check_out || '—'}</td>
                  <td><span className={`badge ${attStatusColor[a.status] || 'badge-secondary'}`}>{a.status.replace('_', ' ')}</span></td>
                  <td style={{ fontSize: 13 }}>{a.overtime_hours}h</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'leaves' && (
        <div className="card">
          <table>
            <thead>
              <tr><th>Employee</th><th>Leave Type</th><th>Start</th><th>End</th><th>Days</th><th>Status</th></tr>
            </thead>
            <tbody>
              {leaveRequests.length === 0 ? (
                <tr><td colSpan={6}><div className="empty-state">No leave requests</div></td></tr>
              ) : leaveRequests.map(l => (
                <tr key={l.id}>
                  <td style={{ fontWeight: 500 }}>{l.employee_name}</td>
                  <td style={{ fontSize: 13 }}>{l.leave_type_name}</td>
                  <td style={{ fontSize: 13 }}>{l.start_date}</td>
                  <td style={{ fontSize: 13 }}>{l.end_date}</td>
                  <td style={{ fontSize: 13 }}>{l.days}</td>
                  <td><span className={`badge ${leaveStatusColor[l.status] || 'badge-secondary'}`}>{l.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
