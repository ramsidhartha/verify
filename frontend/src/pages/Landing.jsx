import { Link } from 'react-router-dom';
import './Landing.css';

export default function Landing() {
    const features = [
        {
            icon: '📝',
            title: 'Submit Claims',
            description: 'Post your technical achievements with evidence links to GitHub, deployed contracts, or live demos.'
        },
        {
            icon: '🤖',
            title: 'AI-Powered Tasks',
            description: 'Our AI generates targeted verification checklists based on the claim type and complexity.'
        },
        {
            icon: '✅',
            title: 'Peer Verification',
            description: 'Complete verification quests to validate claims and earn rewards.'
        },
        {
            icon: '⭐',
            title: 'Build Reputation',
            description: 'Earn trust scores, badges, and tokens as you verify and get verified.'
        }
    ];

    const stats = [
        { value: '2,450+', label: 'Claims Verified' },
        { value: '890+', label: 'Active Verifiers' },
        { value: '98.5%', label: 'Accuracy Rate' },
        { value: '$125K', label: 'Rewards Distributed' }
    ];

    return (
        <div className="landing">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-bg">
                    <div className="hero-glow hero-glow-1"></div>
                    <div className="hero-glow hero-glow-2"></div>
                    <div className="hero-grid"></div>
                </div>

                <div className="container hero-content">
                    <div className="hero-badge">
                        <span className="pulse-dot"></span>
                        Web3 × AI Verification Protocol
                    </div>

                    <h1 className="hero-title">
                        Verify Skills.<br />
                        <span className="text-gradient">Earn Trust.</span>
                    </h1>

                    <p className="hero-subtitle">
                        A gamified platform where developers verify technical claims and build
                        on-chain reputation through AI-assisted peer verification.
                    </p>

                    <div className="hero-actions">
                        <Link to="/submit" className="btn btn-primary btn-lg">
                            Submit a Claim
                            <span className="btn-arrow">→</span>
                        </Link>
                        <Link to="/quests" className="btn btn-secondary btn-lg">
                            Explore Quests
                        </Link>
                    </div>

                    <div className="hero-stats">
                        {stats.map((stat, i) => (
                            <div key={i} className="stat-item">
                                <div className="stat-value">{stat.value}</div>
                                <div className="stat-label">{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Flow Section */}
            <section className="section flow-section">
                <div className="container">
                    <div className="section-header">
                        <h2>How It Works</h2>
                        <p>From claim to reputation in four simple steps</p>
                    </div>

                    <div className="flow-diagram">
                        <div className="flow-step">
                            <div className="flow-icon">📝</div>
                            <div className="flow-content">
                                <h4>Claim</h4>
                                <p>Submit your technical achievement</p>
                            </div>
                        </div>
                        <div className="flow-arrow">→</div>
                        <div className="flow-step">
                            <div className="flow-icon">🤖</div>
                            <div className="flow-content">
                                <h4>AI Tasks</h4>
                                <p>AI generates verification checklist</p>
                            </div>
                        </div>
                        <div className="flow-arrow">→</div>
                        <div className="flow-step">
                            <div className="flow-icon">✅</div>
                            <div className="flow-content">
                                <h4>Verification</h4>
                                <p>Peers complete verification quests</p>
                            </div>
                        </div>
                        <div className="flow-arrow">→</div>
                        <div className="flow-step">
                            <div className="flow-icon">⭐</div>
                            <div className="flow-content">
                                <h4>Reputation</h4>
                                <p>Earn trust scores & rewards</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="section features-section">
                <div className="container">
                    <div className="section-header">
                        <h2>Built for <span className="text-gradient">Builders</span></h2>
                        <p>Everything you need to prove your skills and verify others</p>
                    </div>

                    <div className="features-grid">
                        {features.map((feature, i) => (
                            <div key={i} className="feature-card card">
                                <div className="feature-icon">{feature.icon}</div>
                                <h3>{feature.title}</h3>
                                <p>{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="section cta-section">
                <div className="container">
                    <div className="cta-card">
                        <div className="cta-content">
                            <h2>Ready to Build Your Reputation?</h2>
                            <p>Join the decentralized verification network and start earning trust today.</p>
                            <div className="cta-actions">
                                <Link to="/submit" className="btn btn-primary btn-lg">
                                    Get Started
                                </Link>
                                <Link to="/quests" className="btn btn-outline btn-lg">
                                    Browse Quests
                                </Link>
                            </div>
                        </div>
                        <div className="cta-decoration">
                            <div className="cta-orb cta-orb-1"></div>
                            <div className="cta-orb cta-orb-2"></div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
