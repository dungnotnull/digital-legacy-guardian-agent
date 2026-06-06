from enum import Enum
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field

class Role(Enum):
    OWNER = "owner"
    EXECUTOR = "executor"
    TRUSTEE = "trustee"
    BENEFICIARY = "beneficiary"
    LEGAL_AUDITOR = "legal_auditor"

@dataclass
class ApprovalRequest:
    request_id: str
    action: str
    target_asset: str
    required_roles: List[Role]
    threshold: int
    approvals: Set[str] = field(default_factory=set) # set of user_ids
    status: str = "pending"

class GovernanceEngine:
    """
    Role-Based Access Control (RBAC) and Multi-Party Approval Logic.
    Prevents any single individual (even the executor) from unilaterally releasing assets.
    """
    def __init__(self):
        self.user_roles: Dict[str, Role] = {}
        self.requests: Dict[str, ApprovalRequest] = {}

    def assign_role(self, user_id: str, role: Role):
        self.user_roles[user_id] = role

    def create_request(self, request_id: str, action: str, asset_id: str, roles: List[Role], threshold: int):
        self.requests[request_id] = ApprovalRequest(request_id, action, asset_id, roles, threshold)

    def approve(self, request_id: str, user_id: str):
        if request_id not in self.requests:
            raise ValueError("Request not found")
        
        req = self.requests[request_id]
        user_role = self.user_roles.get(user_id)
        
        if user_role not in req.required_roles:
            raise PermissionError(f"User {user_id} with role {user_role} is not authorized for this request.")
        
        req.approvals.add(user_id)
        if len(req.approvals) >= req.threshold:
            req.status = "approved"

    def is_approved(self, request_id: str) -> bool:
        return self.requests.get(request_id).status == "approved" if request_id in self.requests else False

if __name__ == "__main__":
    gov = GovernanceEngine()
    gov.assign_role("bob", Role.EXECUTOR)
    gov.assign_role("carol", Role.TRUSTEE)
    gov.assign_role("dave", Role.BENEFICIARY)
    
    # Release asset_01 requires 2 approvals from [EXECUTOR, TRUSTEE]
    gov.create_request("req_1", "RELEASE", "asset_01", [Role.EXECUTOR, Role.TRUSTEE], 2)
    
    gov.approve("req_1", "bob") # OK
    print(f"Status after Bob: {gov.is_approved('req_1')}") # False
    
    try:
        gov.approve("req_1", "dave") # Should fail - Beneficiary cannot approve
    except PermissionError as e:
        print(f"Expected error: {e}")
        
    gov.approve("req_1", "carol") # OK
    print(f"Status after Carol: {gov.is_approved('req_1')}") # True
