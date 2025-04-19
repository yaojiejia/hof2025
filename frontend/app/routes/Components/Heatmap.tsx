import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import './Heatmap.css';

const mockData = {
  name: 'Market',
  children: [
    {
      name: 'Tech',
      children: [
        { name: 'AAPL', value: 100, change: 2.3 },
        { name: 'MSFT', value: 80, change: -1.2 },
        { name: 'NVDA', value: 60, change: 3.5 },
      ],
    },
    {
      name: 'Finance',
      children: [
        { name: 'JPM', value: 90, change: 1.2 },
        { name: 'GS', value: 70, change: -0.8 },
      ],
    },
    {
      name: 'Healthcare',
      children: [
        { name: 'JNJ', value: 50, change: 0.5 },
        { name: 'PFE', value: 40, change: -2.0 },
      ],
    },
  ],
};

const Heatmap = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [ windowChanged, setWindowChanged ] = useState(0);

  // on browser resize: rerun heatmap dimensions useEffect
  useEffect(() => {
    const handleResize = () => {
      setWindowChanged( (windowChanged) => windowChanged + 1 );
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // build heatmap dimensions
  useEffect(() => {
    if (!containerRef.current) return;

    // calculate heatmap container's width & height (absolute px)
    const parentElement = containerRef.current.parentElement;
    if (!parentElement) return;
    const width = parentElement.getBoundingClientRect().width - 40;
    const height = width * 0.6;

    const color = d3.scaleLinear<string>()
      .domain([-5, 0, 5])
      .range(['rgb(246, 53, 56)', 'rgb(65, 69, 84)', 'rgb(48, 204, 90)']); // Vibrant red, yellow, and green

    const root = d3.hierarchy(mockData)
      .sum((d: any) => d.value)
      .sort((a, b) => (b.value ?? 0) - (a.value ?? 0));

    d3.treemap()
      .size([width, height])
      .paddingOuter(5) // Padding between sectors
      .paddingInner(1)(root); // Padding between individual stocks

    const container = d3.select(containerRef.current);
    container.selectAll('*').remove(); // Clear on re-render

    // Add sector groups
    const sectors = container
      .style('position', 'relative')
      .style('width', `${width}px`)
      .style('height', `${height}px`)
      .selectAll('div.sector')
      .data(root.children || []) // Top-level sectors
      .join('div')
      .classed('sector', true)
      .style('position', 'absolute')
      .style('left', d => `${d.x0}px`)
      .style('top', d => `${d.y0}px`)
      .style('width', d => `${d.x1 - d.x0}px`)
      .style('height', d => `${d.y1 - d.y0}px`)
      .style('box-sizing', 'border-box')
      .style('overflow', 'hidden')
      .classed('flex flex-col', true); // Use flexbox for layout

    // Add sector labels
    sectors
      .append('div')
      .classed('sector-label', true)
      .style('padding', '12px')
      .style('font-weight', 'bold')
      .style('font-size', '14px')
      .style('color', 'white')
      .text(d => d.data.name);

    // Add stock nodes within each sector
    sectors
      .selectAll('div.stock')
      .data(d => d.children || []) // Individual stocks within the sector
      .join('div')
      .classed('stock', true)
      .style('position', 'absolute')
      .style('left', d => `${d.x0 - d.parent!.x0}px`) // Relative to the sector
      .style('top', d => `${d.y0 - d.parent!.y0}px`) // Relative to the sector
      .style('width', d => `${d.x1 - d.x0}px`)
      .style('height', d => `${d.y1 - d.y0}px`)
      .style('background', d => getColor(d.data.change))
      .style('box-sizing', 'border-box')
      .style('overflow', 'hidden')
      .style('color', 'white')
      .style('font-size', '12px')
      .classed('flex justify-center items-center', true)
      .text(d => `${d.data.name} (${d.data.change}%)`);
  }, [windowChanged]);

  return <div ref={containerRef} />;
};

function getColor(change: number) {
  const opacity = Math.abs(change) / 9;
  
  if (change > 0) return `rgba(106, 206, 98, ${opacity})`;
  if (change < 0) return `rgba(247, 66, 75, ${opacity})`;
  return 'black';
}

export default Heatmap;
