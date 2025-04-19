// import * as d3 from 'd3';
// import React, { useEffect, useRef } from 'react';


// type PricePoint = {
//     date: string; // ISO format (e.g. '2025-04-15')
//     close: number;
//     predicted?: boolean;
//   };


// const Graph: React.FC<{ data: PricePoint[] }> = ({ data }) => {
//     const ref = useRef<SVGSVGElement>(null);
  
//     useEffect(() => {
//       const width = 500;
//       const height = 300;
//       const margin = { top: 20, right: 30, bottom: 30, left: 40 };
  
//       const svg = d3.select(ref.current);
//       svg.selectAll('*').remove(); // clear old content
  
//       const parseDate = d3.timeParse('%Y-%m-%d');
//       const parsedData = data.map(d => ({
//         ...d,
//         date: parseDate(d.date)!,
//       }));
  
//       const x = d3.scaleTime()
//         .domain(d3.extent(parsedData, d => d.date) as [Date, Date])
//         .range([margin.left, width - margin.right]);
  
//       const y = d3.scaleLinear()
//         .domain([d3.min(parsedData, d => d.close)! * 0.95, d3.max(parsedData, d => d.close)! * 1.05])
//         .nice()
//         .range([height - margin.bottom, margin.top]);
  
//       // Line for actual prices
//       const actualLine = d3.line<any>()
//         .x(d => x(d.date))
//         .y(d => y(d.close));
  
//       // Separate data for line: only real (first 4)
//       const realPoints = parsedData.filter(d => !d.predicted);
//       const predictedPoint = parsedData.find(d => d.predicted);
  
//       // Draw axes
//       svg.append('g')
//         .attr('transform', `translate(0,${height - margin.bottom})`)
//         .call(d3.axisBottom(x).ticks(5).tickFormat(d3.timeFormat('%b %d')));
  
//       svg.append('g')
//         .attr('transform', `translate(${margin.left},0)`)
//         .call(d3.axisLeft(y));
  
//       // Draw actual line
//       svg.append('path')
//         .datum(realPoints)
//         .attr('fill', 'none')
//         .attr('stroke', 'steelblue')
//         .attr('stroke-width', 2)
//         .attr('d', actualLine);
  
//       // Draw actual circles
//       svg.selectAll('.real-point')
//         .data(realPoints)
//         .join('circle')
//         .attr('cx', d => x(d.date))
//         .attr('cy', d => y(d.close))
//         .attr('r', 4)
//         .attr('fill', 'steelblue');
  
//       // Draw predicted point in green
//       if (predictedPoint) {
//         svg.append('circle')
//           .attr('cx', x(predictedPoint.date))
//           .attr('cy', y(predictedPoint.close))
//           .attr('r', 5)
//           .attr('fill', 'green');
  
//         // Optional: draw a dashed line from last real to prediction
//         svg.append('line')
//           .attr('x1', x(realPoints[realPoints.length - 1].date))
//           .attr('y1', y(realPoints[realPoints.length - 1].close))
//           .attr('x2', x(predictedPoint.date))
//           .attr('y2', y(predictedPoint.close))
//           .attr('stroke', 'green')
//           .attr('stroke-width', 1.5)
//           .attr('stroke-dasharray', '4');
//       }
  
//     }, [data]);
  
//     return <svg ref={ref} width={500} height={300}></svg>;
//   };

//   export default Graph;