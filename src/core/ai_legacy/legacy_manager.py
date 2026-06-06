from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

@dataclass
class AgentPersona:
    agent_id: str
    model_config: Dict[str, Any] # e.g. {"temperature": 0.7, "top_p": 0.9}
    system_prompt: str
    memory_snapshot_ref: str # Reference to a vector DB snapshot/backup
    capability_set: List[str] # e.g. ["web_search", "code_exec"]

class AILegacyManager:
    """
    AI Legacy Layer.
    Handles the packaging and delivery of autonomous agent identities.
    """
    def __init__(self):
        self.legacy_vault: Dict[str, AgentPersona] = {}

    def archive_agent(self, agent_id: str, persona: AgentPersona):
        # In production, this would integrate with a Vector DB (e.g. Pinecone) to trigger a snapshot
        self.legacy_vault[agent_id] = persona

    def export_inheritance_package(self, agent_id: str) -> str:
        """
        Prepares the final JSON package for the heir to restore the AI agent.
        """
        if agent_id not in self.legacy_vault:
            raise ValueError("Agent not found in legacy vault.")
        
        persona = self.legacy_vault[agent_id]
        package = {
            "version": "1.0",
            "agent_id": persona.agent_id,
            "restore_data": {
                "config": persona.model_config,
                "system_prompt": persona.system_prompt,
                "memory_ref": persona.memory_snapshot_ref,
                "capabilities": persona.capability_set
            },
            "instructions": "To restore this agent, load the memory_ref into your VectorDB and apply the system_prompt."
        }
        return json.dumps(package, indent=4)

if __name__ == "__main__":
    alm = AILegacyManager()
    persona = AgentPersona(
        "researcher_01", 
        {"temp": 0.2}, 
        "You are a legacy researcher.", 
        "snapshot_v1_2026", 
        ["pdf_reader"]
    )
    alm.archive_agent("researcher_01", persona)
    print(alm.export_inheritance_package("researcher_01"))
