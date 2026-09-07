from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint(
            "winner IN ('red', 'green', 'draw') OR winner IS NULL",
            name="check_match_winner",
        ),
        CheckConstraint(
            "move_count BETWEEN 0 AND 9",
            name="check_match_move_count",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    winner: Mapped[str | None] = mapped_column(String(5), nullable=True)
    move_count: Mapped[int] = mapped_column(Integer, default=0)


class Move(Base):
    __tablename__ = "moves"
    __table_args__ = (
        CheckConstraint(
            "player IN ('red', 'green')",
            name="check_move_player",
        ),
        CheckConstraint(
            "position BETWEEN 0 AND 8",
            name="check_move_position",
        ),
        UniqueConstraint(
            "match_id",
            "position",
            name="unique_position_per_match",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        index=True,
    )
    player: Mapped[str] = mapped_column(String(5))
    position: Mapped[int] = mapped_column(Integer)