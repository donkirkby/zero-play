from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QSizePolicy

from zero_play.pixmap_differ import PixmapDiffer
from zero_play.scaled_radio_button import ScaledRadioButton
from zero_play.tictactoe.display import TicTacToeDisplay


# noinspection DuplicatedCode
def test_text(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'scaled_radio_button_text') as (
            actual,
            expected):
        ex_widget = QWidget()
        ex_layout = QVBoxLayout(ex_widget)
        ex_radio1 = QRadioButton('Lorem ipsum')
        ex_radio2 = QRadioButton('Lorem ipsum')
        ex_font = ex_radio1.font()
        if ex_font.family() == 'Sans Serif':
            # Fonts are different on Travis CI.
            big_font_size = 26
            small_font_size = 25
            ex_radio1.setStyleSheet('QRadioButton::indicator {width: 26} '
                                    'QRadioButton {spacing: 13}')
            ex_radio2.setStyleSheet('QRadioButton::indicator {width: 25} '
                                    'QRadioButton {spacing: 12}')
        else:
            big_font_size = 29
            small_font_size = 28
            ex_radio1.setStyleSheet('QRadioButton::indicator {width: 29} '
                                    'QRadioButton {spacing: 14}')
            ex_radio2.setStyleSheet('QRadioButton::indicator {width: 28} '
                                    'QRadioButton {spacing: 14}')
        ex_font.setPointSize(big_font_size)
        ex_radio1.setFont(ex_font)
        ex_font.setPointSize(small_font_size)
        ex_radio2.setFont(ex_font)
        ex_size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        ex_radio1.setSizePolicy(ex_size_policy)
        ex_radio2.setSizePolicy(ex_size_policy)
        ex_layout.addWidget(ex_radio1)
        ex_layout.addWidget(ex_radio2)
        ex_layout.setStretch(0, 4)
        ex_layout.setStretch(1, 1)

        ex_widget.resize(300, 240)
        expected.drawPixmap(0, 0, ex_widget.grab())

        widget = QWidget()
        layout = QVBoxLayout(widget)
        radio1 = ScaledRadioButton('Lorem ipsum')
        radio2 = ScaledRadioButton('Lorem ipsum')
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        radio1.setSizePolicy(size_policy)
        radio2.setSizePolicy(size_policy)
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        widget.resize(300, 240)

        actual.drawPixmap(0, 0, widget.grab())


# noinspection DuplicatedCode
def test_icon(pixmap_differ: PixmapDiffer):
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(300, 240, 'scaled_radio_button_icon') as (
            actual,
            expected):
        display = TicTacToeDisplay()
        icon = display.player1_icon
        display.close()
        ex_widget = QWidget()
        ex_layout = QVBoxLayout(ex_widget)
        ex_radio1 = QRadioButton()
        ex_radio2 = QRadioButton('Lorem ipsum')
        ex_radio1.setIcon(icon)
        ex_radio2.setIcon(icon)
        ex_font = ex_radio1.font()
        if ex_font.family() == 'Sans Serif':
            # Fonts are different on Travis CI.
            big_font_size = 93
            small_font_size = 22
            ex_radio1.setStyleSheet('QRadioButton::indicator {width: 93} '
                                    'QRadioButton {spacing: 46}')
            ex_radio2.setStyleSheet('QRadioButton::indicator {width: 22} '
                                    'QRadioButton {spacing: 11}')
        else:
            big_font_size = 93
            small_font_size = 25
            ex_radio1.setStyleSheet('QRadioButton::indicator {width: 93} '
                                    'QRadioButton {spacing: 46}')
            ex_radio2.setStyleSheet('QRadioButton::indicator {width: 25} '
                                    'QRadioButton {spacing: 12}')
        ex_radio1.setIconSize(QSize(big_font_size*3//2, big_font_size*3//2))
        ex_radio2.setIconSize(QSize(small_font_size*3//2, small_font_size*3//2))
        ex_font.setPointSize(big_font_size)
        ex_radio1.setFont(ex_font)
        ex_font.setPointSize(small_font_size)
        ex_radio2.setFont(ex_font)
        ex_size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        ex_radio1.setSizePolicy(ex_size_policy)
        ex_radio2.setSizePolicy(ex_size_policy)
        ex_layout.addWidget(ex_radio1)
        ex_layout.addWidget(ex_radio2)
        ex_layout.setStretch(0, 4)
        ex_layout.setStretch(1, 1)

        ex_widget.resize(300, 240)
        expected.drawPixmap(0, 0, ex_widget.grab())

        widget = QWidget()
        layout = QVBoxLayout(widget)
        radio1 = ScaledRadioButton()
        radio2 = ScaledRadioButton('Lorem ipsum')
        radio1.setIcon(icon)
        radio2.setIcon(icon)
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        radio1.setSizePolicy(size_policy)
        radio2.setSizePolicy(size_policy)
        layout.addWidget(radio1)
        layout.addWidget(radio2)
        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        widget.resize(300, 240)

        actual.drawPixmap(0, 0, widget.grab())
