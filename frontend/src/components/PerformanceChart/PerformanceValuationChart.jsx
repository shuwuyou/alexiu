import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  Area,
  ComposedChart
} from 'recharts';
import './PerformanceValuationChart.css';

const PerformanceValuationChart = ({ data = [] }) => {
  // Placeholder data
  const placeholderData = [
    { displayDate: 'Jan 2023', performance: 75, marketValue: 4500000 },
    { displayDate: 'Feb 2023', performance: 78, marketValue: 4800000 },
    { displayDate: 'Mar 2023', performance: 82, marketValue: 5500000 },
    { displayDate: 'Apr 2023', performance: 80, marketValue: 5800000 },
    { displayDate: 'May 2023', performance: 85, marketValue: 6500000 },
    { displayDate: 'Jun 2023', performance: 88, marketValue: 7000000 },
    { displayDate: 'Jul 2023', performance: 86, marketValue: 7200000 },
    { displayDate: 'Aug 2023', performance: 90, marketValue: 7800000 },
  ];

  const chartData = data.length > 0 ? data : placeholderData;

  // Format currency for display
  const formatCurrency = (value) => {
    if (value >= 1000000) {
      return `€${(value / 1000000).toFixed(1)}M`;
    }
    return `€${(value / 1000).toFixed(0)}K`;
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const performanceData = payload.find(p => p.dataKey === 'performance');
      const marketValueData = payload.find(p => p.dataKey === 'marketValue');
      
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{payload[0].payload.displayDate}</p>
          {performanceData && (
            <p className="tooltip-performance">
              Performance Score: <span>{performanceData.value.toFixed(1)}</span>
            </p>
          )}
          {marketValueData && (
            <p className="tooltip-valuation">
              Market Value: <span>{formatCurrency(marketValueData.value)}</span>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card performance-chart-card">
      <div className="card-header">
        <h3>Performance vs Market Valuation Over Time</h3>
        <p className="card-subtitle">Universal Performance Score (0-100) and Market Value Trend</p>
      </div>
      <div className="performance-chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 50, left: 20, bottom: 10 }}>
            <defs>
              <linearGradient id="colorPerformance" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#4c6ef5" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#4c6ef5" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
            <XAxis 
              dataKey="displayDate" 
              stroke="var(--text-secondary)"
              style={{ fontSize: '11px' }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            {/* Left Y-Axis for Performance Score */}
            <YAxis 
              yAxisId="left"
              stroke="var(--text-secondary)"
              style={{ fontSize: '12px' }}
              label={{ value: 'Performance Score', angle: -90, position: 'insideLeft', style: { fill: 'var(--text-secondary)' } }}
              domain={[0, 100]}
            />
            {/* Right Y-Axis for Market Value */}
            <YAxis 
              yAxisId="right"
              orientation="right"
              stroke="var(--text-secondary)"
              style={{ fontSize: '12px', color: '#51cf66' }}
              tickFormatter={formatCurrency}
              label={{ value: 'Market Value', angle: 90, position: 'insideRight', style: { fill: 'var(--text-secondary)' } }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              yAxisId="left"
              type="monotone"
              dataKey="performance"
              fill="url(#colorPerformance)"
              stroke="none"
            />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="performance" 
              stroke="#4c6ef5" 
              strokeWidth={2}
              dot={{ fill: '#4c6ef5', r: 3 }}
              activeDot={{ r: 6 }}
              name="Performance Score"
            />
            <Line 
              yAxisId="right"
              type="monotone" 
              dataKey="marketValue" 
              stroke="#51cf66" 
              strokeWidth={2}
              dot={{ fill: '#51cf66', r: 3 }}
              activeDot={{ r: 6 }}
              name="Market Value"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PerformanceValuationChart;
