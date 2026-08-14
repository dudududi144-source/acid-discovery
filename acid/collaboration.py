"""
ACID Collaboration
Multi-user collaboration features.
"""
import time
import json


class CollaborationSpace:
    """Shared workspace for multiple users."""
    
    def __init__(self, space_id):
        self.space_id = space_id
        self.members = {}
        self.artifacts = {}
        self.activity_log = []
        self.created = time.time()
    
    def add_member(self, user_id, role="member"):
        """Add a member to the space."""
        self.members[user_id] = {
            "user_id": user_id,
            "role": role,
            "joined": time.time(),
            "contributions": 0
        }
        self._log("member_joined", {"user_id": user_id, "role": role})
    
    def remove_member(self, user_id):
        """Remove a member from the space."""
        if user_id in self.members:
            del self.members[user_id]
            self._log("member_left", {"user_id": user_id})
    
    def share_artifact(self, artifact_hash, shared_by):
        """Share an artifact with the space."""
        self.artifacts[artifact_hash] = {
            "hash": artifact_hash,
            "shared_by": shared_by,
            "shared_at": time.time()
        }
        if shared_by in self.members:
            self.members[shared_by]["contributions"] += 1
        self._log("artifact_shared", {"hash": artifact_hash, "by": shared_by})
    
    def get_shared_artifacts(self):
        """Get all shared artifacts."""
        return list(self.artifacts.values())
    
    def get_activity(self, limit=50):
        """Get recent activity."""
        return self.activity_log[-limit:]
    
    def _log(self, event_type, data):
        """Log an activity."""
        self.activity_log.append({
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        })
        if len(self.activity_log) > 500:
            self.activity_log = self.activity_log[-250:]
    
    def to_dict(self):
        """Export space state."""
        return {
            "space_id": self.space_id,
            "members": self.members,
            "artifacts": self.artifacts,
            "activity": self.activity_log[-20:],
            "created": self.created
        }


class ArtifactMarketplace:
    """Marketplace for sharing and discovering artifacts."""
    
    def __init__(self):
        self.listings = {}
        self.categories = {}
    
    def list_artifact(self, artifact, category, description, author):
        """List an artifact in the marketplace."""
        listing_id = "listing_" + str(int(time.time() * 1000))
        self.listings[listing_id] = {
            "id": listing_id,
            "artifact": artifact,
            "category": category,
            "description": description,
            "author": author,
            "listed_at": time.time(),
            "downloads": 0,
            "rating": 0,
            "ratings": []
        }
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(listing_id)
        
        return listing_id
    
    def get_listings(self, category=None, limit=20):
        """Get marketplace listings."""
        if category:
            listing_ids = self.categories.get(category, [])
            return [self.listings[lid] for lid in listing_ids[:limit]]
        return list(self.listings.values())[:limit]
    
    def download(self, listing_id):
        """Download an artifact (increments download count)."""
        if listing_id in self.listings:
            self.listings[listing_id]["downloads"] += 1
            return self.listings[listing_id]["artifact"]
        return None
    
    def rate(self, listing_id, rating):
        """Rate an artifact (1-5)."""
        if listing_id in self.listings and 1 <= rating <= 5:
            listing = self.listings[listing_id]
            listing["ratings"].append(rating)
            listing["rating"] = sum(listing["ratings"]) / len(listing["ratings"])
            return listing["rating"]
        return None
    
    def search(self, query):
        """Search listings by description."""
        query_lower = query.lower()
        results = []
        for listing in self.listings.values():
            if query_lower in listing["description"].lower():
                results.append(listing)
        return results
    
    def get_top_rated(self, limit=10):
        """Get top rated artifacts."""
        rated = [l for l in self.listings.values() if l["rating"] > 0]
        rated.sort(key=lambda x: -x["rating"])
        return rated[:limit]
    
    def get_most_downloaded(self, limit=10):
        """Get most downloaded artifacts."""
        listings = list(self.listings.values())
        listings.sort(key=lambda x: -x["downloads"])
        return listings[:limit]
