import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/shared/Navbar';
import { LandingPage } from './pages/LandingPage';
import { GraphPage } from './pages/GraphPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { ReportsPage } from './pages/ReportsPage';
import { StressSimulatorPage } from './pages/StressSimulatorPage';
import { TimelinePage } from './pages/TimelinePage';

const App: React.FC = () => (
  <BrowserRouter>
    <div className="h-screen flex flex-col bg-gray-950 text-white overflow-hidden">
      <Navbar />
      <main className="flex-1 flex overflow-hidden">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/graph" element={<GraphPage />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/stress" element={<StressSimulatorPage />} />
          <Route path="/timeline" element={<TimelinePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  </BrowserRouter>
);

export default App;
