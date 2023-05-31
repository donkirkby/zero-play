from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from zero_play.models import Base
from zero_play.models.match_player import MatchPlayerRecord


class PlayerRecord(Base):
    __tablename__ = 'players'

    HUMAN_TYPE = 'H'
    PLAYOUT_TYPE = 'P'
    NEURAL_NETWORK_TYPE = 'N'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    milliseconds = Column(Integer)
    match_players = relationship(MatchPlayerRecord, back_populates='player')

    def __repr__(self):
        return f'PlayerRecord({self.id}, {self.name})'
