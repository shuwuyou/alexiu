/**
 * Chatbot Service for Ask Alexiu
 * Handles communication with the chatbot API backend
 */

// API base URL - adjust this to your backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Session storage keys
const SESSION_ID_KEY = 'alexiu_session_id';
const CURRENT_REPORT_KEY = 'alexiu_current_report';

/**
 * Get or create a session ID for the chatbot
 * @param {string} userId - User identifier (can be generated client-side)
 * @returns {string} Session ID
 */
export const getOrCreateSessionId = () => {
  let sessionId = sessionStorage.getItem(SESSION_ID_KEY);
  if (!sessionId) {
    // Generate a new client-side session ID (UUID v4)
    sessionId = crypto.randomUUID();
    sessionStorage.setItem(SESSION_ID_KEY, sessionId);
  }
  return sessionId;
};

/**
 * Clear the current session (starts a fresh conversation)
 */
export const clearSession = () => {
  sessionStorage.removeItem(SESSION_ID_KEY);
  sessionStorage.removeItem(CURRENT_REPORT_KEY);
};

/**
 * Store the current report for the chatbot to reference
 * @param {Object} report - The generated player report
 */
export const setCurrentReport = (report) => {
  if (report) {
    sessionStorage.setItem(CURRENT_REPORT_KEY, JSON.stringify(report));
  } else {
    sessionStorage.removeItem(CURRENT_REPORT_KEY);
  }
};

/**
 * Get the current report from storage
 * @returns {Object|null} Current report or null
 */
export const getCurrentReport = () => {
  const reportStr = sessionStorage.getItem(CURRENT_REPORT_KEY);
  return reportStr ? JSON.parse(reportStr) : null;
};

/**
 * Send a message to the chatbot with streaming response
 * @param {string} message - User's message
 * @param {string} userId - User identifier
 * @param {Object} options - Optional parameters
 * @param {string} options.mode - Chat mode: 'general' or 'report' (defaults to 'general')
 * @param {Object} options.report - Player report data for report-specific queries
 * @param {Object} options.playerData - Original player statistics
 * @param {Function} options.onChunk - Callback for each streamed chunk
 * @param {Function} options.onComplete - Callback when streaming completes
 * @param {Function} options.onError - Callback for errors
 * @returns {Promise<string>} Complete response text
 */
export const sendChatMessage = async (message, userId, options = {}) => {
  const { mode = 'general', report, playerData, onChunk, onComplete, onError } = options;
  
  try {
    const sessionId = getOrCreateSessionId();
    
    // Determine which endpoint to use based on explicit mode
    const endpoint = mode === 'report'
      ? `${API_BASE_URL}/api/chatbot/report-chat`
      : `${API_BASE_URL}/api/chatbot/chat`;
    
    // Build request body
    const requestBody = {
      user_id: userId,
      message: message,
      session_id: sessionId
    };
    
    // Add report data if in report mode
    if (mode === 'report' && report) {
      requestBody.report = report;
    }
    
    // Add player data if provided
    if (playerData) {
      requestBody.player_data = playerData;
    }
    
    // Make streaming request
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // Update session ID from response headers if provided
    const newSessionId = response.headers.get('X-Session-ID');
    if (newSessionId) {
      sessionStorage.setItem(SESSION_ID_KEY, newSessionId);
    }
    
    // Process streaming response
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullResponse = '';
    
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        break;
      }
      
      const chunk = decoder.decode(value, { stream: true });
      fullResponse += chunk;
      
      // Call onChunk callback if provided
      if (onChunk) {
        onChunk(chunk);
      }
    }
    
    // Call onComplete callback if provided
    if (onComplete) {
      onComplete(fullResponse);
    }
    
    return fullResponse;
    
  } catch (error) {
    console.error('Error sending chat message:', error);
    
    const errorMessage = error.message || 'Failed to send message';
    
    // Call onError callback if provided
    if (onError) {
      onError(errorMessage);
    }
    
    throw error;
  }
};

/**
 * End the current chatbot session
 * This should be called when a new report is generated
 */
export const endSession = () => {
  clearSession();
};

/**
 * Check if there's an active report context
 * @returns {boolean} True if there's a report available
 */
export const hasReportContext = () => {
  return getCurrentReport() !== null;
};

/**
 * Get a simple user ID (can be enhanced with actual auth later)
 * @returns {string} User ID
 */
export const getUserId = () => {
  let userId = localStorage.getItem('alexiu_user_id');
  if (!userId) {
    userId = `user_${crypto.randomUUID()}`;
    localStorage.setItem('alexiu_user_id', userId);
  }
  return userId;
};
