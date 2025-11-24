/**
 * Temporary Report Storage Service
 * Stores reports in sessionStorage for the current session
 * These are cleared when the browser tab is closed
 */

const TEMP_REPORTS_KEY = 'alexiu_temp_reports';
const ACTIVE_REPORT_KEY = 'alexiu_active_report_id';

/**
 * Save a report to temporary storage
 * @param {Object} report - The report object to save
 * @param {string} playerName - Player name for identification
 * @returns {string} Report ID
 */
export const saveTempReport = (report, playerName) => {
  try {
    const reports = getTempReports();
    const reportId = `temp_${Date.now()}`;
    
    const tempReport = {
      id: reportId,
      playerName: playerName || 'Unknown Player',
      report: report,
      createdAt: new Date().toISOString()
    };
    
    reports.push(tempReport);
    sessionStorage.setItem(TEMP_REPORTS_KEY, JSON.stringify(reports));
    
    return reportId;
  } catch (error) {
    console.error('Error saving temp report:', error);
    return null;
  }
};

/**
 * Get all temporary reports
 * @returns {Array} Array of temp report objects
 */
export const getTempReports = () => {
  try {
    const reports = sessionStorage.getItem(TEMP_REPORTS_KEY);
    return reports ? JSON.parse(reports) : [];
  } catch (error) {
    console.error('Error reading temp reports:', error);
    return [];
  }
};

/**
 * Get a specific temp report by ID
 * @param {string} reportId - The report ID
 * @returns {Object|null} Report object or null
 */
export const getTempReportById = (reportId) => {
  try {
    const reports = getTempReports();
    const found = reports.find(r => r.id === reportId);
    return found ? found.report : null;
  } catch (error) {
    console.error('Error getting temp report:', error);
    return null;
  }
};

/**
 * Delete a temp report
 * @param {string} reportId - The report ID to delete
 * @returns {boolean} Success status
 */
export const deleteTempReport = (reportId) => {
  try {
    const reports = getTempReports();
    const filtered = reports.filter(r => r.id !== reportId);
    sessionStorage.setItem(TEMP_REPORTS_KEY, JSON.stringify(filtered));
    
    // Clear active report if it was deleted
    if (getActiveReportId() === reportId) {
      clearActiveReport();
    }
    
    return true;
  } catch (error) {
    console.error('Error deleting temp report:', error);
    return false;
  }
};

/**
 * Clear all temp reports
 */
export const clearAllTempReports = () => {
  try {
    sessionStorage.removeItem(TEMP_REPORTS_KEY);
    sessionStorage.removeItem(ACTIVE_REPORT_KEY);
    return true;
  } catch (error) {
    console.error('Error clearing temp reports:', error);
    return false;
  }
};

/**
 * Set the active report for chatbot analysis
 * @param {string} reportId - The report ID to set as active
 */
export const setActiveReport = (reportId) => {
  try {
    sessionStorage.setItem(ACTIVE_REPORT_KEY, reportId);
  } catch (error) {
    console.error('Error setting active report:', error);
  }
};

/**
 * Get the active report ID
 * @returns {string|null} Active report ID or null
 */
export const getActiveReportId = () => {
  try {
    return sessionStorage.getItem(ACTIVE_REPORT_KEY);
  } catch (error) {
    console.error('Error getting active report:', error);
    return null;
  }
};

/**
 * Get the active report object
 * @returns {Object|null} Active report or null
 */
export const getActiveReport = () => {
  const reportId = getActiveReportId();
  return reportId ? getTempReportById(reportId) : null;
};

/**
 * Clear the active report
 */
export const clearActiveReport = () => {
  try {
    sessionStorage.removeItem(ACTIVE_REPORT_KEY);
  } catch (error) {
    console.error('Error clearing active report:', error);
  }
};
