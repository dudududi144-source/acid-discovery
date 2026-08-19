"""
discovery-engine: Proprietary breakthrough discovery infrastructure.

The moat comes from:
  1. Proprietary fitness functions (only you know what "good" is)
  2. Proprietary data (only you have the history/context/labels)
  3. Domain-specific primitives (operations meaningful only in your domain)

The algorithm (optuna/nevergrad) is commodity.
The moat is in what you feed it and how you evaluate.
"""

from dataclasses import dataclass, field
from typing import List, Callable, Optional, Any
import json
from datetime import datetime


@dataclass
class Primitive:
    """A domain-specific primitive operation."""
    name: str
    arity: int
    description: str
    implementation: Optional[Callable] = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "arity": self.arity,
            "description": self.description,
        }


@dataclass
class FitnessFunction:
    """A proprietary fitness function.
    
    This is the strongest moat component. Only you know
    what "good" means in your domain.
    """
    name: str
    description: str
    evaluate: Callable[[Any], float]
    constraints: List[str] = field(default_factory=list)
    
    def __call__(self, candidate: Any) -> float:
        return self.evaluate(candidate)
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "constraints": self.constraints,
        }


@dataclass
class DiscoveryResult:
    """Result of a discovery run."""
    candidate: Any
    fitness: float
    evals: int
    duration_ms: float
    primitives_used: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            "candidate": str(self.candidate),
            "fitness": self.fitness,
            "evals": self.evals,
            "duration_ms": self.duration_ms,
            "primitives_used": self.primitives_used,
            "timestamp": self.timestamp,
        }


class DiscoveryEngine:
    """
    The discovery engine.
    
    Takes a fitness function (proprietary), primitives (domain-specific),
    and budget (compute constraint). Searches for the best candidate.
    
    The algorithm (optuna/nevergrad) is commodity.
    The moat is in the fitness function and primitives.
    """
    
    def __init__(self, fitness, primitives, budget=10000, optimizer="optuna"):
        self.fitness = fitness
        self.primitives = primitives
        self.budget = budget
        self.optimizer = optimizer
        self.results = []
        self.best = None
    
    def discover(self, seed=42):
        """Run discovery and return the best result."""
        import time
        start = time.time()
        
        try:
            import optuna
            optuna.logging.set_verbosity(optuna.logging.WARNING)
            
            def objective(trial):
                candidate = self._generate_candidate(trial)
                return self.fitness(candidate)
            
            study = optuna.create_study(
                direction="maximize",
                sampler=optuna.samplers.TPESampler(seed=seed),
            )
            study.optimize(objective, n_trials=self.budget)
            
            best_candidate = self._generate_candidate(study.best_trial)
            best_fitness = study.best_value
            
        except ImportError:
            import random
            rng = random.Random(seed)
            best_candidate = None
            best_fitness = float("-inf")
            
            for _ in range(self.budget):
                candidate = self._generate_candidate_random(rng)
                fitness = self.fitness(candidate)
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_candidate = candidate
        
        duration_ms = (time.time() - start) * 1000
        
        result = DiscoveryResult(
            candidate=best_candidate,
            fitness=best_fitness,
            evals=self.budget,
            duration_ms=duration_ms,
            primitives_used=[p.name for p in self.primitives],
        )
        
        self.results.append(result)
        if self.best is None or result.fitness > self.best.fitness:
            self.best = result
        
        return result
    
    def _generate_candidate(self, trial):
        """Generate a candidate from primitives using optuna trial."""
        n_primitives = trial.suggest_int("n_primitives", 1, len(self.primitives))
        selected = []
        for i in range(n_primitives):
            idx = trial.suggest_int("primitive_" + str(i), 0, len(self.primitives) - 1)
            selected.append(self.primitives[idx])
        
        params = {}
        for i, prim in enumerate(selected):
            for j in range(prim.arity):
                params[prim.name + "_" + str(i) + "_" + str(j)] = trial.suggest_float(
                    "param_" + str(i) + "_" + str(j), -100, 100
                )
        
        return {"primitives": selected, "params": params}
    
    def _generate_candidate_random(self, rng):
        """Generate a candidate from primitives using random search."""
        n_primitives = rng.randint(1, len(self.primitives))
        selected = rng.sample(self.primitives, n_primitives)
        
        params = {}
        for i, prim in enumerate(selected):
            for j in range(prim.arity):
                params[prim.name + "_" + str(i) + "_" + str(j)] = rng.uniform(-100, 100)
        
        return {"primitives": selected, "params": params}
    
    def export_results(self):
        """Export results as JSON."""
        return json.dumps({
            "fitness": self.fitness.to_dict(),
            "primitives": [p.to_dict() for p in self.primitives],
            "budget": self.budget,
            "results": [r.to_dict() for r in self.results],
            "best": self.best.to_dict() if self.best else None,
        }, indent=2)
