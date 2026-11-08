import json
import re
from pathlib import Path

# ---------------------------------------------------------------
# 1. Terms (from the glossary) — aliases are used for counting
# ---------------------------------------------------------------
TERMS = [
    # Core model concepts
    {"id": "Language model", "group": "Core concepts",
     "aliases": ["language model", "LLM", "model"],
     "definition": "A program that predicts text, one token at a time, based on patterns learned in training."},
    {"id": "Token", "group": "Core concepts",
     "aliases": ["token"],
     "definition": "The unit a model works with; text is split into tokens and limits are counted in tokens."},
    {"id": "Context window", "group": "Core concepts",
     "aliases": ["context window", "context"],
     "definition": "The maximum amount of text (in tokens) a model can hold at once: question, documents and answer."},
    {"id": "Inference", "group": "Core concepts",
     "aliases": ["inference", "infer"],
     "definition": "Running a trained model to get an answer; happens every time we ask the LLM something."},
    {"id": "Prompt", "group": "Core concepts",
     "aliases": ["prompt"],
     "definition": "The input you give the model."},
    {"id": "Hallucination", "group": "Risks",
     "aliases": ["hallucinat"],
     "definition": "When a model states something false with full confidence, e.g. invented functions or libraries."},
    {"id": "Fine-tuning", "group": "Core concepts",
     "aliases": ["fine-tun", "retrain"],
     "definition": "Training an existing model further on your own data to adapt it to a domain or style."},

    # Agents
    {"id": "Agent", "group": "Agents",
     "aliases": ["agent"],
     "definition": "A model that takes multi-step actions: plans, acts, checks the result and retries."},

    # Retrieval and grounding
    {"id": "RAG", "group": "Retrieval & grounding",
     "aliases": ["RAG", "retrieval-augmented"],
     "definition": "Retrieval-Augmented Generation: look up relevant documents first, then pass them to the model."},
    {"id": "Retrieval", "group": "Retrieval & grounding",
     "aliases": ["retriev"],
     "definition": "Searching and fetching the most relevant information for a question before answering."},
    {"id": "Chunking", "group": "Retrieval & grounding",
     "aliases": ["chunk"],
     "definition": "Splitting a long document into smaller passages before storing it."},
    {"id": "Embedding", "group": "Retrieval & grounding",
     "aliases": ["embedding", "embedded"],
     "definition": "Text converted into a list of numbers representing its meaning; similar meanings sit close together."},
    {"id": "Vector database", "group": "Retrieval & grounding",
     "aliases": ["vector database"],
     "definition": "Storage that finds the items closest to a given embedding (similarity search, not exact match)."},
    {"id": "Grounding", "group": "Retrieval & grounding",
     "aliases": ["ground"],
     "definition": "Making the model answer from supplied sources rather than memory, so answers can be checked."},
    {"id": "Bottleneck", "group": "Retrieval & grounding",
     "aliases": ["bottleneck"],
     "definition": "The narrowest part of a system that limits everything else; in RAG usually retrieval."},

    # Visual generation
    {"id": "Diffusion model", "group": "Visual generation",
     "aliases": ["diffusion"],
     "definition": "Image-generation architecture: starts from noise and removes it step by step, guided by the prompt."},
    {"id": "Temporal consistency", "group": "Visual generation",
     "aliases": ["temporal consistency", "consistent with its neighbours"],
     "definition": "In video, each frame must be credible alone and fit neighbouring frames."},
    {"id": "Seed", "group": "Visual generation",
     "aliases": ["seed"],
     "definition": "The random starting value of a generation; same prompt + same seed = same image."},
]

