"""
ACID Monitoring
Real-time system health, performance tracking, alerting.
"""
import time
import json

class Monitor:
    def __init__(self):
        self.metrics = {
            "solves": 0,
            "successes": 0,
            "failures": 0,
            "total_evals": 0,
            "total_time": 0,
            "kb_size": 0,
            "active_users": 0,
            "sse_connections": 0
        }
        self.alerts = []
        self.history = []
    
    def record(self, event_type, data):
        """Record a system event."""
        entry = {
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        }
        self.history.append(entry)
        
        # Update metrics
        if event_type == "solve_started":
            self.metrics["solves"] += 1
        elif event_type == "solve_complete":
            self.metrics["successes"] += 1
            self.metrics["total_time"] += data.get("time", 0)
            self.metrics["total_evals"] += data.get("evals", 0)
        elif event_type == "solve_failed":
            self.metrics["failures"] += 1
        elif event_type == "artifact_stored":
            self.metrics["kb_size"] += 1
        
        # Keep history bounded
        if len(self.history) > 1000:
            self.history = self.history[-500:]
        
        # Check for alerts
        self._check_alerts()
        
        return entry
    
    def _check_alerts(self):
        """Check for conditions that need alerting."""
        # High failure rate
        if self.metrics["solves"] > 10:
            failure_rate = self.metrics["failures"] / self.metrics["solves"]
            if failure_rate > 0.5:
                self.alerts.append({
                    "type": "high_failure_rate",
                    "value": failure_rate,
                    "timestamp": time.time()
                })
        
        # Slow solves
        if self.metrics["successes"] > 0:
            avg_time = self.metrics["total_time"] / self.metrics["successes"]
            if avg_time > 10:
                self.alerts.append({
                    "type": "slow_solves",
                    "value": avg_time,
                    "timestamp": time.time()
                })
        
        # Keep alerts bounded
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-50:]
    
    def get_health(self):
        """Get current system health."""
        success_rate = 0
        if self.metrics["solves"] > 0:
            success_rate = self.metrics["successes"] / self.metrics["solves"]
        
        avg_time = 0
        if self.metrics["successes"] > 0:
            avg_time = self.metrics["total_time"] / self.metrics["successes"]
        
        avg_evals = 0
        if self.metrics["successes"] > 0:
            avg_evals = self.metrics["total_evals"] / self.metrics["successes"]
        
        return {
            "status": "healthy" if success_rate > 0.5 else "degraded",
            "success_rate": success_rate,
            "avg_time": avg_time,
            "avg_evals": avg_evals,
            "kb_size": self.metrics["kb_size"],
            "active_alerts": len(self.alerts),
            "metrics": self.metrics
        }
    
    def get_alerts(self):
        """Get active alerts."""
        return self.alerts[-10:]
    
    def get_history(self, limit=50):
        """Get recent event history."""
        return self.history[-limit:]
    
    def to_dict(self):
        """Export monitor state."""
        return {
            "metrics": self.metrics,
            "alerts": self.alerts,
            "health": self.get_health()
        }


class PerformanceTracker:
    """Track performance over time."""
    
    def __init__(self):
        self.snapshots = []
    
    def snapshot(self, metrics):
        """Take a performance snapshot."""
        self.snapshots.append({
            "timestamp": time.time(),
            "metrics": metrics
        })
        
        # Keep bounded
        if len(self.snapshots) > 100:
            self.snapshots = self.snapshots[-50:]
    
    def get_trend(self, metric_name, window=10):
        """Get trend for a specific metric."""
        values = []
        for snap in self.snapshots[-window:]:
            if metric_name in snap["metrics"]:
                values.append(snap["metrics"][metric_name])
        
        if len(values) < 2:
            return {"trend": "unknown", "values": values}
        
        # Simple trend: compare first half to second half
        mid = len(values) // 2
        first_avg = sum(values[:mid]) / mid
        second_avg = sum(values[mid:]) / (len(values) - mid)
        
        if second_avg > first_avg * 1.1:
            trend = "increasing"
        elif second_avg < first_avg * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {"trend": trend, "values": values, "first_avg": first_avg, "second_avg": second_avg}
