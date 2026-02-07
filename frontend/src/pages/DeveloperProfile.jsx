import { mockUserProfile, tiers } from '../data/mockData';
import TrustScore from '../components/TrustScore';
import ProgressBar from '../components/ProgressBar';
import Badge from '../components/Badge';
import './DeveloperProfile.css';

export default function DeveloperProfile() {
    const user = mockUserProfile;
    const currentTier = tiers.find(t => user.xp >= t.minXP && (!tiers[tiers.indexOf(t) + 1] || user.xp < tiers[tiers.indexOf(t) + 1].minXP));
    const nextTier = tiers[tiers.indexOf(currentTier) + 1];

    const getRarityClass = (rarity) => {
        switch (rarity) {
            case 'legendary': return 'badge-legendary';
            case 'epic': return 'badge-epic';
            case 'rare': return 'badge-rare';
            case 'uncommon': return 'badge-uncommon';
            default: return 'badge-common';
        }
    };

    const getActivityIcon = (type) => {
        switch (type) {
            case 'verification': return '✅';
            case 'submission': return '📝';
            case 'badge': return '🏆';
            default: return '•';
        }
    };

    const getResultClass = (result) => {
        switch (result) {
            case 'approved': return 'result-approved';
            case 'rejected': return 'result-rejected';
            case 'pending': return 'result-pending';
            default: return '';
        }
    };

    return (
        <div className="developer-profile-page">
            <div className="container">
                {/* Profile Header */}
                <div className="profile-header card">
                    <div className="profile-bg">
                        <div className="profile-glow"></div>
                    </div>

                    <div className="profile-content">
                        <div className="profile-main">
                            <img src={user.avatar} alt={user.name} className="profile-avatar" />
                            <div className="profile-info">
                                <div className="profile-tier" style={{ color: currentTier.color }}>
                                    {currentTier.icon} {currentTier.name}
                                </div>
                                <h1 className="profile-name">{user.displayName}</h1>
                                <p className="profile-handle">@{user.name}</p>
                                <p className="profile-bio">{user.bio}</p>
                            </div>
                        </div>

                        <div className="profile-trust">
                            <TrustScore score={user.trustScore} size="lg" />
                        </div>
                    </div>

                    {/* XP Progress */}
                    <div className="xp-section">
                        <div className="xp-info">
                            <span className="xp-current">{user.xp.toLocaleString()} XP</span>
                            {nextTier && (
                                <span className="xp-next">Next: {nextTier.icon} {nextTier.name} at {nextTier.minXP.toLocaleString()} XP</span>
                            )}
                        </div>
                        <ProgressBar
                            value={user.xp - currentTier.minXP}
                            max={nextTier ? nextTier.minXP - currentTier.minXP : 1}
                            size="lg"
                        />
                    </div>
                </div>

                <div className="profile-layout">
                    {/* Stats Section */}
                    <div className="stats-section">
                        <div className="stats-grid">
                            <div className="stat-card card">
                                <div className="stat-icon">📝</div>
                                <div className="stat-value">{user.stats.claimsSubmitted}</div>
                                <div className="stat-label">Claims Submitted</div>
                            </div>
                            <div className="stat-card card">
                                <div className="stat-icon">✅</div>
                                <div className="stat-value">{user.stats.verificationsCompleted}</div>
                                <div className="stat-label">Verifications</div>
                            </div>
                            <div className="stat-card card">
                                <div className="stat-icon">🎯</div>
                                <div className="stat-value">{user.stats.accuracy}%</div>
                                <div className="stat-label">Accuracy</div>
                            </div>
                            <div className="stat-card card">
                                <div className="stat-icon">🔥</div>
                                <div className="stat-value">{user.stats.streak}</div>
                                <div className="stat-label">Day Streak</div>
                            </div>
                            <div className="stat-card card">
                                <div className="stat-icon">🪙</div>
                                <div className="stat-value">{user.tokensEarned}</div>
                                <div className="stat-label">Tokens Earned</div>
                            </div>
                            <div className="stat-card card">
                                <div className="stat-icon">🏅</div>
                                <div className="stat-value">#{user.stats.rank}</div>
                                <div className="stat-label">Global Rank</div>
                            </div>
                        </div>

                        {/* Badges Section */}
                        <div className="badges-section card">
                            <h2>🏆 Achievements</h2>
                            <div className="badges-grid">
                                {user.badges.map(badge => (
                                    <div key={badge.id} className={`achievement-badge ${getRarityClass(badge.rarity)}`}>
                                        <span className="badge-icon-large">{badge.icon}</span>
                                        <div className="badge-info">
                                            <span className="badge-name">{badge.name}</span>
                                            <span className="badge-desc">{badge.description}</span>
                                        </div>
                                        <span className={`badge-rarity ${badge.rarity}`}>{badge.rarity}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Activity Section */}
                    <div className="activity-section card">
                        <h2>📊 Recent Activity</h2>
                        <div className="activity-timeline">
                            {user.recentActivity.map((activity, i) => (
                                <div key={i} className="activity-item">
                                    <div className="activity-icon">{getActivityIcon(activity.type)}</div>
                                    <div className="activity-content">
                                        <div className="activity-main">
                                            {activity.type === 'verification' && (
                                                <>
                                                    <span className="activity-action">Verified</span>
                                                    <span className="activity-claim">{activity.claim}</span>
                                                    <span className={`activity-result ${getResultClass(activity.result)}`}>
                                                        {activity.result}
                                                    </span>
                                                </>
                                            )}
                                            {activity.type === 'submission' && (
                                                <>
                                                    <span className="activity-action">Submitted</span>
                                                    <span className="activity-claim">{activity.claim}</span>
                                                    <Badge variant="purple" size="sm">{activity.result}</Badge>
                                                </>
                                            )}
                                            {activity.type === 'badge' && (
                                                <>
                                                    <span className="activity-action">Earned badge</span>
                                                    <span className="activity-badge-name">{activity.badge}</span>
                                                </>
                                            )}
                                        </div>
                                        <div className="activity-meta">
                                            {activity.xp > 0 && <span className="activity-xp">+{activity.xp} XP</span>}
                                            <span className="activity-date">{activity.date}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
