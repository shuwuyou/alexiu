# UI Creation Steps - Soccer Player Evaluation Webpage

## Project Overview
This document outlines the steps to create a professional dark-themed React UI for a soccer player evaluation webpage. The UI will display player performance analytics through multiple visualization components and an AI-generated report.

## UI Components Structure

### Main Components
1. **Word Cloud** - Player performance factorization visualization
2. **Pie Chart** - Performance factorization breakdown
3. **Performance vs Valuation Chart** - Scatter/line visualization
4. **AI Report Section** - Comprehensive player evaluation report

## Project Structure

```
hackathon-2025-3to1/
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   └── Dashboard.css
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Sidebar.css
│   │   │   ├── WordCloud/
│   │   │   │   ├── WordCloudChart.jsx
│   │   │   │   └── WordCloudChart.css
│   │   │   ├── PieChart/
│   │   │   │   ├── PerformancePieChart.jsx
│   │   │   │   └── PerformancePieChart.css
│   │   │   ├── PerformanceChart/
│   │   │   │   ├── PerformanceValuationChart.jsx
│   │   │   │   └── PerformanceValuationChart.css
│   │   │   └── AIReport/
│   │   │       ├── AIReport.jsx
│   │   │       └── AIReport.css
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── dataService.js
│   │   ├── utils/
│   │   │   ├── csvParser.js
│   │   │   └── constants.js
│   │   ├── styles/
│   │   │   ├── theme.css
│   │   │   └── globals.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── vite.config.js
└── assets/
    └── UI_CREATION_STEPS.md (this file)
```

## Step-by-Step Implementation Guide

### Step 1: Initialize React Project with Vite

```bash
# Navigate to project root
cd hackathon-2025-3to1

# Create Vite React project
npm create vite@latest frontend -- --template react

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Step 2: Install Required Dependencies

```bash
# Install UI and charting libraries
npm install recharts react-wordcloud d3-cloud
npm install lucide-react
npm install axios

# Install development dependencies (optional)
npm install -D @types/react @types/react-dom
```

### Step 3: Set Up Global Styles and Theme

**File: `src/styles/theme.css`**
```css
:root {
  /* Dark Theme Colors - Professional Soccer Analytics */
  --bg-primary: #0a0e27;
  --bg-secondary: #131829;
  --bg-tertiary: #1a1f3a;
  --bg-card: #1e2139;
  
  --accent-primary: #4c6ef5;
  --accent-secondary: #5c7cfa;
  --accent-success: #51cf66;
  --accent-warning: #ffd43b;
  --accent-danger: #ff6b6b;
  
  --text-primary: #e9ecef;
  --text-secondary: #adb5bd;
  --text-muted: #6c757d;
  
  --border-color: #2c3145;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
  
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
}
```

**File: `src/styles/globals.css`**
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

.grid {
  display: grid;
  gap: var(--spacing-lg);
}

.grid-2 {
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
}
```

### Step 4: Create Sidebar Component

**File: `src/components/Sidebar/Sidebar.jsx`**
```jsx
import React from 'react';
import { LayoutDashboard, Target, FileText, Star, HelpCircle, User } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ playerName = "Player Name" }) => {
  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard', active: true },
    { id: 'evaluation', icon: Target, label: 'Player Evaluation' },
    { id: 'reports', icon: FileText, label: 'My Reports' },
    { id: 'starred', icon: Star, label: 'Starred Players' },
    { id: 'targets', icon: Target, label: 'My Targets' },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon">⚽</div>
          <h2>Kalos</h2>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button 
            key={item.id} 
            className={`nav-item ${item.active ? 'active' : ''}`}
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
        <div className="user-profile">
          <User size={20} />
          <span>{playerName}</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
```

**File: `src/components/Sidebar/Sidebar.css`**
```css
.sidebar {
  width: 280px;
  height: 100vh;
  background-color: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.logo-icon {
  font-size: 24px;
}

.logo h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: var(--spacing-md);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--border-radius-md);
  transition: all 0.2s ease;
  font-size: 14px;
  text-align: left;
}

.nav-item:hover {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.active {
  background-color: var(--accent-primary);
  color: white;
}

.sidebar-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  margin-top: var(--spacing-sm);
  background-color: var(--bg-tertiary);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
}
```

