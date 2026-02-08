"""
Gemini AI Service - Real AI integration for Verifi Protocol
Uses Gemini 2.0 Flash for claim analysis and task generation
"""
import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Use Gemini 2.0 Flash
model = genai.GenerativeModel('gemini-2.0-flash')


def classify_claim(claim_text: str, context: str = None) -> Dict[str, Any]:
    """
    Use Gemini to classify a technical claim and identify verification dimensions.
    """
    prompt = f"""You are an AI that analyzes technical claims for a verification protocol.

Analyze this technical claim and return a JSON response:

CLAIM: {claim_text}
{f'CONTEXT: {context}' if context else ''}

Return a JSON object with:
{{
    "dimensions": ["list of verification dimensions like 'performance', 'security', 'correctness', 'reproducibility'"],
    "complexity": "low" | "medium" | "high",
    "red_flags": ["list of potential issues or concerns"],
    "ambiguities": ["list of unclear aspects that need clarification"],
    "required_skills": ["list of skills needed to verify this claim"],
    "estimated_effort_hours": number
}}

Return ONLY valid JSON, no markdown or explanation."""

    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        return result
    except Exception as e:
        print(f"Gemini classification error: {e}")
        # Fallback to basic classification
        return {
            "dimensions": ["correctness", "reproducibility"],
            "complexity": "medium",
            "red_flags": [],
            "ambiguities": ["Claim needs more specific metrics"],
            "required_skills": ["general programming"],
            "estimated_effort_hours": 2
        }


def generate_verification_tasks(claim_text: str, classification: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Use Gemini to generate specific verification tasks from a claim.
    """
    prompt = f"""You are an AI that creates verification tasks for technical claims.

Given this claim and classification, generate 2-4 specific verification tasks:

CLAIM: {claim_text}
CLASSIFICATION: {json.dumps(classification)}

Each task should be independently verifiable by a validator.

Return a JSON array of tasks:
[
    {{
        "task_id": "T-001",
        "description": "Short task title",
        "instructions": "Detailed step-by-step instructions for the validator",
        "parameters": {{"key": "value"}},
        "min_validators": 2 or 3,
        "estimated_minutes": 30-120,
        "required_skills": ["skill1", "skill2"],
        "priority": "high" | "medium" | "low"
    }}
]

Return ONLY valid JSON array, no markdown or explanation."""

    try:
        response = model.generate_content(prompt)
        tasks = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        
        # Ensure task IDs are unique
        for i, task in enumerate(tasks):
            task['task_id'] = f"T-{1001 + i}"
        
        return tasks
    except Exception as e:
        print(f"Gemini task generation error: {e}")
        # Fallback to basic task
        return [{
            "task_id": "T-1001",
            "description": "Reproduce and verify the claim",
            "instructions": f"Verify the following claim: {claim_text}",
            "parameters": {},
            "min_validators": 2,
            "estimated_minutes": 60,
            "required_skills": classification.get("required_skills", ["general"]),
            "priority": "medium"
        }]


def analyze_claim_full(claim_text: str, context: str = None) -> Dict[str, Any]:
    """
    Full claim analysis - classification + task generation in one call.
    """
    # First classify
    classification = classify_claim(claim_text, context)
    
    # Then generate tasks
    tasks = generate_verification_tasks(claim_text, classification)
    
    return {
        "classification": classification,
        "tasks": tasks,
        "coverage": len(classification.get("dimensions", [])) / 4 * 100,  # Approximate coverage
        "warnings": classification.get("red_flags", [])
    }
