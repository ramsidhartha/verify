// Verifi Protocol - API Service
// Configure this to your deployed backend URL
const API_BASE_URL = 'https://verify-oeuf.onrender.com';

// API Service
const api = {
    // Claims
    async submitClaim(claimData) {
        const response = await fetch(`${API_BASE_URL}/claims/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(claimData)
        });
        if (!response.ok) throw new Error('Failed to submit claim');
        return response.json();
    },

    async getClaim(claimId) {
        const response = await fetch(`${API_BASE_URL}/claims/${claimId}`);
        if (!response.ok) throw new Error('Claim not found');
        return response.json();
    },

    // Tasks
    async getTasks(wallet = null, status = null) {
        let url = `${API_BASE_URL}/tasks/`;
        const params = new URLSearchParams();
        if (wallet) params.append('wallet', wallet);
        if (status) params.append('status', status);
        if (params.toString()) url += `?${params.toString()}`;

        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch tasks');
        return response.json();
    },

    async acceptTask(taskId, wallet) {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/accept`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wallet })
        });
        if (!response.ok) throw new Error('Failed to accept task');
        return response.json();
    },

    async submitResult(taskId, wallet, passed, evidence) {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wallet, passed, evidence })
        });
        if (!response.ok) throw new Error('Failed to submit result');
        return response.json();
    },

    // Users
    async registerUser(wallet, skills = []) {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wallet, skills })
        });
        if (!response.ok) throw new Error('Failed to register');
        return response.json();
    },

    async getUser(wallet) {
        const response = await fetch(`${API_BASE_URL}/users/${wallet}`);
        if (!response.ok) throw new Error('User not found');
        return response.json();
    },

    async getUserStats(wallet) {
        const response = await fetch(`${API_BASE_URL}/users/${wallet}/stats`);
        if (!response.ok) throw new Error('Stats not found');
        return response.json();
    }
};

// Wallet Connection (mock for demo)
let connectedWallet = null;

function connectWallet() {
    // In production, use ethers.js or web3.js to connect to MetaMask
    connectedWallet = '0x' + Math.random().toString(16).substr(2, 40);
    updateWalletUI();
    localStorage.setItem('wallet', connectedWallet);
    return connectedWallet;
}

function disconnectWallet() {
    connectedWallet = null;
    localStorage.removeItem('wallet');
    updateWalletUI();
}

function getWallet() {
    if (!connectedWallet) {
        connectedWallet = localStorage.getItem('wallet');
    }
    return connectedWallet;
}

function updateWalletUI() {
    const walletBtns = document.querySelectorAll('.btn-wallet, .navbar .btn-secondary');
    walletBtns.forEach(btn => {
        if (connectedWallet) {
            btn.textContent = `${connectedWallet.slice(0, 6)}...${connectedWallet.slice(-4)}`;
            btn.onclick = disconnectWallet;
        } else {
            btn.textContent = 'Connect Wallet';
            btn.onclick = connectWallet;
        }
    });
}

// Toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        padding: 16px 24px;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#0ea5e9'};
        color: white;
        border-radius: 8px;
        font-size: 14px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    getWallet();
    updateWalletUI();
});
