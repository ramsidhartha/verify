import { LineChart, Bug, Clock, Braces, Shield, Zap } from 'lucide-react';
import { Card } from './ui/card';

export function Features() {
  const features = [
    {
      icon: Clock,
      title: 'Time Complexity Analysis',
      description: 'Automatically verify Big O claims for your algorithms. We test with multiple input sizes and patterns to confirm your complexity assertions.',
    },
    {
      icon: LineChart,
      title: 'Space Complexity Tracking',
      description: 'Monitor memory usage and validate space complexity claims. Identify memory leaks and optimization opportunities.',
    },
    {
      icon: Bug,
      title: 'Edge Case Detection',
      description: 'Discover corner cases you might have missed. Our intelligent test generation finds edge cases that break your algorithm.',
    },
    {
      icon: Shield,
      title: 'Correctness Verification',
      description: 'Prove your algorithm produces correct results. Compare against reference implementations and validate output properties.',
    },
    {
      icon: Braces,
      title: 'Multi-Language Support',
      description: 'Works with Python, JavaScript, Java, C++, Go, and more. Same powerful analysis across all major programming languages.',
    },
    {
      icon: Zap,
      title: 'Performance Benchmarking',
      description: 'Real-world performance metrics with detailed reports. Compare implementations and identify bottlenecks instantly.',
    },
  ];

  return (
    <div id="features" className="max-w-7xl mx-auto px-6 py-24">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl mb-4 text-white">
          Everything You Need to Verify Algorithms
        </h2>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Comprehensive testing and validation tools to ensure your algorithms work as claimed.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <Card 
              key={index} 
              className="p-6 bg-gray-900/50 border-gray-800 hover:border-blue-500/50 transition-all hover:shadow-lg hover:shadow-blue-500/10 group"
            >
              <div className="size-12 rounded-lg bg-blue-500/10 flex items-center justify-center mb-4 group-hover:bg-blue-500/20 transition-colors">
                <Icon className="size-6 text-blue-500" />
              </div>
              <h3 className="text-xl mb-2 text-white">{feature.title}</h3>
              <p className="text-gray-400 leading-relaxed">{feature.description}</p>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
