import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import Resources from './pages/Resources';
import Finance from './pages/Finance';
import Procurement from './pages/Procurement';
import HumanResources from './pages/HumanResources';
import Documents from './pages/Documents';
import Login from './pages/Login';
import './App.css';

function PrivateLayout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <TopBar />
        <div className="page-content">
          {children}
        </div>
      </div>
    </div>
  );
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access_token'));

  useEffect(() => {
    const checkAuth = () => setIsAuthenticated(!!localStorage.getItem('access_token'));
    window.addEventListener('storage', checkAuth);
    return () => window.removeEventListener('storage', checkAuth);
  }, []);

  const handleLogin = (tokens) => {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.clear();
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    );
  }

  return (
    <Router>
      <PrivateLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:id" element={<ProjectDetail />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/finance" element={<Finance />} />
          <Route path="/procurement" element={<Procurement />} />
          <Route path="/hr" element={<HumanResources />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </PrivateLayout>
    </Router>
  );
}

export default App;
