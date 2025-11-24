import React, { useEffect, useRef, useState } from 'react';
import cloud from 'd3-cloud';
import * as d3Scale from 'd3-scale';
import './WordCloudChart.css';

const WordCloudChart = ({ data = [], title = "Performance Factors", subtitle = "Factors affecting Transfer Fee" }) => {
  const svgRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 600, height: 300 });

  // Placeholder data structure
  const placeholderData = [
    { text: 'Speed', value: 85, sentiment: 'positive' },
    { text: 'Passing', value: 78, sentiment: 'positive' },
    { text: 'Shooting', value: 82, sentiment: 'positive' },
    { text: 'Dribbling', value: 90, sentiment: 'positive' },
    { text: 'Defense', value: 65, sentiment: 'negative' },
    { text: 'Stamina', value: 75, sentiment: 'positive' },
    { text: 'Positioning', value: 88, sentiment: 'positive' },
    { text: 'Vision', value: 80, sentiment: 'positive' },
    { text: 'Control', value: 86, sentiment: 'positive' },
    { text: 'Agility', value: 83, sentiment: 'positive' },
  ];

  const words = data.length > 0 ? data : placeholderData;

  useEffect(() => {
    if (!svgRef.current || words.length === 0) return;

    const svg = svgRef.current;
    const containerWidth = svg.parentElement?.offsetWidth || 600;
    const containerHeight = 300;

    setDimensions({ width: containerWidth, height: containerHeight });

    // Clear previous content
    svg.innerHTML = '';

    // Color based on sentiment with gradient effect
    const getColor = (word) => {
      if (word.sentiment === 'positive') {
        return '#40c057'; // Vibrant green for positive SHAP values
      } else if (word.sentiment === 'negative') {
        return '#fa5252'; // Vibrant red for negative SHAP values
      }
      return '#4c6ef5'; // Default blue
    };

    // Create font size scale based on absolute value with better range
    const fontScale = d3Scale.scaleLinear()
      .domain([Math.min(...words.map(w => w.value)), Math.max(...words.map(w => w.value))])
      .range([16, 48]); // Reduced max size to prevent overflow

    // Add padding to prevent boundary overflow
    const padding = 40;
    const effectiveWidth = containerWidth - (padding * 2);
    const effectiveHeight = containerHeight - (padding * 2);

    // Layout the word cloud with better spacing
    const layout = cloud()
      .size([effectiveWidth, effectiveHeight])
      .words(words.map(d => ({ ...d, size: fontScale(d.value) })))
      .padding(12) // Increased padding between words
      .rotate(() => 0) // Most words horizontal for readability
      .fontSize(d => d.size)
      .spiral('archimedean') // Better packing algorithm
      .on('end', draw);

    layout.start();

    function draw(words) {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      // Center with padding offset
      g.setAttribute('transform', `translate(${containerWidth / 2},${containerHeight / 2})`);

      words.forEach((word) => {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.style.fontSize = `${word.size}px`;
        text.style.fontFamily = 'Inter, -apple-system, BlinkMacSystemFont, sans-serif';
        text.style.fontWeight = '700';
        text.style.fill = getColor(word);
        text.style.cursor = 'move';
        text.style.transition = 'all 0.3s ease';
        text.style.opacity = '0.95';
        text.style.userSelect = 'none';
        text.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.1))';
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('transform', `translate(${word.x},${word.y}) rotate(${word.rotate})`);
        text.textContent = word.text;
        
        // Drag state
        let isDragging = false;
        let currentX = word.x;
        let currentY = word.y;
        let startX, startY;
        
        // Enhanced hover effects - subtle for better dragging experience
        text.addEventListener('mouseenter', () => {
          if (!isDragging) {
            text.style.opacity = '1';
            text.style.filter = 'drop-shadow(0 2px 6px rgba(0,0,0,0.2))';
          }
        });
        text.addEventListener('mouseleave', () => {
          if (!isDragging) {
            text.style.opacity = '0.95';
            text.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.1))';
          }
        });
        
        // Drag functionality
        const onMouseDown = (e) => {
          isDragging = true;
          text.style.cursor = 'grabbing';
          text.style.opacity = '1';
          text.style.filter = 'drop-shadow(0 4px 12px rgba(0,0,0,0.3))';
          
          // Get mouse position relative to SVG
          const svgRect = svg.getBoundingClientRect();
          const centerX = containerWidth / 2;
          const centerY = containerHeight / 2;
          
          startX = e.clientX - svgRect.left - centerX - currentX;
          startY = e.clientY - svgRect.top - centerY - currentY;
          
          e.preventDefault();
        };
        
        const onMouseMove = (e) => {
          if (!isDragging) return;
          
          const svgRect = svg.getBoundingClientRect();
          const centerX = containerWidth / 2;
          const centerY = containerHeight / 2;
          
          // Calculate new position
          let newX = e.clientX - svgRect.left - centerX - startX;
          let newY = e.clientY - svgRect.top - centerY - startY;
          
          // Apply boundaries (keep within container with padding)
          const maxX = containerWidth / 2 - padding;
          const maxY = containerHeight / 2 - padding;
          const minX = -maxX;
          const minY = -maxY;
          
          newX = Math.max(minX, Math.min(maxX, newX));
          newY = Math.max(minY, Math.min(maxY, newY));
          
          currentX = newX;
          currentY = newY;
          
          text.setAttribute('transform', `translate(${currentX},${currentY}) rotate(${word.rotate})`);
        };
        
        const onMouseUp = () => {
          if (isDragging) {
            isDragging = false;
            text.style.cursor = 'move';
            text.style.opacity = '0.95';
            text.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.1))';
          }
        };
        
        text.addEventListener('mousedown', onMouseDown);
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
        
        // Add detailed tooltip
        const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
        const shapInfo = word.shapValue !== undefined 
          ? `${word.text}\nSHAP Value: ${word.shapValue.toFixed(4)}\nImpact: ${word.sentiment}` 
          : `${word.text}: ${word.value}`;
        title.textContent = shapInfo;
        text.appendChild(title);
        
        g.appendChild(text);
      });

      svg.appendChild(g);
    }
  }, [words]);

  return (
    <div className="card wordcloud-card">
      <div className="card-header">
        <h3>{title}</h3>
        <p className="card-subtitle">{subtitle}</p>
        <div className="legend">
          <span className="legend-item positive">
            <span className="legend-color"></span>
            Positive Impact
          </span>
          <span className="legend-item negative">
            <span className="legend-color"></span>
            Negative Impact
          </span>
        </div>
      </div>
      <div className="wordcloud-container">
        {words.length > 0 ? (
          <svg 
            ref={svgRef} 
            width={dimensions.width} 
            height={dimensions.height}
            className="wordcloud-svg"
          />
        ) : (
          <div className="placeholder">No data available</div>
        )}
      </div>
    </div>
  );
};

export default WordCloudChart;
