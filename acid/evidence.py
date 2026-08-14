"""
EVIDENCE GRAPH
Persistent provenance tracking with logical structure.
Every claim must have evidence. No evidence = not proven.
"""
import json
import time


CLAIM_TYPES = ["FACT", "DERIVED", "INFERRED", "EXPERIMENTAL_RESULT", "UNVERIFIED", "SPECULATIVE", "UNKNOWN"]
VERDICTS = ["CONFIRMED", "REFUTED", "INCONCLUSIVE"]
COMPLETION_STATES = ["NOT_STARTED", "IMPLEMENTED", "EXECUTED", "VERIFIED", "REPRODUCED", "ACCEPTED"]


class EvidenceGraph:
    """Tracks claims, experiments, and their logical relationships."""

    def __init__(self):
        self.claims = []
        self.experiments = []
        self.verdicts = []
        self.artifacts = []

    def add_claim(self, text, claim_type="EXPERIMENTAL_RESULT", depends_on=None):
        claim = {
            "id": len(self.claims),
            "text": text,
            "type": claim_type,
            "status": "UNVERIFIED",
            "evidence_ids": [],
            "depends_on": depends_on or [],
            "timestamp": time.time()
        }
        self.claims.append(claim)
        return claim["id"]

    def add_experiment(self, claim_id, description, data, outcome):
        exp = {
            "id": len(self.experiments),
            "claim_id": claim_id,
            "description": description,
            "data": data,
            "outcome": outcome,
            "timestamp": time.time()
        }
        self.experiments.append(exp)
        if claim_id < len(self.claims):
            self.claims[claim_id]["evidence_ids"].append(exp["id"])
        return exp["id"]

    def set_verdict(self, claim_id, verdict, justification=""):
        if claim_id < len(self.claims):
            self.claims[claim_id]["status"] = verdict
            self.verdicts.append({
                "claim_id": claim_id,
                "verdict": verdict,
                "justification": justification,
                "timestamp": time.time()
            })

    def get_claim(self, claim_id):
        if claim_id >= len(self.claims):
            return None
        claim = self.claims[claim_id]
        evidence = [e for e in self.experiments if e["claim_id"] == claim_id]
        return {"claim": claim, "evidence": evidence}

    def get_unsupported_claims(self):
        return [c for c in self.claims if not c["evidence_ids"] and c["status"] != "FACT"]

    def summary(self):
        return {
            "total_claims": len(self.claims),
            "total_experiments": len(self.experiments),
            "confirmed": sum(1 for c in self.claims if c["status"] == "CONFIRMED"),
            "refuted": sum(1 for c in self.claims if c["status"] == "REFUTED"),
            "inconclusive": sum(1 for c in self.claims if c["status"] == "INCONCLUSIVE"),
            "unverified": sum(1 for c in self.claims if c["status"] == "UNVERIFIED"),
            "unsupported_claims": len(self.get_unsupported_claims())
        }

    def export(self):
        return json.dumps({
            "claims": self.claims,
            "experiments": self.experiments,
            "verdicts": self.verdicts
        }, indent=2, default=str)
