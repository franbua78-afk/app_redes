import { Link, Outlet, useLocation } from 'react-router-dom'

export function AppShell() {
  const { pathname } = useLocation()
  const active = (p: string) => pathname === p ? 'text-blue-600' : 'text-gray-600'
  return (
    <div className="min-h-screen">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link to="/" className="font-semibold">AI Shorts Studio</Link>
          <nav className="flex gap-4">
            <Link className={active('/')} to="/">Dashboard</Link>
            <Link className={active('/calendar')} to="/calendar">Calendar</Link>
            <Link className={active('/analytics')} to="/analytics">Analytics</Link>
            <Link className={active('/templates')} to="/templates">Templates</Link>
          </nav>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}

