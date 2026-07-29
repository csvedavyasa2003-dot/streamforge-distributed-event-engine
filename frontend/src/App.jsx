import { useState, useEffect } from 'react'
import DashboardPage from './pages/DashboardPage.jsx'
import TopologyPage from './pages/TopologyPage.jsx'
import AlertsPage from './pages/AlertsPage.jsx'
import IntroLoader from './components/IntroLoader.jsx'

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'topology', label: 'Topology' },
  { id: 'alerts', label: 'Alerts' },
]

const INTRO_DURATION_MS = 2200

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [showIntro, setShowIntro] = useState(true)
  const [isFadingOut, setIsFadingOut] = useState(false)

  useEffect(() => {
    const fadeTimer = setTimeout(() => setIsFadingOut(true), INTRO_DURATION_MS - 400)
    const removeTimer = setTimeout(() => setShowIntro(false), INTRO_DURATION_MS)
    return () => {
      clearTimeout(fadeTimer)
      clearTimeout(removeTimer)
    }
  }, [])

  if (showIntro) {
    return (
      <div className={isFadingOut ? 'intro-wrapper intro-wrapper--fade' : 'intro-wrapper'}>
        <IntroLoader />
      </div>
    )
  }

  return (
    <div className="app-shell app-shell--enter">
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