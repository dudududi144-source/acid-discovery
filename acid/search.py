"""
STRUCTURED DISCOVERY ENGINE
Not just random mutation. Observe -> Hypothesize -> Construct -> Refine.
"""
import random
import time
from acid.substrate import SubstrateProgram as Program, Executor, PRIMITIVES, MAX_PROGRAM_LENGTH


class Candidate:
    """A discovered candidate with full provenance."""
    def __init__(self, program, generation=0, seed=0, parent_hash=None, mutations=None, source="random"):
        self.program = program
        self.generation = generation
        self.seed = seed
        self.parent_hash = parent_hash
        self.mutations = mutations or []
        self.source = source  # "random" | "constructed" | "mutated" | "crossover"
        self.evaluation = None
        self.verification = None
        self.novelty_status = "UNCERTAIN"
        self.transfer_status = "NOT_TESTED"
        self.created_at = time.time()

    def to_dict(self):
        return {
            "hash": self.program.hash(),
            "generation": self.generation,
            "source": self.source,
            "novelty": self.novelty_status,
            "transfer": self.transfer_status,
            "evaluation": self.evaluation,
            "mutations": self.mutations,
            "instructions": self.program.instructions,
            "constants": self.program.constants
        }



# ============================================================
# BUILDING BLOCKS - Common program fragments for discovery
# ============================================================

BLOCKS = {
    "read_pair_add": [("READ", 0), ("READ", 1), ("ADD", 0)],
    "read_add_write": [("READ", 0), ("READ", 1), ("ADD", 0), ("WRITE", 2)],
    "read_triple_add": [("READ", 0), ("READ", 1), ("ADD", 0), ("READ", 2), ("ADD", 0), ("WRITE", 3)],
    "push_write": [("PUSH", 0), ("WRITE", 1)],
    "read_write": [("READ", 0), ("WRITE", 1)],
    "dup_add": [("READ", 0), ("DUP", 0), ("ADD", 0), ("WRITE", 1)],
}


def compose_from_blocks(rng, block_names=None, extra_len=3):
    """Compose a program from building blocks + random tail."""
    from acid.substrate import PRIMITIVES, SubstrateProgram
    
    if block_names is None:
        block_names = list(BLOCKS.keys())
    
    instructions = []
    constants = [rng.randint(0, 50) for _ in range(5)]
    
    for name in block_names:
        if name in BLOCKS:
            instructions.extend(BLOCKS[name])
    
    for _ in range(extra_len):
        op = rng.choice(PRIMITIVES + ["HALT"])
        instructions.append((op, rng.randint(0, 10)))
    
    instructions.append(("HALT", 0))
    return SubstrateProgram(instructions[:200], constants)


