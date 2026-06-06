from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

class AssetCategory(Enum):
    LIQUID = "liquid"           # Crypto, Cash
    ACCESS = "access"            # Passwords, Keys
    INTELLECTUAL = "intellectual" # Repos, Domains
    AI_LEGACY = "ai_legacy"      # Agent states, Weights
    LEGAL = "legal"              # Wills, Deeds

@dataclass
class Asset:
    id: str
    name: str
    category: AssetCategory
    payload_ref: str # Reference to the vault blob
    beneficiaries: List[str]
    release_day: int # Offset from trigger date

@dataclass
class Beneficiary:
    id: str
    name: str
    contact: str
    trust_score: int # 0-100
    verified_id: bool = False

class EstateManager:
    """
    Digital Estate Engine.
    Handles complex asset mapping and the Progressive Disclosure workflow.
    """
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.beneficiaries: Dict[str, Beneficiary] = {}

    def add_asset(self, asset: Asset):
        self.assets[asset.id] = asset

    def add_beneficiary(self, ben: Beneficiary):
        self.beneficiaries[ben.id] = ben

    def get_release_batch(self, current_day: int) -> List[Asset]:
        """
        Returns all assets eligible for release on the current day.
        """
        return [a for a in self.assets.values() if a.release_day <= current_day]

    def get_assets_for_beneficiary(self, ben_id: str) -> List[Asset]:
        return [a for a in self.assets.values() if ben_id in a.beneficiaries]

if __name__ == "__main__":
    em = EstateManager()
    em.add_beneficiary(Beneficiary("b1", "Alice", "a@e.com", 80))
    
    # Staged release
    em.add_asset(Asset("a1", "Immediate Funds", AssetCategory.LIQUID, "blob1", ["b1"], 0))
    em.add_asset(Asset("a2", "Private Keys", AssetCategory.ACCESS, "blob2", ["b1"], 30))
    em.add_asset(Asset("a3", "AI Brain", AssetCategory.AI_LEGACY, "blob3", ["b1"], 90))
    
    print(f"Day 0 assets: {[a.name for a in em.get_release_batch(0)]}") # Immediate Funds
    print(f"Day 45 assets: {[a.name for a in em.get_release_batch(45)]}") # Immediate + Keys
    print(f"Day 100 assets: {[a.name for a in em.get_release_batch(100)]}") # All
