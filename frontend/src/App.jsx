import { useEffect, useState } from 'react'
import './App.css'

const EMPTY_BOARD = Array(9).fill(null)

function App() {
  const [backendStatus, setBackendStatus] = useState('checking')
  const [match, setMatch] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
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
    setIsLoading(true)
    setError('')

    try {
      const response = await fetch('/api/matches', {
        method: 'POST',
      })

      if (!response.ok) {
        throw new Error('Could not create match')
      }

      const newMatch = await response.json()

      setMatch({
        ...newMatch,
        board: [...EMPTY_BOARD],
        current_player: 'red',
      })
    } catch {
      setError('Could not start the game.')
    } finally {
      setIsLoading(false)
    }
  }

  async function playMove(position) {
    if (
      isLoading ||
      match.winner ||
      match.board[position] !== null
    ) {
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const response = await fetch(
        `/api/matches/${match.id}/moves`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ position }),
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail)
      }

      setMatch(data)
    } catch (requestError) {
      setError(requestError.message || 'Could not make move.')
    } finally {
      setIsLoading(false)
    }
  }

  function getStatusMessage() {
    if (match.winner === 'draw') {
      return 'The match is a draw!'
    }

    if (match.winner) {
      return `Player ${match.winner} wins!`
    }

    return `Player ${match.current_player}'s turn`
  }

  if (!match) {
    return (
      <main className="landing-page">
        <h1>Tic Tac Toe</h1>
        <p>A local game for Player Red and Player Green.</p>
        <p>Backend status: {backendStatus}</p>

        <button
          type="button"
          disabled={backendStatus !== 'ok' || isLoading}
          onClick={startGame}
        >
          {isLoading ? 'Starting...' : 'Start game'}
        </button>

        {error && <p role="alert">{error}</p>}
      </main>
    )
  }

  return (
    <main className="game-page">
      <h1>Tic Tac Toe</h1>
      <p>Match #{match.id}</p>
      <h2>{getStatusMessage()}</h2>

      <div className="board">
        {match.board.map((player, position) => (
          <button
            className={`square ${player || ''}`}
            type="button"
            key={position}
            disabled={Boolean(player) || Boolean(match.winner) || isLoading}
            onClick={() => playMove(position)}
            aria-label={`Square ${position + 1}${player ? `: ${player}` : ''}`}
          >
            {player === 'red' ? 'R' : player === 'green' ? 'G' : ''}
          </button>
        ))}
      </div>

      <p>Moves: {match.move_count}</p>

      <button type="button" disabled={isLoading} onClick={startGame}>
        New match
      </button>

      {error && <p role="alert">{error}</p>}
    </main>
  )
}

export default App