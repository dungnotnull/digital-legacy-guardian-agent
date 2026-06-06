# ??? Digital Legacy Guardian Agent
> **Secure, Verifiable, and Legally-Aware Digital Asset Succession for the AI Era.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)
![Security](https://img.shields.io/badge/Security-AES--256--GCM%20%7C%20SSS-orange.svg)

Digital Legacy Guardian is an enterprise-grade infrastructure platform designed to solve the "Dead Man's Switch" problem for the modern age. It ensures that your most critical digital assets—cryptographic keys, AI agent memories, cloud credentials, and intellectual property—are transferred to your designated heirs only when cryptographically and legally verified.

---

## ?? Core Philosophy
**"The system never decides ownership; it only executes pre-authorized, cryptographically verifiable instructions."**

Our architecture follows a **Zero-Trust** model where no single entity (including the platform operator) can unilaterally access or transfer assets.

## ??? Architecture Layers

### 1. ?? Cryptographic Vault (`src/core/crypto`)
- **Shamir's Secret Sharing (SSS)**: High-entropy secrets are split into $k$-of-$n$ shares.
- **AES-256-GCM**: All data at rest is encrypted using authenticated encryption to prevent tampering.
- **Secure Reconstruction**: Secrets are reconstructed only in memory upon authorized trigger.

### 2. ?? Dead Man's Switch (`src/core/switch`)
- **Multi-Stage Escalation**: Transitions from `DORMANT` $\rightarrow$ `WARNING` $\rightarrow$ `CRITICAL` $\rightarrow$ `TRIGGERED`.
- **Weighted Verification**: Uses multiple independent signals (Gov APIs, Legal sign-offs, Social activity) to confirm a trigger event, preventing accidental activation.

### 3. ?? Governance Engine (`src/core/governance`)
- **RBAC**: Strict Role-Based Access Control (Owner, Executor, Trustee, Beneficiary).
- **M-of-N Approvals**: Critical assets require multiple independent approvals from designated fiduciaries before release.

### 4. ??? Estate Manager (`src/core/estate`)
- **Progressive Disclosure**: Assets are released on a schedule (e.g., Liquid funds on Day 0, Private keys on Day 30, AI Personas on Day 90).
- **Beneficiary Mapping**: Precise mapping of asset categories to specific heirs.

### 5. ?? AI Legacy Support (`src/core/ai_legacy`)
- **Persona Packaging**: Archives AI agent system prompts, hyperparameters, and vector database snapshot references.
- **Memory Transfer**: Facilitates the "inheritance" of AI-native knowledge bases.

### 6. ?? Forensic Audit Trail (`src/core/audit`)
- **Hash-Chaining**: Every event is cryptographically linked to the previous one, creating a tamper-evident ledger.
- **Integrity Verification**: Built-in tools to prove that audit logs have not been modified post-facto.

---

## ??? Technical Stack
- **Language**: Python 3.10+
- **Encryption**: `cryptography` (PyCA)
- **Security**: SHA-256 Chaining, AES-GCM, SSS
- **Design Pattern**: Orchestrator Pattern

## ?? Quick Start

### Installation
```bash
git clone https://github.com/dungnotnull/digital-legacy-guardian-agent.git
cd digital-legacy-guardian-agent
pip install cryptography
```

### Running the System Simulation
```bash
# Run the production orchestrator simulation
python src/core/production/orchestrator.py

# Run the full test suite to verify integrity
python run_tests.py
```

## ??? Security Posture
- [x] **No Plaintext Secrets**: All keys are encrypted or split.
- [x] **Deterministic Logic**: AI assists in documentation but NEVER authorizes transfers.
- [x] **Tamper-Evident Logs**: Cryptographic chaining of all administrative actions.
- [x] **Multi-Channel Verification**: Prevents "single point of failure" triggers.

## ?? License
MIT License. See `LICENSE` for details.
