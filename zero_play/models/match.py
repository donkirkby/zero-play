from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from zero_play.models import Base
from zero_play.models.match_note import MatchNoteRecord
from zero_play.models.match_player import MatchPlayerRecord
if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from zero_play.models.game import GameRecord


class MatchRecord(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('GameRecord', back_populates='matches')
    start_time = Column(DateTime)
    total_seconds = Column(Integer)
    move_count = Column(Integer)
    notes = relationship(MatchNoteRecord, back_populates='match')
    match_players = relationship(MatchPlayerRecord, back_populates='match')

    def __repr__(self):
        return f'MatchRecord({self.id})'