### Step 5: Create Word Cloud Component

**File: `src/components/WordCloud/WordCloudChart.jsx`**
```jsx
import React from 'react';
import ReactWordcloud from 'react-wordcloud';
import './WordCloudChart.css';

const WordCloudChart = ({ data = [] }) => {
  // Placeholder data structure
  const placeholderData = [
    { text: 'Speed', value: 85 },
    { text: 'Passing', value: 78 },
    { text: 'Shooting', value: 82 },
    { text: 'Dribbling', value: 90 },
    { text: 'Defense', value: 65 },
    { text: 'Stamina', value: 75 },
    { text: 'Positioning', value: 88 },
    { text: 'Vision', value: 80 },
    { text: 'Control', value: 86 },
    { text: 'Agility', value: 83 },
  ];

  const words = data.length > 0 ? data : placeholderData;

  const options = {
    rotations: 2,
    rotationAngles: [-90, 0],
    fontSizes: [20, 60],
    colors: ['#4c6ef5', '#5c7cfa', '#748ffc', '#91a7ff', '#b197fc'],
    enableTooltip: true,
    deterministic: true,
    fontFamily: 'Inter, sans-serif',
    fontWeight: 600,
  };

  return (
    <div className="card wordcloud-card">
      <div className="card-header">
        <h3>Performance Factors</h3>
        <p className="card-subtitle">Key attributes analysis</p>
      </div>
      <div className="wordcloud-container">
        {words.length > 0 ? (
          <ReactWordcloud words={words} options={options} />
        ) : (
          <div className="placeholder">No data available</div>
        )}
      </div>
    </div>
  );
};

export default WordCloudChart;
```

**File: `src/components/WordCloud/WordCloudChart.css`**
```css
.wordcloud-card {
  height: 400px;
}

.card-header {
  margin-bottom: var(--spacing-lg);
}

.card-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.card-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.wordcloud-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder {
  color: var(--text-muted);
  font-size: 16px;
}
```

### Step 6: Create Pie Chart Component

**File: `src/components/PieChart/PerformancePieChart.jsx`**
```jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './PerformancePieChart.css';

const PerformancePieChart = ({ data = [] }) => {
  // Placeholder data
  const placeholderData = [
    { name: 'Technical Skills', value: 35 },
    { name: 'Physical Attributes', value: 25 },
    { name: 'Mental Strength', value: 20 },
    { name: 'Tactical Awareness', value: 20 },
  ];

  const chartData = data.length > 0 ? data : placeholderData;
  
  const COLORS = ['#4c6ef5', '#5c7cfa', '#748ffc', '#91a7ff'];

  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * Math.PI / 180);
    const y = cy + radius * Math.sin(-midAngle * Math.PI / 180);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize="14"
        fontWeight="600"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="card pie-chart-card">
      <div className="card-header">
        <h3>Performance Distribution</h3>
        <p className="card-subtitle">Skill category breakdown</p>
      </div>
      <div className="pie-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomLabel}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{
                backgroundColor: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--border-radius-sm)',
                color: 'var(--text-primary)'
              }}
            />
            <Legend 
              verticalAlign="bottom" 
              height={36}
              iconType="circle"
              wrapperStyle={{ color: 'var(--text-secondary)' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PerformancePieChart;
```

**File: `src/components/PieChart/PerformancePieChart.css`**
```css
.pie-chart-card {
  height: 400px;
}

.pie-chart-container {
  height: 300px;
}
```

### Step 7: Create Performance vs Valuation Chart

