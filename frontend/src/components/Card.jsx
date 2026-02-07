import './Card.css';

export default function Card({
    children,
    className = '',
    variant = 'default',
    hoverable = true,
    glowing = false,
    onClick
}) {
    const classes = [
        'card',
        `card-${variant}`,
        hoverable ? 'card-hoverable' : '',
        glowing ? 'card-glowing' : '',
        className
    ].filter(Boolean).join(' ');

    return (
        <div className={classes} onClick={onClick}>
            {children}
        </div>
    );
}
