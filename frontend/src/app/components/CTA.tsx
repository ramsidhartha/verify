import { Button } from './ui/button';
import { ArrowRight, Play } from 'lucide-react';

export function CTA() {
  return (
    <div className="max-w-7xl mx-auto px-6 py-24">
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-1">
        <div className="bg-gray-950 rounded-3xl p-12 md:p-16">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-4xl md:text-5xl mb-6 text-white">
              Stop Guessing. Start Verifying.
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of developers who trust AlgoVerify to validate their algorithms. Get instant feedback and fix issues before they reach production.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button className="bg-white text-gray-900 hover:bg-gray-100 text-lg px-8 py-6">
                <Play className="mr-2 size-5" />
                Try It Free
              </Button>
              <Button 
                variant="outline" 
                className="border-gray-600 text-white hover:bg-gray-900 text-lg px-8 py-6"
              >
                View Documentation
                <ArrowRight className="ml-2 size-5" />
              </Button>
            </div>

            <p className="mt-8 text-gray-400 text-sm">
              Free for open source projects • No credit card required
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
