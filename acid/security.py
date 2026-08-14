"""
ACID Security
Authentication, authorization, rate limiting, audit trail.
"""
import time
import hashlib
import json


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, rate=10, burst=20):
        self.rate = rate  # tokens per second
        self.burst = burst  # max tokens
        self.buckets = {}  # user_id -> (tokens, last_time)
    
    def allow(self, user_id):
        """Check if a request is allowed."""
        now = time.time()
        
        if user_id not in self.buckets:
            self.buckets[user_id] = (self.burst - 1, now)
            return True
        
        tokens, last_time = self.buckets[user_id]
        
        # Add tokens based on elapsed time
        elapsed = now - last_time
        tokens = min(self.burst, tokens + elapsed * self.rate)
        
        if tokens >= 1:
            self.buckets[user_id] = (tokens - 1, now)
            return True
        else:
            self.buckets[user_id] = (tokens, now)
            return False
    
    def get_remaining(self, user_id):
        """Get remaining tokens for a user."""
        if user_id not in self.buckets:
            return self.burst
        
        tokens, last_time = self.buckets[user_id]
        elapsed = time.time() - last_time
        return min(self.burst, tokens + elapsed * self.rate)


class AuditTrail:
    """Comprehensive audit trail for all system actions."""
    
    def __init__(self):
        self.entries = []
        self.max_entries = 10000
    
    def log(self, action, user_id=None, details=None, severity="info"):
        """Log an action."""
        entry = {
            "id": len(self.entries),
            "action": action,
            "user_id": user_id,
            "details": details or {},
            "severity": severity,
            "timestamp": time.time()
        }
        self.entries.append(entry)
        
        # Keep bounded
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries // 2:]
        
        return entry["id"]
    
    def get_entries(self, action=None, user_id=None, severity=None, limit=100):
        """Get audit entries with optional filters."""
        entries = self.entries
        
        if action:
            entries = [e for e in entries if e["action"] == action]
        if user_id:
            entries = [e for e in entries if e["user_id"] == user_id]
        if severity:
            entries = [e for e in entries if e["severity"] == severity]
        
        return entries[-limit:]
    
    def get_stats(self):
        """Get audit statistics."""
        total = len(self.entries)
        by_action = {}
        by_severity = {}
        
        for entry in self.entries:
            action = entry["action"]
            severity = entry["severity"]
            by_action[action] = by_action.get(action, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        return {
            "total_entries": total,
            "by_action": by_action,
            "by_severity": by_severity
        }
    
    def export(self, format="json"):
        """Export audit trail."""
        if format == "json":
            return json.dumps(self.entries, indent=2)
        return str(self.entries)


class Authenticator:
    """Simple token-based authentication."""
    
    def __init__(self):
        self.tokens = {}  # token -> user_id
        self.users = {}  # user_id -> user_data
    
    def register(self, user_id, name=None):
        """Register a user and return an API token."""
        token = hashlib.sha256(
            f"{user_id}:{time.time()}:{name}".encode()
        ).hexdigest()[:32]
        
        self.tokens[token] = user_id
        self.users[user_id] = {
            "user_id": user_id,
            "name": name or user_id,
            "created": time.time(),
            "token": token
        }
        
        return token
    
    def authenticate(self, token):
        """Authenticate a token and return user_id."""
        return self.tokens.get(token)
    
    def revoke(self, token):
        """Revoke a token."""
        if token in self.tokens:
            user_id = self.tokens[token]
            del self.tokens[token]
            if user_id in self.users:
                del self.users[user_id]
            return True
        return False
    
    def get_user(self, user_id):
        """Get user data."""
        return self.users.get(user_id)


class Authorizer:
    """Role-based authorization."""
    
    ROLES = {
        "admin": ["read", "write", "delete", "admin"],
        "user": ["read", "write"],
        "viewer": ["read"]
    }
    
    def __init__(self):
        self.user_roles = {}  # user_id -> role
    
    def set_role(self, user_id, role):
        """Set a user's role."""
        if role in self.ROLES:
            self.user_roles[user_id] = role
            return True
        return False
    
    def can(self, user_id, permission):
        """Check if a user has a permission."""
        role = self.user_roles.get(user_id, "viewer")
        return permission in self.ROLES.get(role, [])
    
    def get_role(self, user_id):
        """Get a user's role."""
        return self.user_roles.get(user_id, "viewer")


class SecurityManager:
    """Unified security manager."""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.audit = AuditTrail()
        self.authenticator = Authenticator()
        self.authorizer = Authorizer()
    
    def check_request(self, user_id, action, token=None):
        """Full security check for a request."""
        # Rate limiting
        if not self.rate_limiter.allow(user_id):
            self.audit.log("rate_limited", user_id, {"action": action}, "warning")
            return {"allowed": False, "reason": "rate_limited"}
        
        # Authentication (if token provided)
        if token:
            auth_user = self.authenticator.authenticate(token)
            if auth_user != user_id:
                self.audit.log("auth_failed", user_id, {"action": action}, "error")
                return {"allowed": False, "reason": "auth_failed"}
        
        # Authorization
        permission = "write" if action in ["solve", "store_artifact"] else "read"
        if not self.authorizer.can(user_id, permission):
            self.audit.log("authz_failed", user_id, {"action": action}, "warning")
            return {"allowed": False, "reason": "unauthorized"}
        
        # Log successful check
        self.audit.log(action, user_id, {}, "info")
        
        return {"allowed": True}
