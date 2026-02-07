// Mock data for Verifi demo

// Sample claims available for verification
export const mockClaims = [
    {
        id: 'claim-001',
        title: 'Built a DeFi Lending Protocol',
        description: 'Developed a fully functional lending protocol with flash loans, collateralization, and liquidation mechanisms on Ethereum.',
        category: 'Smart Contracts',
        difficulty: 'Advanced',
        xpReward: 500,
        tokenReward: 50,
        status: 'open',
        verifiersNeeded: 3,
        verifiersCompleted: 0,
        submittedBy: {
            name: 'alex.eth',
            avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=alex',
            trustScore: 85
        },
        createdAt: '2024-02-05',
        tags: ['Solidity', 'DeFi', 'ERC-20'],
        evidence: [
            { type: 'github', url: 'https://github.com/example/defi-lending' },
            { type: 'contract', url: 'https://etherscan.io/address/0x...' }
        ]
    },
    {
        id: 'claim-002',
        title: 'ML Model for NFT Price Prediction',
        description: 'Created a machine learning model that predicts NFT floor prices with 87% accuracy using historical data and sentiment analysis.',
        category: 'AI/ML',
        difficulty: 'Intermediate',
        xpReward: 350,
        tokenReward: 35,
        status: 'in-progress',
        verifiersNeeded: 3,
        verifiersCompleted: 1,
        submittedBy: {
            name: 'datawhiz.lens',
            avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=datawhiz',
            trustScore: 72
        },
        createdAt: '2024-02-04',
        tags: ['Python', 'TensorFlow', 'NFT'],
        evidence: [
            { type: 'github', url: 'https://github.com/example/nft-predictor' },
            { type: 'demo', url: 'https://nft-predict.demo.com' }
        ]
    },
    {
        id: 'claim-003',
        title: 'Zero-Knowledge Proof Implementation',
        description: 'Implemented a ZK-SNARK circuit for private voting on-chain using Circom and SnarkJS.',
        category: 'Cryptography',
        difficulty: 'Expert',
        xpReward: 750,
        tokenReward: 100,
        status: 'open',
        verifiersNeeded: 5,
        verifiersCompleted: 0,
        submittedBy: {
            name: 'zkmaster.eth',
            avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=zkmaster',
            trustScore: 94
        },
        createdAt: '2024-02-06',
        tags: ['ZK-SNARKs', 'Circom', 'Privacy'],
        evidence: [
            { type: 'github', url: 'https://github.com/example/zk-voting' }
        ]
    },
    {
        id: 'claim-004',
        title: 'Cross-Chain Bridge Development',
        description: 'Built a secure cross-chain bridge between Ethereum and Polygon using LayerZero.',
        category: 'Infrastructure',
        difficulty: 'Advanced',
        xpReward: 600,
        tokenReward: 60,
        status: 'completed',
        verifiersNeeded: 3,
        verifiersCompleted: 3,
        submittedBy: {
            name: 'bridgebuilder.eth',
            avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=bridge',
            trustScore: 88
        },
        createdAt: '2024-02-01',
        tags: ['LayerZero', 'Solidity', 'Cross-chain'],
        evidence: [
            { type: 'github', url: 'https://github.com/example/cross-bridge' },
            { type: 'contract', url: 'https://etherscan.io/address/0x...' }
        ]
    },
    {
        id: 'claim-005',
        title: 'DAO Governance Framework',
        description: 'Developed a modular governance framework with delegation, timelock, and multi-sig capabilities.',
        category: 'Smart Contracts',
        difficulty: 'Intermediate',
        xpReward: 400,
        tokenReward: 40,
        status: 'open',
        verifiersNeeded: 3,
        verifiersCompleted: 0,
        submittedBy: {
            name: 'govguru.eth',
            avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=govguru',
            trustScore: 79
        },
        createdAt: '2024-02-06',
        tags: ['Governance', 'DAO', 'Solidity'],
        evidence: [
            { type: 'github', url: 'https://github.com/example/dao-gov' }
        ]
    },
    {
        id: 'claim-006',
        title: 'AI-Powered Smart Contract Auditor',
        description: 'Built an AI tool that analyzes Solidity code for common vulnerabilities and suggests fixes.',
        category: 'AI/ML',
        difficulty: 'Advanced',
        xpReward: 550,
        tokenReward: 55,
        status: 'in-progress',
        verifiersNeeded: 4,
        verifiersCompleted: 2,
        submittedBy: {
            name: 'auditai.lens',
            avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=auditai',
            trustScore: 91
        },
        createdAt: '2024-02-03',
        tags: ['GPT-4', 'Security', 'Solidity'],
        evidence: [
            { type: 'github', url: 'https://github.com/example/ai-auditor' },
            { type: 'demo', url: 'https://ai-audit.demo.com' }
        ]
    }
];

