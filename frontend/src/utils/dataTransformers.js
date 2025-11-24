/**
 * Transform JSON generator output to report generator format
 * @param {Object} jsonData - The full JSON output from the generator
 * @returns {Object} - Transformed data for report generator
 */
export const transformToReportFormat = (jsonData) => {
  const basicInfo = jsonData.basic_info || {};
  const careerTotals = jsonData.career_totals || {};
  const recentForm = jsonData.recent_form_last_10_games?.summary || {};
  const timeSeries = jsonData.performance_time_series || [];
  
  // Calculate latest performance score from time series
  const latestPerformance = timeSeries.length > 0 
    ? timeSeries[timeSeries.length - 1] 
    : {};

  return {
    player_info: {
      id: String(basicInfo.player_id || ''),
      name: basicInfo.name || 'Unknown Player',
      position: basicInfo.primary_position || 'Unknown',
      age: basicInfo.age_at_reference_date || 0,
      club: basicInfo.current_club_name || 'Unknown Club',
      nationality: basicInfo.nationality || 'Unknown',
      preferredFoot: basicInfo.preferred_foot,
      growthScore: basicInfo.growth_potential_score,
      growthPotentialScore: basicInfo.growth_potential_score
    },
    statistics: {
      matches_played: careerTotals.matches_played || 0,
      goals: careerTotals.goals || 0,
      assists: careerTotals.assists || 0,
      goals_per_match: careerTotals.goals_per_90 || 0,
      assists_per_match: careerTotals.assists_per_90 || 0,
      shots_per_match: 0, // Not available in JSON
      shot_accuracy: 0, // Not available in JSON
      pass_completion_rate: 0, // Not available in JSON
      key_passes_per_match: 0, // Not available in JSON
      dribbles_per_match: 0, // Not available in JSON
      dribble_success_rate: 0, // Not available in JSON
      touches_per_match: careerTotals.touches || 0,
      minutes_played: careerTotals.minutes_played || 0
    },
    performance_metrics: {
      current_form: recentForm.minutes_played > 0 ? "active" : "inactive",
      form_trend: "stable", // Can be calculated from time series
      fitness_level: recentForm.minutes_played / (recentForm.matches_played * 90) || 0,
      injury_risk: 0.15, // Not available, using default
      consistency_score: 0.80 // Not available, using default
    },
    ml_predictions: {
      performance_score: latestPerformance.universal_score_100 / 10 || 0, // Scale to 0-10
      next_season_goals_prediction: Math.round(careerTotals.goals_per_90 * 34) || 0, // Estimate based on 34 games
      next_season_assists_prediction: Math.round(careerTotals.assists_per_90 * 34) || 0,
      market_value_prediction: basicInfo.market_value_eur_latest || 0,
      transfer_probability: 0.25, // Not available, using default
      injury_risk_prediction: 0.18, // Not available, using default
      career_longevity_score: 0.75 // Not available, using default
    },
    comparative_stats: {
      position_rank: 0, // Not available
      league_rank: 0, // Not available
      percentile_goals: 0, // Not available
      percentile_assists: 0, // Not available
      percentile_overall: Math.round(latestPerformance.universal_score_100 || 0)
    }
  };
};

/**
 * Extract SHAP values for word cloud visualization
 * @param {Object} jsonData - The full JSON output from the generator
 * @returns {Array} - Array of {text, value, sentiment} objects for word cloud
 */
export const extractShapValues = (jsonData) => {
  const shapSummary = jsonData.shap_summary || {};
  const positiveFeatures = shapSummary.positive_features || [];
  const negativeFeatures = shapSummary.negative_features || [];
  
  // Use Map to handle duplicates case-insensitively and merge by higher absolute value
  const featuresMap = new Map();
  
  // Process positive features
  positiveFeatures.forEach(feature => {
    const featureName = formatFeatureName(feature.feature);
    const featureKey = featureName.toLowerCase();
    const absValue = Math.abs(feature.shap_value);
    
    if (!featuresMap.has(featureKey) || featuresMap.get(featureKey).absValue < absValue) {
      featuresMap.set(featureKey, {
        text: featureName,
        value: absValue * 100, // Scale for visibility
        sentiment: 'positive',
        shapValue: feature.shap_value,
        absValue: absValue
      });
    }
  });
  
  // Process negative features
  negativeFeatures.forEach(feature => {
    const featureName = formatFeatureName(feature.feature);
    const featureKey = featureName.toLowerCase();
    const absValue = Math.abs(feature.shap_value);
    
    if (!featuresMap.has(featureKey) || featuresMap.get(featureKey).absValue < absValue) {
      featuresMap.set(featureKey, {
        text: featureName,
        value: absValue * 100, // Scale for visibility
        sentiment: 'negative',
        shapValue: feature.shap_value,
        absValue: absValue
      });
    }
  });
  
  // Convert map to array and remove absValue helper property
  return Array.from(featuresMap.values()).map(({ absValue, ...word }) => word);
};

