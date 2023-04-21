import pytest
from PySide6.QtWidgets import QApplication
from matplotlib import pyplot as plt

from zero_play.pixmap_differ import PixmapDiffer


@pytest.fixture(scope='session')
def pixmap_differ_session():
    app = QApplication()

    yield PixmapDiffer()

    assert app


@pytest.fixture()
def pixmap_differ(pixmap_differ_session):
    plt.close('all')  # In case pixmap differ is comparing plots.

    yield pixmap_differ_session
