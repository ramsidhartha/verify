import './TrustScore.css';

export default function TrustScore({ score, size = 'md', showLabel = true }) {
    const sizes = {
        sm: { width: 80, fontSize: '1.25rem' },
        md: { width: 120, fontSize: '1.75rem' },
        lg: { width: 160, fontSize: '2.5rem' }
    };

    const { width, fontSize } = sizes[size];

    // Determine color based on score
    const getScoreColor = (score) => {
        if (score >= 80) return 'var(--accent-green)';
        if (score >= 60) return 'var(--accent-cyan)';
        if (score >= 40) return 'var(--accent-orange)';
        return 'var(--accent-pink)';
    };

    return (
        <div className="trust-score-container">
            <div
                className="trust-score"
                style={{
                    '--score': score,
                    '--score-color': getScoreColor(score),
                    width: `${width}px`,
                    height: `${width}px`
                }}
            >
                <div className="trust-score-ring">
                    <svg viewBox="0 0 100 100">
                        <circle
                            className="trust-score-bg"
                            cx="50"
                            cy="50"
                            r="45"
                            fill="none"
                            strokeWidth="8"
                        />
                        <circle
                            className="trust-score-progress"
                            cx="50"
                            cy="50"
                            r="45"
                            fill="none"
                            strokeWidth="8"
                            strokeLinecap="round"
                            style={{
                                strokeDasharray: `${score * 2.83} 283`,
                                stroke: getScoreColor(score)
                            }}
                        />
                    </svg>
                    <div className="trust-score-value" style={{ fontSize }}>
                        {score}
                    </div>
                </div>
            </div>
            {showLabel && (
                <div className="trust-score-label">Trust Score</div>
            )}
        </div>
    );
}
