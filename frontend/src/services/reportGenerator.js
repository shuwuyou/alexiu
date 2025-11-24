import axios from 'axios';

// API base URL - adjust this to your backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Generate a comprehensive player report using the backend API
 * @param {Object} playerData - Player statistics and ML predictions
 * @param {string} playerName - Optional player name (extracted from playerData if not provided)
 * @param {string} club - Optional club name (extracted from playerData if not provided)
 * @returns {Promise<Object>} Generated report data
 */
export const generatePlayerReport = async (playerData, playerName = null, club = null) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/reports/generate`, {
      player_data: playerData,
      player_name: playerName,
      club: club
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 180000 // 180 second timeout for report generation
    });

    if (response.data.success) {
      return {
        success: true,
        report: response.data.report
      };
    } else {
      return {
        success: false,
        error: response.data.message || 'Failed to generate report'
      };
    }
  } catch (error) {
    console.error('Error generating player report:', error);
    
    let errorMessage = 'Failed to generate report';
    
    if (error.response) {
      // Server responded with error status
      errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage;
    } else if (error.request) {
      // Request made but no response
      errorMessage = 'No response from server. Please ensure the backend is running.';
    } else {
      // Other errors
      errorMessage = error.message;
    }
    
    return {
      success: false,
      error: errorMessage
    };
  }
};

/**
 * Check if the backend API is healthy and reachable
 * @returns {Promise<boolean>} True if API is healthy
 */
export const checkAPIHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, {
      timeout: 5000
    });
    return response.data?.status === 'healthy';
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};
