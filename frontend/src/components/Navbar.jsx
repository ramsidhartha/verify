import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
    const location = useLocation();

    const navLinks = [
        { path: '/', label: 'Home' },
        { path: '/quests', label: 'Quests' },
        { path: '/submit', label: 'Submit Claim' },
        { path: '/profile', label: 'Profile' }
    ];

    return (
        <nav className="navbar">
            <div className="container navbar-content">
                <Link to="/" className="navbar-logo">
                    <div className="logo-icon">
                        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="50" cy="50" r="45" stroke="url(#logoGrad)" strokeWidth="4" />
                            <path d="M30 50 L45 65 L70 35" stroke="url(#logoGrad)" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
                            <defs>
                                <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stopColor="#8B5CF6" />
                                    <stop offset="100%" stopColor="#06B6D4" />
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                    <span className="logo-text">Verifi</span>
                </Link>

                <div className="navbar-links">
                    {navLinks.map(link => (
                        <Link
                            key={link.path}
                            to={link.path}
                            className={`nav-link ${location.pathname === link.path ? 'active' : ''}`}
                        >
                            {link.label}
                        </Link>
                    ))}
                </div>

                <div className="navbar-actions">
                    <button className="btn btn-secondary btn-sm">
                        <span className="wallet-icon">◈</span>
                        Connect Wallet
                    </button>
                </div>
            </div>
        </nav>
    );
}