// Sample verification tasks for a claim
export const mockVerificationTasks = [
    {
        id: 'task-001',
        title: 'Repository Structure Analysis',
        description: 'Verify the project has proper structure with source files, tests, and documentation.',
        type: 'automated',
        status: 'completed',
        checklist: [
            { id: 'c1', text: 'Has README.md with project description', completed: true },
            { id: 'c2', text: 'Contains source code in organized directories', completed: true },
            { id: 'c3', text: 'Includes package.json or equivalent config', completed: true },
            { id: 'c4', text: 'Test directory present with test files', completed: true }
        ]
    },
    {
        id: 'task-002',
        title: 'Code Quality Assessment',
        description: 'Review code for best practices, security patterns, and documentation.',
        type: 'manual',
        status: 'in-progress',
        checklist: [
            { id: 'c5', text: 'Code follows consistent style guidelines', completed: true },
            { id: 'c6', text: 'Functions are properly documented', completed: true },
            { id: 'c7', text: 'No obvious security vulnerabilities', completed: false },
            { id: 'c8', text: 'Error handling is implemented', completed: false }
        ]
    },
    {
        id: 'task-003',
        title: 'Functionality Verification',
        description: 'Test the claimed functionality works as described.',
        type: 'manual',
        status: 'pending',
        checklist: [
            { id: 'c9', text: 'Core features work as claimed', completed: false },
            { id: 'c10', text: 'Edge cases are handled', completed: false },
            { id: 'c11', text: 'Performance is acceptable', completed: false }
        ]
    },
    {
        id: 'task-004',
        title: 'On-Chain Verification',
        description: 'Verify deployed contracts match the source code.',
        type: 'automated',
        status: 'pending',
        checklist: [
            { id: 'c12', text: 'Contract is verified on Etherscan', completed: false },
            { id: 'c13', text: 'Bytecode matches repository', completed: false },
            { id: 'c14', text: 'Contract interactions work correctly', completed: false }
        ]
    }
];

// User profile data
export const mockUserProfile = {
    id: 'user-001',
    name: 'vitalik.eth',
    displayName: 'Vitalik Builder',
    avatar: 'https://api.dicebear.com/7.x/identicon/svg?seed=vitalik',
    bio: 'Full-stack Web3 developer | ZK enthusiast | Building the decentralized future',
    trustScore: 87,
    tier: 'Diamond',
    xp: 12450,
    nextTierXP: 15000,
    tokensEarned: 1240,
    joinedDate: '2023-06-15',
    stats: {
        claimsSubmitted: 24,
        claimsVerified: 156,
        verificationsCompleted: 89,
        accuracy: 96.5,
        streak: 14,
        rank: 42
    },
    badges: [
        { id: 'b1', name: 'Early Adopter', icon: '🌟', description: 'Joined during beta', rarity: 'legendary' },
        { id: 'b2', name: 'ZK Master', icon: '🔐', description: 'Verified 10+ ZK proofs', rarity: 'epic' },
        { id: 'b3', name: 'Code Ninja', icon: '⚔️', description: '100+ verifications', rarity: 'rare' },
        { id: 'b4', name: 'Truth Seeker', icon: '🔍', description: '95%+ accuracy', rarity: 'epic' },
        { id: 'b5', name: 'Streak Master', icon: '🔥', description: '7 day streak', rarity: 'common' },
        { id: 'b6', name: 'DeFi Expert', icon: '💰', description: 'Verified 20+ DeFi claims', rarity: 'rare' },
        { id: 'b7', name: 'AI Pioneer', icon: '🤖', description: 'First AI claim verified', rarity: 'legendary' },
        { id: 'b8', name: 'Community Helper', icon: '🤝', description: 'Helped 50+ developers', rarity: 'uncommon' }
    ],
    recentActivity: [
        { type: 'verification', claim: 'Cross-Chain Bridge Development', result: 'approved', xp: 200, date: '2024-02-06' },
        { type: 'verification', claim: 'DAO Governance Framework', result: 'approved', xp: 150, date: '2024-02-05' },
        { type: 'submission', claim: 'ZK Identity Protocol', result: 'pending', xp: 0, date: '2024-02-05' },
        { type: 'verification', claim: 'NFT Marketplace v2', result: 'rejected', xp: 50, date: '2024-02-04' },
        { type: 'badge', badge: 'Streak Master', xp: 100, date: '2024-02-03' },
        { type: 'verification', claim: 'AI Smart Contract Auditor', result: 'approved', xp: 175, date: '2024-02-02' }
    ]
};

// Tiers configuration
export const tiers = [
    { name: 'Bronze', minXP: 0, color: '#CD7F32', icon: '🥉' },
    { name: 'Silver', minXP: 1000, color: '#C0C0C0', icon: '🥈' },
    { name: 'Gold', minXP: 5000, color: '#FFD700', icon: '🥇' },
    { name: 'Platinum', minXP: 10000, color: '#E5E4E2', icon: '💎' },
    { name: 'Diamond', minXP: 15000, color: '#B9F2FF', icon: '👑' }
];

// Categories for claims
export const categories = [
    'Smart Contracts',
    'AI/ML',
    'Infrastructure',
    'Cryptography',
    'Frontend',
    'Backend',
    'Full Stack',
    'Security',
    'Data Science',
    'DevOps'
];

// Difficulty levels
export const difficulties = [
    { name: 'Beginner', color: '#10b981', xpMultiplier: 1 },
    { name: 'Intermediate', color: '#f59e0b', xpMultiplier: 1.5 },
    { name: 'Advanced', color: '#8b5cf6', xpMultiplier: 2 },
    { name: 'Expert', color: '#ec4899', xpMultiplier: 3 }
];
