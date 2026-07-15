import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Search from './pages/Search'
import Advisor from './pages/Advisor'
import Planner from './pages/Planner'
import './App.css'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="navbar">
          <span className="nav-brand">AI Academic Advisor</span>
          <div className="nav-links">
            <NavLink to="/" end>Dashboard</NavLink>
            <NavLink to="/search">Course Search</NavLink>
            <NavLink to="/advisor">Advisor</NavLink>
            <NavLink to="/planner">Degree Planner</NavLink>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/search" element={<Search />} />
            <Route path="/advisor" element={<Advisor />} />
            <Route path="/planner" element={<Planner />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
