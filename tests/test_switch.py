import unittest
import time
from src.core.switch.dead_man_switch import DeadManSwitch, SwitchState

class TestDeadManSwitch(unittest.TestCase):
    def setUp(self):
        # 1 day heartbeat, 2 days warning, 3 days trigger
        self.sw = DeadManSwitch(1, 2, 3)
        self.sw.add_channel("GovCert", "GovAPI", 0.7)
        self.sw.add_channel("Legal", "Lawyer", 0.4)

    def test_state_transitions(self):
        # Normal
        self.assertEqual(self.sw.update_state(), SwitchState.DORMANT)
        
        # Simulate 2.1 days silence -> Warning
        self.sw.last_heartbeat = time.time() - (2.1 * 24 * 3600)
        self.assertEqual(self.sw.update_state(), SwitchState.WARNING)
        
        # Simulate 3.1 days silence -> Critical
        self.sw.last_heartbeat = time.time() - (3.1 * 24 * 3600)
        self.assertEqual(self.sw.update_state(), SwitchState.CRITICAL)

    def test_verification_logic(self):
        self.sw.last_heartbeat = time.time() - (4 * 24 * 3600)
        self.sw.update_state() # Now Critical
        
        # Case 1: Insufficient weight (Legal only = 0.4 < 0.6)
        self.assertFalse(self.sw.verify_death(["Legal"]))
        
        # Case 2: Sufficient weight (GovCert = 0.7 >= 0.6)
        self.assertTrue(self.sw.verify_death(["GovCert"]))
        self.assertEqual(self.sw.state, SwitchState.TRIGGERED)

if __name__ == "__main__":
    unittest.main()
