from io import BytesIO
from pathlib import Path

import pytest
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QApplication
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from zero_play.pixmap_differ import PixmapDiffer


@pytest.fixture(scope='session')
def qapp():
    yield QApplication()


@pytest.fixture(scope='session')
def pixmap_differ_session(qapp):
    diffs_path = Path(__file__).parent / 'pixmap_diffs'

    differ = PixmapDiffer(diffs_path)
    yield differ
    differ.remove_common_prefix()

    assert qapp


@pytest.fixture()
def pixmap_differ(request, pixmap_differ_session):
    """ Pass the current request to the session pixmap differ. """
    plt.close('all')  # In case pixmap differ is comparing plots.
    pixmap_differ_session.request = request

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
