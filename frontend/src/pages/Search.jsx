import { useState } from 'react'
import { searchCourses } from '../api'

export default function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    const res = await searchCourses(query)
    setResults(res.data.results)
    setLoading(false)
    setSearched(true)
  }

  return (
    <div>
      <h1>Course Search</h1>
      <p className="subtitle">Search courses by topic, interest, or goal</p>

      <div className="card">
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.75rem' }}>
          <input
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="e.g. machine learning, computer vision, algorithms..."
          />
          <button type="submit" disabled={loading} style={{ whiteSpace: 'nowrap' }}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>
      </div>

      {searched && results.length === 0 && (
        <p className="loading">No results found.</p>
      )}

      {results.map(course => (
        <div key={course.id} className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <strong>{course.id}</strong> — {course.name}
              <p style={{ color: '#64748b', fontSize: '0.9rem', marginTop: '0.4rem' }}>
                {course.description}
              </p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', marginLeft: '1rem', alignItems: 'flex-end' }}>
              <span className="tag">{course.credits} cr</span>
              <span className="tag" style={{ background: '#f0fdf4', color: '#16a34a' }}>
                {Math.round(course.relevance_score * 100)}% match
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
