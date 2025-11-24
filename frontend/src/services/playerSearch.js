/**
 * Service for player search and JSON generation
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Search for players by name or ID
 * @param {string} query - Search query (player name or ID)
 * @param {number} limit - Maximum number of results (default: 10)
 * @returns {Promise<Object>} Search results
 */
export const searchPlayers = async (query, limit = 10) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/players/search`, {
      params: { query, limit },
      timeout: 10000,
    });

    return {
      success: true,
      players: response.data,
      count: response.data.length,
    };
  } catch (error) {
    console.error('Player search error:', error);
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Failed to search players',
      players: [],
      count: 0,
    };
  }
};

/**
 * Generate complete player JSON data (json_generator pipeline)
 * @param {number} playerId - Player ID
 * @returns {Promise<Object>} Generated JSON data
 */
export const generatePlayerJson = async (playerId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/players/generate/${playerId}`, {
      timeout: 30000, // 30 seconds for data generation
    });

    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Player JSON generation error:', error);
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Failed to generate player data',
      data: null,
    };
  }
};

/**
 * Get basic player information
 * @param {number} playerId - Player ID
 * @returns {Promise<Object>} Player info
 */
export const getPlayerInfo = async (playerId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/players/info/${playerId}`, {
      timeout: 5000,
    });

    return {
      success: true,
      player: response.data,
    };
  } catch (error) {
    console.error('Get player info error:', error);
    return {
      success: false,
      error: error.response?.data?.detail || error.message || 'Failed to get player info',
      player: null,
    };
  }
};
