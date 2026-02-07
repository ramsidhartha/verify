import './Badge.css';

export default function Badge({ children, variant = 'purple', size = 'md', icon }) {
    return (
        <span className={`badge badge-${variant} badge-size-${size}`}>
            {icon && <span className="badge-icon">{icon}</span>}
            {children}
        </span>
    );
}
