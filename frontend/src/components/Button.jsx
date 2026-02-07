import './Button.css';

export default function Button({
    children,
    variant = 'primary',
    size = 'md',
    icon,
    iconRight,
    disabled = false,
    loading = false,
    fullWidth = false,
    onClick,
    type = 'button',
    className = ''
}) {
    const classes = [
        'btn',
        `btn-${variant}`,
        `btn-${size}`,
        fullWidth ? 'btn-full' : '',
        loading ? 'btn-loading' : '',
        className
    ].filter(Boolean).join(' ');

    return (
        <button
            type={type}
            className={classes}
            onClick={onClick}
            disabled={disabled || loading}
        >
            {loading ? (
                <span className="btn-spinner" />
            ) : (
                <>
                    {icon && <span className="btn-icon">{icon}</span>}
                    {children}
                    {iconRight && <span className="btn-icon-right">{iconRight}</span>}
                </>
            )}
        </button>
    );
}