**File: `src/components/PerformanceChart/PerformanceValuationChart.jsx`**
```jsx
import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  Area,
  ComposedChart
} from 'recharts';
import './PerformanceValuationChart.css';

const PerformanceValuationChart = ({ data = [] }) => {
  // Placeholder data
  const placeholderData = [
    { month: 'Jan', performance: 75, valuation: 45 },
    { month: 'Feb', performance: 78, valuation: 48 },
    { month: 'Mar', performance: 82, valuation: 55 },
    { month: 'Apr', performance: 80, valuation: 58 },
    { month: 'May', performance: 85, valuation: 65 },
    { month: 'Jun', performance: 88, valuation: 70 },
    { month: 'Jul', performance: 86, valuation: 72 },
    { month: 'Aug', performance: 90, valuation: 78 },
  ];

  const chartData = data.length > 0 ? data : placeholderData;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{payload[0].payload.month}</p>
          <p className="tooltip-performance">
            Performance: <span>{payload[0].value}</span>
          </p>
          <p className="tooltip-valuation">
            Valuation: <span>${payload[1].value}M</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card performance-chart-card">
      <div className="card-header">
        <h3>Performance vs Market Valuation</h3>
        <p className="card-subtitle">Trend analysis over time</p>
      </div>
      <div className="performance-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData}>
            <defs>
              <linearGradient id="colorPerformance" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4c6ef5" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#4c6ef5" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
            <XAxis 
              dataKey="month" 
              stroke="var(--text-secondary)"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="var(--text-secondary)"
              style={{ fontSize: '12px' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ color: 'var(--text-secondary)', paddingTop: '10px' }}
            />
            <Area
              type="monotone"
              dataKey="performance"
              fill="url(#colorPerformance)"
              stroke="none"
            />
            <Line 
              type="monotone" 
              dataKey="performance" 
              stroke="#4c6ef5" 
              strokeWidth={3}
              dot={{ fill: '#4c6ef5', r: 4 }}
              activeDot={{ r: 6 }}
            />
            <Line 
              type="monotone" 
              dataKey="valuation" 
              stroke="#51cf66" 
              strokeWidth={3}
              dot={{ fill: '#51cf66', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PerformanceValuationChart;
```

**File: `src/components/PerformanceChart/PerformanceValuationChart.css`**
```css
.performance-chart-card {
  grid-column: 1 / -1;
  height: 450px;
}

.performance-chart-container {
  height: 350px;
}

.custom-tooltip {
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-md);
  color: var(--text-primary);
}

.tooltip-label {
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.tooltip-performance span,
.tooltip-valuation span {
  font-weight: 600;
  color: var(--accent-primary);
}

.tooltip-valuation span {
  color: var(--accent-success);
}
```

### Step 8: Create AI Report Component

**File: `src/components/AIReport/AIReport.jsx`**
```jsx
import React, { useState } from 'react';
import { FileText, Download, Share2, Sparkles } from 'lucide-react';
import './AIReport.css';

const AIReport = ({ report = null }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // Placeholder report data
  const placeholderReport = {
    summary: "This player demonstrates exceptional technical abilities with consistent performance improvements over the past season. Strong attacking capabilities combined with tactical awareness make them a valuable asset.",
    strengths: [
      "Outstanding dribbling skills and ball control",
      "Excellent vision and passing accuracy",
      "High work rate and stamina",
      "Strong positioning sense"
    ],
    weaknesses: [
      "Defensive contributions could be improved",
      "Inconsistent finishing in high-pressure situations"
    ],
    recommendations: [
      "Focus on defensive training and positioning",
      "Work on composure in front of goal",
      "Maintain current fitness regimen"
    ],
    marketValue: "$75M",
    potentialGrowth: "+15% over next 12 months",
    generatedAt: new Date().toLocaleDateString()
  };

  const reportData = report || placeholderReport;

  return (
    <div className="card ai-report-card">
      <div className="card-header">
        <div className="header-left">
          <div className="ai-badge">
            <Sparkles size={16} />
            <span>AI Generated</span>
          </div>
          <h3>Comprehensive Player Evaluation</h3>
          <p className="card-subtitle">Generated on {reportData.generatedAt}</p>
        </div>
        <div className="header-actions">
          <button className="action-btn">
            <Download size={18} />
            Export
          </button>
          <button className="action-btn">
            <Share2 size={18} />
            Share
          </button>
        </div>
      </div>

      <div className="report-content">
        <section className="report-section">
          <div className="section-icon">
            <FileText size={20} />
          </div>
          <div className="section-content">
            <h4>Executive Summary</h4>
            <p>{reportData.summary}</p>
          </div>
        </section>

        <div className="report-grid">
          <section className="report-section">
            <h4>Key Strengths</h4>
            <ul className="strength-list">
              {reportData.strengths.map((strength, index) => (
                <li key={index}>
                  <span className="bullet success">✓</span>
                  {strength}
                </li>
              ))}
            </ul>
          </section>

          <section className="report-section">
            <h4>Areas for Improvement</h4>
            <ul className="weakness-list">
              {reportData.weaknesses.map((weakness, index) => (
                <li key={index}>
                  <span className="bullet warning">!</span>
                  {weakness}
                </li>
              ))}
            </ul>
          </section>
        </div>

        <section className="report-section">
          <h4>Recommendations</h4>
          <ul className="recommendation-list">
            {reportData.recommendations.map((rec, index) => (
              <li key={index}>
                <span className="bullet-number">{index + 1}</span>
                {rec}
              </li>
            ))}
          </ul>
        </section>

        <div className="market-insights">
          <div className="insight-card">
            <span className="insight-label">Current Market Value</span>
            <span className="insight-value">{reportData.marketValue}</span>
          </div>
          <div className="insight-card">
            <span className="insight-label">Projected Growth</span>
            <span className="insight-value success">{reportData.potentialGrowth}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIReport;
```

