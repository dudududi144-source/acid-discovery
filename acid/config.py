"""
ACID Configuration
Centralized configuration management.
"""
import json
import os


DEFAULT_CONFIG = {
    # Substrate
    "substrate": {
        "max_stack": 256,
        "max_memory": 64,
        "max_steps": 10000,
        "max_program_length": 200
    },
    
    # Discovery
    "discovery": {
        "default_generations": 200,
        "default_pop_size": 50,
        "mutation_rate": 0.15,
        "max_kb_seeds": 5
    },
    
    # Verification
    "verification": {
        "test_cases": 10,
        "determinism_runs": 5,
        "max_steps": 5000
    },
    
    # API
    "api": {
        "base_url": "https://acid-api.rabotatony.workers.dev",
        "timeout": 60,
        "rate_limit": 10,
        "rate_burst": 20
    },
    
    # Storage
    "storage": {
        "max_artifacts": 1000,
        "max_versions_per_artifact": 10,
        "max_history_entries": 100
    },
    
    # Monitoring
    "monitoring": {
        "alert_threshold_failure_rate": 0.5,
        "alert_threshold_avg_time": 10,
        "history_size": 100
    }
}


class Config:
    """Configuration manager."""
    
    def __init__(self, config=None):
        self.config = config or dict(DEFAULT_CONFIG)
    
    def get(self, key, default=None):
        """Get a config value using dot notation."""
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Set a config value using dot notation."""
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def load_from_file(self, path):
        """Load config from a JSON file."""
        try:
            with open(path, "r") as f:
                loaded = json.load(f)
                self._merge(self.config, loaded)
                return True
        except Exception:
            return False
    
    def save_to_file(self, path):
        """Save config to a JSON file."""
        try:
            with open(path, "w") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_from_env(self, prefix="ACID_"):
        """Load config from environment variables."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("__", ".")
                try:
                    self.set(config_key, json.loads(value))
                except json.JSONDecodeError:
                    self.set(config_key, value)
    
    def _merge(self, base, override):
        """Recursively merge configs."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge(base[key], value)
            else:
                base[key] = value
    
    def to_dict(self):
        """Export config as dict."""
        return dict(self.config)
    
    def to_json(self):
        """Export config as JSON."""
        return json.dumps(self.config, indent=2)


# Global config instance
config = Config()
