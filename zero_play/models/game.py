from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from zero_play.game_state import GameState
from zero_play.models import Base, SessionBase
from zero_play.models.match import MatchRecord


class GameRecord(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    matches = relationship(MatchRecord, back_populates='game')

    def __repr__(self):
        return f'GameRecord({self.id}, {self.name!r})'

    @staticmethod
    def find_or_create(db_session: SessionBase,
                       game_state: GameState) -> 'GameRecord':
        game_record = db_session.query(GameRecord).filter_by(
            name=game_state.game_name).one_or_none()
        if game_record is None:
            game_record = GameRecord(name=game_state.game_name)
            db_session.add(game_record)
        return game_record
