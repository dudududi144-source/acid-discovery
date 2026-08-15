"""
ACID - Autonomous Computational Intelligence Discovery

A system that discovers, verifies, distills, and transfers
computational mechanisms through evolutionary search.
"""

__version__ = "10.0.0"

from acid.substrate import Program, Executor, PRIMITIVES
from acid.search import DiscoveryEngine, random_program, mutate_program
from acid.verifier import IndependentVerifier
from acid.distiller import DistillationPipeline
from acid.transfer import TransferEngine
from acid.evidence import EvidenceGraph
from acid.adversary import Adversary
from acid.improver import SelfImprovementMeasurer
from acid.knowledge_graph import KnowledgeGraph, build_graph_from_history
from acid.experiment import Experiment, AblationStudy, StatisticalTest
from acid.feedback import FeedbackLoop
from acid.monitor import Monitor, PerformanceTracker
from acid.task_library import TASKS, get_tasks_by_category, get_tasks_by_difficulty
from acid.kg_viz import generate_svg, generate_text_report, generate_mermaid
from acid.client import ACIDClient, quick_solve, quick_status
from acid.batch import BatchRunner, ParallelRunner
from acid.testing import TestSuite, TestResult, run_all_tests
from acid.collaboration import CollaborationSpace, ArtifactMarketplace
from acid.deploy import DeploymentPipeline, ComponentRegistry
from acid.advanced_tasks import ADVANCED_TASKS, get_advanced_tasks_by_difficulty
from acid.dashboard import Dashboard, generate_dashboard_html
from acid.plugins import Plugin, PluginRegistry, LoggingPlugin, MetricsPlugin, create_default_registry
from acid.security import RateLimiter, AuditTrail, Authenticator, Authorizer, SecurityManager
from acid.config import Config, config, DEFAULT_CONFIG
from acid.utils import compute_hash, format_duration, format_number, retry, validate_inputs

__all__ = [
    "Program", "Executor", "PRIMITIVES",
    "DiscoveryEngine", "random_program", "mutate_program",
    "IndependentVerifier",
    "DistillationPipeline",
    "TransferEngine",
    "EvidenceGraph",
    "Adversary",
    "SelfImprovementMeasurer",
    "KnowledgeGraph", "build_graph_from_history",
    "Experiment", "AblationStudy", "StatisticalTest",
    "FeedbackLoop",
    "Monitor", "PerformanceTracker",
    "TASKS", "get_tasks_by_category", "get_tasks_by_difficulty",
    "generate_svg", "generate_text_report", "generate_mermaid",
    "ACIDClient", "quick_solve", "quick_status",
    "BatchRunner", "ParallelRunner",
    "TestSuite", "TestResult", "run_all_tests",
    "CollaborationSpace", "ArtifactMarketplace",
    "DeploymentPipeline", "ComponentRegistry",
    "ADVANCED_TASKS", "get_advanced_tasks_by_difficulty",
    "Dashboard", "generate_dashboard_html",
    "Plugin", "PluginRegistry", "LoggingPlugin", "MetricsPlugin", "create_default_registry",
    "RateLimiter", "AuditTrail", "Authenticator", "Authorizer", "SecurityManager",
    "Config", "config", "DEFAULT_CONFIG",
    "compute_hash", "format_duration", "format_number", "retry", "validate_inputs",
]
