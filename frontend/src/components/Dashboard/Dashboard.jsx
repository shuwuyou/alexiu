import React, { useState, useEffect, useRef } from 'react';
import { Search, Target, Upload, Save } from 'lucide-react';
import WordCloudChart from '../WordCloud/WordCloudChart';
import PerformanceValuationChart from '../PerformanceChart/PerformanceValuationChart';
import AIReport from '../AIReport/AIReport';
import PlayerInfo from '../PlayerInfo/PlayerInfo';
import { generatePlayerReport } from '../../services/reportGenerator';
import { searchPlayers, generatePlayerJson } from '../../services/playerSearch';
import { endSession } from '../../services/chatbotService';
import { saveReport } from '../../services/reportStorage';
import { 
  transformToReportFormat, 
  extractShapValues, 
  extractTimeSeriesData,
  getPlayerBasicInfo 
} from '../../utils/dataTransformers';
import './Dashboard.css';

const Dashboard = () => {
  const [playerInput, setPlayerInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedReport, setGeneratedReport] = useState(null);
  const [error, setError] = useState(null);
  const [playerData, setPlayerData] = useState(null);
  const [rawJsonData, setRawJsonData] = useState(null); // Store original JSON generator format
  const [shapData, setShapData] = useState([]);
  const [timeSeriesData, setTimeSeriesData] = useState([]);
  const [playerInfo, setPlayerInfo] = useState(null);
  
  // Autocomplete states
  const [searchSuggestions, setSearchSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState(-1);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const searchTimeoutRef = useRef(null);
  const suggestionsRef = useRef(null);

  // Handle input change with debounced search
  useEffect(() => {
    if (playerInput.length >= 2) {
      // Clear previous timeout
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }

      // Set new timeout for search
      searchTimeoutRef.current = setTimeout(async () => {
        const result = await searchPlayers(playerInput, 10);
        if (result.success) {
          setSearchSuggestions(result.players);
          setShowSuggestions(true);
        }
      }, 300); // 300ms debounce
    } else {
      setSearchSuggestions([]);
      setShowSuggestions(false);
    }

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [playerInput]);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelectSuggestion = (player) => {
    setPlayerInput(player.name);
    setSelectedPlayer(player);
    setShowSuggestions(false);
    setSearchSuggestions([]);
    setSelectedSuggestionIndex(-1);
  };

  const handleKeyDown = (e) => {
    if (!showSuggestions || searchSuggestions.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedSuggestionIndex((prev) =>
        prev < searchSuggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedSuggestionIndex((prev) => (prev > 0 ? prev - 1 : -1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedSuggestionIndex >= 0) {
        handleSelectSuggestion(searchSuggestions[selectedSuggestionIndex]);
      } else {
        handleSearch();
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  const handleSearch = async () => {
    if (!playerInput.trim()) {
      setError('Please enter a player name or ID');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      let playerId = selectedPlayer?.player_id;

      // If no player selected, try to search
      if (!playerId) {
        const searchResult = await searchPlayers(playerInput, 1);
        if (!searchResult.success || searchResult.players.length === 0) {
          setError('Player not found. Please try a different name or ID.');
          setIsLoading(false);
          return;
        }
        playerId = searchResult.players[0].player_id;
        setSelectedPlayer(searchResult.players[0]);
      }

      // Generate player JSON using json_generator pipeline
      const jsonResult = await generatePlayerJson(playerId);
      
      if (!jsonResult.success) {
        setError(jsonResult.error);
        setIsLoading(false);
        return;
      }

      const jsonData = jsonResult.data;

      // Store raw JSON generator data
      setRawJsonData(jsonData);

      // Transform to report format
      const transformedData = transformToReportFormat(jsonData);
      setPlayerData(transformedData);

      // Extract SHAP data for word cloud
      const shap = extractShapValues(jsonData);
      setShapData(shap);

      // Extract time series data for performance chart
      const timeSeries = extractTimeSeriesData(jsonData);
      setTimeSeriesData(timeSeries);

      // Get player basic info
      const playerBasicInfo = getPlayerBasicInfo(jsonData);
      setPlayerInfo(playerBasicInfo);
      setPlayerInput(playerBasicInfo.name);

      setError(null);
    } catch (err) {
      setError('Unexpected error occurred while analyzing player');
      console.error('Player analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!playerData) {
      setError('Please upload player data first');
      return;
    }

    setIsLoading(true);
    setError(null);
    setGeneratedReport(null);

    try {
      // Use raw JSON data if available (from file upload), otherwise use playerData
      const dataToSend = rawJsonData || playerData;
      
      const result = await generatePlayerReport(
        dataToSend,
        dataToSend.basic_info?.name || dataToSend.player_info?.name,
        dataToSend.basic_info?.current_club_name || dataToSend.player_info?.club
      );

      if (result.success) {
        setGeneratedReport(result.report);
        setError(null);
        
        // End chatbot session
        endSession();
        
        // Dispatch custom event to notify other components
        window.dispatchEvent(new CustomEvent('reportUpdated'));
      } else {
        setError(result.error);
        setGeneratedReport(null);
      }
    } catch (err) {
      setError('Unexpected error occurred while generating report');
      console.error('Report generation error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const jsonData = JSON.parse(e.target.result);
          
          // Check if this is JSON generator format (has basic_info) or report format (has player_info)
          const isJsonGeneratorFormat = jsonData.basic_info !== undefined;
          
          if (isJsonGeneratorFormat) {
            // Store raw JSON generator data
            setRawJsonData(jsonData);
            
            // Transform to report format
            const transformedData = transformToReportFormat(jsonData);
            setPlayerData(transformedData);
            
            // Extract SHAP data for word cloud
            const shap = extractShapValues(jsonData);
            setShapData(shap);
            
            // Extract time series data for performance chart
            const timeSeries = extractTimeSeriesData(jsonData);
            setTimeSeriesData(timeSeries);
            
            // Get player basic info
            const playerBasicInfo = getPlayerBasicInfo(jsonData);
            setPlayerInfo(playerBasicInfo);
            setPlayerInput(playerBasicInfo.name);
          } else {
            // Assume it's already in report format
            setPlayerData(jsonData);
            setPlayerInput(jsonData.player_info?.name || 'Uploaded Player');
            setShapData([]);
            setTimeSeriesData([]);
          }
          
          setError(null);
          setGeneratedReport(null);
        } catch (err) {
          setError('Invalid JSON file format');
          console.error('JSON parse error:', err);
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="welcome-section">
          <h1>Player Performance Analytics</h1>
          <p className="subtitle">Comprehensive evaluation and insights</p>
        </div>

        <div className="search-section">
          <div className="search-bar" ref={suggestionsRef}>
            <Search size={20} />
            <input
              type="text"
              placeholder="Search player by name or ID..."
              value={playerInput}
              onChange={(e) => {
                setPlayerInput(e.target.value);
                setSelectedPlayer(null); // Clear selection when typing
              }}
              onKeyDown={handleKeyDown}
              onFocus={() => searchSuggestions.length > 0 && setShowSuggestions(true)}
            />
            <button 
              className="search-btn" 
              onClick={handleSearch}
              disabled={isLoading}
            >
              <Target size={18} />
              {isLoading ? 'Analyzing...' : 'Analyze'}
            </button>
            
            {/* Autocomplete Suggestions */}
            {showSuggestions && searchSuggestions.length > 0 && (
              <div className="search-suggestions">
                {searchSuggestions.map((player, index) => (
                  <div
                    key={player.player_id}
                    className={`suggestion-item ${index === selectedSuggestionIndex ? 'selected' : ''}`}
                    onClick={() => handleSelectSuggestion(player)}
                    onMouseEnter={() => setSelectedSuggestionIndex(index)}
                  >
                    <div className="suggestion-main">
                      <span className="suggestion-name">{player.name}</span>
                      <span className="suggestion-id">#{player.player_id}</span>
                    </div>
                    <div className="suggestion-details">
                      <span>{player.position}</span>
                      {player.current_club_name && (
                        <>
                          <span className="separator">•</span>
                          <span>{player.current_club_name}</span>
                        </>
                      )}
                      {player.nationality && (
                        <>
                          <span className="separator">•</span>
                          <span>{player.nationality}</span>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="report-controls">
            <input
              type="file"
              id="player-data-upload"
              accept=".json"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            <label htmlFor="player-data-upload" className="upload-btn">
              <Upload size={18} />
              Upload Player Data (JSON)
            </label>

            <button 
              className="generate-btn"
              onClick={handleGenerateReport}
              disabled={isLoading || !playerData}
            >
              {isLoading ? 'Generating...' : 'Generate AI Report'}
            </button>
          </div>

          {error && (
            <div className="error-message">
              <span>⚠️ {error}</span>
            </div>
          )}

          {playerData && !error && (
            <div className="success-message">
              <span>✓ Player data loaded: {playerData.player_info?.name || 'Unknown'}</span>
            </div>
          )}
        </div>
      </div>

      <div className="dashboard-content">
        <PlayerInfo playerInfo={playerInfo} />
        
        <WordCloudChart 
          data={shapData} 
          title="Factors affecting Transfer Fee"
          subtitle="Transfer fee prediction factors"
        />

        <PerformanceValuationChart data={timeSeriesData} />

        <AIReport 
          report={generatedReport} 
          isLoading={isLoading} 
          rawJsonData={rawJsonData}
          shapData={shapData}
          timeSeriesData={timeSeriesData}
          playerInfo={playerInfo}
        />
      </div>
    </div>
  );
};

export default Dashboard;
