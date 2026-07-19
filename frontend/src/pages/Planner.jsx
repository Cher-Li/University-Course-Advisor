import { useState } from 'react'
import { checkGraduation, getRecommendations } from '../api'

export default function Planner() {
  const [completed, setCompleted] = useState('COMP250, MATH240')
  const [report, setReport] = useState(null)
  const [available, setAvailable] = useState([])
  const [loading, setLoading] = useState(false)

  const handleCheck = async (e) => {
    e.preventDefault()
    setLoading(true)
    const completedList = completed.split(',').map(s => s.trim()).filter(Boolean)
    const [gradRes, recRes] = await Promise.all([
      checkGraduation(completedList),
      getRecommendations(completedList),
    ])
    setReport(gradRes.data)
    setAvailable(recRes.data.available)
    setLoading(false)
  }

  return (
    <div>
      <h1>Degree Planner</h1>
      <p className="subtitle">Check your graduation requirements</p>

      <div className="card">
        <form onSubmit={handleCheck} style={{ display: 'flex', gap: '0.75rem' }}>
          <input
            value={completed}
            onChange={e => setCompleted(e.target.value)}
            placeholder="Completed courses, comma separated"
          />
          <button type="submit" disabled={loading} style={{ whiteSpace: 'nowrap' }}>
            {loading ? 'Checking...' : 'Check Status'}
          </button>
        </form>
      </div>

      {report && (
        <>
          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <h3>Graduation Status</h3>
              <span className={`tag ${report.can_graduate ? 'green' : 'red'}`}>
                {report.can_graduate ? '✓ Ready to graduate' : '✗ Not yet'}
              </span>
            </div>
            {report.requirements.map(req => (
              <div key={req.name} className="status-row">
                <div>
                  <strong style={{ fontSize: '0.9rem' }}>{req.name}</strong>
                  <p style={{ color: '#64748b', fontSize: '0.85rem', marginTop: '0.15rem' }}>{req.detail}</p>
                </div>
                <span className={`tag ${req.satisfied ? 'green' : 'red'}`}>
                  {req.satisfied ? '✓' : '✗'}
                </span>
              </div>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginBottom: '0.75rem' }}>Available to Take Next</h3>
            {available.length === 0 ? (
              <p style={{ color: '#64748b' }}>No courses available with current completed set.</p>
            ) : (
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {available.map(id => (
                  <span key={id} className="tag">{id}</span>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}
