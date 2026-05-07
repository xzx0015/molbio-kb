// molbio-kb Concept Graph — D3.js 2D Circular Clustered Layout
// Placeholders: {GRAPH_DATA} {HREFS_JSON}

const graphData = {GRAPH_DATA};
const W = document.getElementById("graph-container").clientWidth;
const H = document.getElementById("graph-container").clientHeight;
const CX = W / 2, CY = H / 2;

const cats = [...new Set(graphData.nodes.map(n => n.category))];
const catRadius = Math.min(W, H) * 0.38;
const catRing = {};
cats.forEach((c, i) => { catRing[c] = catRadius * (0.45 + 0.55 * (i + 1) / cats.length); });

const colorScale = d3.scaleOrdinal()
  .domain(cats)
  .range(["#1d4ed8","#2563eb","#db2777","#059669","#ea580c","#6366f1","#7c3aed","#db2777","#0891b2","#7c3aed","#64748b"]);

const nodeMap = new Map();
graphData.nodes.forEach(n => {
  const cat = n.category || "概念";
  const r = catRing[cat] || catRadius * 0.8;
  const a = Math.random() * Math.PI * 2;
  n.x = CX + r * Math.cos(a);
  n.y = CY + r * Math.sin(a);
  nodeMap.set(n.id || n.name, n);
  nodeMap.set(n.name, n);  // also key by Chinese name for link resolution
});

const linksData = [];
graphData.links.forEach(l => {
  const src = nodeMap.get(l.source);
  const tgt = nodeMap.get(l.target);
  if (src && tgt) linksData.push({source: src, target: tgt, type: l.type || "related"});
});

const allNodes = graphData.nodes.filter(n => nodeMap.has(n.id || n.name));

const svg = d3.select("#graph-container").append("svg").attr("width", W).attr("height", H);
const g = svg.append("g");

// Ring circles
cats.forEach(c => {
  g.append("circle").attr("cx", CX).attr("cy", CY).attr("r", catRing[c])
    .attr("fill", "none").attr("stroke", colorScale(c)).attr("stroke-width", 1).attr("stroke-opacity", 0.15).attr("stroke-dasharray", "4,4");
});
g.selectAll(".ring-label").data(cats).enter().append("text")
  .attr("x", d => CX + catRing[d] + 8).attr("y", CY).attr("text-anchor", "start")
  .attr("fill", d => colorScale(d)).attr("font-size", "12px").attr("font-weight", "600").text(d => d);

// Links
const relColors = {"is-a":"#667eea","part-of":"#764ba2","regulates":"#e74c3c","catalyzes":"#27ae60","participates-in":"#f39c12","related":"#95a5a6"};
const link = g.selectAll(".link").data(linksData).enter().append("line")
  .attr("class", "link")
  .attr("stroke", d => relColors[d.type] || "#aaa")
  .attr("stroke-width", d => ["is-a","part-of","regulates"].includes(d.type) ? 1.2 : 0.5)
  .attr("stroke-opacity", 0.35);

// Nodes
const node = g.selectAll(".node").data(allNodes).enter().append("g").attr("class", "node").style("cursor", "pointer");
node.append("circle")
  .attr("r", d => d.importance === "core-important" ? 6 : 4.5)
  .attr("fill", d => colorScale(d.category)).attr("fill-opacity", 0.88)
  .attr("stroke", "#fff").attr("stroke-width", 1.2);
node.filter(d => d.importance === "core-important").append("text")
  .attr("dx", 8).attr("dy", 3).text(d => d.name).attr("font-size", "10px").attr("fill", "var(--ink2)");

// Interaction
const tooltip = document.getElementById("tooltip");
node.on("mouseover", (ev, d) => {
  tooltip.style.display = "block";
  tooltip.innerHTML = "<b>" + d.name + "</b><br><span style='font-size:.75rem;opacity:.7'>" + d.category + "</span>";
  d3.select(ev.currentTarget).select("circle").attr("r", 10).attr("fill-opacity", 1).attr("stroke", "#333").attr("stroke-width", 2.5);
  link.attr("stroke-opacity", l => (l.source === d || l.target === d) ? 0.95 : 0.04)
      .attr("stroke-width", l => (l.source === d || l.target === d) ? 2.5 : 0.2);
}).on("mousemove", ev => {
  tooltip.style.left = (ev.offsetX + 16) + "px";
  tooltip.style.top = (ev.offsetY - 12) + "px";
}).on("mouseout", (ev, d) => {
  tooltip.style.display = "none";
  d3.select(ev.currentTarget).select("circle").attr("r", d.importance === "core-important" ? 6 : 4.5).attr("fill-opacity", 0.88).attr("stroke", "#fff").attr("stroke-width", 1.2);
  link.attr("stroke-opacity", 0.35).attr("stroke-width", d => ["is-a","part-of","regulates"].includes(d.type) ? 1.2 : 0.5);
});

// Double-click navigation
const entityHrefs = {HREFS_JSON};
node.on("dblclick", (ev, d) => {
  if (entityHrefs[d.name]) window.location = entityHrefs[d.name];
});

// Force simulation
const sim = d3.forceSimulation(allNodes)
  .force("link", d3.forceLink(linksData).id(d => d.id || d.name).distance(30).strength(0.08))
  .force("charge", d3.forceManyBody().strength(-20))
  .force("center", d3.forceCenter(CX, CY))
  .force("radial", d => {
    const r = catRing[d.category] || catRadius * 0.8;
    const dx = d.x - CX, dy = d.y - CY, dist = Math.sqrt(dx*dx + dy*dy) || 1;
    d.vx += (dx / dist) * (r - dist) * 0.06;
    d.vy += (dy / dist) * (r - dist) * 0.06;
  })
  .alphaDecay(0.015)
  .on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
  });

// Zoom
const zoom = d3.zoom().scaleExtent([0.3, 5]).on("zoom", e => g.attr("transform", e.transform));
svg.call(zoom);
window.zoomIn = () => svg.transition().duration(300).call(zoom.scaleBy, 1.4);
window.zoomOut = () => svg.transition().duration(300).call(zoom.scaleBy, 0.7);

// Drag
node.call(d3.drag()
  .on("start", (ev, d) => { if (!ev.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
  .on("drag", (ev, d) => { d.fx = ev.x; d.fy = ev.y; })
  .on("end", (ev, d) => { if (!ev.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));
