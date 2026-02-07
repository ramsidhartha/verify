// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VerifiTrust
 * @dev Handles Validator Reputation and Verification Proofs
 * Focus: Immutability, Incentives, Trust
 */
contract VerifiTrust {

    // --- STRUCTS (The Schema) ---

    // 1. Validator Profile
    // Stores the identity and their accumulated trust score.
    struct Validator {
        address wallet;         // "Validator identity (wallet)"
        uint256 reputation;     // "Reputation update" (Accumulates over time)
        uint256 totalTasksCompleted; // To track experience
        bool isActive;          // Is this validator allowed to work?
    }

    // 2. Verification Record
    // Stores the permanent proof of work.
    struct Verification {
        uint256 taskId;         // "Task ID" (Links to the off-chain job)
        string evidenceHash;    // "Evidence hash" (IPFS/Cloud link to logs/screenshots)
        bool outcome;           // "Validation outcome" (Verified vs Rejected)
        uint256 timestamp;      // When did it happen?
    }

    // --- STATE VARIABLES (The Database) ---

    // Look up a Validator by their address
    mapping(address => Validator) public validators;

    // Look up validations for a specific Task ID
    // One task might be validated by multiple people
    mapping(uint256 => Verification[]) public taskValidations;

    // --- EVENTS (The "Off-chain" Logs) ---
    // This allows the Frontend to see updates without querying the blockchain constantly.
    event ValidatorRegistered(address indexed validator);
    event ProofSubmitted(uint256 indexed taskId, address indexed validator, bool outcome, string evidenceHash);
    event ReputationIncreased(address indexed validator, uint256 newScore);

    // Constructor (Runs once when you deploy)
    constructor() {
        // You (the deployer) are the first admin
    }

    // --- FUNCTIONS (The Logic) ---

    // 1. Join the Network
    // Anyone can become a validator (Permissionless), but they start with 0 trust.
    function registerValidator() external {
        require(!validators[msg.sender].isActive, "Already registered");

        validators[msg.sender] = Validator({
            wallet: msg.sender,
            reputation: 0,           // Start at zero
            totalTasksCompleted: 0,
            isActive: true
        });

        emit ValidatorRegistered(msg.sender);
    }

    // 2. Submit Proof & Earn Reputation
    // This is the CORE function. It connects the "Work" to the "Reward".
    // It takes the Task ID, the IPFS Hash (Evidence), and their Verdict (True/False).
    function submitProof(uint256 _taskId, string calldata _evidenceHash, bool _outcome) external {
        // Check: Must be a registered validator
        require(validators[msg.sender].isActive, "Not a registered validator");

        // 1. Record the Proof (Immutability)
        taskValidations[_taskId].push(Verification({
            taskId: _taskId,
            evidenceHash: _evidenceHash, // The "Pointer to Truth"
            outcome: _outcome,
            timestamp: block.timestamp
        }));

        // 2. Update Reputation (Incentives)
        // Simple Logic: +10 points for doing work.
        // In V2, you can make this complex (e.g., only pay if others agree).
        validators[msg.sender].reputation += 10;
        validators[msg.sender].totalTasksCompleted += 1;

        // 3. Emit Event (Transparency)
        emit ProofSubmitted(_taskId, msg.sender, _outcome, _evidenceHash);
        emit ReputationIncreased(msg.sender, validators[msg.sender].reputation);
    }

    // Helper: Read all validations for a task
    function getValidations(uint256 _taskId) external view returns (Verification[] memory) {
        return taskValidations[_taskId];
    }
}