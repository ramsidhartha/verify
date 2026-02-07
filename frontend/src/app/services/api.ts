// API service for connecting to backend
const API_BASE = 'http://localhost:8000';

export interface ClaimResponse {
  claim_id: string;
  status: string;
  coverage: number;
  tasks_count: number;
  tasks: Array<{
    task_id: string;
    description: string;
    min_validators: number;
    estimated_minutes: number;
  }>;
}

export interface Task {
  task_id: string;
  claim_id: string;
  task_type: string;
  description: string;
  min_validators: number;
  estimated_minutes: number;
  required_skills: string[];
  status: string;
}

export async function submitClaim(claimText: string, wallet: string): Promise<ClaimResponse> {
  const response = await fetch(`${API_BASE}/claims/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      claim_text: claimText,
      wallet: wallet,
      context: null,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to submit claim');
  }
  
  return response.json();
}

export async function getClaimStatus(claimId: string): Promise<any> {
  const response = await fetch(`${API_BASE}/claims/${claimId}`);
  if (!response.ok) {
    throw new Error('Failed to get claim status');
  }
  return response.json();
}

export async function getTasks(wallet: string): Promise<Task[]> {
  const response = await fetch(`${API_BASE}/tasks/?wallet=${wallet}`);
  if (!response.ok) {
    throw new Error('Failed to get tasks');
  }
  return response.json();
}

export async function registerUser(wallet: string, skills: string[]): Promise<any> {
  const response = await fetch(`${API_BASE}/users/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ wallet, skills }),
  });
  if (!response.ok) {
    throw new Error('Failed to register user');
  }
  return response.json();
}