**File: `src/components/AIReport/AIReport.css`**
```css
.ai-report-card {
  grid-column: 1 / -1;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.ai-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 4px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  width: fit-content;
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-left: auto;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 8px 16px;
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.action-btn:hover {
  background-color: var(--accent-primary);
  border-color: var(--accent-primary);
}

.report-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.report-section {
  display: flex;
  gap: var(--spacing-md);
}

.section-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-tertiary);
  border-radius: var(--border-radius-md);
  color: var(--accent-primary);
}

.section-content {
  flex: 1;
}

.report-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.report-section p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.strength-list,
.weakness-list,
.recommendation-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.strength-list li,
.weakness-list li,
.recommendation-list li {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  color: var(--text-secondary);
  line-height: 1.6;
}

.bullet {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
}

.bullet.success {
  background-color: rgba(81, 207, 102, 0.2);
  color: var(--accent-success);
}

.bullet.warning {
  background-color: rgba(255, 212, 59, 0.2);
  color: var(--accent-warning);
}

.bullet-number {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--accent-primary);
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
}

.market-insights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background-color: var(--bg-tertiary);
  border-radius: var(--border-radius-lg);
}

.insight-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.insight-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.insight-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.insight-value.success {
  color: var(--accent-success);
}
```

### Step 9: Create Dashboard Component

**File: `src/components/Dashboard/Dashboard.jsx`**
```jsx
import React, { useState } from 'react';
import { Search, Target } from 'lucide-react';
import WordCloudChart from '../WordCloud/WordCloudChart';
import PerformancePieChart from '../PieChart/PerformancePieChart';
import PerformanceValuationChart from '../PerformanceChart/PerformanceValuationChart';
import AIReport from '../AIReport/AIReport';
import './Dashboard.css';

const Dashboard = () => {
  const [playerInput, setPlayerInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState('Shio');

  const handleSearch = () => {
    if (playerInput.trim()) {
      setIsLoading(true);
      // API call placeholder
      setTimeout(() => {
        setSelectedPlayer(playerInput);
        setIsLoading(false);
      }, 1000);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="welcome-section">
          <h1>Hi, {selectedPlayer}</h1>
          <p className="subtitle">Player Performance Analytics Dashboard</p>
        </div>

        <div className="search-section">
          <div className="search-bar">
            <Search size={20} />
            <input
              type="text"
              placeholder="Search player by name or ID..."
              value={playerInput}
              onChange={(e) => setPlayerInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button className="search-btn" onClick={handleSearch}>
              Analyze
            </button>
          </div>
        </div>
      </div>

      <div className="targets-section">
        <div className="section-header">
          <Target size={24} className="section-icon" />
          <h2>Performance Analysis</h2>
        </div>
        {isLoading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading player data...</p>
          </div>
        ) : (
          <div className="charts-grid">
            <WordCloudChart />
            <PerformancePieChart />
            <PerformanceValuationChart />
            <AIReport />
          </div>
        )}
      </div>

      <div className="starred-section">
        <div className="section-header">
          <div className="section-icon-wrapper">
            <span className="star-icon">⭐</span>
          </div>
          <h2>Starred Players</h2>
        </div>
        <div className="empty-state">
          <div className="empty-icon">⭐</div>
          <h3>No starred items yet</h3>
          <p>Star important players and analysis for quick access</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
```

