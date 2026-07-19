import { useState } from 'react'
import { getAdvice } from '../api'

export default function Advisor() {
  const [goal, setGoal] = useState('')
  const [completed, setCompleted] = useState('COMP250, MATH240')
  const [advice, setAdvice] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!goal.trim()) return
    setLoading(true)
    setAdvice('')
    const completedList = completed.split(',').map(s => s.trim()).filter(Boolean)
    const res = await getAdvice(goal, completedList)
    setAdvice(res.data.advice)
    setLoading(false)
  }

  return (
    <div>
      <h1>AI Advisor</h1>
      <p className="subtitle">Describe your goal and get personalized course advice</p>

      <div className="card">
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.4rem', fontWeight: 500, fontSize: '0.9rem' }}>
              Your goal
            </label>
            <input
              value={goal}
              onChange={e => setGoal(e.target.value)}
              placeholder="e.g. I want to get an ML internship"
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.4rem', fontWeight: 500, fontSize: '0.9rem' }}>
              Completed courses (comma separated)
            </label>
            <input
              value={completed}
              onChange={e => setCompleted(e.target.value)}
              placeholder="e.g. COMP250, MATH240, COMP302"
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Getting advice...' : 'Get Advice'}
          </button>
        </form>
      </div>

      {advice && (
        <div className="card">
          <h3 style={{ marginBottom: '0.75rem' }}>Advisor Response</h3>
          <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7, fontSize: '0.95rem' }}>{advice}</p>
        </div>
      )}
    </div>
  )
}
