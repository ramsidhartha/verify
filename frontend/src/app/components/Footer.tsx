export function Footer() {
  return (
    <footer className="bg-gray-50">
      <div className="max-w-7xl mx-auto px-12 py-16">
        <div className="grid grid-cols-4 gap-12 mb-16">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="size-5 bg-gray-900 rounded"></div>
              <span className="text-base font-medium text-gray-900">Verifi</span>
            </div>
            <p className="text-sm text-gray-600">
              Built for Web3 × AI
            </p>
          </div>

          <div>
            <div className="text-xs uppercase tracking-wider text-gray-500 mb-4">Protocol</div>
            <ul className="space-y-2">
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Documentation</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Whitepaper</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">API Reference</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">GitHub</a></li>
            </ul>
          </div>

          <div>
            <div className="text-xs uppercase tracking-wider text-gray-500 mb-4">Resources</div>
            <ul className="space-y-2">
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Examples</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Case Studies</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">FAQ</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Support</a></li>
            </ul>
          </div>

          <div>
            <div className="text-xs uppercase tracking-wider text-gray-500 mb-4">Community</div>
            <ul className="space-y-2">
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Discord</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Twitter</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Blog</a></li>
              <li><a href="#" className="text-sm text-gray-600 hover:text-gray-900 transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-gray-200 flex justify-between items-center">
          <p className="text-xs text-gray-500">
            © 2026 Verifi Protocol. All rights reserved.
          </p>
          <div className="flex gap-6">
            <a href="#" className="text-xs text-gray-500 hover:text-gray-900 transition-colors">Privacy</a>
            <a href="#" className="text-xs text-gray-500 hover:text-gray-900 transition-colors">Terms</a>
            <a href="#" className="text-xs text-gray-500 hover:text-gray-900 transition-colors">Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
