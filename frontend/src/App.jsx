import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState('checking')
  const [match, setMatch] = useState(null)
  const [isStarting, setIsStarting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function checkBackend() {
      try {
        const response = await fetch('/api/health')
        const data = await response.json()
        setBackendStatus(data.status)
      } catch {
        setBackendStatus('offline')
      }
    }

    checkBackend()
  }, [])

  async function startGame() {
    setIsStarting(true)
    setError('')

    try {
      const response = await fetch('/api/matches', {
        method: 'POST',
      })

      if (!response.ok) {
        throw new Error('Could not create match')
      }

      setMatch(await response.json())
    } catch {
      setError('Could not start the game.')
    } finally {
      setIsStarting(false)
    }
  }

  if (match) {
    return (
      <main>
        <h1>Game screen</h1>
        <p>Match #{match.id}</p>
        <p>Moves: {match.move_count}</p>
      </main>
    )
  }

  return (
    <main>
      <h1>Tic Tac Toe</h1>
      <p>A local game for Player Red and Player Green.</p>
      <p>Backend status: {backendStatus}</p>

      <button
        type="button"
        disabled={backendStatus !== 'ok' || isStarting}
        onClick={startGame}
      >
        {isStarting ? 'Starting...' : 'Start game'}
      </button>

      {error && <p role="alert">{error}</p>}
    </main>
  )
}

export default App