"""
ACID Experiment Framework
Structured experiments with controls, ablations, and statistical analysis.
"""
import time
import json
import os

class Experiment:
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.results = []
        self.start_time = None
        self.end_time = None
        self.status = "pending"
    
    def run(self, run_fn):
        """Run the experiment."""
        self.start_time = time.time()
        self.status = "running"
        
        try:
            result = run_fn(self.config)
            self.results.append(result)
            self.status = "completed"
        except Exception as e:
            self.results.append({"error": str(e)})
            self.status = "failed"
        
        self.end_time = time.time()
        return self.results[-1]
    
    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0
    
    def to_dict(self):
        return {
            "name": self.name,
            "config": self.config,
            "results": self.results,
            "status": self.status,
            "duration": self.duration()
        }


class AblationStudy:
    """Run ablation studies to determine component importance."""
    
    def __init__(self, base_config, components):
        self.base_config = base_config
        self.components = components  # list of component names to ablate
        self.results = {}
    
    def run(self, run_fn):
        """Run full ablation study."""
        # Baseline (all components)
        self.results["baseline"] = run_fn(self.base_config)
        
        # Ablate each component
        for comp in self.components:
            ablated_config = dict(self.base_config)
            ablated_config["disabled_" + comp] = True
            self.results["without_" + comp] = run_fn(ablated_config)
        
        return self.results
    
    def analyze(self):
        """Analyze ablation results."""
        analysis = {}
        baseline_score = self.results.get("baseline", {}).get("score", 0)
        
        for key, result in self.results.items():
            if key == "baseline":
                continue
            score = result.get("score", 0)
            impact = baseline_score - score
            analysis[key] = {
                "score": score,
                "impact": impact,
                "importance": "HIGH" if impact > 0.2 else "MEDIUM" if impact > 0.05 else "LOW"
            }
        
        return analysis


class StatisticalTest:
    """Simple statistical tests for experiment results."""
    
    @staticmethod
    def mean(values):
        if not values:
            return 0
        return sum(values) / len(values)
    
    @staticmethod
    def std(values):
        if len(values) < 2:
            return 0
        m = StatisticalTest.mean(values)
        variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5
    
    @staticmethod
    def t_test(group1, group2):
        """Simple two-sample t-test."""
        n1, n2 = len(group1), len(group2)
        if n1 < 2 or n2 < 2:
            return {"t": 0, "significant": False}
        
        m1 = StatisticalTest.mean(group1)
        m2 = StatisticalTest.mean(group2)
        s1 = StatisticalTest.std(group1)
        s2 = StatisticalTest.std(group2)
        
        se = ((s1**2/n1) + (s2**2/n2)) ** 0.5
        if se == 0:
            return {"t": 0, "significant": False}
        
        t = (m1 - m2) / se
        # Approximate: |t| > 2 is roughly significant at p < 0.05
        significant = abs(t) > 2
        
        return {"t": t, "significant": significant, "mean1": m1, "mean2": m2}


def save_experiment(experiment, output_dir="output"):
    """Save experiment results to file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"exp_{experiment.name}.json")
    with open(filename, "w") as f:
        json.dump(experiment.to_dict(), f, indent=2)
    return filename
