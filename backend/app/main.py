from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.game import get_winner, is_draw
from app.models import Match, Move
from app.schemas import GameStateResponse, MatchResponse, MoveCreate


app = FastAPI(title="Tic Tac Toe API")

DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/api/matches",
    response_model=MatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_match(database: DatabaseSession):
    match = Match()

    database.add(match)
    database.commit()
    database.refresh(match)

    return match


@app.post(
    "/api/matches/{match_id}/moves",
    response_model=GameStateResponse,
)
def create_move(
    match_id: int,
    move_data: MoveCreate,
    database: DatabaseSession,
):
    match = database.get(Match, match_id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    if match.winner is not None:
        raise HTTPException(status_code=409, detail="Match is already finished")

    moves = database.scalars(
        select(Move)
        .where(Move.match_id == match_id)
        .order_by(Move.id)
    ).all()

    board = [None] * 9

    for existing_move in moves:
        board[existing_move.position] = existing_move.player

    if board[move_data.position] is not None:
        raise HTTPException(status_code=409, detail="Position is already occupied")

    player = "red" if match.move_count % 2 == 0 else "green"
    board[move_data.position] = player

    move = Move(
        match_id=match.id,
        player=player,
        position=move_data.position,
    )

    match.move_count += 1

    winner = get_winner(board)

    if winner is not None:
        match.winner = winner
    elif is_draw(board):
        match.winner = "draw"

    database.add(move)
    database.commit()
    database.refresh(match)

    next_player = None
    if match.winner is None:
        next_player = "red" if match.move_count % 2 == 0 else "green"

    return GameStateResponse(
        id=match.id,
        started_at=match.started_at,
        winner=match.winner,
        move_count=match.move_count,
        board=board,
        current_player=next_player,
    )
