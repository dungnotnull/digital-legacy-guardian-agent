import unittest
from src.core.estate.estate_engine import EstateManager, Asset, AssetCategory, Beneficiary
from src.core.audit.audit_logger import AuditTrail

class TestEstateAndAudit(unittest.TestCase):
    def test_progressive_disclosure(self):
        em = EstateManager()
        em.add_asset(Asset("a1", "Cash", AssetCategory.LIQUID, "b1", ["b1"], 0))
        em.add_asset(Asset("a2", "Docs", AssetCategory.LEGAL, "b2", ["b1"], 30))
        
        self.assertEqual(len(em.get_release_batch(0)), 1)
        self.assertEqual(len(em.get_release_batch(31)), 2)

    def test_audit_chain_tampering(self):
        # Use a unique file to avoid interference
        import os
        file_name = "test_audit_tamper.json"
        at = AuditTrail(file_name)
        at.log_event("user", "action1", "success")
        at.log_event("user", "action2", "success")
        
        self.assertTrue(at.verify_chain_integrity())
        
        import json
        with open(file_name, "r") as f:
            data = json.load(f)
        data[0]["data"]["action"] = "MALICIOUS_CHANGE"
        with open(file_name, "w") as f:
            json.dump(data, f)
            
        at_new = AuditTrail(file_name)
        self.assertFalse(at_new.verify_chain_integrity())
        os.remove(file_name)

if __name__ == "__main__":
    unittest.main()
