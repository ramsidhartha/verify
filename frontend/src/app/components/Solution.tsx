import { ArrowRight } from 'lucide-react';

export function Solution() {
  const steps = [
    {
      number: '01',
      title: 'Claim',
      description: 'Developer submits a code claim with stated properties (correctness, complexity, behavior).',
    },
    {
      number: '02',
      title: 'AI Task Breakdown',
      description: 'AI coordinator analyzes the claim and breaks it into discrete verification tasks.',
    },
    {
      number: '03',
      title: 'Human Verification',
      description: 'Community validators review and verify each task, providing evidence and reasoning.',
    },
    {
      number: '04',
      title: 'On-chain Proof',
      description: 'Verified claims are recorded on-chain as immutable, auditable proof.',
    },
  ];

  return (
    <div id="solution" className="border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-12 py-32">
        <div className="max-w-3xl mb-16">
          <div className="text-sm uppercase tracking-wider text-gray-500 mb-4">Our Approach</div>
          <h2 className="text-4xl mb-6 text-gray-900 leading-tight">
            How Verifi Works
          </h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            A systematic verification protocol that combines AI coordination, human expertise, 
            and blockchain immutability to create verifiable proof of code correctness.
          </p>
        </div>

        <div className="grid grid-cols-4 gap-6">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              <div className="mb-6">
                <div className="text-sm font-mono text-gray-400 mb-3">{step.number}</div>
                <div className="text-xl font-medium text-gray-900 mb-3">{step.title}</div>
                <div className="text-sm text-gray-600 leading-relaxed">{step.description}</div>
              </div>
              
              {index < steps.length - 1 && (
                <div className="absolute top-6 -right-3 text-gray-300">
                  <ArrowRight className="size-4" />
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-16 p-8 bg-gray-50 border border-gray-200 rounded-sm">
          <div className="grid grid-cols-2 gap-12">
            <div>
              <div className="text-lg font-medium text-gray-900 mb-3">Verification as a Service</div>
              <p className="text-sm text-gray-600 leading-relaxed">
                Verifi acts as infrastructure, not a platform. Developers submit claims, 
                validators verify them, and the protocol ensures fair compensation and 
                reputation tracking for all participants.
              </p>
            </div>
            <div>
              <div className="text-lg font-medium text-gray-900 mb-3">Trust Through Evidence</div>
              <p className="text-sm text-gray-600 leading-relaxed">
                Every verification includes reasoning, test cases, and analysis. The on-chain 
                record becomes a professional audit trail that anyone can inspect and trust.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
