"""
ACID Plugin System
Extensible plugin architecture for custom discovery strategies.
"""
import time
import json


class Plugin:
    """Base class for ACID plugins."""
    
    def __init__(self, name, version="1.0.0"):
        self.name = name
        self.version = version
        self.enabled = False
        self.hooks = {}
    
    def enable(self):
        """Enable the plugin."""
        self.enabled = True
        self.on_enable()
    
    def disable(self):
        """Disable the plugin."""
        self.enabled = False
        self.on_disable()
    
    def on_enable(self):
        """Called when plugin is enabled."""
        pass
    
    def on_disable(self):
        """Called when plugin is disabled."""
        pass
    
    def register_hook(self, hook_name, callback):
        """Register a hook callback."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
    
    def trigger_hook(self, hook_name, *args, **kwargs):
        """Trigger a hook."""
        if hook_name in self.hooks:
            results = []
            for callback in self.hooks[hook_name]:
                try:
                    results.append(callback(*args, **kwargs))
                except Exception as e:
                    results.append({"error": str(e)})
            return results
        return []


class PluginRegistry:
    """Registry for managing plugins."""
    
    def __init__(self):
        self.plugins = {}
    
    def register(self, plugin):
        """Register a plugin."""
        self.plugins[plugin.name] = plugin
        return plugin.name
    
    def get(self, name):
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def enable(self, name):
        """Enable a plugin."""
        plugin = self.plugins.get(name)
        if plugin:
            plugin.enable()
            return True
        return False
    
    def disable(self, name):
        """Disable a plugin."""
        plugin = self.plugins.get(name)
        if plugin:
            plugin.disable()
            return True
        return False
    
    def list_plugins(self):
        """List all registered plugins."""
        return [
            {
                "name": p.name,
                "version": p.version,
                "enabled": p.enabled
            }
            for p in self.plugins.values()
        ]
    
    def trigger_hook(self, hook_name, *args, **kwargs):
        """Trigger a hook across all enabled plugins."""
        results = []
        for plugin in self.plugins.values():
            if plugin.enabled:
                results.extend(plugin.trigger_hook(hook_name, *args, **kwargs))
        return results


# Built-in plugins

class LoggingPlugin(Plugin):
    """Plugin that logs all discovery events."""
    
    def __init__(self):
        super().__init__("logging", "1.0.0")
        self.logs = []
        self.register_hook("solve_started", self.on_solve_started)
        self.register_hook("solve_complete", self.on_solve_complete)
        self.register_hook("solve_failed", self.on_solve_failed)
    
    def on_solve_started(self, solve_id, problem):
        self.logs.append({
            "event": "solve_started",
            "solve_id": solve_id,
            "problem": problem,
            "timestamp": time.time()
        })
    
    def on_solve_complete(self, solve_id, time_taken, evals):
        self.logs.append({
            "event": "solve_complete",
            "solve_id": solve_id,
            "time": time_taken,
            "evals": evals,
            "timestamp": time.time()
        })
    
    def on_solve_failed(self, solve_id, reason):
        self.logs.append({
            "event": "solve_failed",
            "solve_id": solve_id,
            "reason": reason,
            "timestamp": time.time()
        })
    
    def get_logs(self, limit=50):
        return self.logs[-limit:]


class MetricsPlugin(Plugin):
    """Plugin that collects metrics."""
    
    def __init__(self):
        super().__init__("metrics", "1.0.0")
        self.metrics = {
            "total_solves": 0,
            "total_successes": 0,
            "total_failures": 0,
            "total_evals": 0,
            "total_time": 0
        }
        self.register_hook("solve_started", self.on_solve_started)
        self.register_hook("solve_complete", self.on_solve_complete)
        self.register_hook("solve_failed", self.on_solve_failed)
    
    def on_solve_started(self, solve_id, problem):
        self.metrics["total_solves"] += 1
    
    def on_solve_complete(self, solve_id, time_taken, evals):
        self.metrics["total_successes"] += 1
        self.metrics["total_time"] += time_taken
        self.metrics["total_evals"] += evals
    
    def on_solve_failed(self, solve_id, reason):
        self.metrics["total_failures"] += 1
    
    def get_metrics(self):
        return dict(self.metrics)


def create_default_registry():
    """Create a plugin registry with default plugins."""
    registry = PluginRegistry()
    registry.register(LoggingPlugin())
    registry.register(MetricsPlugin())
    return registry
