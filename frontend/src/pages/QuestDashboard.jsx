import { useState } from 'react';
import { Link } from 'react-router-dom';
import { mockClaims, categories, difficulties } from '../data/mockData';
import Badge from '../components/Badge';
import ProgressBar from '../components/ProgressBar';
import './QuestDashboard.css';

export default function QuestDashboard() {
    const [filter, setFilter] = useState('all');
    const [categoryFilter, setCategoryFilter] = useState('');
    const [searchQuery, setSearchQuery] = useState('');

    const filteredClaims = mockClaims.filter(claim => {
        if (filter !== 'all' && claim.status !== filter) return false;
        if (categoryFilter && claim.category !== categoryFilter) return false;
        if (searchQuery && !claim.title.toLowerCase().includes(searchQuery.toLowerCase())) return false;
        return true;
    });

    const getStatusBadge = (status) => {
        switch (status) {
            case 'open':
                return <Badge variant="green">Open</Badge>;
            case 'in-progress':
                return <Badge variant="orange">In Progress</Badge>;
            case 'completed':
                return <Badge variant="purple">Completed</Badge>;
            default:
                return null;
        }
    };

    const getDifficultyColor = (difficulty) => {
        const diff = difficulties.find(d => d.name === difficulty);
        return diff ? diff.color : '#8b5cf6';
    };

    return (
        <div className="quest-dashboard">
            <div className="container">
                <div className="page-header">
                    <div className="header-content">
                        <h1>Quest <span className="text-gradient">Board</span></h1>
                        <p>Verify claims, earn XP, and build your reputation</p>
                    </div>
                    <div className="header-stats">
                        <div className="stat-box">
                            <span className="stat-number">{mockClaims.filter(c => c.status === 'open').length}</span>
                            <span className="stat-text">Open Quests</span>
                        </div>
                        <div className="stat-box">
                            <span className="stat-number">{mockClaims.reduce((sum, c) => sum + c.xpReward, 0).toLocaleString()}</span>
                            <span className="stat-text">Total XP Available</span>
                        </div>
                    </div>
                </div>

                {/* Filters */}
                <div className="filters-bar">
                    <div className="search-box">
                        <span className="search-icon">🔍</span>
                        <input
                            type="text"
                            placeholder="Search quests..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="search-input"
                        />
                    </div>

                    <div className="filter-tabs">
                        {['all', 'open', 'in-progress', 'completed'].map(status => (
                            <button
                                key={status}
                                className={`filter-tab ${filter === status ? 'active' : ''}`}
                                onClick={() => setFilter(status)}
                            >
                                {status === 'all' ? 'All' : status.charAt(0).toUpperCase() + status.slice(1).replace('-', ' ')}
                            </button>
                        ))}
                    </div>

                    <select
                        className="form-select category-filter"
                        value={categoryFilter}
                        onChange={(e) => setCategoryFilter(e.target.value)}
                    >
                        <option value="">All Categories</option>
                        {categories.map(cat => (
                            <option key={cat} value={cat}>{cat}</option>
                        ))}
                    </select>
                </div>

                {/* Quest Grid */}
                <div className="quest-grid">
                    {filteredClaims.map(claim => (
                        <Link to={`/task/${claim.id}`} key={claim.id} className="quest-card card">
                            <div className="quest-header">
                                <div className="quest-meta">
                                    {getStatusBadge(claim.status)}
                                    <span
                                        className="difficulty-badge"
                                        style={{ borderColor: getDifficultyColor(claim.difficulty), color: getDifficultyColor(claim.difficulty) }}
                                    >
                                        {claim.difficulty}
                                    </span>
                                </div>
                                <div className="quest-rewards">
                                    <span className="xp-reward">+{claim.xpReward} XP</span>
                                    <span className="token-reward">🪙 {claim.tokenReward}</span>
                                </div>
                            </div>

                            <h3 className="quest-title">{claim.title}</h3>
                            <p className="quest-description">{claim.description}</p>

                            <div className="quest-tags">
                                {claim.tags.map((tag, i) => (
                                    <span key={i} className="quest-tag">{tag}</span>
                                ))}
                            </div>

                            <div className="quest-footer">
                                <div className="quest-submitter">
                                    <img src={claim.submittedBy.avatar} alt="" className="submitter-avatar" />
                                    <div className="submitter-info">
                                        <span className="submitter-name">{claim.submittedBy.name}</span>
                                        <span className="submitter-trust">Trust: {claim.submittedBy.trustScore}</span>
                                    </div>
                                </div>

                                <div className="quest-progress">
                                    <span className="progress-text">
                                        {claim.verifiersCompleted}/{claim.verifiersNeeded} verified
                                    </span>
                                    <ProgressBar
                                        value={claim.verifiersCompleted}
                                        max={claim.verifiersNeeded}
                                        size="sm"
                                    />
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>

                {filteredClaims.length === 0 && (
                    <div className="empty-state">
                        <div className="empty-icon">🔍</div>
                        <h3>No quests found</h3>
                        <p>Try adjusting your filters or search query</p>
                    </div>
                )}
            </div>
        </div>
    );
}
