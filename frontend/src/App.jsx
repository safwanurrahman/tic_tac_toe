import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [gameStarted, setGameStarted] = useState(false)
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    async function checkBackend() {
      try {
        const response = await fetch('/api/health')

        if (!response.ok) {
          throw new Error('Backend request failed')
        }

        const data = await response.json()
        setBackendStatus(data.status)
      } catch {
        setBackendStatus('offline')
      }
    }

    checkBackend()
  }, [])

  if (gameStarted) {
    return (
      <main>
        <h1>Game screen</h1>
        <p>We will build the board next.</p>
      </main>
    )
  }

  return (
    <main>
      <h1>Tic Tac Toe</h1>
      <p>A local game for Player Red and Player Green.</p>
      <p>Backend status: {backendStatus}</p>
      <button type="button" onClick={() => setGameStarted(true)}>
        Start game
      </button>
    </main>
  )
}

export default App

