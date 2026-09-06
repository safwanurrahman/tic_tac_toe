import { useState } from 'react'
import './App.css'

function App() {
  const [gameStarted, setGameStarted] = useState(false)

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
      <button type="button" onClick={() => setGameStarted(true)}>
        Start game
      </button>
    </main>
  )
}

export default App