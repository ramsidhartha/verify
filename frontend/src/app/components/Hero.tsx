import { useState } from 'react';
import { Button } from './ui/button';
import { ClaimModal } from './ClaimModal';

export function Hero() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="border-b border-gray-200">
      <nav className="max-w-7xl mx-auto px-12 py-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="size-6 bg-gray-900 rounded"></div>
          <span className="text-lg font-medium text-gray-900">Verifi</span>
        </div>
        <div className="flex items-center gap-8">
          <a href="#problem" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Problem</a>
          <a href="#solution" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">How It Works</a>
          <a href="#docs" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Documentation</a>
          <Button variant="outline" className="text-sm border-gray-300 text-gray-900 hover:bg-gray-50">
            View Verifications
          </Button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-12 py-32">
        <div className="max-w-3xl">
          <h1 className="text-6xl tracking-tight mb-6 text-gray-900 leading-tight">
            Making Code Verification Trustworthy
          </h1>

          <p className="text-xl text-gray-600 mb-12 leading-relaxed max-w-2xl">
            A Web3 x AI developer protocol that turns code verification into a verifiable,
            on-chain reputation system. Making correctness, trust, and verification visible.
          </p>

          <div className="flex items-center gap-4">
            <Button
              className="bg-gray-900 text-white hover:bg-gray-800 px-6 py-6"
              onClick={() => setIsModalOpen(true)}
            >
              Submit a Claim
            </Button>
            <Button variant="outline" className="border-gray-300 text-gray-900 hover:bg-gray-50 px-6 py-6">
              View Verifications
            </Button>
          </div>

          <div className="mt-16 pt-16 border-t border-gray-200">
            <div className="grid grid-cols-3 gap-12">
              <div>
                <div className="text-3xl font-medium text-gray-900 mb-1">AI-Coordinated</div>
                <div className="text-sm text-gray-600">Task breakdown and verification routing</div>
              </div>
              <div>
                <div className="text-3xl font-medium text-gray-900 mb-1">Human-Verified</div>
                <div className="text-sm text-gray-600">Community validators ensure correctness</div>
              </div>
              <div>
                <div className="text-3xl font-medium text-gray-900 mb-1">On-Chain Proof</div>
                <div className="text-sm text-gray-600">Immutable verification records</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <ClaimModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