def block_seeded_population(rng, pop_size, block_names=None):
    """Create a population seeded with block-based programs."""
    population = []
    
    for _ in range(pop_size // 3):
        name = rng.choice(list(BLOCKS.keys())) if block_names is None else rng.choice(block_names)
        population.append(compose_from_blocks(rng, [name], extra_len=rng.randint(0, 5)))
    
    while len(population) < pop_size:
        population.append(random_program(rng, max_len=25))
    
    return population


def random_program(rng, max_len=50):
    """Generate a random program."""
    length = rng.randint(5, max_len)
    constants = [rng.randint(0, 100) for _ in range(rng.randint(1, 10))]
    instructions = []
    for _ in range(length):
        op = rng.choice(PRIMITIVES + ["HALT"])
        arg = rng.randint(0, max(len(constants) - 1, 10))
        instructions.append((op, arg))
    return Program(instructions, constants)


def mutate_program(program, rng, rate=0.15):
    """Mutate a program. Returns (new_program, mutation_list)."""
    instructions = list(program.instructions)
    constants = list(program.constants)
    mutations = []

    i = 0
    while i < len(instructions):
        if rng.random() < rate:
            r = rng.random()
            if r < 0.25:
                new_op = rng.choice(PRIMITIVES + ["HALT"])
                mutations.append(f"op:{i}:{instructions[i][0]}->{new_op}")
                instructions[i] = (new_op, instructions[i][1])
            elif r < 0.45:
                mutations.append(f"arg:{i}")
                instructions[i] = (instructions[i][0], rng.randint(0, 20))
            elif r < 0.65 and len(instructions) < MAX_PROGRAM_LENGTH:
                op = rng.choice(PRIMITIVES)
                mutations.append(f"ins:{i}:{op}")
                instructions.insert(i, (op, rng.randint(0, 10)))
            elif r < 0.85 and len(instructions) > 3:
                mutations.append(f"del:{i}:{instructions[i][0]}")
                instructions.pop(i)
                i -= 1
        i += 1

    if rng.random() < 0.3 and constants:
        idx = rng.randint(0, len(constants) - 1)
        old_val = constants[idx]
        constants[idx] = rng.randint(0, 100)
        mutations.append(f"const:{idx}:{old_val}->{constants[idx]}")

    return Program(instructions, constants), mutations


def crossover(p1, p2, rng):
    """Crossover two programs."""
    if len(p1.instructions) < 2 or len(p2.instructions) < 2:
        return p1
    cut1 = rng.randint(1, len(p1.instructions) - 1)
    cut2 = rng.randint(1, len(p2.instructions) - 1)
    new_instr = p1.instructions[:cut1] + p2.instructions[cut2:]
    new_consts = list(set(p1.constants + p2.constants))[:10]
    return Program(new_instr[:MAX_PROGRAM_LENGTH], new_consts)


class DiscoveryEngine:
    """
    Structured discovery:
    Phase 1: Random exploration
    Phase 2: Observe patterns in successes
    Phase 3: Form hypotheses
    Phase 4: Construct programs testing hypotheses
    Phase 5: Refine via mutation/crossover
    """

    def __init__(self, seed=42, population_size=50, max_generations=100):
        self.rng = random.Random(seed)
        self.population_size = population_size
        self.max_generations = max_generations
        self.executor = Executor()
        self.seen_hashes = set()
        self.archive = {}
        self.observations = []
        self.hypotheses = []
        self.stats = {
            "generated": 0, "executed": 0, "verified": 0,
            "novel": 0, "failed": 0, "cannotRun": 0
        }

    def evaluate(self, program, task_fn, inputs=None):
        """Evaluate a program against a task."""
        try:
            result = self.executor.execute(program, inputs=inputs)
            self.stats["executed"] += 1
            score = task_fn(result)
            return {"score": score, "steps": result["steps"],
                    "outputs": result["outputs"][:10], "error": None}
        except Exception as e:
            self.stats["failed"] += 1
            return {"score": 0, "steps": 0, "outputs": [], "error": str(e)}

    def classify_novelty(self, program):
        """Strict novelty classification."""
        h = program.hash()
        if h in self.seen_hashes:
            return "IDENTICAL"
        self.seen_hashes.add(h)
        if len(self.seen_hashes) <= 10:
            return "STRUCTURALLY_NOVEL"
        return "UNCERTAIN"

    def observe_patterns(self, successful_programs):
        """Phase 2: Observe what patterns correlate with success."""
        if len(successful_programs) < 2:
            return []
        observations = []
        op_positions = {}
        for prog in successful_programs:
            for i, (op, arg) in enumerate(prog.instructions):
                if op not in op_positions:
                    op_positions[op] = []
                op_positions[op].append(i)
        for op, positions in op_positions.items():
            if len(positions) >= 2:
                avg_pos = sum(positions) / len(positions)
                observations.append({
                    "type": "op_position",
                    "op": op,
                    "count": len(positions),
                    "avg_position": avg_pos
                })
        self.observations = observations
        return observations

    def form_hypotheses(self, observations):
        """Phase 3: Form testable hypotheses from observations."""
        hypotheses = []
        for obs in observations:
            if obs["type"] == "op_position" and obs["count"] >= 3:
                hypotheses.append({
                    "text": f"{obs['op']} at position ~{int(obs['avg_position'])} correlates with success",
                    "op": obs["op"],
                    "position": int(obs["avg_position"]),
                    "testable": True
                })
        self.hypotheses = hypotheses[:5]
        return self.hypotheses

    def construct_from_hypothesis(self, hypothesis, task_inputs):
        """Phase 4: Construct a program testing a hypothesis."""
        op = hypothesis.get("op", "ADD")
        pos = hypothesis.get("position", 5)
        instructions = []
        constants = [self.rng.randint(0, 50) for _ in range(5)]
        for i in range(max(pos + 3, 10)):
            if i == pos:
                instructions.append((op, 0))
            elif i < 3:
                instructions.append(("READ", i % 3))
            elif i == pos + 1:
                instructions.append(("WRITE", 0))
            else:
                instructions.append((self.rng.choice(PRIMITIVES), self.rng.randint(0, 5)))
        instructions.append(("HALT", 0))
        return Program(instructions[:MAX_PROGRAM_LENGTH], constants)

    def discover(self, task_fn, inputs=None, generations=None):
        """Run the full structured discovery loop."""
        generations = generations or self.max_generations
        best_candidates = []

        # Phase 1: Random exploration
        population = [random_program(self.rng) for _ in range(self.population_size)]
        self.stats["generated"] += self.population_size

        for gen in range(generations):
            scored = []
            for prog in population:
                ev = self.evaluate(prog, task_fn, inputs)
                scored.append((ev["score"], prog, ev))
            scored.sort(key=lambda x: -x[0])

            # Track best
            if scored and scored[0][0] > 0:
                best_prog = scored[0][1]
                novelty = self.classify_novelty(best_prog)
                cand = Candidate(best_prog, generation=gen,
                               seed=self.rng.randint(0, 999999), source="random")
                cand.evaluation = {"score": scored[0][0], "steps": scored[0][2]["steps"]}
                cand.novelty_status = novelty
                self.archive[best_prog.hash()] = best_prog.canonical()
                best_candidates.append(cand)
                if novelty in ("STRUCTURALLY_NOVEL", "FUNCTIONALLY_NOVEL"):
                    self.stats["novel"] += 1

            # Phase 2-4: Observe, hypothesize, construct (every 10 gens)
            if gen % 10 == 0 and gen > 0:
                successful = [s[1] for s in scored if s[0] > 0][:10]
                if len(successful) >= 2:
                    obs = self.observe_patterns(successful)
                    hyps = self.form_hypotheses(obs)
                    for h in hyps[:2]:
                        constructed = self.construct_from_hypothesis(h, inputs)
                        self.stats["generated"] += 1
                        ev = self.evaluate(constructed, task_fn, inputs)
                        if ev["score"] > 0:
                            cand = Candidate(constructed, generation=gen,
                                           seed=self.rng.randint(0, 999999),
                                           source="constructed")
                            cand.evaluation = ev
                            cand.novelty_status = self.classify_novelty(constructed)
                            best_candidates.append(cand)

            # Phase 5: Refine - build next generation
            survivors = [s[1] for s in scored[:max(1, self.population_size // 4)]]
            new_pop = []
            while len(new_pop) < self.population_size:
                r = self.rng.random()
                if r < 0.4 and survivors:
                    parent = self.rng.choice(survivors)
                    child, muts = mutate_program(parent, self.rng)
                    new_pop.append(child)
                elif r < 0.7 and len(survivors) >= 2:
                    p1, p2 = self.rng.choice(survivors), self.rng.choice(survivors)
                    new_pop.append(crossover(p1, p2, self.rng))
                else:
                    new_pop.append(random_program(self.rng))
                self.stats["generated"] += 1
            population = new_pop

        return best_candidates

    def get_stats(self):
        return dict(self.stats)


# ============================================================
# SMART DISCOVERY - Added for powerful search
# ============================================================

def smart_mutate(program, score, rng=None):
    """Smart mutation: adapts strategy based on current score.
    
    score > 0.5: Fine-tuning (small changes)
    score > 0:   Pattern addition (add useful fragments)
    score = 0:   Exploration (big changes)
    """
    if rng is None:
        import random
        rng = random.Random()
    
    instructions = list(program.instructions)
    constants = list(program.constants)
    
    if score > 0.5:
        # FINE-TUNING
        if len(instructions) > 2:
            idx = rng.randint(0, len(instructions) - 1)
            instructions[idx] = (instructions[idx][0], rng.randint(0, 20))
    elif score > 0:
        # PATTERN ADDITION
        patterns = [
            [("READ", rng.randint(0, 3)), ("ADD", 0)],
            [("DUP", 0), ("ADD", 0)],
            [("READ", rng.randint(0, 3)), ("MUL", 0)],
        ]
        pattern = rng.choice(patterns)
        pos = rng.randint(0, len(instructions))
        for i, op in enumerate(pattern):
            instructions.insert(pos + i, op)
    else:
        # EXPLORATION
        r = rng.random()
        if r < 0.3 and len(instructions) > 0:
            idx = rng.randint(0, len(instructions) - 1)
            instructions[idx] = (rng.choice(PRIMITIVES + ["HALT"]), instructions[idx][1])
        elif r < 0.6 and len(instructions) < MAX_PROGRAM_LENGTH:
            instructions.insert(rng.randint(0, len(instructions)), (rng.choice(PRIMITIVES), rng.randint(0, 10)))
        elif len(instructions) > 3:
            instructions.pop(rng.randint(0, len(instructions) - 1))
    
    if rng.random() < 0.3 and constants:
        constants[rng.randint(0, len(constants) - 1)] = rng.randint(0, 50)
    
    return SubstrateProgram(instructions[:MAX_PROGRAM_LENGTH], constants)


def smart_discover(task_fn, inputs, expected, generations=500, pop_size=100, seed_kb=None, rng=None):
    """Smart discovery: adaptive mutation + crossover + KB seeding.
    
    This is the main discovery function that combines:
    1. Smart mutation (3 strategies based on score)
    2. Crossover (combines successful programs)
    3. KB seeding (uses known solutions as starting points)
    4. History tracking (records progress for self-improvement)
    """
    if rng is None:
        import random
        rng = random.Random()
    
    from acid.substrate import Executor
    
    # Initialize population with KB seeds
    population = []
    if seed_kb:
        for artifact in seed_kb[:pop_size // 4]:
            if hasattr(artifact, 'instructions'):
                population.append(SubstrateProgram(artifact.instructions, artifact.constants))
    
    # Fill with random programs
    while len(population) < pop_size:
        population.append(random_program(rng, max_len=25))
    
    ex = Executor()
    total_evals = 0
    best_score = 0
    history = []
    
    for gen in range(generations):
        scored = []
        for prog in population:
            try:
                result = ex.execute(prog, inputs=inputs)
                total_evals += 1
                if result["outputs"] and result["outputs"] == expected:
                    score = 1.0
                elif result["outputs"] and result["outputs"] and len(result["outputs"]) == len(expected) and all(abs(a-b) <= 1 for a,b in zip(result["outputs"], expected)):
                    score = 0.3
                else:
                    score = 0.0
                scored.append((score, prog))
                if score > best_score:
                    best_score = score
                if score >= 1.0:
                    return {"found": True, "program": prog, "evals": total_evals, "gen": gen, "history": history}
            except Exception:
                total_evals += 1
                scored.append((0.0, prog))
        
        scored.sort(key=lambda x: -x[0])
        survivors = [s[1] for s in scored[:max(2, pop_size // 4)]]
        survivor_scores = [s[0] for s in scored[:max(2, pop_size // 4)]]
        
        new_pop = [scored[0][1]] if scored else []
        while len(new_pop) < pop_size:
            r = rng.random()
            if r < 0.3 and survivors:
                idx = rng.randint(0, len(survivors) - 1)
                new_pop.append(smart_mutate(survivors[idx], survivor_scores[idx], rng))
            elif r < 0.5 and len(survivors) >= 2:
                new_pop.append(crossover(rng.choice(survivors), rng.choice(survivors)))
            else:
                new_pop.append(random_program(rng, max_len=25))
        
        population = new_pop
        history.append({"gen": gen, "evals": total_evals, "score": best_score})
    
    return {"found": False, "evals": total_evals, "gen": generations, "best_score": best_score, "history": history}

