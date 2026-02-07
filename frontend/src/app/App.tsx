import { Hero } from './components/Hero';
import { Problem } from './components/Problem';
import { Solution } from './components/Solution';
import { Principles } from './components/Principles';
import { Trust } from './components/Trust';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <Hero />
      <Problem />
      <Solution />
      <Principles />
      <Trust />
      <Footer />
    </div>
  );
}
