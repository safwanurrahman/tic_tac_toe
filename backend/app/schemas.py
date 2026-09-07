from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


Winner = Literal["red", "green", "draw"]


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime
    winner: Winner | None
    move_count: int

