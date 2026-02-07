#!/usr/bin/env python3
"""
Verifi Demo - Full Claim Verification Flow

Run this to see the complete flow:
1. Submit a claim
2. AI generates tasks
3. Validators get matched
4. Results submitted
5. Blockchain records proof

Usage:
    cd verifi
    python3 demo.py
"""

import sys
sys.path.insert(0, '.')

from api.services.database import db
from api.services.ai_core import process_claim
from api.services.blockchain import blockchain, register_on_chain, submit_proof_on_chain

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def main():
    print_header("VERIFI DEMO - Lending V2 Protocol Verification")
    
    # =========================================================================
    # STEP 1: Setup Users
    # =========================================================================
    print_header("STEP 1: Creating Users")
    
    # Claimant (the protocol developer)
    claimant = db.create_user("0xClaimant_Protocol_Dev", ["defi", "solidity"])
    print(f"[OK] Claimant: {claimant['wallet']}")
    
    # Validators with different skills
    validators = [
        db.create_user("0xValidator_Alice", ["security", "smart_contracts", "defi"]),
        db.create_user("0xValidator_Bob", ["performance", "testing", "load_testing"]),
        db.create_user("0xValidator_Carol", ["correctness", "math", "interest_models"]),
    ]
    
    # Update reputations
    db.update_user("0xValidator_Alice", {"reputation": 0.92})
    db.update_user("0xValidator_Bob", {"reputation": 0.85})
    db.update_user("0xValidator_Carol", {"reputation": 0.78})
    
    for v in validators:
        print(f"[OK] Validator: {v['wallet']} | Skills: {v['skills']}")
    
    # Register on blockchain
    for v in validators:
        register_on_chain(v['wallet'])
    print("[OK] All validators registered on blockchain")
    
    # =========================================================================
    # STEP 2: Submit Claim
    # =========================================================================
    print_header("STEP 2: Submitting Claim")
    
    claim_text = """
    Verification of lending logic, liquidation parameters, and interest rate models for V2 deployment. 
    The claim asserts that the interest rate model behaves linearly within the utilization rate of 0% to 80% 
    and follows a steep exponential curve thereafter.
    
    Evidence Required:
    - Execution logs showing input parameters and returned rates.
    - Transaction hash of the test execution on Amoy Testnet.
    - Signed verification statement.
    """
    
    print(f"Claim: Lending V2 Protocol Verification")
    print(f"Submitted by: 0xClaimant_Protocol_Dev")
    
    # AI Core processes the claim
    ai_result = process_claim(claim_text)
    
    print(f"\nAI Classification:")
    for dim, score in sorted(ai_result["classification"]["dimensions"].items(), key=lambda x: -x[1]):
        if score > 0.05:
            print(f"   {dim}: {score:.0%}")
    
    # Create claim in database
    claim = db.create_claim(
        claim_text=claim_text,
        author="0xClaimant_Protocol_Dev",
        tasks=ai_result["tasks"],
        coverage=ai_result["coverage"]
    )
    
    print(f"\n[OK] Claim ID: {claim['claim_id']}")
    print(f"[OK] Tasks Generated: {len(ai_result['tasks'])}")
    
    # =========================================================================
    # STEP 3: Show Tasks by Category
    # =========================================================================
    print_header("STEP 3: Generated Verification Tasks")
    
    # Group by skill
    security_tasks = [t for t in ai_result['tasks'] if 'security' in t['required_skills']]
    perf_tasks = [t for t in ai_result['tasks'] if 'performance' in t['required_skills'] or 'load_testing' in t['required_skills']]
    correctness_tasks = [t for t in ai_result['tasks'] if 'correctness' in t['required_skills']]
    
    print(f"\nSecurity Tasks ({len(security_tasks)}):")
    for t in security_tasks[:3]:
        print(f"   - {t['task_id']} ({t['estimated_minutes']}min, {t['min_validators']} validators)")
    
    print(f"\nPerformance Tasks ({len(perf_tasks)}):")
    for t in perf_tasks[:3]:
        print(f"   - {t['task_id']} ({t['estimated_minutes']}min, {t['min_validators']} validators)")
    
    print(f"\nCorrectness Tasks ({len(correctness_tasks)}):")
    for t in correctness_tasks[:3]:
        print(f"   - {t['task_id']} ({t['estimated_minutes']}min, {t['min_validators']} validators)")
    
    # =========================================================================
    # STEP 4: Validators Accept Tasks
    # =========================================================================
    print_header("STEP 4: Validators Accept Tasks")
    
    # Get tasks for each validator
    all_tasks = db.get_claim_tasks(claim['claim_id'])
    
    # Alice accepts security tasks
    alice_tasks = [t for t in all_tasks if 'security' in t.get('required_skills', [])][:2]
    for t in alice_tasks:
        db.assign_task(t['task_id'], "0xValidator_Alice")
        print(f"[OK] Alice accepted: {t['task_type']}")
    
    # Bob accepts performance task
    bob_tasks = [t for t in all_tasks if 'performance' in t.get('required_skills', [])][:1]
    for t in bob_tasks:
        db.assign_task(t['task_id'], "0xValidator_Bob")
        print(f"[OK] Bob accepted: {t['task_type']}")
    
    # Carol accepts correctness task
    carol_tasks = [t for t in all_tasks if 'correctness' in t.get('required_skills', [])][:1]
    for t in carol_tasks:
        db.assign_task(t['task_id'], "0xValidator_Carol")
        print(f"[OK] Carol accepted: {t['task_type']}")
    
    # =========================================================================
    # STEP 5: Submit Results (with blockchain proof)
    # =========================================================================
    print_header("STEP 5: Validators Submit Results")
    
    # Alice submits security findings
    for t in alice_tasks:
        db.submit_result(t['task_id'], "0xValidator_Alice", passed=True, evidence="ipfs://QmSecurityAuditReport123")
        bc_result = submit_proof_on_chain("0xValidator_Alice", t['task_id'], "ipfs://QmSecurityAuditReport123", True)
        print(f"[OK] Alice submitted {t['task_type']}: PASSED")
        print(f"     Blockchain TX: {bc_result['tx_hash'][:30]}...")
    
    # Bob submits performance results
    for t in bob_tasks:
        db.submit_result(t['task_id'], "0xValidator_Bob", passed=True, evidence="ipfs://QmLoadTestResults456")
        bc_result = submit_proof_on_chain("0xValidator_Bob", t['task_id'], "ipfs://QmLoadTestResults456", True)
        print(f"[OK] Bob submitted {t['task_type']}: PASSED")
        print(f"     Blockchain TX: {bc_result['tx_hash'][:30]}...")
    
    # Carol submits correctness check
    for t in carol_tasks:
        db.submit_result(t['task_id'], "0xValidator_Carol", passed=True, evidence="ipfs://QmMathVerification789")
        bc_result = submit_proof_on_chain("0xValidator_Carol", t['task_id'], "ipfs://QmMathVerification789", True)
        print(f"[OK] Carol submitted {t['task_type']}: PASSED")
        print(f"     Blockchain TX: {bc_result['tx_hash'][:30]}...")
    
    # =========================================================================
    # STEP 6: Check Results
    # =========================================================================
    print_header("STEP 6: Final Status")
    
    # Validator reputations on blockchain
    print("\nValidator Reputations (on-chain):")
    for wallet in ["0xValidator_Alice", "0xValidator_Bob", "0xValidator_Carol"]:
        v = blockchain.get_validator(wallet)
        if v:
            print(f"   {wallet}: {v['reputation']} points ({v['totalTasksCompleted']} tasks)")
    
    # Blockchain events
    print("\nRecent Blockchain Events:")
    events = blockchain.get_recent_events(5)
    for e in events:
        print(f"   [{e['event']}] Block #{e['blockNumber']}")
    
    print_header("DEMO COMPLETE")
    print("""
    What happened:
    1. Claimant submitted a DeFi protocol claim
    2. AI Core generated 20 verification tasks
    3. Validators with matching skills accepted tasks
    4. Results submitted -> recorded on blockchain
    5. Validator reputations increased
    
    To run the API server:
        uvicorn api.main:app --reload
    
    Then open: http://localhost:8000/docs
    """)

if __name__ == "__main__":
    main()
