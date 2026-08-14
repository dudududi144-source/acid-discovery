"""
ACID Deployment Pipeline
Automated deployment and versioning system.
"""
import time
import json
import hashlib


class DeploymentPipeline:
    """Manage deployments of the ACID system."""
    
    def __init__(self):
        self.deployments = []
        self.versions = {}
    
    def create_version(self, components):
        """Create a new version from components."""
        version_hash = hashlib.sha256(
            json.dumps(components, sort_keys=True).encode()
        ).hexdigest()[:12]
        
        version = {
            "hash": version_hash,
            "components": components,
            "created": time.time(),
            "status": "created"
        }
        
        self.versions[version_hash] = version
        return version_hash
    
    def deploy(self, version_hash, environment="production"):
        """Deploy a version to an environment."""
        if version_hash not in self.versions:
            return {"error": "Version not found"}
        
        deployment = {
            "id": "deploy_" + str(int(time.time() * 1000)),
            "version": version_hash,
            "environment": environment,
            "status": "deploying",
            "started": time.time()
        }
        
        self.deployments.append(deployment)
        
        # Simulate deployment steps
        steps = [
            "validate_components",
            "run_tests",
            "build_artifacts",
            "deploy_to_environment",
            "verify_deployment"
        ]
        
        for step in steps:
            deployment["current_step"] = step
            # In a real system, this would execute the step
            time.sleep(0.01)  # Simulate work
        
        deployment["status"] = "deployed"
        deployment["completed"] = time.time()
        
        return deployment
    
    def rollback(self, deployment_id):
        """Rollback a deployment."""
        for dep in self.deployments:
            if dep["id"] == deployment_id:
                dep["status"] = "rolled_back"
                dep["rolled_back_at"] = time.time()
                return dep
        
        return {"error": "Deployment not found"}
    
    def get_deployments(self, environment=None, limit=10):
        """Get deployment history."""
        deps = self.deployments
        if environment:
            deps = [d for d in deps if d["environment"] == environment]
        return deps[-limit:]
    
    def get_current_version(self, environment="production"):
        """Get the current deployed version for an environment."""
        for dep in reversed(self.deployments):
            if dep["environment"] == environment and dep["status"] == "deployed":
                return dep["version"]
        return None
    
    def to_dict(self):
        """Export pipeline state."""
        return {
            "deployments": self.deployments,
            "versions": self.versions
        }


class ComponentRegistry:
    """Registry of system components."""
    
    def __init__(self):
        self.components = {}
    
    def register(self, name, version, metadata=None):
        """Register a component."""
        key = f"{name}@{version}"
        self.components[key] = {
            "name": name,
            "version": version,
            "metadata": metadata or {},
            "registered_at": time.time()
        }
        return key
    
    def get(self, name, version=None):
        """Get a component."""
        if version:
            return self.components.get(f"{name}@{version}")
        
        # Get latest version
        matching = [k for k in self.components if k.startswith(name + "@")]
        if matching:
            return self.components[sorted(matching)[-1]]
        return None
    
    def list_components(self):
        """List all registered components."""
        return list(self.components.values())
    
    def get_versions(self, name):
        """Get all versions of a component."""
        return [
            self.components[k] for k in self.components
            if k.startswith(name + "@")
        ]
