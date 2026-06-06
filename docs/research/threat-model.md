# Threat Model: Digital Legacy Guardian

## 1. Asset & Trust Boundary
- **Assets**: Cryptographic keys, AI memories, credentials, legal documents.
- **Trust Boundary**: The boundary between the Guardian Agent's secure enclave (TEE) and the untrusted rest of the internet/OS.

## 2. Attacker Profiles
### The Malicious Heir
- **Goal**: Trigger the Dead Man's Switch prematurely to steal assets.
- **Vector**: Collusion with other share-holders or attacking the heartbeat system.

### The Sophisticated External Hacker
- **Goal**: Compromise the vault to steal all managed digital estates.
- **Vector**: Exploiting vulnerabilities in the TEE or the cloud infrastructure.

### The Coercive State/Entity
- **Goal**: Force the user or the agent to reveal secrets.
- **Vector**: Legal subpoenas or physical coercion.

## 3. Primary Attack Vectors & Mitigations

| Threat | Attack Vector | Mitigation |
| :--- | :--- | :--- |
| **Premature Trigger** | Faking the user's death or disabling heartbeats. | **Multi-channel verification**: Require 3+ independent signals (e.g., Govt death record, Lawyer sign-off, Social inactivity). |
| **Key Leakage** | Stealing a single share from a beneficiary. | **Threshold Cryptography**: Require $k$ shares. Ensure shares are stored in hardware wallets. |
| **Agent Compromise** | Attacking the reconstruction logic. | **TEE/Enclave Execution**: Run the secret reconstruction inside a secure enclave; output only to the beneficiary. |
| **Denial of Service** | Disabling the switch to prevent heirs from getting assets. | **Decentralized Redundancy**: Distribute the "Switch" logic across multiple cloud providers. |
| **Social Engineering** | Tricking the Agent into authorizing a transfer. | **Deterministic Policy**: AI does NOT authorize; only cryptographically signed policies do. |

## 4. Failure Modes
- **Scenario A**: User loses all their shares. $\rightarrow$ **Result**: Permanent asset loss (Acceptable risk for high security).
- **Scenario B**: All beneficiaries lose their shares. $\rightarrow$ **Result**: Permanent asset loss.
- **Scenario C**: Heartbeat system fails globally. $\rightarrow$ **Result**: False trigger or failure to trigger.

## 5. Security Posture
The system adopts a **"Zero-Trust Architecture"**. No single entity (including the platform operator) should ever possess enough information to reconstruct a secret alone.
