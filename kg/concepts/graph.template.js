// molbio-kb Concept Graph — D3.js 2D Force-Directed Layout
// Placeholders: {GRAPH_DATA} {HREFS_JSON}

const graphData = {GRAPH_DATA};
const W = document.getElementById("graph-container").clientWidth;
const H = document.getElementById("graph-container").clientHeight;
const CX = W / 2, CY = H / 2;

const cats = [...new Set(graphData.nodes.map(n => n.category))];
const colors = ["#1d4ed8","#db2777","#ea580c","#059669","#6366f1","#7c3aed","#db2777","#0891b2","#7c3aed","#64748b"];
const colorScale = d3.scaleOrdinal().domain(cats).range(colors);

// Group radii by category
const catRadius = Math.min(W, H) * 0.36;
const catRing = {};
cats.forEach((c, i) => { catRing[c] = catRadius * (0.5 + 0.5 * i / Math.max(1, cats.length - 1)); });

const nodeMap = new Map();
graphData.nodes.forEach(n => {
  const r = catRing[n.category || "概念"] || catRadius * 0.7;
  const a = Math.random() * Math.PI * 2;
  n.x = CX + r * Math.cos(a);
  n.y = CY + r * Math.sin(a);
  n.r = n.importance === "core-important" ? 7 : 4.5;
  nodeMap.set(n.id || n.name, n);
  nodeMap.set(n.name, n);
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

// ── Draw links ──
const relColors = {"is-a":"#667eea","part-of":"#764ba2","regulates":"#e74c3c","catalyzes":"#27ae60","participates-in":"#f39c12","related":"#95a5a6"};
const linkTypes = {"is-a": "是一种", "part-of": "组成", "regulates": "调控", "catalyzes": "催化", "participates-in": "参与", "related": "相关"};
const link = g.selectAll(".link").data(linksData).enter().append("line")
  .attr("stroke", d => relColors[d.type] || "#aaa")
  .attr("stroke-width", d => ["is-a","part-of","regulates"].includes(d.type) ? 1.5 : 0.6)
  .attr("stroke-opacity", 0.28);

// ── Draw nodes ──
const node = g.selectAll(".node").data(allNodes).enter().append("g")
  .attr("class", "node").style("cursor", "pointer");

node.append("circle")
  .attr("r", d => d.r)
  .attr("fill", d => colorScale(d.category))
  .attr("fill-opacity", 0.85)
  .attr("stroke", "#fff").attr("stroke-width", 1.2);

// Label core-important nodes
node.filter(d => d.importance === "core-important").append("text")
  .attr("dx", d => d.r + 4).attr("dy", 4)
  .text(d => d.name)
  .attr("font-size", "11px")
  .attr("fill", "var(--ink2)")
  .style("pointer-events", "none");

// ── Interaction with enhanced tooltip ──
const tooltip = document.getElementById("tooltip");
node.on("mouseover", (ev, d) => {
  const nLinks = linksData.filter(l => l.source === d || l.target === d).length;
  tooltip.style.display = "block";
  tooltip.innerHTML = "<b>" + d.name + "</b><br><span style='font-size:.75rem;opacity:.7'>" + d.category + " · " + nLinks + "条关联</span>";
  d3.select(ev.currentTarget).select("circle").attr("r", 12).attr("fill-opacity", 1).attr("stroke", "#333").attr("stroke-width", 2.5);
  link.attr("stroke-opacity", l => (l.source === d || l.target === d) ? 0.95 : 0.03)
      .attr("stroke-width", l => (l.source === d || l.target === d) ? 3 : 0.2);
}).on("mousemove", ev => {
  tooltip.style.left = (ev.offsetX + 16) + "px";
  tooltip.style.top = (ev.offsetY - 12) + "px";
}).on("mouseout", (ev, d) => {
  tooltip.style.display = "none";
  d3.select(ev.currentTarget).select("circle").attr("r", d.r).attr("fill-opacity", 0.85).attr("stroke", "#fff").attr("stroke-width", 1.2);
  link.attr("stroke-opacity", 0.28).attr("stroke-width", d => ["is-a","part-of","regulates"].includes(d.type) ? 1.5 : 0.6);
}).on("dblclick", (ev, d) => {
  const hrefs = {HREFS_JSON};
  if (hrefs[d.name]) window.location = hrefs[d.name];
});

// ── Force simulation ──
const sim = d3.forceSimulation(allNodes)
  .force("link", d3.forceLink(linksData).id(d => d.id || d.name).distance(35).strength(0.06))
  .force("charge", d3.forceManyBody().strength(-25))
  .force("center", d3.forceCenter(CX, CY))
  .force("radial", d => {
    const r = catRing[d.category] || catRadius * 0.7;
    const dx = d.x - CX, dy = d.y - CY, dist = Math.sqrt(dx*dx + dy*dy) || 1;
    d.vx += (dx / dist) * (r - dist) * 0.05;
    d.vy += (dy / dist) * (r - dist) * 0.05;
  })
  .alphaDecay(0.012)
  .on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
  });

// ── Zoom ──
const zoom = d3.zoom().scaleExtent([0.25, 5]).on("zoom", e => g.attr("transform", e.transform));
svg.call(zoom);
window.zoomIn = () => svg.transition().duration(300).call(zoom.scaleBy, 1.4);
window.zoomOut = () => svg.transition().duration(300).call(zoom.scaleBy, 0.7);

// ── Drag ──
node.call(d3.drag()
  .on("start", (ev, d) => { if (!ev.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
  .on("drag", (ev, d) => { d.fx = ev.x; d.fy = ev.y; })
  .on("end", (ev, d) => { if (!ev.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));

// ── Search highlight ──
window.highlightEntity = function(query) {
  query = query.trim().toLowerCase();
  if (!query) {
    node.select("circle").attr("fill-opacity", 0.85);
    link.attr("stroke-opacity", 0.28);
    return;
  }
  node.select("circle").attr("fill-opacity", d => 
    d.name.toLowerCase().includes(query) || (d.id||"").toLowerCase().includes(query) ? 1 : 0.15
  ).attr("stroke", d => 
    d.name.toLowerCase().includes(query) ? "#333" : "#fff"
  ).attr("stroke-width", d => 
    d.name.toLowerCase().includes(query) ? 3 : 0.5
  );
  link.attr("stroke-opacity", l => {
    const srcMatch = l.source.name.toLowerCase().includes(query) || (l.source.id||"").toLowerCase().includes(query);
    const tgtMatch = l.target.name.toLowerCase().includes(query) || (l.target.id||"").toLowerCase().includes(query);
    return (srcMatch || tgtMatch) ? 0.8 : 0.02;
  });
};
