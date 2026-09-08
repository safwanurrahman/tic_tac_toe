from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.database import SessionLocal
from app.main import app
from app.models import Match, Move


client = TestClient(app)


def test_complete_match_red_wins():
    response = client.post("/api/matches")

    assert response.status_code == 201
    match_id = response.json()["id"]

    try:
        positions = [0, 3, 1, 4, 2]

        for move_count, position in enumerate(positions, start=1):
            response = client.post(
                f"/api/matches/{match_id}/moves",
                json={"position": position},
            )

            assert response.status_code == 200
            assert response.json()["move_count"] == move_count

        game = response.json()

        assert game["winner"] == "red"
        assert game["current_player"] is None
        assert game["board"] == [
            "red", "red", "red",
            "green", "green", None,
            None, None, None,
        ]

        with SessionLocal() as database:
            stored_match = database.get(Match, match_id)
            stored_moves = database.scalars(
                select(Move).where(Move.match_id == match_id)
            ).all()

            assert stored_match is not None
            assert stored_match.winner == "red"
            assert stored_match.move_count == 5
            assert len(stored_moves) == 5

    finally:
        with SessionLocal() as database:
            database.execute(
                delete(Move).where(Move.match_id == match_id)
            )
            database.execute(
                delete(Match).where(Match.id == match_id)
            )
            database.commit()