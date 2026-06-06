import unittest
from src.core.governance.governance import GovernanceEngine, Role

class TestGovernance(unittest.TestCase):
    def setUp(self):
        self.gov = GovernanceEngine()
        self.gov.assign_role("alice", Role.EXECUTOR)
        self.gov.assign_role("bob", Role.TRUSTEE)
        self.gov.assign_role("charlie", Role.BENEFICIARY)

    def test_approval_thresholds(self):
        # Request needs 2 approvals from [EXECUTOR, TRUSTEE]
        self.gov.create_request("req1", "RELEASE", "a1", [Role.EXECUTOR, Role.TRUSTEE], 2)
        
        self.gov.approve("req1", "alice")
        self.assertFalse(self.gov.is_approved("req1"))
        
        self.gov.approve("req1", "bob")
        self.assertTrue(self.gov.is_approved("req1"))

    def test_unauthorized_role(self):
        self.gov.create_request("req2", "RELEASE", "a1", [Role.EXECUTOR], 1)
        with self.assertRaises(PermissionError):
            # Beneficiary cannot approve executor-only request
            self.gov.approve("req2", "charlie")

if __name__ == "__main__":
    unittest.main()