# ---------------------------------------------------------------
# 2. Relations between terms (source -> target : label)
# ---------------------------------------------------------------
RELATIONS = [
    ("Prompt", "Language model", "input to"),
    ("Token", "Context window", "measures"),
    ("Context window", "Language model", "limits"),
    ("Inference", "Language model", "runs"),
    ("Language model", "Hallucination", "can produce"),
    ("Fine-tuning", "Language model", "adapts"),
    ("Agent", "Language model", "built on"),
    ("Agent", "Inference", "runs many steps of"),

    ("RAG", "Retrieval", "starts with"),
    ("RAG", "Grounding", "achieves"),
    ("RAG", "Context window", "fills with passages"),
    ("RAG", "Fine-tuning", "alternative to"),
    ("Chunking", "Embedding", "chunks become"),
    ("Embedding", "Vector database", "stored in"),
    ("Retrieval", "Vector database", "searches"),
    ("Retrieval", "Bottleneck", "usually the"),
    ("Grounding", "Hallucination", "reduces"),

    ("Diffusion model", "Prompt", "guided by"),
    ("Diffusion model", "Seed", "starts from"),
    ("Diffusion model", "Temporal consistency", "video requires"),
]

# ---------------------------------------------------------------
# 3. Statistics from the use-case document
# ---------------------------------------------------------------
text = Path("research-report.md").read_text(encoding="utf-8")
paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def make_pattern(aliases):
    alts = sorted(aliases, key=len, reverse=True)  # longest match first
    return re.compile(r"\b(?:" + "|".join(re.escape(a) for a in alts) + r")", re.IGNORECASE)


patterns = {t["id"]: make_pattern(t["aliases"]) for t in TERMS}


def cooccurrence(a, b):
    """Number of paragraphs where both terms appear."""
    return sum(1 for p in paragraphs if patterns[a].search(p) and patterns[b].search(p))


nodes = [{
    "id": t["id"],
    "group": t["group"],
    "definition": t["definition"],
    "mentions": len(patterns[t["id"]].findall(text)),
} for t in TERMS]

links = [{
    "source": s,
    "target": t,
    "label": label,
    "cooccurrence": cooccurrence(s, t),
} for s, t, label in RELATIONS]

