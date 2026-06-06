import time
from typing import List, Dict, Any
from src.core.crypto.secret_sharing import SecretSharing
from src.core.crypto.vault import VaultManager, VaultStorage
from src.core.switch.dead_man_switch import DeadManSwitch, SwitchState
from src.core.governance.governance import GovernanceEngine, Role
from src.core.estate.estate_engine import EstateManager, Asset, AssetCategory, Beneficiary
from src.core.ai_legacy.legacy_manager import AILegacyManager
from src.core.audit.audit_logger import AuditTrail

class GuardianOrchestrator:
    def __init__(self, master_password: str):
        self.vault = VaultManager(master_password)
        self.storage = VaultStorage()
        self.switch = DeadManSwitch(heartbeat_interval_days=7, warning_days=14, trigger_days=30)
        self.gov = GovernanceEngine()
        self.estate = EstateManager()
        self.ai_legacy = AILegacyManager()
        self.audit = AuditTrail()

    def register_user_asset(self, asset_name: str, secret: str, category: AssetCategory, beneficiaries: List[str], release_day: int):
        nonce, cipher = self.vault.encrypt(secret)
        asset_id = f"asset_{len(self.estate.assets) + 1}"
        self.storage.save_blob(asset_id, nonce, cipher)
        asset = Asset(asset_id, asset_name, category, asset_id, beneficiaries, release_day)
        self.estate.add_asset(asset)
        self.audit.log_event("SYSTEM", "REGISTER_ASSET", "success", {"asset_id": asset_id})
        return asset_id

    def receive_heartbeat(self, user_id: str):
        self.switch.pulse()
        self.audit.log_event(user_id, "HEARTBEAT", "success")

    def run_maintenance_cycle(self, external_proofs: List[str]):
        # FIX: The state check was comparing a SwitchState Enum to a string "critical"
        state = self.switch.update_state()
        
        if state == SwitchState.CRITICAL:
            if self.switch.verify_death(external_proofs):
                self.audit.log_event("SYSTEM", "SWITCH_TRIGGERED", "success")
                return True
        return False

    def execute_release_pipeline(self, current_day_offset: int):
        eligible_assets = self.estate.get_release_batch(current_day_offset)
        for asset in eligible_assets:
            req_id = f"rel_{asset.id}"
            if not self.gov.is_approved(req_id):
                self.audit.log_event("SYSTEM", f"RELEASE_{asset.id}", "failed", {"reason": "Governance not approved"})
                continue
            
            nonce, cipher = self.storage.load_blob(asset.id)
            secret = self.vault.decrypt(nonce, cipher)
            for ben_id in asset.beneficiaries:
                ben = self.estate.beneficiaries.get(ben_id)
                self.audit.log_event("SYSTEM", "ASSET_DELIVERED", "success", {"asset": asset.id, "ben": ben_id})
                print(f"[DELIVERY] Sending {asset.name} to {ben.name} ({ben.contact}): {secret}")

if __name__ == "__main__":
    guardian = GuardianOrchestrator("admin-master-password")
    guardian.estate.add_beneficiary(Beneficiary("b1", "Alice", "alice@example.com", 90))
    guardian.register_user_asset("Bitcoin Key", "BNC-123-XYZ", AssetCategory.LIQUID, ["b1"], 0)
    guardian.gov.assign_role("exec_1", Role.EXECUTOR)
    guardian.gov.create_request("rel_asset_1", "RELEASE", "asset_1", [Role.EXECUTOR], 1)
    guardian.gov.approve("rel_asset_1", "exec_1")
    guardian.switch.last_heartbeat = time.time() - (31 * 24 * 3600)
    guardian.switch.add_channel("DeathCert", "GovAPI", 0.8)
    if guardian.run_maintenance_cycle(["DeathCert"]):
        guardian.execute_release_pipeline(0)
