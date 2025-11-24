import React from 'react';
import './PlayerInfo.css';

const PlayerInfo = ({ playerInfo }) => {
  if (!playerInfo) return null;

  const formatCurrency = (value) => {
    if (!value) return 'N/A';
    if (value >= 1000000) {
      return `€${(value / 1000000).toFixed(1)}M`;
    }
    return `€${(value / 1000).toFixed(0)}K`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <div className="card player-info-card">
      <div className="player-info-container">
        <div className="player-image-section">
          {playerInfo.imageUrl ? (
            <img 
              src={playerInfo.imageUrl} 
              alt={playerInfo.name} 
              className="player-image"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
          ) : null}
          <div className="player-image-placeholder" style={{ display: playerInfo.imageUrl ? 'none' : 'flex' }}>
            <span className="placeholder-text">{playerInfo.name?.charAt(0) || '?'}</span>
          </div>
        </div>

        <div className="player-details-section">
          <h2 className="player-name">{playerInfo.name}</h2>
          
          <div className="player-basic-info">
            <div className="info-row">
              <div className="info-item">
                <span className="info-label">Age</span>
                <span className="info-value">{playerInfo.age || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Date of Birth</span>
                <span className="info-value">{formatDate(playerInfo.dateOfBirth)}</span>
              </div>
            </div>

            <div className="info-row">
              <div className="info-item">
                <span className="info-label">Country</span>
                <span className="info-value">{playerInfo.nationality || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Position</span>
                <span className="info-value">{playerInfo.position || 'N/A'}</span>
              </div>
            </div>

            <div className="info-row">
              <div className="info-item">
                <span className="info-label">Height</span>
                <span className="info-value">{playerInfo.height ? `${playerInfo.height} cm` : 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Preferred Foot</span>
                <span className="info-value">{playerInfo.preferredFoot || playerInfo.foot || 'N/A'}</span>
              </div>
            </div>

            <div className="info-row">
              <div className="info-item">
                <span className="info-label">Club</span>
                <span className="info-value">{playerInfo.club || playerInfo.currentClub || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Growth Score</span>
                <span className="info-value growth-score">{playerInfo.growthScore || playerInfo.growthPotentialScore ? (playerInfo.growthScore || playerInfo.growthPotentialScore).toFixed(2) : 'N/A'}</span>
              </div>
            </div>

            {playerInfo.predictedTransferFee && (
              <div className="transfer-fee-section">
                <h4 className="transfer-title">Latest Transfer Information</h4>
                <div className="info-row">
                  <div className="info-item">
                    <span className="info-label">From Club</span>
                    <span className="info-value">{playerInfo.transferFromClub || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">To Club</span>
                    <span className="info-value">{playerInfo.transferToClub || 'N/A'}</span>
                  </div>
                </div>
                <div className="info-row">
                  <div className="info-item">
                    <span className="info-label">Transfer Season</span>
                    <span className="info-value">{playerInfo.transferSeason || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Transfer Date</span>
                    <span className="info-value">{formatDate(playerInfo.transferDate)}</span>
                  </div>
                </div>
                <div className="info-row">
                  <div className="info-item">
                    <span className="info-label">Predicted Transfer Fee</span>
                    <span className="info-value transfer-fee">{formatCurrency(playerInfo.predictedTransferFee)}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Actual Transfer Fee</span>
                    <span className="info-value transfer-fee">{formatCurrency(playerInfo.actualTransferFee)}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="career-stats-section">
          <h3 className="section-title">Career Stats</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Matches</span>
              <span className="stat-value">{playerInfo.careerMatches || '0'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Goals</span>
              <span className="stat-value">{playerInfo.careerGoals || '0'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Assists</span>
              <span className="stat-value">{playerInfo.careerAssists || '0'}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlayerInfo;
