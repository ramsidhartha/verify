import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Landing from './pages/Landing';
import SubmitClaim from './pages/SubmitClaim';
import QuestDashboard from './pages/QuestDashboard';
import TaskExecution from './pages/TaskExecution';
import DeveloperProfile from './pages/DeveloperProfile';

function App() {
    return (
        <Router>
            <div className="app">
                <Navbar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Landing />} />
                        <Route path="/submit" element={<SubmitClaim />} />
                        <Route path="/quests" element={<QuestDashboard />} />
                        <Route path="/task/:id" element={<TaskExecution />} />
                        <Route path="/profile" element={<DeveloperProfile />} />
                    </Routes>
                </main>
                <Footer />
            </div>
        </Router>
    );
}

export default App;
