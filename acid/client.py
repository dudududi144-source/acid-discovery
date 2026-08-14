"""
ACID API Client
Python client for the ACID API.
"""
import json

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class ACIDClient:
    """Client for the ACID API."""
    
    def __init__(self, base_url="https://acid-api.rabotatony.workers.dev"):
        self.base_url = base_url.rstrip("/")
        self.session_id = None
        self.user_id = None
    
    def _request(self, method, path, data=None):
        """Make an HTTP request."""
        url = self.base_url + path
        
        if HAS_HTTPX:
            if method == "GET":
                resp = httpx.get(url, timeout=30)
            elif method == "POST":
                resp = httpx.post(url, json=data, timeout=60)
            else:
                raise ValueError(f"Unsupported method: {method}")
            return resp.json()
        elif HAS_REQUESTS:
            if method == "GET":
                resp = requests.get(url, timeout=30)
            elif method == "POST":
                resp = requests.post(url, json=data, timeout=60)
            else:
                raise ValueError(f"Unsupported method: {method}")
            return resp.json()
        else:
            raise ImportError("No HTTP library available. Install httpx or requests.")
    
    def status(self):
        """Get system status."""
        return self._request("GET", "/api/status")
    
    def solve(self, problem, inputs=None, expected=None):
        """Submit a problem for discovery."""
        data = {"problem": problem}
        if inputs:
            data["inputs"] = inputs
        if expected:
            data["expected"] = expected
        if self.user_id:
            data["user_id"] = self.user_id
        return self._request("POST", "/api/solve", data)
    
    def get_knowledge(self):
        """Get all artifacts."""
        return self._request("GET", "/api/knowledge")
    
    def get_artifact(self, artifact_hash):
        """Get a specific artifact."""
        return self._request("GET", f"/api/knowledge/{artifact_hash}")
    
    def store_artifact(self, artifact):
        """Store an artifact."""
        return self._request("POST", "/api/knowledge", artifact)
    
    def get_analytics(self):
        """Get analytics."""
        return self._request("GET", "/api/analytics")
    
    def transfer(self, source, target, inputs=None, expected=None):
        """Run a transfer test."""
        data = {"source": source, "target": target}
        if inputs:
            data["inputs"] = inputs
        if expected:
            data["expected"] = expected
        return self._request("POST", "/api/transfer", data)
    
    def register(self, name="anonymous"):
        """Register a new user."""
        result = self._request("POST", "/api/user/register", {"name": name})
        self.user_id = result.get("user_id")
        return result
    
    def login(self, user_id):
        """Login with a user ID."""
        result = self._request("POST", "/api/user/login", {"user_id": user_id})
        self.session_id = result.get("session_id")
        self.user_id = user_id
        return result
    
    def get_evidence(self):
        """Get evidence log."""
        return self._request("GET", "/api/evidence")


def quick_solve(problem, inputs=None, expected=None):
    """Quick solve without creating a client instance."""
    client = ACIDClient()
    return client.solve(problem, inputs, expected)


def quick_status():
    """Quick status check."""
    client = ACIDClient()
    return client.status()
