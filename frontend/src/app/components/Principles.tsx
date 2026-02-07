export function Principles() {
  const principles = [
    {
      title: 'AI as the Coordinator',
      description: 'AI breaks down complex verification claims into discrete, verifiable tasks. It routes work, synthesizes results, and ensures consistency — but does not make final judgments.',
      technical: 'Task decomposition, validation routing, and proof synthesis',
    },
    {
      title: 'Community as Validators',
      description: 'Human experts review code, test edge cases, and provide reasoning. Validators are compensated fairly and build reputation through quality verification work.',
      technical: 'Distributed verification, peer review, economic incentives',
    },
    {
      title: 'Blockchain as the Trust Layer',
      description: 'All verification records are stored on-chain as immutable proof. The history of claims, verifications, and validator performance becomes a public, auditable record.',
      technical: 'Immutable audit logs, cryptographic proofs, reputation ledger',
    },
  ];

  return (
    <div className="border-b border-gray-200 bg-gray-50">
      <div className="max-w-7xl mx-auto px-12 py-32">
        <div className="max-w-3xl mb-16">
          <div className="text-sm uppercase tracking-wider text-gray-500 mb-4">System Design</div>
          <h2 className="text-4xl mb-6 text-gray-900 leading-tight">
            System Principles
          </h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            Verifi is built on three core pillars that work together to create 
            a trustworthy verification infrastructure.
          </p>
        </div>

        <div className="grid grid-cols-3 gap-8">
          {principles.map((principle, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-sm p-8">
              <div className="text-sm font-mono text-gray-400 mb-4">{String(index + 1).padStart(2, '0')}</div>
              <h3 className="text-xl font-medium text-gray-900 mb-4">{principle.title}</h3>
              <p className="text-sm text-gray-600 leading-relaxed mb-6">{principle.description}</p>
              <div className="pt-4 border-t border-gray-200">
                <div className="text-xs font-mono text-gray-500">{principle.technical}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
