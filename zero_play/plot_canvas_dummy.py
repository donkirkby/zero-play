from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget
from sqlalchemy.orm import Session


class PlotCanvasDummy(QLabel):
    """ A dummy view to use when Matplotlib is not installed. """
    def __init__(self, parent: QWidget):
        super().__init__('Matplotlib is not installed.', parent)
        self.setAlignment(Qt.AlignCenter)  # type: ignore

    def requery(self, db_session: Session):
        pass
