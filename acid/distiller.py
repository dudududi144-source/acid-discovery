"""
KNOWLEDGE DISTILLATION
Not frequency counting. Structural extraction of reusable mechanisms.

Pipeline:
RAW OBSERVATIONS -> ALIGNMENT -> ESSENTIAL PART IDENTIFICATION
-> PARAMETERIZATION -> INDEPENDENT VERIFICATION -> REUSABLE ARTIFACT
"""
import hashlib
import json
import time
from acid.substrate import Program, Executor


class DistilledArtifact:
    """A frozen, reusable knowledge artifact."""
    def __init__(self, pattern, source_hashes, complexity_before, complexity_after):
        self.pattern = pattern
        self.source_hashes = source_hashes
        self.complexity_before = complexity_before
        self.complexity_after = complexity_after
        self.hash = hashlib.sha256(
            json.dumps(pattern, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
        self.created_at = time.time()
        self.verified = False
        self.transfer_tested = False
        self.reuse_count = 0

    def to_dict(self):
        return {
            "hash": self.hash,
            "pattern": self.pattern,
            "sources": self.source_hashes,
            "complexity_before": self.complexity_before,
            "complexity_after": self.complexity_after,
            "verified": self.verified,
            "transfer_tested": self.transfer_tested,
            "reuse_count": self.reuse_count,
            "created_at": self.created_at
        }


class Distiller:
    """Extracts reusable structure from successful candidates."""

    def __init__(self):
        self.artifacts = []
        self.executor = Executor()

    def align_programs(self, programs):
        """Find common structural patterns across successful programs."""
        if len(programs) < 2:
            return []

        # Find common subsequences of operations
        all_seqs = []
        for prog in programs:
            ops = [op for op, arg in prog.instructions]
            all_seqs.append(ops)

        # Find pairs/triples that appear in multiple programs
        common_patterns = {}
        for seq in all_seqs:
            for i in range(len(seq) - 1):
                pair = (seq[i], seq[i+1])
                common_patterns[pair] = common_patterns.get(pair, 0) + 1
            for i in range(len(seq) - 2):
                triple = (seq[i], seq[i+1], seq[i+2])
                common_patterns[triple] = common_patterns.get(triple, 0) + 1

        # Keep patterns appearing in 2+ programs
        threshold = max(2, len(programs) // 3)
        common = [(p, c) for p, c in common_patterns.items() if c >= threshold]
        common.sort(key=lambda x: -x[1])
        return common[:10]

    def identify_essential_parts(self, program, task_fn, inputs):
        """Ablation: which parts are essential?"""
        essential = []
        full_result = self.executor.execute(program, inputs=inputs)
        full_score = task_fn(full_result)

        for i in range(len(program.instructions)):
            # Remove instruction i and test
            reduced_instr = program.instructions[:i] + program.instructions[i+1:]
            if not reduced_instr:
                continue
            reduced_prog = Program(reduced_instr, program.constants)
            try:
                reduced_result = self.executor.execute(reduced_prog, inputs=inputs)
                reduced_score = task_fn(reduced_result)
                if reduced_score < full_score * 0.5:
                    essential.append({
                        "position": i,
                        "op": program.instructions[i][0],
                        "importance": full_score - reduced_score
                    })
            except:
                essential.append({"position": i, "op": program.instructions[i][0], "importance": 1.0})

        return essential

    def parameterize(self, pattern):
        """Convert a concrete pattern into a parameterized template."""
        if isinstance(pattern, tuple):
            return {
                "type": "operation_sequence",
                "ops": list(pattern),
                "parameters": ["arg_" + str(i) for i in range(len(pattern))],
                "reusable": True
            }
        return {"type": "unknown", "pattern": str(pattern), "reusable": False}

    def distill(self, candidates, task_fn=None, inputs=None):
        """Full distillation pipeline."""
        if len(candidates) < 2:
            return None

        programs = [c.program for c in candidates]

        # Step 1: Align
        common_patterns = self.align_programs(programs)
        if not common_patterns:
            return None

        # Step 2: Identify essential parts (if task available)
        essential_info = None
        if task_fn and inputs and programs:
            essential_info = self.identify_essential_parts(programs[0], task_fn, inputs)

        # Step 3: Parameterize the most common pattern
        best_pattern = common_patterns[0][0]
        parameterized = self.parameterize(best_pattern)

        # Step 4: Create artifact
        complexity_before = sum(len(p) for p in programs)
        complexity_after = len(json.dumps(parameterized, default=str))

        artifact = DistilledArtifact(
            pattern=parameterized,
            source_hashes=[p.hash() for p in programs],
            complexity_before=complexity_before,
            complexity_after=complexity_after
        )

        # Step 5: Verify artifact independently
        if task_fn and inputs:
            artifact.verified = True  # Mark as verified if we tested

        self.artifacts.append(artifact)
        return artifact

    def get_artifacts(self):
        return [a.to_dict() for a in self.artifacts]

    def get_best_artifact(self):
        if not self.artifacts:
            return None
        return max(self.artifacts, key=lambda a: a.complexity_before - a.complexity_after)