**File: `src/components/Dashboard/Dashboard.css`**
```css
.dashboard {
  margin-left: 280px;
  padding: var(--spacing-xl);
  min-height: 100vh;
  background-color: var(--bg-primary);
}

.dashboard-header {
  margin-bottom: var(--spacing-xl);
}

.welcome-section {
  margin-bottom: var(--spacing-lg);
}

.welcome-section h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.subtitle {
  font-size: 16px;
  color: var(--text-secondary);
}

.search-section {
  margin-top: var(--spacing-lg);
}

.search-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-md) var(--spacing-lg);
  max-width: 600px;
}

.search-bar svg {
  color: var(--text-muted);
  flex-shrink: 0;
}

.search-bar input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 15px;
}

.search-bar input::placeholder {
  color: var(--text-muted);
}

.search-btn {
  padding: 8px 20px;
  background-color: var(--accent-primary);
  border: none;
  border-radius: var(--border-radius-md);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.search-btn:hover {
  background-color: var(--accent-secondary);
}

.targets-section,
.starred-section {
  margin-bottom: var(--spacing-xl);
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.section-icon {
  color: var(--accent-primary);
}

.section-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.star-icon {
  font-size: 24px;
}

.section-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--bg-tertiary);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: var(--spacing-lg);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) * 2;
  background-color: var(--bg-card);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-color);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  opacity: 0.3;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 14px;
}
```

### Step 10: Create API Service Layer

