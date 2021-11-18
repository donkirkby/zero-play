from PySide6.QtGui import QPainter, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel, QHBoxLayout

from zero_play.grid_display import GridDisplay
from zero_play.pixmap_differ import PixmapDiffer
from zero_play.scaled_label import ScaledLabel


# noinspection DuplicatedCode
def test_text(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'scaled_label_text') as (
            actual,
            expected):
        ex_widget = QWidget()
        ex_layout = QVBoxLayout(ex_widget)
        ex_label1 = QLabel('Lorem ipsum')
        ex_label2 = QLabel('Lorem ipsum')
        ex_font = ex_label1.font()
        if ex_font.family() == 'Sans Serif':
            # Fonts are different on Travis CI.
            big_font_size = 30
            small_font_size = 25
        else:
            big_font_size = 35
            small_font_size = 28
        ex_font.setPointSize(big_font_size)
        ex_label1.setFont(ex_font)
        ex_font.setPointSize(small_font_size)
        ex_label2.setFont(ex_font)
        ex_size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        ex_label1.setSizePolicy(ex_size_policy)
        ex_label1.setAlignment(Qt.AlignBottom)
        ex_label2.setAlignment(Qt.AlignTop)
        ex_label2.setSizePolicy(ex_size_policy)
        ex_layout.addWidget(ex_label1)
        ex_layout.addWidget(ex_label2)
        ex_layout.setStretch(0, 4)
        ex_layout.setStretch(1, 1)

        ex_widget.resize(300, 240)
        expected.drawPixmap(0, 0, ex_widget.grab())

        widget = QWidget()
        layout = QVBoxLayout(widget)
        label1 = ScaledLabel('Lorem ipsum')
        label2 = ScaledLabel('Lorem ipsum')
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        label1.setSizePolicy(size_policy)
        label2.setSizePolicy(size_policy)
        label1.setScaledContents(True)
        label2.setScaledContents(True)
        label1.setAlignment(Qt.AlignBottom)
        label2.setAlignment(Qt.AlignTop)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        widget.resize(300, 240)

        actual.drawPixmap(0, 0, widget.grab())


# noinspection DuplicatedCode
def test_pixmap(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'scaled_label_pixmap') as (
            actual,
            expected):
        ex_widget = QWidget()
        ex_widget.resize(300, 240)
        expected.drawPixmap(0, 0, ex_widget.grab())
        icon = GridDisplay.create_icon(GridDisplay.player2_colour)

        expected.drawPixmap(0, 0, icon.scaled(120, 120,
                                              Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation))
        expected.drawPixmap(110, 120, icon.scaled(80, 80,
                                                  Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation))
        expected.drawPixmap(260, 200, icon.scaled(40, 40,
                                                  Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation))

        widget = QWidget()
        layout = QVBoxLayout(widget)
        label1 = ScaledLabel()
        label2 = ScaledLabel()
        label3 = ScaledLabel()
        label1.setPixmap(icon)
        label2.setPixmap(icon)
        label3.setPixmap(icon)
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        label1.setSizePolicy(size_policy)
        label2.setSizePolicy(size_policy)
        label3.setSizePolicy(size_policy)
        label1.setScaledContents(True)
        label2.setScaledContents(True)
        label3.setScaledContents(True)
        label1.setAlignment(Qt.AlignLeft)
        label2.setAlignment(Qt.AlignCenter)
        label3.setAlignment(Qt.AlignRight)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.setStretch(0, 3)
        layout.setStretch(1, 2)
        layout.setStretch(2, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widget.resize(300, 240)

        actual.drawPixmap(0, 0, widget.grab())


# noinspection DuplicatedCode
def test_pixmap_vertical(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'scaled_label_pixmap_vertical') as (
            actual,
            expected):
        ex_widget = QWidget()
        ex_widget.resize(300, 240)
        expected.drawPixmap(0, 0, ex_widget.grab())
        icon = GridDisplay.create_icon(GridDisplay.player2_colour)

        expected.drawPixmap(0, 0, icon.scaled(150, 150,
                                              Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation))
        expected.drawPixmap(150, 70, icon.scaled(100, 100,
                                                 Qt.KeepAspectRatio,
                                                 Qt.SmoothTransformation))
        expected.drawPixmap(250, 190, icon.scaled(50, 50,
                                                  Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation))

        widget = QWidget()
        layout = QHBoxLayout(widget)
        label1 = ScaledLabel()
        label2 = ScaledLabel()
        label3 = ScaledLabel()
        label1.setPixmap(icon)
        label2.setPixmap(icon)
        label3.setPixmap(icon)
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        label1.setSizePolicy(size_policy)
        label2.setSizePolicy(size_policy)
        label3.setSizePolicy(size_policy)
        label1.setScaledContents(True)
        label2.setScaledContents(True)
        label3.setScaledContents(True)
        label1.setAlignment(Qt.AlignTop)
        label2.setAlignment(Qt.AlignCenter)
        label3.setAlignment(Qt.AlignBottom)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.setStretch(0, 3)
        layout.setStretch(1, 2)
        layout.setStretch(2, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widget.resize(300, 240)

        actual.drawPixmap(0, 0, widget.grab())
