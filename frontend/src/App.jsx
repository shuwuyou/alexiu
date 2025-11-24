import React, { useState } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import Dashboard from './components/Dashboard/Dashboard';
import AskAlexiu from './components/AskAlexiu/AskAlexiu';
import MyReports from './components/MyReports/MyReports';
import './styles/theme.css';
import './styles/globals.css';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState('dashboard');

  const handleNavigate = (view) => {
    setActiveView(view);
  };

  return (
    <div className="app">
      <Sidebar activeView={activeView} onNavigate={handleNavigate} />
      {activeView === 'dashboard' && <Dashboard />}
      {activeView === 'chat' && <AskAlexiu />}
      {activeView === 'reports' && <MyReports />}
    </div>
  );
}

export default App;
