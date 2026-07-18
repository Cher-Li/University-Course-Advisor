import { useEffect, useState } from 'react'
import { getCourses, getRecommendations } from '../api'

const DEFAULT_COMPLETED = ['COMP250', 'MATH240']

export default function Dashboard() {
  const [courses, setCourses] = useState([])
  const [available, setAvailable] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getCourses(),
      getRecommendations(DEFAULT_COMPLETED),
    ]).then(([coursesRes, recRes]) => {
      setCourses(coursesRes.data)
      setAvailable(recRes.data.available)
      setLoading(false)
    })
  }, [])

  if (loading) return <p className="loading">Loading...</p>

  return (
    <div>
      <h1>Dashboard</h1>
      <p className="subtitle">Your academic overview</p>

      <div className="card">
        <h3 style={{ marginBottom: '0.75rem' }}>Completed Courses</h3>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {DEFAULT_COMPLETED.map(id => (
            <span key={id} className="tag green">{id}</span>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: '0.75rem' }}>Available to Take Next</h3>
        {available.length === 0 ? (
          <p style={{ color: '#64748b' }}>No courses available yet.</p>
        ) : (
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {available.map(id => (
              <span key={id} className="tag">{id}</span>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h3 style={{ marginBottom: '0.75rem' }}>All Courses ({courses.length})</h3>
        {courses.map(c => (
          <div key={c.id} className="status-row">
            <div>
              <strong>{c.id}</strong> — {c.name}
            </div>
            <span className="tag" style={{ marginLeft: '1rem' }}>{c.credits} cr</span>
          </div>
        ))}
      </div>
    </div>
  )
}