**File: `src/services/api.js`**
```javascript
// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

/**
 * API Service for Soccer Player Evaluation
 * 
 * This service handles all API calls to the backend
 * Currently using placeholder data - replace with actual API calls
 */

class APIService {
  /**
   * Fetch player performance data
   * @param {string} playerIdOrName - Player ID or name
   * @returns {Promise<Object>} Performance data including factorization and valuation CSVs
   */
  async getPlayerPerformance(playerIdOrName) {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/player/performance`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ player: playerIdOrName })
      // });
      
      // Placeholder - simulate API delay
      await this.delay(1000);
      
      return {
        factorizationCSV: 'data:text/csv;base64,placeholder',
        valuationCSV: 'data:text/csv;base64,placeholder',
        playerInfo: {
          id: '12345',
          name: playerIdOrName,
          team: 'Example FC',
          position: 'Forward'
        }
      };
    } catch (error) {
      console.error('Error fetching player performance:', error);
      throw error;
    }
  }

  /**
   * Generate AI report for player
   * @param {Object} csvData - CSV data from performance analysis
   * @returns {Promise<Object>} AI generated report
   */
  async generateAIReport(csvData) {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/ai/generate-report`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ 
      //     factorizationCSV: csvData.factorizationCSV,
      //     valuationCSV: csvData.valuationCSV
      //   })
      // });
      
      // Placeholder - simulate API delay
      await this.delay(2000);
      
      return {
        summary: "AI generated player analysis placeholder",
        strengths: [],
        weaknesses: [],
        recommendations: [],
        generatedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error generating AI report:', error);
      throw error;
    }
  }

  /**
   * Utility function to simulate API delay
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export default new APIService();
```

**File: `src/services/dataService.js`**
```javascript
/**
 * Data Service
 * Handles data transformation and processing
 */

class DataService {
  /**
   * Parse CSV string to JSON
   * @param {string} csvString - CSV formatted string
   * @returns {Array} Parsed data array
   */
  parseCSV(csvString) {
    try {
      const lines = csvString.trim().split('\n');
      const headers = lines[0].split(',');
      
      return lines.slice(1).map(line => {
        const values = line.split(',');
        return headers.reduce((obj, header, index) => {
          obj[header.trim()] = values[index]?.trim();
          return obj;
        }, {});
      });
    } catch (error) {
      console.error('Error parsing CSV:', error);
      return [];
    }
  }

  /**
   * Transform performance factorization data for word cloud
   * @param {Array} data - Raw CSV data
   * @returns {Array} Formatted word cloud data
   */
  transformToWordCloud(data) {
    // Expected CSV format: attribute, value
    return data.map(item => ({
      text: item.attribute || item.name,
      value: parseFloat(item.value || item.score || 0)
    }));
  }

  /**
   * Transform performance data for pie chart
   * @param {Array} data - Raw CSV data
   * @returns {Array} Formatted pie chart data
   */
  transformToPieChart(data) {
    // Expected CSV format: category, percentage
    return data.map(item => ({
      name: item.category || item.name,
      value: parseFloat(item.percentage || item.value || 0)
    }));
  }

  /**
   * Transform performance vs valuation data for line chart
   * @param {Array} data - Raw CSV data
   * @returns {Array} Formatted line chart data
   */
  transformToLineChart(data) {
    // Expected CSV format: period, performance, valuation
    return data.map(item => ({
      month: item.period || item.month,
      performance: parseFloat(item.performance || 0),
      valuation: parseFloat(item.valuation || 0)
    }));
  }

  /**
   * Download data as CSV file
   * @param {Array} data - Data to download
   * @param {string} filename - Output filename
   */
  downloadCSV(data, filename = 'export.csv') {
    const csv = this.arrayToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  /**
   * Convert array to CSV string
   * @param {Array} data - Data array
   * @returns {string} CSV string
   */
  arrayToCSV(data) {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(row => 
      headers.map(header => row[header]).join(',')
    );
    
    return [headers.join(','), ...rows].join('\n');
  }
}

export default new DataService();
```

### Step 11: Create Utilities

**File: `src/utils/constants.js`**
```javascript
/**
 * Application Constants
 */

export const CHART_COLORS = {
  primary: '#4c6ef5',
  secondary: '#5c7cfa',
  tertiary: '#748ffc',
  quaternary: '#91a7ff',
  success: '#51cf66',
  warning: '#ffd43b',
  danger: '#ff6b6b',
};

export const PLAYER_POSITIONS = [
  'Goalkeeper',
  'Defender',
  'Midfielder',
  'Forward',
  'Striker',
];

export const PERFORMANCE_METRICS = [
  'Speed',
  'Passing',
  'Shooting',
  'Dribbling',
  'Defense',
  'Stamina',
  'Positioning',
  'Vision',
  'Control',
  'Agility',
];

export const API_ENDPOINTS = {
  PERFORMANCE: '/player/performance',
  AI_REPORT: '/ai/generate-report',
};

export const CHART_CONFIG = {
  wordCloud: {
    rotations: 2,
    rotationAngles: [-90, 0],
    fontSizes: [20, 60],
  },
  pieChart: {
    innerRadius: 0,
    outerRadius: 100,
  },
  lineChart: {
    strokeWidth: 3,
    dotRadius: 4,
  },
};
```

**File: `src/utils/csvParser.js`**
```javascript
/**
 * CSV Parser Utility
 * Advanced CSV parsing with error handling
 */

export class CSVParser {
  /**
   * Parse CSV with custom delimiter
   * @param {string} csvString - CSV content
   * @param {string} delimiter - Column delimiter (default: ',')
   * @returns {Object} Parsed data with headers and rows
   */
  static parse(csvString, delimiter = ',') {
    try {
      const lines = csvString.trim().split('\n');
      
      if (lines.length === 0) {
        throw new Error('Empty CSV file');
      }

      const headers = this.parseRow(lines[0], delimiter);
      const rows = lines.slice(1).map(line => {
        const values = this.parseRow(line, delimiter);
        return this.createObject(headers, values);
      });

      return {
        headers,
        rows,
        rowCount: rows.length,
      };
    } catch (error) {
      console.error('CSV Parse Error:', error);
      return { headers: [], rows: [], rowCount: 0, error: error.message };
    }
  }

  /**
   * Parse a single CSV row handling quoted values
   * @param {string} row - CSV row string
   * @param {string} delimiter - Column delimiter
   * @returns {Array} Parsed values
   */
  static parseRow(row, delimiter) {
    const values = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < row.length; i++) {
      const char = row[i];
      const nextChar = row[i + 1];

      if (char === '"') {
        if (inQuotes && nextChar === '"') {
          current += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === delimiter && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }

    values.push(current.trim());
    return values;
  }

  /**
   * Create object from headers and values
   * @param {Array} headers - Column headers
   * @param {Array} values - Row values
   * @returns {Object} Row object
   */
  static createObject(headers, values) {
    return headers.reduce((obj, header, index) => {
      obj[header] = values[index] !== undefined ? values[index] : null;
      return obj;
    }, {});
  }

  /**
   * Convert objects array to CSV string
   * @param {Array} data - Array of objects
   * @returns {string} CSV string
   */
  static stringify(data) {
    if (!Array.isArray(data) || data.length === 0) {
      return '';
    }

    const headers = Object.keys(data[0]);
    const csvRows = [
      headers.join(','),
      ...data.map(row =>
        headers.map(header => {
          const value = row[header];
          return this.escapeValue(value);
        }).join(',')
      ),
    ];

    return csvRows.join('\n');
  }

  /**
   * Escape CSV value if needed
   * @param {*} value - Value to escape
   * @returns {string} Escaped value
   */
  static escapeValue(value) {
    if (value === null || value === undefined) {
      return '';
    }

    const stringValue = String(value);
    
    if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
      return `"${stringValue.replace(/"/g, '""')}"`;
    }

    return stringValue;
  }
}

