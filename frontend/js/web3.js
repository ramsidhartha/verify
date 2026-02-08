/**
 * Web3 Integration for Verifi Protocol
 * Connects to deployed VerifiTrust contract on Polygon Amoy
 */

// Contract deployed on Polygon Amoy
const CONTRACT_ADDRESS = "0x6e0aB964C76b37110F1e1eFDA5819872b770D117";
const CHAIN_ID = 80002; // Polygon Amoy

// Contract ABI (simplified for our use case)
const CONTRACT_ABI = [
    // Register as validator
    "function registerValidator() external",
    // Submit proof
    "function submitProof(uint256 _taskId, string calldata _evidenceHash, bool _outcome) external",
    // Read validator info
    "function validators(address) view returns (address wallet, uint256 reputation, uint256 totalTasksCompleted, bool isActive)",
    // Get validations for task
    "function getValidations(uint256 _taskId) view returns (tuple(uint256 taskId, string evidenceHash, bool outcome, uint256 timestamp)[])",
    // Events
    "event ValidatorRegistered(address indexed validator)",
    "event ProofSubmitted(uint256 indexed taskId, address indexed validator, bool outcome, string evidenceHash)",
    "event ReputationIncreased(address indexed validator, uint256 newScore)"
];

// State
let provider = null;
let signer = null;
let contract = null;
let connectedWallet = null;

/**
 * Check if MetaMask is installed
 */
function isMetaMaskInstalled() {
    return typeof window.ethereum !== 'undefined' && window.ethereum.isMetaMask;
}

/**
 * Switch to Polygon Amoy network
 */
async function switchToAmoy() {
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: '0x' + CHAIN_ID.toString(16) }],
        });
    } catch (switchError) {
        // Network not added, add it
        if (switchError.code === 4902) {
            await window.ethereum.request({
                method: 'wallet_addEthereumChain',
                params: [{
                    chainId: '0x' + CHAIN_ID.toString(16),
                    chainName: 'Polygon Amoy Testnet',
                    nativeCurrency: {
                        name: 'POL',
                        symbol: 'POL',
                        decimals: 18
                    },
                    rpcUrls: ['https://rpc-amoy.polygon.technology'],
                    blockExplorerUrls: ['https://amoy.polygonscan.com']
                }]
            });
        }
    }
}

/**
 * Connect to MetaMask
 */
async function connectWallet() {
    if (!isMetaMaskInstalled()) {
        showToast('Please install MetaMask to continue', 'error');
        window.open('https://metamask.io/download/', '_blank');
        return null;
    }

    try {
        // Request account access
        const accounts = await window.ethereum.request({
            method: 'eth_requestAccounts'
        });

        if (accounts.length === 0) {
            showToast('No accounts found', 'error');
            return null;
        }

        // Switch to Amoy network
        await switchToAmoy();

        // Set up ethers
        provider = new ethers.BrowserProvider(window.ethereum);
        signer = await provider.getSigner();
        connectedWallet = accounts[0];

        // Connect to contract
        contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);

        // Save to storage
        localStorage.setItem('wallet', connectedWallet);

        // Update UI
        updateWalletUI();
        showToast('Wallet connected!', 'success');

        return connectedWallet;
    } catch (error) {
        console.error('Connection error:', error);
        showToast('Failed to connect wallet', 'error');
        return null;
    }
}

/**
 * Disconnect wallet
 */
function disconnectWallet() {
    connectedWallet = null;
    provider = null;
    signer = null;
    contract = null;
    localStorage.removeItem('wallet');
    updateWalletUI();
    showToast('Wallet disconnected', 'info');
}

/**
 * Get connected wallet
 */
function getWallet() {
    if (connectedWallet) return connectedWallet;
    return localStorage.getItem('wallet');
}

/**
 * Update wallet button UI
 */
function updateWalletUI() {
    const walletBtn = document.querySelector('.wallet-btn, #connectWalletBtn, [data-wallet-btn]');
    if (!walletBtn) return;

    const wallet = getWallet();
    if (wallet) {
        walletBtn.textContent = wallet.slice(0, 6) + '...' + wallet.slice(-4);
        walletBtn.classList.add('connected');
        walletBtn.onclick = disconnectWallet;
    } else {
        walletBtn.textContent = 'Connect Wallet';
        walletBtn.classList.remove('connected');
        walletBtn.onclick = connectWallet;
    }
}

