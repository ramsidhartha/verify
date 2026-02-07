import { CheckCircle, XCircle } from 'lucide-react';

export function TechStack() {
  const examples = [
    {
      title: 'Binary Search',
      claim: 'O(log n)',
      status: 'verified',
      result: 'Verified across 1000+ test cases',
    },
    {
      title: 'Bubble Sort',
      claim: 'O(n log n)',
      status: 'failed',
      result: 'Actually O(n²) - claim incorrect',
    },
    {
      title: 'Merge Sort',
      claim: 'O(n log n)',
      status: 'verified',
      result: 'Time & space complexity confirmed',
    },
  ];

  return (
    <div id="examples" className="max-w-7xl mx-auto px-6 py-24">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl mb-4 text-white">
          How It Works
        </h2>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Simply paste your algorithm, state your claims, and we'll verify them automatically.
        </p>
      </div>

      <div className="relative">
        {/* Background decoration */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 rounded-3xl blur-3xl"></div>
        
        <div className="relative bg-gray-900/50 border border-gray-800 rounded-2xl p-8 md:p-12">
          <div className="space-y-4 mb-12">
            {examples.map((example, index) => (
              <div 
                key={index}
                className="flex items-center justify-between p-4 bg-gray-950/50 border border-gray-800 rounded-lg hover:border-gray-700 transition-all"
              >
                <div className="flex items-center gap-4">
                  {example.status === 'verified' ? (
                    <CheckCircle className="size-6 text-green-500" />
                  ) : (
                    <XCircle className="size-6 text-red-500" />
                  )}
                  <div>
                    <div className="text-white font-medium">{example.title}</div>
                    <div className="text-sm text-gray-400">Claimed: {example.claim}</div>
                  </div>
                </div>
                <div className={`text-sm ${example.status === 'verified' ? 'text-green-400' : 'text-red-400'}`}>
                  {example.result}
                </div>
              </div>
            ))}
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-gray-950/30 rounded-xl border border-gray-800">
              <div className="size-12 rounded-full bg-blue-500/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-500">1</span>
              </div>
              <h3 className="text-lg mb-2 text-white">Submit Algorithm</h3>
              <p className="text-gray-400 text-sm">
                Paste your code and state your complexity claims
              </p>
            </div>
            
            <div className="text-center p-6 bg-gray-950/30 rounded-xl border border-gray-800">
              <div className="size-12 rounded-full bg-purple-500/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-500">2</span>
              </div>
              <h3 className="text-lg mb-2 text-white">Auto-Testing</h3>
              <p className="text-gray-400 text-sm">
                We run thousands of tests with varying inputs
              </p>
            </div>
            
            <div className="text-center p-6 bg-gray-950/30 rounded-xl border border-gray-800">
              <div className="size-12 rounded-full bg-pink-500/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-pink-500">3</span>
              </div>
              <h3 className="text-lg mb-2 text-white">Get Results</h3>
              <p className="text-gray-400 text-sm">
                Receive detailed verification report with suggestions
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
