// Local Storage Service for Player Reports
// Stores player evaluation reports in browser's localStorage

const REPORTS_KEY = 'alexiu_player_reports';

/**
 * Get all saved reports from localStorage
 * @returns {Array} Array of report objects
 */
export const getAllReports = () => {
  try {
    const reports = localStorage.getItem(REPORTS_KEY);
    return reports ? JSON.parse(reports) : [];
  } catch (error) {
    console.error('Error reading reports from localStorage:', error);
    return [];
  }
};

/**
 * Save a new report to localStorage
 * @param {Object} report - Report object to save
 * @returns {boolean} Success status
 */
export const saveReport = (report) => {
  try {
    const reports = getAllReports();
    const newReport = {
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
      ...report
    };
    reports.unshift(newReport); // Add to beginning
    localStorage.setItem(REPORTS_KEY, JSON.stringify(reports));
    return true;
  } catch (error) {
    console.error('Error saving report to localStorage:', error);
    return false;
  }
};

/**
 * Get a specific report by ID
 * @param {string} reportId - The report ID
 * @returns {Object|null} Report object or null if not found
 */
export const getReportById = (reportId) => {
  try {
    const reports = getAllReports();
    return reports.find(report => report.id === reportId) || null;
  } catch (error) {
    console.error('Error fetching report:', error);
    return null;
  }
};

/**
 * Delete a report by ID
 * @param {string} reportId - The report ID to delete
 * @returns {boolean} Success status
 */
export const deleteReport = (reportId) => {
  try {
    const reports = getAllReports();
    const filteredReports = reports.filter(report => report.id !== reportId);
    localStorage.setItem(REPORTS_KEY, JSON.stringify(filteredReports));
    return true;
  } catch (error) {
    console.error('Error deleting report:', error);
    return false;
  }
};

/**
 * Clear all reports from localStorage
 * @returns {boolean} Success status
 */
export const clearAllReports = () => {
  try {
    localStorage.removeItem(REPORTS_KEY);
    return true;
  } catch (error) {
    console.error('Error clearing reports:', error);
    return false;
  }
};

/**
 * Export reports as JSON file
 * @returns {string} JSON string of all reports
 */
export const exportReports = () => {
  const reports = getAllReports();
  return JSON.stringify(reports, null, 2);
};

/**
 * Import reports from JSON string
 * @param {string} jsonString - JSON string of reports
 * @returns {boolean} Success status
 */
export const importReports = (jsonString) => {
  try {
    const importedReports = JSON.parse(jsonString);
    if (!Array.isArray(importedReports)) {
      throw new Error('Invalid format: expected an array');
    }
    localStorage.setItem(REPORTS_KEY, JSON.stringify(importedReports));
    return true;
  } catch (error) {
    console.error('Error importing reports:', error);
    return false;
  }
};