// ============================================================================
// Contract Interactions
// ============================================================================

/**
 * Register as a validator on-chain
 */
async function registerValidator() {
    if (!contract) {
        showToast('Please connect wallet first', 'error');
        await connectWallet();
        return null;
    }

    try {
        showToast('Signing transaction...', 'info');
        const tx = await contract.registerValidator();
        showToast('Transaction submitted! Waiting for confirmation...', 'info');

        const receipt = await tx.wait();
        showToast('Successfully registered as validator!', 'success');

        return receipt;
    } catch (error) {
        console.error('Registration error:', error);
        if (error.message.includes('Already registered')) {
            showToast('You are already registered as a validator', 'info');
        } else {
            showToast('Registration failed: ' + (error.reason || error.message), 'error');
        }
        return null;
    }
}

/**
 * Submit verification proof on-chain
 */
async function submitProofOnChain(taskId, evidenceHash, passed) {
    if (!contract) {
        showToast('Please connect wallet first', 'error');
        await connectWallet();
        return null;
    }

    try {
        // Convert task ID to number (remove prefixes)
        const numericTaskId = parseInt(taskId.replace(/\D/g, '')) || Date.now();

        showToast('Signing transaction...', 'info');
        const tx = await contract.submitProof(numericTaskId, evidenceHash, passed);
        showToast('Transaction submitted! Waiting for confirmation...', 'info');

        const receipt = await tx.wait();
        showToast('Proof submitted on-chain! +10 reputation', 'success');

        return receipt;
    } catch (error) {
        console.error('Submit proof error:', error);
        showToast('Failed to submit proof: ' + (error.reason || error.message), 'error');
        return null;
    }
}

/**
 * Get validator info from chain
 */
async function getValidatorInfo(address) {
    if (!contract) {
        // Create read-only provider
        const readProvider = new ethers.JsonRpcProvider('https://rpc-amoy.polygon.technology');
        const readContract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, readProvider);

        try {
            const info = await readContract.validators(address);
            return {
                wallet: info.wallet,
                reputation: Number(info.reputation),
                totalTasksCompleted: Number(info.totalTasksCompleted),
                isActive: info.isActive
            };
        } catch (error) {
            console.error('Error fetching validator:', error);
            return null;
        }
    }

    try {
        const info = await contract.validators(address);
        return {
            wallet: info.wallet,
            reputation: Number(info.reputation),
            totalTasksCompleted: Number(info.totalTasksCompleted),
            isActive: info.isActive
        };
    } catch (error) {
        console.error('Error fetching validator:', error);
        return null;
    }
}

// ============================================================================
// Toast Notifications
// ============================================================================

function showToast(message, type = 'info') {
    // Remove existing toasts
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;

    // Add styles if not present
    if (!document.getElementById('toast-styles')) {
        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            .toast {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 16px 24px;
                border-radius: 12px;
                background: #1a1a2e;
                color: white;
                display: flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                z-index: 10000;
                animation: slideIn 0.3s ease;
            }
            .toast-success { background: #059669; }
            .toast-error { background: #dc2626; }
            .toast-info { background: #2563eb; }
            .toast button {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                opacity: 0.7;
            }
            .toast button:hover { opacity: 1; }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

// ============================================================================
// Initialize
// ============================================================================

// Auto-reconnect on page load
document.addEventListener('DOMContentLoaded', async () => {
    updateWalletUI();

    // Check if already connected
    const savedWallet = localStorage.getItem('wallet');
    if (savedWallet && isMetaMaskInstalled()) {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_accounts' });
            if (accounts.length > 0 && accounts[0].toLowerCase() === savedWallet.toLowerCase()) {
                connectedWallet = accounts[0];
                provider = new ethers.BrowserProvider(window.ethereum);
                signer = await provider.getSigner();
                contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);
                updateWalletUI();
            }
        } catch (e) {
            console.log('Auto-connect failed:', e);
        }
    }
});

// Listen for account changes
if (typeof window.ethereum !== 'undefined') {
    window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length === 0) {
            disconnectWallet();
        } else {
            connectedWallet = accounts[0];
            localStorage.setItem('wallet', connectedWallet);
            updateWalletUI();
            location.reload();
        }
    });

    window.ethereum.on('chainChanged', () => {
        location.reload();
    });
}