/**
 * Extract time series data for performance and valuation chart
 * Sample data points to reduce chart density and improve performance
 * @param {Object} jsonData - The full JSON output from the generator
 * @returns {Array} - Array of {date, performance, marketValue} objects
 */
export const extractTimeSeriesData = (jsonData) => {
  const timeSeries = jsonData.performance_time_series || [];
  
  // Sample data points - take every Nth point based on data size
  const sampleRate = Math.max(1, Math.floor(timeSeries.length / 50)); // Max 50 points
  const sampledData = timeSeries.filter((_, index) => index % sampleRate === 0);
  
  return sampledData.map(point => ({
    date: point.date,
    performance: point.universal_score_100 || 0,
    marketValue: point.market_value || 0,
    // Format for display
    displayDate: new Date(point.date).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short' 
    })
  }));
};

/**
 * Format feature names for display (convert snake_case to Title Case)
 * @param {string} featureName - The feature name in snake_case
 * @returns {string} - Formatted feature name
 */
const formatFeatureName = (featureName) => {
  return featureName
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
    .replace(/Per90/g, 'Per 90')
    .replace(/365/g, ' (365 days)')
    .replace(/In Eur/g, '')
    .replace(/Log /g, '');
};

/**
 * Get player basic information for display
 * @param {Object} jsonData - The full JSON output from the generator
 * @returns {Object} - Player info for display
 */
export const getPlayerBasicInfo = (jsonData) => {
  const basicInfo = jsonData.basic_info || {};
  const careerTotals = jsonData.career_totals || {};
  const mlrCoefficients = jsonData.mlr_coefficients || {};
  const latestTransfer = mlrCoefficients.transfers && mlrCoefficients.transfers.length > 0 
    ? mlrCoefficients.transfers[mlrCoefficients.transfers.length - 1] 
    : {};
  
  return {
    id: basicInfo.player_id,
    name: basicInfo.name || 'Unknown Player',
    age: basicInfo.age_at_reference_date,
    dateOfBirth: basicInfo.date_of_birth,
    position: basicInfo.primary_position,
    club: basicInfo.current_club_name,
    currentClub: basicInfo.current_club_name,
    nationality: basicInfo.nationality,
    height: basicInfo.height_cm,
    weight: basicInfo.weight_kg,
    marketValue: basicInfo.market_value_eur_latest,
    highestValue: basicInfo.highest_market_value_eur,
    imageUrl: basicInfo.image_url,
    preferredFoot: basicInfo.preferred_foot,
    foot: basicInfo.preferred_foot,
    growthScore: basicInfo.growth_potential_score,
    growthPotentialScore: basicInfo.growth_potential_score,
    careerMatches: careerTotals.matches_played,
    careerGoals: careerTotals.goals,
    careerAssists: careerTotals.assists,
    // Transfer fee information
    transferFromClub: latestTransfer.from_club_name,
    transferToClub: latestTransfer.to_club_name,
    transferSeason: latestTransfer.transfer_season,
    transferDate: latestTransfer.transfer_date,
    predictedLogTransferFee: latestTransfer.pred_log_transfer_fee,
    predictedTransferFee: latestTransfer.pred_transfer_fee,
    actualTransferFee: latestTransfer.actual_transfer_fee,
    residualLog: latestTransfer.residual_log
  };
};

/**
 * Calculate performance statistics for PieChart
 * @param {Object} jsonData - The full JSON output from the generator
 * @returns {Object} - Performance breakdown data
 */
export const calculatePerformanceBreakdown = (jsonData) => {
  const careerTotals = jsonData.career_totals || {};
  const timeSeries = jsonData.performance_time_series || [];
  
  const latestPerformance = timeSeries.length > 0 
    ? timeSeries[timeSeries.length - 1].universal_score_100 
    : 50;
  
  const goalsContribution = (careerTotals.goals_per_90 || 0) * 100;
  const assistsContribution = (careerTotals.assists_per_90 || 0) * 100;
  const consistencyScore = latestPerformance || 50;
  
  return {
    attacking: Math.min(goalsContribution * 2, 40),
    playmaking: Math.min(assistsContribution * 2, 30),
    consistency: Math.min(consistencyScore / 3, 30)
  };
};
