from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from zero_play.models import Base
from zero_play.models.match import MatchRecord


class GameRecord(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    matches = relationship(MatchRecord, back_populates='game')

    def __repr__(self):
        return f'GameRecord({self.id}, {self.name!r})'
