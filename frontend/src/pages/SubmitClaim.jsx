import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { categories, difficulties } from '../data/mockData';
import './SubmitClaim.css';

export default function SubmitClaim() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: '',
        difficulty: '',
        githubUrl: '',
        demoUrl: '',
        contractUrl: '',
        tags: ''
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showPreview, setShowPreview] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Navigate to quests after submission
        navigate('/quests');
    };

    return (
        <div className="submit-claim-page">
            <div className="container">
                <div className="page-header">
                    <h1>Submit a <span className="text-gradient">Claim</span></h1>
                    <p>Share your technical achievement and let the community verify it</p>
                </div>

                <div className="submit-layout">
                    <form className="claim-form card" onSubmit={handleSubmit}>
                        <div className="form-section">
                            <h3>📝 Claim Details</h3>

                            <div className="form-group">
                                <label className="form-label">Claim Title *</label>
                                <input
                                    type="text"
                                    name="title"
                                    className="form-input"
                                    placeholder="e.g., Built a DeFi Lending Protocol"
                                    value={formData.title}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">Description *</label>
                                <textarea
                                    name="description"
                                    className="form-textarea"
                                    placeholder="Describe what you built, the technologies used, and any notable features..."
                                    value={formData.description}
                                    onChange={handleChange}
                                    required
                                    rows={5}
                                />
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label className="form-label">Category *</label>
                                    <select
                                        name="category"
                                        className="form-select"
                                        value={formData.category}
                                        onChange={handleChange}
                                        required
                                    >
                                        <option value="">Select category</option>
                                        {categories.map(cat => (
                                            <option key={cat} value={cat}>{cat}</option>
                                        ))}
                                    </select>
                                </div>

                                <div className="form-group">
                                    <label className="form-label">Difficulty *</label>
                                    <select
                                        name="difficulty"
                                        className="form-select"
                                        value={formData.difficulty}
                                        onChange={handleChange}
                                        required
                                    >
                                        <option value="">Select difficulty</option>
                                        {difficulties.map(diff => (
                                            <option key={diff.name} value={diff.name}>{diff.name}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="form-group">
                                <label className="form-label">Tags</label>
                                <input
                                    type="text"
                                    name="tags"
                                    className="form-input"
                                    placeholder="e.g., Solidity, React, DeFi (comma separated)"
                                    value={formData.tags}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        <div className="form-section">
                            <h3>🔗 Evidence Links</h3>
                            <p className="form-hint">Provide at least one evidence link</p>

                            <div className="form-group">
                                <label className="form-label">
                                    <span className="link-icon">📁</span> GitHub Repository
                                </label>
                                <input
                                    type="url"
                                    name="githubUrl"
                                    className="form-input"
                                    placeholder="https://github.com/username/repo"
                                    value={formData.githubUrl}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">
                                    <span className="link-icon">🌐</span> Live Demo URL
                                </label>
                                <input
                                    type="url"
                                    name="demoUrl"
                                    className="form-input"
                                    placeholder="https://your-demo.com"
                                    value={formData.demoUrl}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">
                                    <span className="link-icon">📜</span> Smart Contract (Etherscan)
                                </label>
                                <input
                                    type="url"
                                    name="contractUrl"
                                    className="form-input"
                                    placeholder="https://etherscan.io/address/0x..."
                                    value={formData.contractUrl}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        <div className="form-actions">
                            <button
                                type="button"
                                className="btn btn-secondary"
                                onClick={() => setShowPreview(!showPreview)}
                            >
                                {showPreview ? 'Hide Preview' : 'Preview Claim'}
                            </button>
                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? (
                                    <>
                                        <span className="btn-spinner"></span>
                                        Submitting...
                                    </>
                                ) : (
                                    <>Submit Claim</>
                                )}
                            </button>
                        </div>
                    </form>

                    {/* Preview Panel */}
                    <div className={`preview-panel ${showPreview ? 'active' : ''}`}>
                        <div className="preview-card card">
                            <div className="preview-header">
                                <h3>Preview</h3>
                                <span className="badge badge-purple">Draft</span>
                            </div>

                            <div className="preview-content">
                                <h4>{formData.title || 'Your Claim Title'}</h4>
                                <p className="preview-desc">
                                    {formData.description || 'Your claim description will appear here...'}
                                </p>

                                <div className="preview-meta">
                                    {formData.category && (
                                        <span className="badge badge-cyan">{formData.category}</span>
                                    )}
                                    {formData.difficulty && (
                                        <span className="badge badge-orange">{formData.difficulty}</span>
                                    )}
                                </div>

                                {formData.tags && (
                                    <div className="preview-tags">
                                        {formData.tags.split(',').map((tag, i) => (
                                            <span key={i} className="tag">{tag.trim()}</span>
                                        ))}
                                    </div>
                                )}

                                <div className="preview-evidence">
                                    <h5>Evidence</h5>
                                    {formData.githubUrl && (
                                        <div className="evidence-link">📁 GitHub Repository</div>
                                    )}
                                    {formData.demoUrl && (
                                        <div className="evidence-link">🌐 Live Demo</div>
                                    )}
                                    {formData.contractUrl && (
                                        <div className="evidence-link">📜 Smart Contract</div>
                                    )}
                                    {!formData.githubUrl && !formData.demoUrl && !formData.contractUrl && (
                                        <p className="no-evidence">No evidence links added yet</p>
                                    )}
                                </div>
                            </div>
                        </div>

                        <div className="rewards-info card">
                            <h4>🎁 Potential Rewards</h4>
                            <div className="reward-item">
                                <span>XP Earned</span>
                                <span className="reward-value">
                                    +{formData.difficulty === 'Expert' ? '750' :
                                        formData.difficulty === 'Advanced' ? '500' :
                                            formData.difficulty === 'Intermediate' ? '350' : '200'} XP
                                </span>
                            </div>
                            <div className="reward-item">
                                <span>Trust Score Boost</span>
                                <span className="reward-value text-gradient">Up to +5</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
