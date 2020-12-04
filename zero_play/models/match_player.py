from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from zero_play.models import Base
if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from zero_play.models.match import MatchRecord
    # noinspection PyUnresolvedReferences
    from zero_play.models.player import PlayerRecord


class MatchPlayerRecord(Base):
    __tablename__ = 'match_players'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('MatchRecord', back_populates='match_players')
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('PlayerRecord', back_populates='match_players')
    player_number = Column(Integer)
    result = Column(Integer)  # Win = 1, Loss = -1, Tie = 0
    avg_think = Column(Float)
    min_think = Column(Float)
    max_think = Column(Float)

    def __repr__(self):
        return f'MatchPlayerRecord({self.id})'