data = {"nodes": nodes, "links": links}
Path("graph_data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

# Print the statistics for your report
print(f"{'Term':<22}Mentions")
for n in sorted(nodes, key=lambda n: -n["mentions"]):
    print(f"{n['id']:<22}{n['mentions']}")

# ---------------------------------------------------------------
# 4. HTML + JS (D3.js) template
# ---------------------------------------------------------------
TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>GenAI Terms – Relations Graph</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  body { margin: 0; font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; overflow: hidden; }
  h1 { font-size: 18px; margin: 12px 16px 0; }
  p.sub { margin: 4px 16px; font-size: 13px; color: #94a3b8; }
  svg { width: 100vw; height: calc(100vh - 60px); }
  .link { stroke: #64748b; stroke-opacity: .7; }
  .link-label { font-size: 10px; fill: #94a3b8; pointer-events: none; text-anchor: middle; }
  .node circle { stroke: #0f172a; stroke-width: 2; cursor: grab; }
  .node text { font-size: 12px; fill: #f8fafc; pointer-events: none; text-anchor: middle; }
  .faded { opacity: .12; }
  #tip { position: absolute; max-width: 280px; padding: 8px 10px; background: #1e293b;
         border: 1px solid #334155; border-radius: 6px; font-size: 12px; pointer-events: none; opacity: 0; }
  #legend { position: absolute; top: 70px; right: 16px; background: #1e293b; padding: 10px 12px;
            border-radius: 6px; font-size: 12px; line-height: 1.8; }
</style>
</head>
<body>
<h1>GenAI Terms – Relations Graph</h1>
<p class="sub">Node size = mentions in the use-case document · Edge thickness = paragraph co-occurrence · Drag nodes, scroll to zoom, hover for definitions</p>
<div id="legend"></div>
<div id="tip"></div>
<svg></svg>
<script>
const data = __DATA__;

const svg = d3.select("svg");
const width = window.innerWidth, height = window.innerHeight - 60;
const color = d3.scaleOrdinal()
  .domain([...new Set(data.nodes.map(d => d.group))])
  .range(["#38bdf8", "#f472b6", "#34d399", "#a78bfa", "#fbbf24"]);
const radius = d => 10 + Math.sqrt(d.mentions) * 4;

// Arrow marker
svg.append("defs").append("marker")
  .attr("id", "arrow").attr("viewBox", "0 -5 10 10")
  .attr("refX", 10).attr("refY", 0)
  .attr("markerWidth", 6).attr("markerHeight", 6).attr("orient", "auto")
  .append("path").attr("d", "M0,-5L10,0L0,5").attr("fill", "#64748b");

const g = svg.append("g");
svg.call(d3.zoom().scaleExtent([0.3, 3]).on("zoom", e => g.attr("transform", e.transform)));

const sim = d3.forceSimulation(data.nodes)
  .force("link", d3.forceLink(data.links).id(d => d.id).distance(140))
  .force("charge", d3.forceManyBody().strength(-550))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collide", d3.forceCollide().radius(d => radius(d) + 22));

const link = g.append("g").selectAll("line").data(data.links).join("line")
  .attr("class", "link")
  .attr("stroke-width", d => 1 + d.cooccurrence)
  .attr("marker-end", "url(#arrow)");

const linkLabel = g.append("g").selectAll("text").data(data.links).join("text")
  .attr("class", "link-label").text(d => d.label);

const node = g.append("g").selectAll("g").data(data.nodes).join("g")
  .attr("class", "node").call(drag(sim));

node.append("circle").attr("r", radius).attr("fill", d => color(d.group));
node.append("text").attr("dy", d => radius(d) + 14).text(d => d.id);

sim.on("tick", () => {
  // Stop lines at the circle edge so arrows stay visible
  link.each(function (d) {
    const dx = d.target.x - d.source.x, dy = d.target.y - d.source.y;
    const dist = Math.hypot(dx, dy) || 1;
    const rs = radius(d.source), rt = radius(d.target) + 4;
    d3.select(this)
      .attr("x1", d.source.x + dx / dist * rs).attr("y1", d.source.y + dy / dist * rs)
      .attr("x2", d.target.x - dx / dist * rt).attr("y2", d.target.y - dy / dist * rt);
  });
  linkLabel.attr("x", d => (d.source.x + d.target.x) / 2)
           .attr("y", d => (d.source.y + d.target.y) / 2 - 4);
  node.attr("transform", d => `translate(${d.x},${d.y})`);
});

// Tooltip + highlight neighbours
const tip = d3.select("#tip");
node.on("mouseover", (e, d) => {
    tip.style("opacity", 1)
       .html(`<b>${d.id}</b><br>${d.definition}<br><i>Mentions: ${d.mentions}</i>`);
    const linked = new Set([d.id]);
    data.links.forEach(l => {
      if (l.source.id === d.id) linked.add(l.target.id);
      if (l.target.id === d.id) linked.add(l.source.id);
    });
    const notMine = l => l.source.id !== d.id && l.target.id !== d.id;
    node.classed("faded", n => !linked.has(n.id));
    link.classed("faded", notMine);
    linkLabel.classed("faded", notMine);
  })
  .on("mousemove", e => tip.style("left", (e.pageX + 12) + "px").style("top", (e.pageY + 12) + "px"))
  .on("mouseout", () => {
    tip.style("opacity", 0);
    node.classed("faded", false); link.classed("faded", false); linkLabel.classed("faded", false);
  });

// Legend
const legend = d3.select("#legend");
color.domain().forEach(gr => legend.append("div").html(
  `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color(gr)};margin-right:6px"></span>${gr}`));

function drag(sim) {
  return d3.drag()
    .on("start", (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag",  (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on("end",   (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; });
}
</script>
</body>
</html>
"""

Path("graph.html").write_text(TEMPLATE.replace("__DATA__", json.dumps(data)), encoding="utf-8")
print("\nCreated graph_data.json and graph.html")