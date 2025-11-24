# Alexiu Frontend - Player Analytics Dashboard

Modern React-based frontend for the Alexiu AI-Powered Soccer Player Analytics Platform. Built with React 19, Vite, and a component-based architecture for interactive data visualization and AI-powered insights.

## 🎯 Overview

The frontend provides an intuitive interface for:
- Searching and analyzing soccer players
- Generating AI-powered comprehensive reports
- Interactive chatbot for player insights (Alexiu)
- Visual analytics with charts and word clouds
- Report management and export functionality

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm (or yarn/pnpm)
- Backend API running on `http://localhost:8000` (see main project README)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Application will be available at http://localhost:5173
```

### Build for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

### Linting

```bash
# Run ESLint
npm run lint
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── AIReport/        # AI-generated report display
│   │   ├── AskAlexiu/       # Chatbot interface
│   │   ├── Dashboard/       # Main analytics dashboard
│   │   ├── MyReports/       # Saved reports management
│   │   ├── PerformanceChart/ # Time series visualization
│   │   ├── PlayerInfo/      # Player profile card
│   │   ├── Sidebar/         # Navigation sidebar
│   │   └── WordCloud/       # SHAP feature word cloud
│   ├── services/            # API service modules
│   │   ├── chatbotService.js    # Chatbot API calls
│   │   ├── playerSearch.js      # Player search API
│   │   ├── reportGenerator.js   # Report generation API
│   │   ├── reportStorage.js     # Local storage management
│   │   └── tempReportStorage.js # Temporary report storage
│   ├── utils/               # Utility functions
│   │   └── dataTransformers.js  # Data transformation helpers
│   ├── styles/              # Global styles
│   │   ├── globals.css      # Global CSS variables
│   │   └── theme.css        # Theme definitions
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # Application entry point
│   └── index.css            # Base styles
├── public/                  # Static assets
├── index.html               # HTML entry point
├── vite.config.js          # Vite configuration
├── eslint.config.js        # ESLint configuration
└── package.json            # Dependencies and scripts
```

## 🎨 Component Architecture

### Main Components

#### Dashboard (`components/Dashboard/`)
Main analytics view featuring:
- Player search with autocomplete
- File upload for player JSON data
- Word cloud visualization (SHAP features)
- Performance & valuation charts
- Player profile card
- AI report generation

**Key Features:**
- Real-time player search with debouncing
- Drag-and-drop JSON file upload
- Automatic data transformation
- Integration with all visualization components

#### Ask Alexiu (`components/AskAlexiu/`)
Interactive AI chatbot interface:
- Context-aware responses based on loaded reports
- Session management
- Message history
- Markdown rendering for rich responses

**Features:**
- Query routing (report-specific vs. general questions)
- Query rewriting for better context
- Session persistence
- Active report indicator

#### My Reports (`components/MyReports/`)
Report management dashboard:
- Grid view of saved reports
- Report preview and full view
- Delete and export functionality
- Load reports for chatbot analysis

**Features:**
- Local storage persistence
- Report filtering and search
- Batch export (JSON)
- One-click report loading for Alexiu

#### AI Report (`components/AIReport/`)
Comprehensive report viewer:
- Executive summary
- Key statistics
- Player development analysis
- Strengths and weaknesses
- Recommendations
- News context
- Save, export, and share functionality

**Displays:**
- Formatted report sections
- Statistical grids
- Growth trajectory insights
- Recent news integration

#### PlayerInfo (`components/PlayerInfo/`)
Player profile card displaying:
- Player photo with fallback
- Basic information (age, nationality, position, club, preferred foot)
- Growth score (highlighted in green)
- Career statistics (matches, goals, assists)

#### WordCloudChart (`components/WordCloud/`)
SHAP feature importance visualization:
- D3-based word cloud
- Color-coded by sentiment (positive/negative)
- Interactive hover tooltips
- Responsive sizing

**Data Format:**
```javascript
[
  { text: "Feature Name", value: 85, sentiment: "positive" },
  { text: "Another Feature", value: 62, sentiment: "negative" }
]
```

#### PerformanceChart (`components/PerformanceChart/`)
Dual-axis time series chart:
- Performance score over time
- Market valuation over time
- Interactive tooltips
- Responsive design with Recharts

### Sidebar (`components/Sidebar/`)
Navigation component with:
- Dashboard link
- Ask Alexiu link
- My Reports link
- Help & Support
- Branding

## 🔌 Services Layer

### API Services

#### `chatbotService.js`
```javascript
// Send chatbot query
sendChatbotQuery(message, sessionId, userId)

// End chatbot session
endSession()
```

#### `playerSearch.js`
```javascript
// Search players by name
searchPlayers(query, limit)

// Generate player JSON data
generatePlayerJson(playerId)

// Get basic player info
getPlayerInfo(playerId)
```

#### `reportGenerator.js`
```javascript
// Generate comprehensive player report
generatePlayerReport(playerData, playerName, club)