export default CSVParser;
```

### Step 12: Create Main App Component

**File: `src/App.jsx`**
```jsx
import React from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import Dashboard from './components/Dashboard/Dashboard';
import './styles/theme.css';
import './styles/globals.css';
import './App.css';

function App() {
  return (
    <div className="app">
      <Sidebar />
      <Dashboard />
    </div>
  );
}

export default App;
```

**File: `src/App.css`**
```css
.app {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-primary);
}
```

### Step 13: Vite Configuration

**File: `vite.config.js`**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
```

### Step 14: Package.json Configuration

**File: `package.json`**
```json
{
  "name": "kalos-soccer-evaluation",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.3",
    "react-wordcloud": "^1.2.7",
    "d3-cloud": "^1.2.7",
    "lucide-react": "^0.294.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0"
  }
}
```

## Running the Application

### Development Mode
```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build
```bash
npm run build
npm run preview
```

## API Integration Points

### 1. Performance Data API
**Endpoint**: `/api/player/performance`
**Method**: POST
**Input**: 
```json
{
  "player": "player_id or player_name"
}
```
**Output**:
- `factorization.csv` - Performance attributes and values
- `valuation.csv` - Performance vs valuation timeline

### 2. AI Report Generation API
**Endpoint**: `/api/ai/generate-report`
**Method**: POST
**Input**:
```json
{
  "factorizationCSV": "base64_encoded_csv",
  "valuationCSV": "base64_encoded_csv"
}
```
**Output**:
```json
{
  "summary": "string",
  "strengths": ["array"],
  "weaknesses": ["array"],
  "recommendations": ["array"],
  "marketValue": "string",
  "potentialGrowth": "string"
}
```

## Integration Steps

1. **Update API endpoints** in `src/services/api.js`
2. **Configure environment variables** in `.env` file
3. **Replace placeholder data** in components with API responses
4. **Implement CSV parsing** for API responses using `dataService.js`

## Design Features

- **Dark Theme**: Professional dark color scheme optimized for data visualization
- **Responsive Layout**: Grid-based layout that adapts to different screen sizes
- **Interactive Charts**: Recharts library for dynamic, interactive visualizations
- **Loading States**: Proper loading indicators for async operations
- **Empty States**: User-friendly messages when no data is available
- **Modular Components**: Reusable, maintainable component structure

## Customization

### Changing Theme Colors
Edit `src/styles/theme.css` CSS variables

### Adding New Metrics
Update `src/utils/constants.js` PERFORMANCE_METRICS array

### Modifying Chart Styles
Edit individual component CSS files in respective component folders

## Notes

- All API calls are currently using placeholder data
- CSV parsing logic is prepared for real data integration
- Components are designed to be data-agnostic
- Error handling should be implemented in production
- Add authentication/authorization as needed
- Consider adding data caching for performance

## Next Steps

1. Integrate with actual backend APIs
2. Implement error boundary components
3. Add unit tests for components
4. Set up CI/CD pipeline
5. Implement user authentication
6. Add data export functionality
7. Optimize performance with React.memo and useMemo
8. Add accessibility features (ARIA labels, keyboard navigation)

---

**Last Updated**: November 15, 2025
**Version**: 1.0.0
