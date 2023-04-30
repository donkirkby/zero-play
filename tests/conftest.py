from io import BytesIO

import pytest
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QApplication
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

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


def paint_figure(figure: Figure, painter: QPainter):
    data = BytesIO()
    dpi = figure.dpi
    figure.set_size_inches(painter.window().width()/dpi,
                           painter.window().height()/dpi)
    figure.tight_layout()
    figure.savefig(data)
    image = QImage.fromData(data.getvalue())
    painter.drawImage(0, 0, image)
