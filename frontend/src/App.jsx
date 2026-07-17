import { useState } from 'react'
import DashboardPage from './pages/DashboardPage.jsx'
import TopologyPage from './pages/TopologyPage.jsx'
import AlertsPage from './pages/AlertsPage.jsx'

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'topology', label: 'Topology' },
  { id: 'alerts', label: 'Alerts' },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">🚚 StreamForge</div>
        <nav className="app-nav">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.id}
              className={activeTab === item.id ? 'nav-btn active' : 'nav-btn'}
              onClick={() => setActiveTab(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'dashboard' && <DashboardPage />}
        {activeTab === 'topology' && <TopologyPage />}
        {activeTab === 'alerts' && <AlertsPage />}
      </main>
    </div>
  )
}