import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any

class AuditTrail:
    """
    Layer 7: Verification & Auditing.
    """
    def __init__(self, log_file: str = "audit_chain.json"):
        self.log_file = log_file
        self.chain: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        try:
            with open(self.log_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def log_event(self, actor: str, action: str, status: str, metadata: Dict = None):
        prev_hash = self.chain[-1]["hash"] if self.chain else "GENESIS"
        
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "actor": actor,
            "action": action,
            "status": status,
            "metadata": metadata or {}
        }
        
        event_string = json.dumps(event_data, sort_keys=True) + prev_hash
        event_hash = hashlib.sha256(event_string.encode()).hexdigest()
        
        entry = {
            "data": event_data,
            "prev_hash": prev_hash,
            "hash": event_hash
        }
        
        self.chain.append(entry)
        self._save()

    def _save(self):
        with open(self.log_file, "w") as f:
            json.dump(self.chain, f, indent=4)

    def verify_chain_integrity(self) -> bool:
        # To ensure the very first entry is correct, we must verify the first hash too
        for i in range(len(self.chain)):
            curr = self.chain[i]
            prev_hash = self.chain[i-1]["hash"] if i > 0 else "GENESIS"
            
            # we MUST use exactly the same sort_keys=True and precision as log_event
            event_string = json.dumps(curr["data"], sort_keys=True) + prev_hash
            if hashlib.sha256(event_string.encode()).hexdigest() != curr["hash"]:
                return False
        return True
