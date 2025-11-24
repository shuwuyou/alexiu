import React from 'react';
import { FileText, Download, Share2, Save, Sparkles, TrendingUp, Award, Target, BarChart3 } from 'lucide-react';
import './AIReport.css';
import { saveReport } from '../../services/reportStorage';

const AIReport = ({ report = null, isLoading = false, rawJsonData = null, shapData = [], timeSeriesData = [], playerInfo = null }) => {
  // Placeholder report data
  const placeholderReport = {
    playerName: 'Sample Player',
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

  // Transform API report to component format
  const getReportData = () => {
    if (!report) return placeholderReport;

    // New schema structure from report_schema.json
    return {
      playerName: report.player_info?.name || 'Unknown Player',
      position: report.player_info?.position,
      age: report.player_info?.age,
      club: report.player_info?.club,
      // Main report sections from new schema
      executiveSummary: report.report?.executive_summary || 'No summary available',
      playerDevelopment: report.report?.player_development || null,
      breakoutAnalysis: report.report?.breakout_analysis || null,
      valuationInsights: report.report?.valuation_insights || null,
      transferFeeAnalysis: report.report?.transfer_fee_analysis || null,
      keyStatistics: report.report?.key_statistics || {},
      strengths: report.report?.strengths || [],
      weaknesses: report.report?.weaknesses || [],
      recommendation: report.report?.recommendation || null,
      newsContext: report.report?.news_context || null,
      news: report.news || [],
      generatedAt: report.generated_at ? new Date(report.generated_at).toLocaleDateString() : new Date().toLocaleDateString()
    };
  };

  const reportData = getReportData();

  const handleExportReport = () => {
    const exportData = report || reportData;
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `player-report-${reportData.playerName || 'unnamed'}-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleShareReport = () => {
    const shareData = {
      title: `Player Report: ${reportData.playerName || 'Player'}`,
      text: `Check out this comprehensive player evaluation for ${reportData.playerName || 'this player'}!\n\nExecutive Summary: ${reportData.executiveSummary?.substring(0, 200)}...`,
      url: window.location.href
    };

    if (navigator.share) {
      navigator.share(shareData)
        .catch((error) => console.log('Error sharing:', error));
    } else {
      // Fallback: copy to clipboard
      const textToCopy = `${shareData.title}\n\n${shareData.text}\n\n${shareData.url}`;
      navigator.clipboard.writeText(textToCopy)
        .then(() => alert('Report link copied to clipboard!'))
        .catch((error) => console.error('Error copying to clipboard:', error));
    }
  };

  const handleSaveReport = () => {
    if (!report || !reportData.playerName || reportData.playerName === 'Sample Player') {
      alert('No valid report to save. Please generate a report first.');
      return;
    }
    
    // Get growth score from rawJsonData if available, otherwise from report
    const growthScore = rawJsonData?.basic_info?.growth_potential_score 
      || report.player_info?.growthScore 
      || report.player_info?.growthPotentialScore;
    
    const saved = saveReport({
      playerName: reportData.playerName,
      summary: reportData.executiveSummary,
      marketValue: reportData.keyStatistics?.current_market_value,
      potentialGrowth: reportData.recommendation?.growth_trajectory,
      growthScore: growthScore,
      growthPotentialScore: growthScore,
      // Include additional sections
      shapData: shapData,
      timeSeriesData: timeSeriesData,
      playerInfo: playerInfo,
      rawJsonData: rawJsonData,
      ...report
    });
    
    if (saved) {
      alert(`Report for ${reportData.playerName} saved successfully!`);
      // Dispatch event to notify chatbot
      window.dispatchEvent(new CustomEvent('reportSaved'));
    } else {
      alert('Failed to save report. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div className="card ai-report-card">
        <div className="card-header ai-report-header">
          <div className="header-left">
            <div className="ai-badge">
              <Sparkles size={16} />
              <span>AI Generated</span>
            </div>
            <h3>Generating Comprehensive Player Evaluation...</h3>
          </div>
        </div>
        <div className="report-content loading-state">
          <div className="loading-spinner"></div>
          <p>Analyzing player data and generating insights...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card ai-report-card">
      <div className="card-header ai-report-header">
        <div className="header-left">
          <div className="ai-badge">
            <Sparkles size={16} />
            <span>AI Generated</span>
          </div>
          <h3>Comprehensive Player Evaluation</h3>
          {reportData.playerName && reportData.playerName !== 'Sample Player' && (
            <p className="player-details">
              {reportData.playerName} • {reportData.position} • Age {reportData.age} • {reportData.club}
            </p>
          )}
          <p className="card-subtitle">Generated on {reportData.generatedAt}</p>
        </div>
        <div className="header-actions">
          <button className="action-btn" onClick={handleSaveReport}>
            <Save size={18} />
            Save
          </button>
          <button className="action-btn" onClick={handleExportReport}>
            <Download size={18} />
            Export
          </button>
          <button className="action-btn" onClick={handleShareReport}>
            <Share2 size={18} />
            Share
          </button>
        </div>
      </div>

      <div className="report-content">
        {/* Executive Summary */}
        <section className="report-section report-summary">
          <div className="section-icon">
            <FileText size={20} />
          </div>
          <div className="section-content">
            <h4>Executive Summary</h4>
            <p>{reportData.executiveSummary}</p>
          </div>
        </section>

        {/* Key Statistics */}
        {reportData.keyStatistics && Object.keys(reportData.keyStatistics).length > 0 && (
          <section className="report-section">
            <div className="section-content">
              <h4><BarChart3 size={18} /> Key Statistics</h4>
              <div className="statistics-grid-compact">
                <div className="stat-item-compact">
                  <span className="stat-label">Current Market Value</span>
                  <span className="stat-value">{reportData.keyStatistics.current_market_value || 'N/A'}</span>
                </div>
                <div className="stat-item-compact">
                  <span className="stat-label">Peak Market Value</span>
                  <span className="stat-value">{reportData.keyStatistics.peak_market_value || 'N/A'}</span>
                </div>
                <div className="stat-item-compact">
                  <span className="stat-label">Career Goals</span>
                  <span className="stat-value">{reportData.keyStatistics.career_goals ?? 'N/A'}</span>
                </div>
                <div className="stat-item-compact">
                  <span className="stat-label">Career Assists</span>
                  <span className="stat-value">{reportData.keyStatistics.career_assists ?? 'N/A'}</span>
                </div>
              </div>
              {reportData.keyStatistics.recent_form && reportData.keyStatistics.recent_form !== 'N/A' && (
                <div className="recent-form-section">
                  <h5>Recent Form</h5>
                  <p className="form-description">{reportData.keyStatistics.recent_form}</p>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Strengths and Weaknesses */}
        <div className="report-grid">
          <section className="report-section">
            <div className="section-content">
              <h4><Award size={18} /> Key Strengths</h4>
              <ul className="strength-list">
                {reportData.strengths.map((strength, index) => (
                  <li key={index}>
                    <span className="bullet success">✓</span>
                    {strength}
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section className="report-section">
            <div className="section-content">
              <h4><Target size={18} /> Areas for Improvement</h4>
              <ul className="weakness-list">
                {reportData.weaknesses.map((weakness, index) => (
                  <li key={index}>
                    <span className="bullet warning">!</span>
                    {weakness}
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </div>

        {/* Player Development */}
        {reportData.playerDevelopment && (
          <section className="report-section">
            <div className="section-content">
              <h4><TrendingUp size={18} /> Player Development Analysis</h4>
              <p className="narrative-text">{reportData.playerDevelopment}</p>
            </div>
          </section>
        )}

        {/* Breakout Analysis */}
        {reportData.breakoutAnalysis && (
          <section className="report-section">
            <div className="section-content">
              <h4><Award size={18} /> Breakout Potential Analysis</h4>
              <p className="narrative-text">{reportData.breakoutAnalysis}</p>
            </div>
          </section>
        )}

        {/* Valuation Insights */}
        {reportData.valuationInsights && (
          <section className="report-section">
            <div className="section-content">
              <h4><TrendingUp size={18} /> Market Valuation Insights</h4>
              <p className="narrative-text">{reportData.valuationInsights}</p>
            </div>
          </section>
        )}

        {/* Transfer Fee Analysis */}
        {reportData.transferFeeAnalysis && (
          <section className="report-section">
            <div className="section-content">
              <h4><BarChart3 size={18} /> Transfer Fee Analysis</h4>
              <p className="narrative-text">{reportData.transferFeeAnalysis}</p>
            </div>
          </section>
        )}

        {/* News Context & Articles */}
        {(reportData.newsContext || (reportData.news && reportData.news.length > 0)) && (
          <section className="report-section">
            <div className="section-content">
              <h4><FileText size={18} /> News & Media Analysis</h4>
              {reportData.newsContext && (
                <p className="narrative-text">{reportData.newsContext}</p>
              )}
              {reportData.news && reportData.news.length > 0 && (
                <div className="news-items">
                  <h5>Recent News:</h5>
                  {reportData.news.map((newsItem, index) => (
                    <div key={index} className="news-item">
                      <strong>{newsItem.title}</strong>
                      <p>{newsItem.summary}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        {/* Recommendation */}
        {reportData.recommendation && (
          <section className="report-section">
            <div className="section-content">
              <h4><Target size={18} /> Recommendation</h4>
              <p className="narrative-text recommendation-text">{reportData.recommendation}</p>
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default AIReport;
