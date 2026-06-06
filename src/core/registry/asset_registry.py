from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class AssetType(Enum):
    CREDENTIAL = "credential"
    CRYPTO_WALLET = "crypto_wallet"
    AI_AGENT = "ai_agent"
    KNOWLEDGE_BASE = "knowledge_base"
    DOMAIN = "domain"
    LEGAL_DOC = "legal_doc"

@dataclass
class DigitalAsset:
    id: str
    name: str
    type: AssetType
    encrypted_payload: str  # The SSS shares or encrypted reference
    beneficiaries: List[str]
    conditions: Dict = field(default_factory=dict)

class AssetRegistry:
    """
    Layer 1: Asset Registry.
    Catalogs the digital estate and maps them to beneficiaries.
    """
    def __init__(self):
        self._assets: Dict[str, DigitalAsset] = {}

    def register_asset(self, asset: DigitalAsset):
        self._assets[asset.id] = asset

    def get_asset(self, asset_id: str) -> Optional[DigitalAsset]:
        return self._assets.get(asset_id)

    def get_assets_for_beneficiary(self, beneficiary_id: str) -> List[DigitalAsset]:
        return [asset for asset in self._assets.values() if beneficiary_id in asset.beneficiaries]

if __name__ == "__main__":
    registry = AssetRegistry()
    asset = DigitalAsset(
        id="wallet_01", 
        name="Main Bitcoin Wallet", 
        type=AssetType.CRYPTO_WALLET, 
        encrypted_payload="share_1:x,y|share_2:x,y", 
        beneficiaries=["heir_01"]
    )
    registry.register_asset(asset)
    print(f"Registered: {registry.get_asset('wallet_01').name}")
