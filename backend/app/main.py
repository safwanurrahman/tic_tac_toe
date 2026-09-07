from typing import Annotated

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Match
from app.schemas import MatchResponse


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