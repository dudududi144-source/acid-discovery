"""
ACID Knowledge Graph Visualization
Generate visual representations of the knowledge graph.
"""

def generate_svg(knowledge_graph, width=800, height=600):
    """Generate an SVG visualization of the knowledge graph."""
    nodes = knowledge_graph.nodes
    edges = knowledge_graph.edges
    
    # Simple force-directed layout (simplified)
    import math
    
    # Position nodes in a circle
    node_positions = {}
    node_list = list(nodes.keys())
    n = len(node_list)
    
    for i, node_id in enumerate(node_list):
        angle = 2 * math.pi * i / max(n, 1)
        x = width / 2 + (width / 3) * math.cos(angle)
        y = height / 2 + (height / 3) * math.sin(angle)
        node_positions[node_id] = (x, y)
    
    # Build SVG
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append(f'<rect width="{width}" height="{height}" fill="#0B0E14"/>')
    
    # Draw edges
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]
        if src in node_positions and tgt in node_positions:
            x1, y1 = node_positions[src]
            x2, y2 = node_positions[tgt]
            color = "#3ECF8E" if edge.get("effective", False) else "#E5726F"
            svg_parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1" opacity="0.5"/>')
    
    # Draw nodes
    for node_id, (x, y) in node_positions.items():
        node = nodes[node_id]
        if node["type"] == "artifact":
            color = "#6E8EF2"
            radius = 8
        else:
            color = "#E5B567"
            radius = 6
        
        svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>')
        
        # Label
        label = node_id[:12] if len(node_id) > 12 else node_id
        svg_parts.append(f'<text x="{x + radius + 4}" y="{y + 4}" fill="#9AA4B8" font-size="10" font-family="monospace">{label}</text>')
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)


def generate_text_report(knowledge_graph):
    """Generate a text report of the knowledge graph."""
    lines = []
    lines.append("ACID Knowledge Graph Report")
    lines.append("=" * 50)
    
    stats = knowledge_graph.to_dict()["stats"]
    lines.append(f"Total nodes: {stats['total_nodes']}")
    lines.append(f"Total edges: {stats['total_edges']}")
    lines.append(f"Artifacts: {stats['artifacts']}")
    lines.append(f"Tasks: {stats['tasks']}")
    lines.append("")
    
    # Most connected artifacts
    lines.append("Most connected artifacts:")
    for node_id, count in knowledge_graph.get_most_connected(5):
        lines.append(f"  {node_id[:16]}: {count} connections")
    
    lines.append("")
    
    # Transfer summary
    transfers = [e for e in knowledge_graph.edges if e["relation"] == "transfer"]
    effective = sum(1 for t in transfers if t.get("effective", False))
    lines.append(f"Transfers: {len(transfers)} total, {effective} effective")
    
    return '\n'.join(lines)


def generate_mermaid(knowledge_graph):
    """Generate a Mermaid diagram of the knowledge graph."""
    lines = []
    lines.append("graph TD")
    
    for node_id, node in knowledge_graph.nodes.items():
        safe_id = node_id.replace(":", "_").replace("-", "_")
        if node["type"] == "artifact":
            lines.append(f"    {safe_id}[{node_id[:12]}]")
        else:
            lines.append(f"    {safe_id}({node_id})")
    
    for edge in knowledge_graph.edges:
        src = edge["source"].replace(":", "_").replace("-", "_")
        tgt = edge["target"].replace(":", "_").replace("-", "_")
        if edge["relation"] == "transfer":
            lines.append(f"    {src} -->|transfer| {tgt}")
        elif edge["relation"] == "derivation":
            lines.append(f"    {src} -.->|derives| {tgt}")
    
    return '\n'.join(lines)
