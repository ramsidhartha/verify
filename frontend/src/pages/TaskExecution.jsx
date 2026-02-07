import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { mockClaims, mockVerificationTasks } from '../data/mockData';
import Badge from '../components/Badge';
import ProgressBar from '../components/ProgressBar';
import './TaskExecution.css';

export default function TaskExecution() {
    const { id } = useParams();
    const claim = mockClaims.find(c => c.id === id) || mockClaims[0];

    const [tasks, setTasks] = useState(mockVerificationTasks);
    const [activeTask, setActiveTask] = useState(tasks[1]); // Start with in-progress task
    const [notes, setNotes] = useState('');

    const totalChecks = tasks.reduce((sum, t) => sum + t.checklist.length, 0);
    const completedChecks = tasks.reduce(
        (sum, t) => sum + t.checklist.filter(c => c.completed).length, 0
    );
    const overallProgress = Math.round((completedChecks / totalChecks) * 100);

    const toggleCheckItem = (taskId, checkId) => {
        setTasks(prevTasks => prevTasks.map(task => {
            if (task.id !== taskId) return task;
            return {
                ...task,
                checklist: task.checklist.map(check =>
                    check.id === checkId ? { ...check, completed: !check.completed } : check
                )
            };
        }));

        // Update active task if needed
        if (activeTask.id === taskId) {
            setActiveTask(prev => ({
                ...prev,
                checklist: prev.checklist.map(check =>
                    check.id === checkId ? { ...check, completed: !check.completed } : check
                )
            }));
        }
    };

    const getTaskStatus = (task) => {
        const completed = task.checklist.filter(c => c.completed).length;
        const total = task.checklist.length;
        if (completed === total) return 'completed';
        if (completed > 0) return 'in-progress';
        return 'pending';
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'completed': return '✅';
            case 'in-progress': return '🔄';
            case 'pending': return '⏳';
            default: return '○';
        }
    };

    return (
        <div className="task-execution-page">
            <div className="container">
                {/* Breadcrumb */}
                <div className="breadcrumb">
                    <Link to="/quests">← Back to Quests</Link>
                </div>

                <div className="task-layout">
                    {/* Main Content */}
                    <div className="task-main">
                        {/* Claim Info Card */}
                        <div className="claim-info card">
                            <div className="claim-header">
                                <div>
                                    <h1>{claim.title}</h1>
                                    <div className="claim-meta">
                                        <Badge variant="cyan">{claim.category}</Badge>
                                        <Badge variant="orange">{claim.difficulty}</Badge>
                                        <span className="claim-date">Submitted {claim.createdAt}</span>
                                    </div>
                                </div>
                                <div className="claim-rewards-box">
                                    <div className="reward-large">+{claim.xpReward} XP</div>
                                    <div className="reward-token">🪙 {claim.tokenReward} tokens</div>
                                </div>
                            </div>
                            <p className="claim-description">{claim.description}</p>

                            <div className="evidence-links">
                                <h4>📎 Evidence</h4>
                                <div className="evidence-list">
                                    {claim.evidence.map((ev, i) => (
                                        <a key={i} href={ev.url} target="_blank" rel="noopener noreferrer" className="evidence-item">
                                            {ev.type === 'github' && '📁 GitHub Repository'}
                                            {ev.type === 'demo' && '🌐 Live Demo'}
                                            {ev.type === 'contract' && '📜 Smart Contract'}
                                        </a>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Active Task Card */}
                        <div className="active-task card">
                            <div className="active-task-header">
                                <div>
                                    <span className="task-type-badge">
                                        {activeTask.type === 'automated' ? '🤖 AI-Assisted' : '👤 Manual Review'}
                                    </span>
                                    <h2>{activeTask.title}</h2>
                                    <p>{activeTask.description}</p>
                                </div>
                            </div>

                            <div className="checklist">
                                <h3>Verification Checklist</h3>
                                {activeTask.checklist.map(check => (
                                    <label
                                        key={check.id}
                                        className={`checklist-item ${check.completed ? 'completed' : ''}`}
                                    >
                                        <input
                                            type="checkbox"
                                            checked={check.completed}
                                            onChange={() => toggleCheckItem(activeTask.id, check.id)}
                                        />
                                        <span className="checkmark">
                                            {check.completed ? '✓' : ''}
                                        </span>
                                        <span className="check-text">{check.text}</span>
                                    </label>
                                ))}
                            </div>

                            <div className="notes-section">
                                <h4>📝 Verification Notes</h4>
                                <textarea
                                    className="form-textarea"
                                    placeholder="Add your notes, observations, or findings here..."
                                    value={notes}
                                    onChange={(e) => setNotes(e.target.value)}
                                    rows={4}
                                />
                            </div>

                            <div className="task-actions">
                                <button className="btn btn-secondary">Save Progress</button>
                                <button className="btn btn-success">
                                    Complete Verification ✓
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Sidebar */}
                    <div className="task-sidebar">
                        {/* Progress Card */}
                        <div className="progress-card card">
                            <h3>Overall Progress</h3>
                            <div className="progress-circle-wrapper">
                                <div
                                    className="progress-circle"
                                    style={{ '--progress': overallProgress }}
                                >
                                    <span className="progress-value">{overallProgress}%</span>
                                </div>
                            </div>
                            <ProgressBar value={completedChecks} max={totalChecks} showLabel />
                            <p className="progress-detail">
                                {completedChecks} of {totalChecks} checks completed
                            </p>
                        </div>

                        {/* Task List */}
                        <div className="task-list card">
                            <h3>Verification Tasks</h3>
                            {tasks.map(task => {
                                const status = getTaskStatus(task);
                                const completed = task.checklist.filter(c => c.completed).length;
                                const total = task.checklist.length;

                                return (
                                    <button
                                        key={task.id}
                                        className={`task-item ${activeTask.id === task.id ? 'active' : ''} ${status}`}
                                        onClick={() => setActiveTask(task)}
                                    >
                                        <span className="task-status-icon">{getStatusIcon(status)}</span>
                                        <div className="task-item-content">
                                            <span className="task-item-title">{task.title}</span>
                                            <span className="task-item-progress">{completed}/{total}</span>
                                        </div>
                                        <ProgressBar value={completed} max={total} size="sm" />
                                    </button>
                                );
                            })}
                        </div>

                        {/* Submitter Info */}
                        <div className="submitter-card card">
                            <h3>Submitted By</h3>
                            <div className="submitter-profile">
                                <img src={claim.submittedBy.avatar} alt="" className="submitter-avatar-lg" />
                                <div>
                                    <div className="submitter-name-lg">{claim.submittedBy.name}</div>
                                    <div className="submitter-trust-lg">
                                        Trust Score: <span className="trust-value">{claim.submittedBy.trustScore}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
