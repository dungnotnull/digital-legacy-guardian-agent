import subprocess
import sys

tests = [
    "tests/test_crypto_sss.py",
    "tests/test_crypto_vault.py",
    "tests/test_switch.py",
    "tests/test_governance.py",
    "tests/test_estate_audit.py",
    "tests/test_integration.py"
]

passed = 0
for test in tests:
    print(f"Running {test}...", end=" ")
    result = subprocess.run([sys.executable, test], capture_output=True, text=True)
    if result.returncode == 0:
        print("? PASSED")
        passed += 1
    else:
        print("? FAILED")
        print(result.stderr)
        print(result.stdout)

print(f"\nFinal Result: {passed}/{len(tests)} tests passed.")
if passed == len(tests):
    print("SYSTEM STATUS: 100% PRODUCTION READY")
else:
    print("SYSTEM STATUS: NEEDS FIXES")
