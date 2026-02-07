import './ProgressBar.css';

export default function ProgressBar({ value, max = 100, size = 'md', showLabel = false, animated = true }) {
    const percentage = Math.min(100, Math.max(0, (value / max) * 100));

    // Determine color based on percentage
    const getProgressColor = (pct) => {
        if (pct >= 100) return 'var(--accent-green)';
        if (pct >= 66) return 'var(--accent-cyan)';
        if (pct >= 33) return 'var(--accent-orange)';
        if (pct > 0) return 'var(--accent-purple)';
        return 'var(--progress-empty)';
    };

    return (
        <div className={`progress-wrapper progress-${size}`}>
            <div className="progress-bar">
                <div
                    className={`progress-fill ${animated ? 'animated' : ''}`}
                    style={{
                        width: `${percentage}%`,
                        background: percentage >= 100
                            ? 'var(--gradient-success)'
                            : `linear-gradient(90deg, ${getProgressColor(percentage)}, ${getProgressColor(percentage)}dd)`
                    }}
                />
            </div>
            {showLabel && (
                <span className="progress-label">{Math.round(percentage)}%</span>
            )}
        </div>
    );
}
