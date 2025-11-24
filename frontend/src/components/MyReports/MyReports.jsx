import React, { useState, useEffect } from 'react';
import { FileText, Trash2, Download, Calendar, Eye, X } from 'lucide-react';
import { getAllReports, deleteReport, exportReports } from '../../services/reportStorage';
import { endSession } from '../../services/chatbotService';
import AIReport from '../AIReport/AIReport';
import WordCloudChart from '../WordCloud/WordCloudChart';
import PerformanceValuationChart from '../PerformanceChart/PerformanceValuationChart';
import PlayerInfo from '../PlayerInfo/PlayerInfo';
import './MyReports.css';

const MyReports = () => {
  const [reports, setReports] = useState([]);
  const [viewingReport, setViewingReport] = useState(null);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = () => {
    const savedReports = getAllReports();
    setReports(savedReports);
  };

  const handleDelete = (reportId) => {
    if (window.confirm('Are you sure you want to delete this report?')) {
      deleteReport(reportId);
      loadReports();
    }
  };

  const handleLoadReport = (report) => {
    // End current chatbot session and set active report
    endSession();
    localStorage.setItem('alexiu_active_report_id', report.id);
    
    // Dispatch custom event to notify other components
    window.dispatchEvent(new CustomEvent('reportUpdated'));
    
    // Show notification to user
    alert(`Report loaded! You can now ask Alexiu questions about ${report.playerName || 'this player'} in the "Ask Alexiu" section.`);
  };

  const handleViewReport = (report) => {
    setViewingReport(report);
  };

  const handleCloseReport = () => {
    setViewingReport(null);
  };

  const handleExportAll = () => {
    const jsonData = exportReports();
    const dataBlob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `all-reports-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="my-reports">
      {viewingReport ? (
        <div className="report-view-container">
          <div className="report-view-header">
            <button className="close-report-btn" onClick={handleCloseReport}>
              <X size={20} />
              Back to My Reports
            </button>
          </div>
          <div className="dashboard-content">
            <PlayerInfo playerInfo={viewingReport.playerInfo} />
            
            <WordCloudChart 
              data={viewingReport.shapData || []} 
              title="SHAP Feature Importance"
              subtitle="Transfer fee prediction factors"
            />

            <PerformanceValuationChart data={viewingReport.timeSeriesData || []} />

            <AIReport 
              report={viewingReport} 
              rawJsonData={viewingReport.rawJsonData}
              shapData={viewingReport.shapData || []}
              timeSeriesData={viewingReport.timeSeriesData || []}
              playerInfo={viewingReport.playerInfo}
            />
          </div>
        </div>
      ) : (
        <>
          <div className="reports-header">
            <div>
              <h1>My Reports</h1>
              <p className="subtitle">View and manage your saved player evaluations</p>
            </div>
            {reports.length > 0 && (
              <button className="export-all-btn" onClick={handleExportAll}>
                <Download size={18} />
                Export All
              </button>
            )}
          </div>

      {reports.length === 0 ? (
        <div className="empty-state">
          <FileText size={64} className="empty-icon" />
          <h3>No saved reports yet</h3>
          <p>Reports you save will appear here for easy access</p>
        </div>
      ) : (
        <div className="reports-grid">
          {reports.map((report) => (
            <div key={report.id} className="report-card" onClick={() => handleViewReport(report)}>
              <div className="report-card-header">
                <div className="report-info">
                  <h3>{report.playerName || 'Unnamed Player'}</h3>
                  <div className="report-meta">
                    <Calendar size={14} />
                    <span>{formatDate(report.createdAt)}</span>
                  </div>
                </div>
                <div className="report-actions" onClick={(e) => e.stopPropagation()}>
                  <button 
                    className="load-report-btn"
                    onClick={() => handleLoadReport(report)}
                    title="Load report for chatbot analysis"
                  >
                    <Eye size={18} />
                  </button>
                  <button 
                    className="delete-btn"
                    onClick={() => handleDelete(report.id)}
                    title="Delete report"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
              
              <div className="report-preview">
                <p>{report.summary?.substring(0, 150)}...</p>
              </div>

              <div className="report-stats">
                <div className="stat">
                  <span className="stat-label">Market Value</span>
                  <span className="stat-value">{report.marketValue || 'N/A'}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Growth Score</span>
                  <span className="stat-value growth-score">{report.growthScore || report.growthPotentialScore ? (report.growthScore || report.growthPotentialScore).toFixed(2) : 'N/A'}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      </>
      )}
    </div>
  );
};

export default MyReports;
