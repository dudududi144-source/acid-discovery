"""
ACID Dashboard
Real-time system dashboard with metrics and visualization.
"""
import time
import json


class Dashboard:
    """System dashboard with real-time metrics."""
    
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
        self.history = []
        self.alerts = []
    
    def update_metrics(self, new_metrics):
        """Update dashboard metrics."""
        self.metrics.update(new_metrics)
        self.history.append({
            "timestamp": time.time(),
            "metrics": dict(self.metrics)
        })
        
        # Keep history bounded
        if len(self.history) > 100:
            self.history = self.history[-50:]
    
    def record_solve(self, success, evals, time_taken):
        """Record a solve attempt."""
        self.metrics["solves"] += 1
        if success:
            self.metrics["successes"] += 1
            self.metrics["total_time"] += time_taken
            self.metrics["total_evals"] += evals
        else:
            self.metrics["failures"] += 1
    
    def get_summary(self):
        """Get dashboard summary."""
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
            "total_solves": self.metrics["solves"],
            "success_rate": success_rate,
            "avg_time": avg_time,
            "avg_evals": avg_evals,
            "kb_size": self.metrics["kb_size"],
            "active_users": self.metrics["active_users"],
            "alerts": len(self.alerts)
        }
    
    def add_alert(self, alert_type, message, severity="info"):
        """Add an alert."""
        self.alerts.append({
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": time.time()
        })
        
        # Keep alerts bounded
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-25:]
    
    def get_alerts(self, severity=None, limit=10):
        """Get alerts, optionally filtered by severity."""
        alerts = self.alerts
        if severity:
            alerts = [a for a in alerts if a["severity"] == severity]
        return alerts[-limit:]
    
    def get_history(self, limit=50):
        """Get metrics history."""
        return self.history[-limit:]
    
    def to_dict(self):
        """Export dashboard state."""
        return {
            "metrics": self.metrics,
            "summary": self.get_summary(),
            "alerts": self.alerts,
            "history": self.history[-20:]
        }


def generate_dashboard_html(dashboard):
    """Generate an HTML dashboard."""
    summary = dashboard.get_summary()
    
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="en">')
    html.append('<head>')
    html.append('<meta charset="UTF-8">')
    html.append('<title>ACID Dashboard</title>')
    html.append('<style>')
    html.append('body { font-family: monospace; background: #0B0E14; color: #E8ECF4; padding: 20px; }')
    html.append('.metric { display: inline-block; margin: 10px; padding: 15px; background: #141926; border-radius: 6px; }')
    html.append('.metric .value { font-size: 24px; color: #6E8EF2; }')
    html.append('.metric .label { font-size: 12px; color: #9AA4B8; }')
    html.append('.alert { padding: 8px; margin: 4px 0; background: #1A2130; border-left: 3px solid #E5B567; }')
    html.append('</style>')
    html.append('</head>')
    html.append('<body>')
    html.append('<h1>ACID Dashboard</h1>')
    
    # Metrics
    html.append('<div>')
    html.append(f'<div class="metric"><div class="value">{summary["total_solves"]}</div><div class="label">Total Solves</div></div>')
    html.append(f'<div class="metric"><div class="value">{summary["success_rate"]:.1%}</div><div class="label">Success Rate</div></div>')
    html.append(f'<div class="metric"><div class="value">{summary["avg_time"]:.1f}s</div><div class="label">Avg Time</div></div>')
    html.append(f'<div class="metric"><div class="value">{summary["kb_size"]}</div><div class="label">KB Size</div></div>')
    html.append('</div>')
    
    # Alerts
    alerts = dashboard.get_alerts(limit=5)
    if alerts:
        html.append('<h2>Alerts</h2>')
        for alert in alerts:
            html.append(f'<div class="alert">{alert["message"]}</div>')
    
    html.append('</body>')
    html.append('</html>')
    
    return '\n'.join(html)
