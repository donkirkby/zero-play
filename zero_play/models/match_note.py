from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from zero_play.models import Base
if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from zero_play.models.match import MatchRecord


class MatchNoteRecord(Base):
    """ Analysis of a match """
    __tablename__ = 'match_notes'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('MatchRecord', back_populates='notes')
    note_type = Column(String)
    value = Column(Float)
    text = Column(String)

    def __repr__(self):
        return f'MatchNoteRecord({self.id})'
