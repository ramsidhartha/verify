import { useState } from 'react';
import { Button } from './ui/button';
import { submitClaim, type ClaimResponse } from '../services/api';

interface ClaimModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export function ClaimModal({ isOpen, onClose }: ClaimModalProps) {
    const [claimText, setClaimText] = useState('');
    const [wallet, setWallet] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<ClaimResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await submitClaim(claimText, wallet || '0xDemo_User');
            setResult(response);
        } catch (err) {
            setError('Failed to submit claim. Make sure the API server is running.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setClaimText('');
        setWallet('');
        setResult(null);
        setError(null);
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-auto">
                <div className="p-6 border-b border-gray-200">
                    <h2 className="text-2xl font-medium text-gray-900">Submit a Claim</h2>
                    <p className="text-sm text-gray-600 mt-1">
                        Describe your code claim and our AI will generate verification tasks
                    </p>
                </div>

                {!result ? (
                    <form onSubmit={handleSubmit} className="p-6">
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Wallet Address (optional)
                            </label>
                            <input
                                type="text"
                                value={wallet}
                                onChange={(e) => setWallet(e.target.value)}
                                placeholder="0x..."
                                className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                            />
                        </div>

                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Claim Description
                            </label>
                            <textarea
                                value={claimText}
                                onChange={(e) => setClaimText(e.target.value)}
                                placeholder="e.g., My API handles 2000 requests per second with sub-100ms latency and implements OAuth2 authentication..."
                                rows={6}
                                className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent resize-none"
                                required
                            />
                        </div>

                        {error && (
                            <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-sm text-sm">
                                {error}
                            </div>
                        )}

                        <div className="flex gap-3">
                            <Button
                                type="submit"
                                disabled={loading || !claimText}
                                className="bg-gray-900 text-white hover:bg-gray-800 px-6 py-3"
                            >
                                {loading ? 'Analyzing...' : 'Submit Claim'}
                            </Button>
                            <Button
                                type="button"
                                variant="outline"
                                onClick={resetForm}
                                className="border-gray-300 text-gray-700 hover:bg-gray-50 px-6 py-3"
                            >
                                Cancel
                            </Button>
                        </div>
                    </form>
                ) : (
                    <div className="p-6">
                        <div className="mb-6">
                            <div className="flex items-center gap-2 mb-2">
                                <div className="size-3 bg-green-500 rounded-full"></div>
                                <span className="text-lg font-medium text-gray-900">Claim Submitted</span>
                            </div>
                            <div className="text-sm text-gray-600">
                                Claim ID: <span className="font-mono">{result.claim_id}</span>
                            </div>
                        </div>

                        <div className="bg-gray-50 border border-gray-200 rounded-sm p-4 mb-6">
                            <div className="grid grid-cols-2 gap-4 mb-4">
                                <div>
                                    <div className="text-sm text-gray-500">Status</div>
                                    <div className="text-lg font-medium text-gray-900">{result.status}</div>
                                </div>
                                <div>
                                    <div className="text-sm text-gray-500">Coverage</div>
                                    <div className="text-lg font-medium text-gray-900">{(result.coverage * 100).toFixed(0)}%</div>
                                </div>
                            </div>
                            <div>
                                <div className="text-sm text-gray-500 mb-2">Tasks Generated</div>
                                <div className="text-3xl font-medium text-gray-900">{result.tasks_count}</div>
                            </div>
                        </div>

                        <div className="mb-6">
                            <div className="text-sm font-medium text-gray-700 mb-3">Verification Tasks</div>
                            <div className="space-y-2 max-h-48 overflow-auto">
                                {result.tasks.slice(0, 5).map((task) => (
                                    <div key={task.task_id} className="p-3 bg-gray-50 border border-gray-200 rounded-sm">
                                        <div className="text-sm font-medium text-gray-900">{task.task_id}</div>
                                        <div className="text-xs text-gray-600 mt-1">{task.description}</div>
                                        <div className="text-xs text-gray-500 mt-1">
                                            {task.min_validators} validators needed | {task.estimated_minutes}min
                                        </div>
                                    </div>
                                ))}
                                {result.tasks.length > 5 && (
                                    <div className="text-sm text-gray-500 text-center py-2">
                                        +{result.tasks.length - 5} more tasks
                                    </div>
                                )}
                            </div>
                        </div>

                        <Button
                            onClick={resetForm}
                            className="w-full bg-gray-900 text-white hover:bg-gray-800 py-3"
                        >
                            Done
                        </Button>
                    </div>
                )}
            </div>
        </div>
    );
}
