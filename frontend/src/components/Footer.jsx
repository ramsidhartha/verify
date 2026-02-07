import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-content">
                    <div className="footer-brand">
                        <Link to="/" className="footer-logo">
                            <div className="logo-icon-sm">
                                <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="50" cy="50" r="45" stroke="url(#footerGrad)" strokeWidth="4" />
                                    <path d="M30 50 L45 65 L70 35" stroke="url(#footerGrad)" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
                                    <defs>
                                        <linearGradient id="footerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stopColor="#8B5CF6" />
                                            <stop offset="100%" stopColor="#06B6D4" />
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                            <span>Verifi</span>
                        </Link>
                        <p className="footer-tagline">
                            Building trust in Web3, one verification at a time.
                        </p>
                    </div>

                    <div className="footer-links">
                        <div className="footer-column">
                            <h4>Platform</h4>
                            <Link to="/quests">Quest Board</Link>
                            <Link to="/submit">Submit Claim</Link>
                            <Link to="/profile">Profile</Link>
                        </div>
                        <div className="footer-column">
                            <h4>Resources</h4>
                            <a href="#">Documentation</a>
                            <a href="#">API</a>
                            <a href="#">SDK</a>
                        </div>
                        <div className="footer-column">
                            <h4>Community</h4>
                            <a href="#">Discord</a>
                            <a href="#">Twitter</a>
                            <a href="#">GitHub</a>
                        </div>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>© 2024 Verifi. Built for B3 Hackathon.</p>
                    <div className="footer-badges">
                        <span className="tech-badge">Web3</span>
                        <span className="tech-badge">AI</span>
                        <span className="tech-badge">ZK</span>
                    </div>
                </div>
            </div>
        </footer>
    );
}
