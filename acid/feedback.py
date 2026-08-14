"""
ACID Feedback Loop
Self-improvement through iterative refinement based on results.
"""

class FeedbackLoop:
    def __init__(self):
        self.history = []
        self.adjustments = []
    
    def record_solve(self, task, result):
        """Record a solve attempt."""
        entry = {
            "task": task,
            "success": result.get("status") == "solved",
            "evals": result.get("evals", 0),
            "time": result.get("time", 0),
            "timestamp": result.get("created", 0)
        }
        self.history.append(entry)
        return entry
    
    def analyze_performance(self):
        """Analyze recent performance and suggest adjustments."""
        if len(self.history) < 5:
            return {"status": "insufficient_data", "adjustments": []}
        
        recent = self.history[-10:]
        success_rate = sum(1 for r in recent if r["success"]) / len(recent)
        avg_evals = sum(r["evals"] for r in recent) / len(recent)
        
        adjustments = []
        
        if success_rate < 0.5:
            adjustments.append({
                "type": "increase_budget",
                "reason": "Success rate below 50%",
                "action": "Increase generations or population size"
            })
        
        if avg_evals > 5000:
            adjustments.append({
                "type": "improve_seeding",
                "reason": "Average evaluations too high",
                "action": "Improve knowledge base seeding"
            })
        
        if success_rate > 0.9:
            adjustments.append({
                "type": "reduce_budget",
                "reason": "Success rate very high, can reduce budget",
                "action": "Reduce generations to save compute"
            })
        
        self.adjustments.extend(adjustments)
        
        return {
            "status": "analyzed",
            "success_rate": success_rate,
            "avg_evals": avg_evals,
            "adjustments": adjustments
        }
    
    def apply_adjustments(self, config):
        """Apply suggested adjustments to config."""
        analysis = self.analyze_performance()
        
        for adj in analysis.get("adjustments", []):
            if adj["type"] == "increase_budget":
                config["generations"] = config.get("generations", 100) * 2
                config["pop_size"] = config.get("pop_size", 30) + 20
            elif adj["type"] == "reduce_budget":
                config["generations"] = max(50, config.get("generations", 100) // 2)
            elif adj["type"] == "improve_seeding":
                config["seed_from_kb"] = True
                config["max_kb_seeds"] = config.get("max_kb_seeds", 3) + 2
        
        return config
    
    def get_metrics(self):
        """Get current metrics."""
        if not self.history:
            return {"total": 0, "success_rate": 0, "avg_evals": 0}
        
        total = len(self.history)
        successes = sum(1 for r in self.history if r["success"])
        avg_evals = sum(r["evals"] for r in self.history) / total
        
        return {
            "total": total,
            "successes": successes,
            "success_rate": successes / total,
            "avg_evals": avg_evals,
            "recent_adjustments": self.adjustments[-5:]
        }
