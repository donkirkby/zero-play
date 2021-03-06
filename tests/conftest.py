import pytest
from PySide2.QtWidgets import QApplication

from zero_play.pixmap_differ import PixmapDiffer


@pytest.fixture(scope='session')
def pixmap_differ():
    app = QApplication()

    yield PixmapDiffer()

    assert app
