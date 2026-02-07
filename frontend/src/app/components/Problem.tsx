export function Problem() {
  return (
    <div id="problem" className="border-b border-gray-200 bg-gray-50">
      <div className="max-w-7xl mx-auto px-12 py-32">
        <div className="max-w-3xl">
          <div className="text-sm uppercase tracking-wider text-gray-500 mb-4">The Challenge</div>
          <h2 className="text-4xl mb-8 text-gray-900 leading-tight">
            The Verification Problem
          </h2>
          
          <div className="space-y-6 text-lg text-gray-600 leading-relaxed">
            <p>
              AI systems generate code at unprecedented speed. But verification remains slow, 
              invisible, and unrewarded. The result is a growing trust gap between what code 
              claims to do and what it actually does.
            </p>
            
            <p>
              Today, trust in code is based on authority — reputation of the author, the company, 
              or the research lab. There is no standardized, verifiable proof of correctness. 
              Verification work is often unpaid and uncredited.
            </p>

            <p>
              As AI-generated code becomes more prevalent, we need infrastructure that makes 
              verification explicit, verifiable, and economically viable.
            </p>
          </div>

          <div className="mt-12 grid grid-cols-3 gap-8">
            <div className="p-6 bg-white border border-gray-200 rounded-sm">
              <div className="text-2xl font-medium text-gray-900 mb-2">Speed Mismatch</div>
              <div className="text-sm text-gray-600">Code generation is fast. Verification is slow and manual.</div>
            </div>
            <div className="p-6 bg-white border border-gray-200 rounded-sm">
              <div className="text-2xl font-medium text-gray-900 mb-2">Invisible Labor</div>
              <div className="text-sm text-gray-600">Verification work is uncredited and economically unrewarded.</div>
            </div>
            <div className="p-6 bg-white border border-gray-200 rounded-sm">
              <div className="text-2xl font-medium text-gray-900 mb-2">Trust by Authority</div>
              <div className="text-sm text-gray-600">No standardized proof. Trust is based on reputation, not evidence.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
