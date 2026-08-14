"""
ACID - Autonomous Computational Intelligence Discovery

A system that discovers, verifies, distills, and transfers
computational mechanisms through evolutionary search.
"""

__version__ = "4.0.0"

from acid.substrate import Program, Executor, PRIMITIVES
from acid.search import DiscoveryEngine, random_program, mutate_program
from acid.verifier import VerificationLayer
from acid.distiller import DistillationPipeline
from acid.transfer import TransferEngine
from acid.evidence import EvidenceGraph
from acid.adversary import Adversary
from acid.improver import SelfImprovementMeasurer
from acid.knowledge_graph import KnowledgeGraph, build_graph_from_history
from acid.experiment import Experiment, AblationStudy, StatisticalTest
from acid.feedback import FeedbackLoop

__all__ = [
    "Program", "Executor", "PRIMITIVES",
    "DiscoveryEngine", "random_program", "mutate_program",
    "VerificationLayer",
    "DistillationPipeline",
    "TransferEngine",
    "EvidenceGraph",
    "Adversary",
    "SelfImprovementMeasurer",
    "KnowledgeGraph", "build_graph_from_history",
    "Experiment", "AblationStudy", "StatisticalTest",
    "FeedbackLoop",
]
