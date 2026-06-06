import unittest
import time
from src.core.production.orchestrator import GuardianOrchestrator
from src.core.estate.estate_engine import AssetCategory, Beneficiary
from src.core.governance.governance import Role

class TestEndToEndPipeline(unittest.TestCase):
    def test_full_system(self):
        guardian = GuardianOrchestrator("prod-pass")
        guardian.estate.add_beneficiary(Beneficiary("b1", "Alice", "a@e.com", 100))
        
        asset_id = guardian.register_user_asset("Gold Wallet", "0xGOLD", AssetCategory.LIQUID, ["b1"], 0)
        
        guardian.gov.assign_role("exec_1", Role.EXECUTOR)
        guardian.gov.create_request(f"rel_{asset_id}", "RELEASE", asset_id, [Role.EXECUTOR], 1)
        guardian.gov.approve(f"rel_{asset_id}", "exec_1")
        
        # Trigger simulation
        guardian.switch.add_channel("GovCert", "GovAPI", 1.0)
        
        # CRITICAL FIX: We must call update_state() inside the orchestrator or here 
        # to ensure the state is set to CRITICAL before verify_death is called.
        guardian.switch.last_heartbeat = time.time() - (31 * 24 * 3600)
        
        # The orchestrator.run_maintenance_cycle() calls update_state() internally.
        success = guardian.run_maintenance_cycle(["GovCert"])
        self.assertTrue(success)
        
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            guardian.execute_release_pipeline(0)
        
        output = f.getvalue()
        self.assertIn("0xGOLD", output)
        self.assertIn("Alice", output)

if __name__ == "__main__":
    unittest.main()
