import json
from datetime import datetime
from typing import Dict, List, Any

class KnowledgeBrain:
    """
    Layer 8: Knowledge Brain.
    A structured intelligence repository that evolves through research ingestion.
    """
    def __init__(self, storage_file: str = "brain_data.json"):
        self.storage_file = storage_file
        self.knowledge_base: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"research": [], "benchmarks": [], "version": "1.0.0"}

    def save(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.knowledge_base, f, indent=4)

    def ingest_research(self, source: str, category: str, findings: str, security_impact: str):
        entry = {
            "id": len(self.knowledge_base["research"]) + 1,
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "category": category,
            "findings": findings,
            "security_impact": security_impact,
            "status": "unverified"
        }
        self.knowledge_base["research"].append(entry)
        self.save()

    def verify_finding(self, entry_id: int, verifier: str):
        for entry in self.knowledge_base["research"]:
            if entry["id"] == entry_id:
                entry["status"] = "verified"
                entry["verifier"] = verifier
                break
        self.save()

if __name__ == "__main__":
    brain = KnowledgeBrain()
    brain.ingest_research(
        "NIST", 
        "Cryptography", 
        "Post-quantum crypto guidance updated.", 
        "High: Requires transition to Kyber/Dilithium"
    )
    brain.verify_finding(1, "Lead_Security_Engineer")
    print(f"Knowledge Base: {brain.knowledge_base}")
