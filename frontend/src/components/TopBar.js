import React from 'react';
import { useNavigate } from 'react-router-dom';
import './TopBar.css';

export default function TopBar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
    window.location.reload();
  };

  return (
    <header className="topbar">
      <div className="topbar-left">
        <span className="topbar-greeting">Full Construction ERP System</span>
      </div>
      <div className="topbar-right">
        <div className="topbar-user">
          <span className="user-avatar">👤</span>
          <span className="user-name">Admin</span>
        </div>
        <button className="logout-btn" onClick={handleLogout} title="Logout">
          ⬅️ Logout
        </button>
      </div>
    </header>
  );
}
