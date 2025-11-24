import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, FileText, X, ChevronDown } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './AskAlexiu.css';
import { 
  sendChatMessage, 
  getUserId, 
  clearSession 
} from '../../services/chatbotService';
import { 
  getAllReports, 
  getReportById
} from '../../services/reportStorage';

const AskAlexiu = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! I'm Alexiu, your AI soccer analytics assistant. Ask me anything about player performance, statistics, or evaluations!",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');
  const [chatMode, setChatMode] = useState('general'); // 'general' or 'report'
  const [hasReport, setHasReport] = useState(false);
  const [availableReports, setAvailableReports] = useState([]);
  const [selectedReportId, setSelectedReportId] = useState(null);
  const messagesEndRef = useRef(null);
  
  const ACTIVE_REPORT_KEY = 'alexiu_active_report_id';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check for report context on mount and updates
  useEffect(() => {
    const reports = getAllReports();
    setAvailableReports(reports);
    
    const activeId = localStorage.getItem(ACTIVE_REPORT_KEY);
    if (activeId && reports.find(r => r.id === activeId)) {
      setSelectedReportId(activeId);
      setChatMode('report');
      setHasReport(true);
    }
  }, []);

  // Listen for report updates
  useEffect(() => {
    const handleReportUpdate = () => {
      const reports = getAllReports();
      setAvailableReports(reports);
      
      const activeId = localStorage.getItem(ACTIVE_REPORT_KEY);
      if (activeId && reports.find(r => r.id === activeId)) {
        setSelectedReportId(activeId);
        setChatMode('report');
        setHasReport(true);
      }
    };
    
    window.addEventListener('reportUpdated', handleReportUpdate);
    window.addEventListener('reportSaved', handleReportUpdate);
    return () => {
      window.removeEventListener('reportUpdated', handleReportUpdate);
      window.removeEventListener('reportSaved', handleReportUpdate);
    };
  }, []);

  const handleClearSession = () => {
    clearSession();
    setMessages([
      {
        id: Date.now(),
        type: 'bot',
        text: "Session cleared! Starting fresh. How can I help you?",
        timestamp: new Date()
      }
    ]);
    setChatMode('general');
    setSelectedReportId(null);
    localStorage.removeItem(ACTIVE_REPORT_KEY);
    setHasReport(false);
  };

  const handleModeChange = (newMode) => {
    if (newMode === 'general') {
      setChatMode('general');
      setSelectedReportId(null);
      localStorage.removeItem(ACTIVE_REPORT_KEY);
      setHasReport(false);
    } else if (newMode === 'report' && availableReports.length > 0) {
      setChatMode('report');
      const firstReport = availableReports[0];
      setSelectedReportId(firstReport.id);
      localStorage.setItem(ACTIVE_REPORT_KEY, firstReport.id);
      setHasReport(true);
    }
  };

  const handleReportSelection = (reportId) => {
    setSelectedReportId(reportId);
    localStorage.setItem(ACTIVE_REPORT_KEY, reportId);
    setChatMode('report');
    setHasReport(true);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return;

    const userId = getUserId();

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);
    setCurrentResponse('');

    // Create a temporary bot message that will be updated with streaming response
    const botMessageId = Date.now() + 1;

    try {
      let fullText = '';
      
      // Get the report if in report mode
      const reportData = chatMode === 'report' && selectedReportId 
        ? getReportById(selectedReportId) 
        : null;
      
      // Extract the actual report object (reportStorage wraps it)
      const report = reportData ? reportData : null;
      
      // Send message with streaming support
      await sendChatMessage(inputMessage, userId, {
        mode: chatMode,
        report: report,
        onChunk: (chunk) => {
          fullText += chunk;
          
          // Update or create the bot message with each chunk
          setMessages(prev => {
            const existing = prev.find(m => m.id === botMessageId);
            if (existing) {
              return prev.map(m => 
                m.id === botMessageId 
                  ? { ...m, text: fullText }
                  : m
              );
            } else {
              // Create the message on first chunk and hide typing indicator
              setIsTyping(false);
              return [...prev, {
                id: botMessageId,
                type: 'bot',
                text: fullText,
                timestamp: new Date()
              }];
            }
          });
        },
        onComplete: (fullResponse) => {
          setIsTyping(false);
          setCurrentResponse('');
        },
        onError: (error) => {
          setIsTyping(false);
          setCurrentResponse('');
          // Add error message
          setMessages(prev => {
            const existing = prev.find(m => m.id === botMessageId);
            if (existing) {
              return prev.map(m => 
                m.id === botMessageId 
                  ? { ...m, text: `Sorry, I encountered an error: ${error}. Please try again.` }
                  : m
              );
            } else {
              return [...prev, {
                id: botMessageId,
                type: 'bot',
                text: `Sorry, I encountered an error: ${error}. Please try again.`,
                timestamp: new Date()
              }];
            }
          });
        }
      });
    } catch (error) {
      console.error('Error in chat:', error);
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="ask-alexiu">
      <div className="chat-header">
        <div className="header-content">
          <div className="ai-avatar">
            <Bot size={24} />
          </div>
          <div>
            <h1>Ask Alexiu</h1>
            <p className="subtitle">AI-powered soccer analytics assistant</p>
          </div>
        </div>
        <div className="header-actions">
          {hasReport && chatMode === 'report' && (
            <div className="report-indicator" title="Report analysis mode active">
              <FileText size={16} />
              <span>Report Mode</span>
            </div>
          )}
          <div className="status-badge">
            <span className="status-dot"></span>
            Online
          </div>
          {messages.length > 1 && (
            <button 
              className="clear-session-btn" 
              onClick={handleClearSession}
              title="Clear conversation and start fresh"
            >
              <X size={16} />
              Clear
            </button>
          )}
        </div>
      </div>

      <div className="chat-mode-selector">
        <div className="mode-tabs">
          <button 
            className={`mode-tab ${chatMode === 'general' ? 'active' : ''}`}
            onClick={() => handleModeChange('general')}
          >
            <Bot size={18} />
            General Chat
          </button>
          <button 
            className={`mode-tab ${chatMode === 'report' ? 'active' : ''}`}
            onClick={() => handleModeChange('report')}
            disabled={availableReports.length === 0}
            title={availableReports.length === 0 ? 'No reports available. Generate a report first.' : 'Analyze saved reports'}
          >
            <FileText size={18} />
            Report Analysis
          </button>
        </div>
        
        {chatMode === 'report' && availableReports.length > 0 && (
          <div className="report-selector">
            <label htmlFor="report-select">Select Report:</label>
            <select 
              id="report-select"
              value={selectedReportId || ''}
              onChange={(e) => handleReportSelection(e.target.value)}
              className="report-select-dropdown"
            >
              {availableReports.map(report => (
                <option key={report.id} value={report.id}>
                  {report.playerName || report.player_info?.name || 'Unknown Player'} - {new Date(report.createdAt).toLocaleString()}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-avatar">
                {message.type === 'bot' ? (
                  <div className="bot-avatar">
                    <Sparkles size={16} />
                  </div>
                ) : (
                  <div className="user-avatar">
                    <User size={16} />
                  </div>
                )}
              </div>
              <div className="message-content">
                <div className="message-text">
                  {message.type === 'bot' ? (
                    <ReactMarkdown>{message.text}</ReactMarkdown>
                  ) : (
                    message.text
                  )}
                </div>
                <div className="message-time">{formatTime(message.timestamp)}</div>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="typing-indicator-container">
              <div className="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <textarea
              className="chat-input"
              placeholder="Ask me anything about player analytics..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              rows="1"
            />
            <button 
              className="send-button"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping}
            >
              <Send size={20} />
            </button>
          </div>
          <div className="chat-hint">
            <span>💡 Tip: Ask about player comparisons, performance trends, or evaluation metrics</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AskAlexiu;
