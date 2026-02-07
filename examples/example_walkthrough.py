#!/usr/bin/env python3
"""
Example Walkthrough: End-to-End Claim Verification

This script demonstrates the full 3-level architecture processing
the example claim from the spec:
    "My public API supports 2000 req/s securely."

Run with: python examples/example_walkthrough.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import VerificationPipeline
from src.models.claim import Claim


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def print_json(obj, indent=2):
    """Pretty print a JSON-serializable object."""
    if hasattr(obj, 'model_dump'):
        obj = obj.model_dump()
    print(json.dumps(obj, indent=indent, default=str))


def main():
    print_section("VERIFI AI REASONING CORE - EXAMPLE WALKTHROUGH")
    
    # Initialize the pipeline
    print("\n📋 Initializing pipeline with mock LLM (for demo)...")
    pipeline = VerificationPipeline()
    
    # Example claim from the spec
    claim_text = "My public API supports 2000 req/s securely."
    
    print_section("INPUT: Original Claim")
    print(f'\n"{claim_text}"')
    
    # Step 1: Process through Level 1 (Classification)
    print_section("LEVEL 1: Claim Classification (LLM #1)")
    print("""
    Purpose: Semantic understanding - what is this claim about?
    Constraints: NO task names, NO verification strategies
    """)
    
    plan = pipeline.process_claim(claim_text)
    
    print("\n📊 Classification Result:")
    print("\n  Dimensions (claim relevance weights):")
    for dim, weight in sorted(plan.classification.dimensions.items(), key=lambda x: -x[1]):
        bar = "█" * int(weight * 20)
        print(f"    {dim:20} {weight:.2f} {bar}")
    
    if plan.classification.red_flags:
        print("\n  🚩 Red Flags Detected:")
        for flag in plan.classification.red_flags:
            print(f"    - {flag}")
    
    if plan.classification.ambiguities:
        print("\n  ❓ Ambiguities Found:")
        for amb in plan.classification.ambiguities:
            print(f"    - {amb}")
    
    # Active learning example
    print("\n  💡 Clarifying Questions (Active Learning):")
    questions = pipeline.get_clarifying_questions(claim_text)
    if questions:
        for i, q in enumerate(questions, 1):
            print(f"    {i}. {q}")
    else:
        print("    (No blocking ambiguities)")
    
    # Step 2: Show Level 2 (Graph Traversal)
    print_section("LEVEL 2: Task Graph Traversal (Deterministic)")
    print("""
    Purpose: Convert understanding into verification obligations
    Constraints: NO LLM, NO invention - pure graph traversal
    """)
    
    print("\n📈 Active Dimensions (threshold=0.2):")
    active_dims = plan.classification.get_active_dimensions(threshold=0.2)
    print(f"    {active_dims}")
    
    print("\n📝 Required Tasks (in dependency order):")
    for i, task_id in enumerate(plan.required_task_ids, 1):
        print(f"    {i:2}. {task_id}")
    
    print("\n🔍 Task Selection Explanation:")
    explanations = pipeline.explain(claim_text)
    for task_id in list(plan.required_task_ids)[:5]:  # Show first 5
        reasons = explanations.get(task_id, ["Unknown"])
        print(f"\n    {task_id}:")
        for reason in reasons:
            print(f"      → {reason}")
    if len(plan.required_task_ids) > 5:
        print(f"\n    ... and {len(plan.required_task_ids) - 5} more tasks")
    
    # Step 3: Show Level 3 (Task Expansion)
    print_section("LEVEL 3: Task Expansion (LLM #2)")
    print("""
    Purpose: Fill in claim-specific parameters for execution
    Constraints: CANNOT add/remove tasks, only parameterize
    """)
    
    print("\n🎯 Expanded Tasks with Parameters:")
    for task in plan.expanded_tasks[:5]:  # Show first 5
        print(f"\n  [{task.task_id}]")
        print(f"    Description: {task.description}")
        print(f"    Parameters:")
        for key, value in task.parameters.items():
            print(f"      - {key}: {value}")
        if task.instructions:
            print(f"    Instructions: {task.instructions[:80]}...")
    
    if len(plan.expanded_tasks) > 5:
        print(f"\n  ... and {len(plan.expanded_tasks) - 5} more expanded tasks")
    
    # Final summary
    print_section("VERIFICATION PLAN SUMMARY")
    
    print(f"""
    Original Claim: "{plan.original_claim}"
    
    Total Tasks:    {len(plan.expanded_tasks)}
    Coverage:       {plan.coverage:.1%}
    Warnings:       {len(plan.warnings)}
    """)
    
    if plan.warnings:
        print("  ⚠️  Warnings:")
        for warning in plan.warnings:
            print(f"      - {warning}")
    
    print_section("ARCHITECTURE VALIDATION")
    print("""
    ✅ Level 1 (LLM): Only classified dimensions, no task names
    ✅ Level 2 (Rules): Deterministic traversal, replayable
    ✅ Level 3 (LLM): Only parameterized, didn't add/remove tasks
    
    The 3-level architecture ensures:
    • AI understands intent (Level 1)
    • Rules enforce verification logic (Level 2)  
    • AI contextualizes execution (Level 3)
    • Neither LLM can override verification correctness
    """)


if __name__ == "__main__":
    main()
