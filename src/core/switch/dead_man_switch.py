import time
from enum import Enum
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field

class SwitchState(Enum):
    DORMANT = "dormant"
    WARNING = "warning"
    CRITICAL = "critical"
    TRIGGERED = "triggered"

@dataclass
class VerificationChannel:
    name: str
    provider_id: str
    weight: float
    is_verified: bool = False

class DeadManSwitch:
    def __init__(self, heartbeat_interval_days: int, warning_days: int, trigger_days: int):
        self.interval = heartbeat_interval_days
        self.warning_days = warning_days
        self.trigger_days = trigger_days
        self.last_heartbeat = time.time()
        self.state = SwitchState.DORMANT
        self.channels: Dict[str, VerificationChannel] = {}

    def add_channel(self, name: str, provider: str, weight: float = 1.0):
        self.channels[name] = VerificationChannel(name, provider, weight)

    def pulse(self):
        self.last_heartbeat = time.time()
        self.state = SwitchState.DORMANT
        for ch in self.channels.values():
            ch.is_verified = False

    def update_state(self) -> SwitchState:
        elapsed = (time.time() - self.last_heartbeat) / (24 * 3600)
        if elapsed >= self.trigger_days:
            # IMPORTANT: If already triggered, stay triggered.
            if self.state == SwitchState.TRIGGERED:
                return self.state
            self.state = SwitchState.CRITICAL
        elif elapsed >= self.warning_days:
            if self.state == SwitchState.TRIGGERED:
                return self.state
            self.state = SwitchState.WARNING
        else:
            if self.state == SwitchState.TRIGGERED:
                return self.state
            self.state = SwitchState.DORMANT
        return self.state

    def verify_death(self, external_proofs: List[str]) -> bool:
        # Must be CRITICAL to move to TRIGGERED
        if self.state != SwitchState.CRITICAL:
            return False
        
        total_weight = sum(ch.weight for ch in self.channels.values())
        if total_weight == 0: return False
        
        verified_weight = 0.0
        for proof in external_proofs:
            if proof in self.channels:
                self.channels[proof].is_verified = True
                verified_weight += self.channels[proof].weight
        
        if verified_weight / total_weight >= 0.6:
            self.state = SwitchState.TRIGGERED
            return True
        return False
