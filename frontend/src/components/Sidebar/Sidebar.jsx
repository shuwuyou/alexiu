import React from 'react';
import { LayoutDashboard, MessageSquare, FileText, HelpCircle } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ activeView, onNavigate }) => {
  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard', active: activeView === 'dashboard' },
    { id: 'chat', icon: MessageSquare, label: 'Ask Alexiu', active: activeView === 'chat' },
    { id: 'reports', icon: FileText, label: 'My Reports', active: activeView === 'reports' },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <img src="/assets/logo.jpg" alt="Alexiu Logo" className="logo-image" />
          <h2>Alexiu</h2>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button 
            key={item.id} 
            className={`nav-item ${item.active ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="nav-item">
          <HelpCircle size={20} />
          <span>Help & Support</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
