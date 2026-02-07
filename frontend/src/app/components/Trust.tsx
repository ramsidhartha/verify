export function Trust() {
  const reputationData = [
    { date: '2025-11', verified: 12, rejected: 1 },
    { date: '2025-12', verified: 18, rejected: 2 },
    { date: '2026-01', verified: 24, rejected: 1 },
    { date: '2026-02', verified: 31, rejected: 0 },
  ];

  return (
    <div className="border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-12 py-32">
        <div className="max-w-3xl mb-16">
          <div className="text-sm uppercase tracking-wider text-gray-500 mb-4">Reputation System</div>
          <h2 className="text-4xl mb-6 text-gray-900 leading-tight">
            Trust & Reputation
          </h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            Verification history becomes a professional record. Every claim, verification, and 
            outcome is recorded on-chain, creating an auditable reputation system based on 
            actual work — not badges or points.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-12">
          <div>
            <h3 className="text-xl font-medium text-gray-900 mb-6">Professional Verification Record</h3>
            
            <div className="bg-gray-50 border border-gray-200 rounded-sm p-8">
              <div className="mb-6">
                <div className="text-sm text-gray-500 mb-1">Validator ID</div>
                <div className="font-mono text-sm text-gray-900">0x7a9f...c3d2</div>
              </div>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Total Verifications</span>
                  <span className="text-lg font-medium text-gray-900">85</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Accuracy Rate</span>
                  <span className="text-lg font-medium text-gray-900">97.6%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Peer Agreement</span>
                  <span className="text-lg font-medium text-gray-900">94.1%</span>
                </div>
              </div>

              <div className="pt-6 border-t border-gray-200">
                <div className="text-xs text-gray-500 mb-3">Recent Activity</div>
                {reputationData.map((item, index) => (
                  <div key={index} className="flex items-center justify-between py-2 border-b border-gray-200 last:border-0">
                    <span className="text-xs font-mono text-gray-500">{item.date}</span>
                    <div className="flex items-center gap-4">
                      <span className="text-xs text-gray-900">{item.verified} verified</span>
                      <span className="text-xs text-gray-500">{item.rejected} rejected</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-medium text-gray-900 mb-6">How Reputation Works</h3>
            
            <div className="space-y-6">
              <div className="pb-6 border-b border-gray-200">
                <div className="text-base font-medium text-gray-900 mb-2">Verification Quality</div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Reputation is based on verification accuracy, thoroughness of analysis, 
                  and agreement with peer validators. Quality matters more than quantity.
                </p>
              </div>

              <div className="pb-6 border-b border-gray-200">
                <div className="text-base font-medium text-gray-900 mb-2">Immutable History</div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  All verification work is recorded on-chain with timestamps, reasoning, 
                  and outcomes. This creates an auditable professional record.
                </p>
              </div>

              <div className="pb-6 border-b border-gray-200">
                <div className="text-base font-medium text-gray-900 mb-2">Professional Credential</div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Verification history serves as proof of expertise in specific domains. 
                  This becomes a portable credential for validators.
                </p>
              </div>

              <div>
                <div className="text-base font-medium text-gray-900 mb-2">Economic Incentives</div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Validators with strong reputation receive higher-value verification tasks 
                  and better compensation based on track record.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
