from io import BytesIO

import matplotlib.pyplot as plt

from PySide6.QtGui import QPainter, QImage

from zero_play.pixmap_differ import PixmapDiffer
from zero_play.strength_history_plot import StrengthHistoryPlot


# noinspection DuplicatedCode
def test_plot(pixmap_differ: PixmapDiffer, monkeypatch):
    size = 260
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((2*size, size)) as (actual, expected):
        strengths = [100, 200]
        future_strength = 150

        plt.plot(strengths, label='past')
        plt.plot([2], [future_strength], 'o', label='next')
        expected_png = BytesIO()
        plt.ylim(0)
        plt.title('Search iterations over time')
        plt.ylabel('Search iterations')
        plt.xlabel('Number of games played')
        plt.legend(loc='lower right')
        plt.xticks([0, 1, 2])
        plt.savefig(expected_png, dpi=60)
        expected.drawImage(0, 0, QImage.fromData(expected_png.getvalue()))

        canvas = StrengthHistoryPlot()
        monkeypatch.setattr(canvas, 'fetch_strengths', lambda _: strengths)

        session = None
        canvas.requery(session, future_strength)
        png_file = BytesIO()
        canvas.axes.figure.savefig(png_file, dpi=60)
        image = QImage.fromData(png_file.getvalue())
        actual.drawImage(0, 0, image)


# noinspection DuplicatedCode
def test_single_plot(pixmap_differ: PixmapDiffer, monkeypatch):
    size = 260
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_qpainters((2*size, size)) as (actual, expected):
        strengths = [100]
        future_strength = 150

        plt.plot(strengths, 'o', label='past')
        plt.plot([1], [future_strength], 'o', label='next')
        expected_png = BytesIO()
        plt.ylim(0)
        plt.title('Search iterations over time')
        plt.ylabel('Search iterations')
        plt.xlabel('Number of games played')
        plt.legend(loc='lower right')
        plt.xticks([0, 1])
        plt.savefig(expected_png, dpi=60)
        expected.drawImage(0, 0, QImage.fromData(expected_png.getvalue()))

        canvas = StrengthHistoryPlot()
        monkeypatch.setattr(canvas, 'fetch_strengths', lambda _: strengths)

        session = None
        canvas.requery(session, future_strength)
        png_file = BytesIO()
        canvas.axes.figure.savefig(png_file, dpi=60)
        image = QImage.fromData(png_file.getvalue())
        actual.drawImage(0, 0, image)
