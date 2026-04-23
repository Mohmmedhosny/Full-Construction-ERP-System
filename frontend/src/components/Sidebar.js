import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import './Sidebar.css';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/projects', label: 'Projects', icon: '🏗️' },
  { path: '/resources', label: 'Resources', icon: '🔧' },
  { path: '/finance', label: 'Finance', icon: '💰' },
  { path: '/procurement', label: 'Procurement', icon: '🛒' },
  { path: '/hr', label: 'Human Resources', icon: '👥' },
  { path: '/documents', label: 'Documents', icon: '📄' },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <span className="logo-icon">🏛️</span>
        <div>
          <div className="logo-title">ConstructERP</div>
          <div className="logo-subtitle">Management System</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `nav-item ${isActive || (item.path !== '/' && location.pathname.startsWith(item.path)) ? 'active' : ''}`
            }
            end={item.path === '/'}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="version-label">v1.0.0</div>
      </div>
    </aside>
  );
}