// Check API health
checkAPIHealth()
```

#### `reportStorage.js`
```javascript
// Local storage operations
getAllReports()
saveReport(report)
getReportById(reportId)
deleteReport(reportId)
exportReports()
importReports(jsonString)
```

## 🎨 Styling System

### CSS Variables (`styles/theme.css`)
The application uses CSS custom properties for consistent theming:

```css
--bg-primary: Background colors
--text-primary: Text colors
--accent-primary: Primary accent (buttons, highlights)
--border-color: Border styling
--spacing-*: Spacing scale
--border-radius-*: Border radius scale
--shadow-*: Box shadow variations
```

### Dark Theme
The UI features a modern dark theme optimized for:
- Reduced eye strain
- Professional appearance
- Data visualization clarity

## 📊 Data Flow

### Player Data Pipeline
1. **User Input** → Search or file upload
2. **API Call** → Backend generates/retrieves player JSON
3. **Data Transformation** → `dataTransformers.js` formats data
4. **Component Rendering** → Dashboard displays all visualizations
5. **Report Generation** → LLM analyzes and generates comprehensive report
6. **Storage** → Reports saved to localStorage

### Chatbot Flow
1. **User Query** → Typed in AskAlexiu
2. **Session Check** → Active report context loaded
3. **API Call** → Backend routes and processes query
4. **Response** → Markdown-formatted answer displayed
5. **History** → Conversation persisted in session

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
# API Base URL (default: http://localhost:8000)
VITE_API_BASE_URL=http://localhost:8000
```

### Vite Configuration (`vite.config.js`)
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'  // Optional proxy setup
    }
  }
})
```

## 📦 Dependencies

### Core Libraries
- **React 19.2.0** - UI framework with latest features
- **React DOM 19.2.0** - React rendering

### Data Visualization
- **Recharts 3.4.1** - Responsive chart library
- **D3-cloud 1.2.7** - Word cloud generation
- **D3-scale 4.0.2** - Data scaling utilities

### UI & Utilities
- **Axios 1.13.2** - HTTP client for API calls
- **Lucide React 0.553.0** - Beautiful icon library
- **React Markdown 9.0.1** - Markdown rendering for chatbot

### Development Tools
- **Vite 7.2.2** - Fast build tool and dev server
- **ESLint 9.39.1** - Code linting
- **@vitejs/plugin-react 5.1.0** - React integration for Vite

## 🎯 Key Features

### Real-time Player Search
- Autocomplete with debouncing (300ms)
- Keyboard navigation (arrow keys, enter, escape)
- Click-outside detection to close suggestions
- Visual feedback for selected items

### File Upload
- Drag-and-drop support
- JSON validation
- Automatic data transformation
- Error handling with user feedback

### Report Management
- LocalStorage persistence
- Unique ID generation
- Timestamp tracking
- Batch operations (export all)

### Responsive Design
- Mobile-friendly layouts
- Flexible grid systems
- Adaptive charts and visualizations
- Sidebar collapse on mobile (if implemented)

## 🧪 Development Tips

### Hot Module Replacement (HMR)
Vite provides instant HMR for rapid development:
- Component changes reflect immediately
- Preserves application state
- Fast rebuild times

### Component Development
```javascript
// Use React DevTools for debugging
// Components are functional with hooks

// Example pattern:
const MyComponent = ({ data }) => {
  const [state, setState] = useState(initialValue);
  
  useEffect(() => {
    // Side effects
  }, [dependencies]);
  
  return <div>...</div>;
};
```

### API Integration
```javascript
// Always handle loading and error states
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);

try {
  setIsLoading(true);
  const result = await apiCall();
  if (result.success) {
    // Handle success
  }
} catch (err) {
  setError(err.message);
} finally {
  setIsLoading(false);
}
```

## 🐛 Troubleshooting

### Common Issues

**API Connection Failed**
- Ensure backend is running on port 8000
- Check CORS settings in backend
- Verify `VITE_API_BASE_URL` is correct

**Components Not Rendering**
- Check browser console for errors
- Verify data structure matches expected format
- Ensure all required props are passed

**Build Errors**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`
- Check for version conflicts in package.json

**LocalStorage Full**
- Clear old reports from My Reports
- Check browser storage limits
- Implement pagination or cleanup logic

## 🚢 Deployment

### Production Build
```bash
# Build optimized bundle
npm run build

# Output will be in dist/ directory
# Deploy dist/ to your hosting service
```

### Hosting Options
- **Vercel**: Automatic deployment from Git
- **Netlify**: Simple drag-and-drop or Git integration
- **GitHub Pages**: Free static hosting
- **AWS S3 + CloudFront**: Scalable cloud hosting

### Environment Setup
Ensure production environment variables are set:
```env
VITE_API_BASE_URL=https://your-api-domain.com
```

## 📈 Performance Optimization

- **Code Splitting**: Vite automatically splits code by route
- **Lazy Loading**: Use `React.lazy()` for heavy components
- **Memoization**: Use `useMemo` and `useCallback` for expensive operations
- **Data Sampling**: Time series data is sampled to max 50 points
- **Debouncing**: Search inputs debounced to reduce API calls

## 🔐 Security Considerations

- API keys never exposed in frontend code
- Input validation before API calls
- XSS prevention with React's built-in escaping
- CORS properly configured in backend
- LocalStorage data sanitized before use

## 🤝 Contributing

When contributing to frontend:
1. Follow existing component structure
2. Use functional components with hooks
3. Maintain consistent styling with theme variables
4. Add PropTypes or TypeScript types
5. Update this README for new features

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Recharts Documentation](https://recharts.org/)
- [Axios Documentation](https://axios-http.com/)

---

**Part of the Alexiu Player Analytics Platform**
