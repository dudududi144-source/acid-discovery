"""
ACID Knowledge Graph
Tracks relationships between artifacts, tasks, and transfers.
"""

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}  # hash -> node data
        self.edges = []  # list of (source, target, relation)
    
    def add_artifact(self, artifact):
        """Add an artifact node."""
        h = artifact.get("hash", "unknown")
        self.nodes[h] = {
            "type": "artifact",
            "hash": h,
            "task": artifact.get("task", ""),
            "evals": artifact.get("evals", 0),
            "created": artifact.get("created", 0),
            "version": artifact.get("version", 1)
        }
        return h
    
    def add_task(self, task_name, task_data):
        """Add a task node."""
        self.nodes["task:" + task_name] = {
            "type": "task",
            "name": task_name,
            "data": task_data
        }
        return "task:" + task_name
    
    def add_transfer(self, source_hash, target_task, effective):
        """Add a transfer edge."""
        self.edges.append({
            "source": source_hash,
            "target": "task:" + target_task,
            "relation": "transfer",
            "effective": effective
        })
    
    def add_derivation(self, parent_hash, child_hash):
        """Add a derivation edge (child derived from parent)."""
        self.edges.append({
            "source": parent_hash,
            "target": child_hash,
            "relation": "derivation"
        })
    
    def get_artifact_history(self, artifact_hash):
        """Get the full history of an artifact."""
        history = []
        for edge in self.edges:
            if edge["target"] == artifact_hash and edge["relation"] == "derivation":
                history.append(edge["source"])
        return history
    
    def get_transfer_targets(self, artifact_hash):
        """Get all tasks this artifact has been transferred to."""
        targets = []
        for edge in self.edges:
            if edge["source"] == artifact_hash and edge["relation"] == "transfer":
                targets.append({
                    "task": edge["target"],
                    "effective": edge["effective"]
                })
        return targets
    
    def get_most_connected(self, limit=10):
        """Get artifacts with most connections."""
        connection_count = {}
        for edge in self.edges:
            src = edge["source"]
            connection_count[src] = connection_count.get(src, 0) + 1
        
        sorted_nodes = sorted(connection_count.items(), key=lambda x: -x[1])
        return sorted_nodes[:limit]
    
    def to_dict(self):
        """Export graph as dict."""
        return {
            "nodes": self.nodes,
            "edges": self.edges,
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "artifacts": sum(1 for n in self.nodes.values() if n["type"] == "artifact"),
                "tasks": sum(1 for n in self.nodes.values() if n["type"] == "task")
            }
        }
    
    def visualize(self):
        """Generate a text visualization of the graph."""
        lines = []
        lines.append("Knowledge Graph")
        lines.append("=" * 40)
        lines.append(f"Nodes: {len(self.nodes)}")
        lines.append(f"Edges: {len(self.edges)}")
        lines.append("")
        
        # Show artifacts
        artifacts = [n for n in self.nodes.values() if n["type"] == "artifact"]
        lines.append(f"Artifacts ({len(artifacts)}):")
        for a in artifacts[:10]:
            lines.append(f"  {a['hash'][:12]} | {a['task'][:30]} | evals={a['evals']}")
        
        lines.append("")
        
        # Show transfers
        transfers = [e for e in self.edges if e["relation"] == "transfer"]
        lines.append(f"Transfers ({len(transfers)}):")
        for t in transfers[:10]:
            eff = "EFFECTIVE" if t["effective"] else "NOT EFFECTIVE"
            lines.append(f"  {t['source'][:12]} -> {t['target']} [{eff}]")
        
        return "\n".join(lines)


def build_graph_from_history(history):
    """Build a knowledge graph from solve history."""
    kg = KnowledgeGraph()
    
    for entry in history:
        if entry.get("artifact"):
            kg.add_artifact({
                "hash": entry["artifact"],
                "task": entry.get("problem", ""),
                "evals": entry.get("evals", 0),
                "created": entry.get("started", 0)
            })
    
    return kg
