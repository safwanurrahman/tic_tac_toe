from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Player = Literal["red", "green"]
Winner = Literal["red", "green", "draw"]


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime
    winner: Winner | None
    move_count: int


class MoveCreate(BaseModel):
    position: int = Field(ge=0, le=8)


class GameStateResponse(MatchResponse):
    board: list[Player | None]
    current_player: Player | None