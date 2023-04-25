import typing
from base64 import standard_b64encode
from contextlib import contextmanager
from pathlib import Path
import turtle

from PySide6.QtCore import (QByteArray, QBuffer, QIODevice, QSize,
                            QRect)
from PySide6.QtGui import QPixmap, QPainter, QColor, QImage, Qt
from PySide6.QtWidgets import QGraphicsView
from space_tracer import LiveImageDiffer, LiveImage, LivePainter

from zero_play.game_display import GameDisplay
from zero_play.live_qpainter import LiveQPainter


def display_diff(actual_image: QImage,
                 diff_image: QImage,
                 expected_image: QImage,
                 diff_count: int):
    # Display image when in live turtle mode.
    display_image = getattr(turtle.Turtle, 'display_image', None)
    if display_image is None:
        return
    t = turtle.Turtle()
    # noinspection PyUnresolvedReferences
    screen = t.screen  # type: ignore
    w = screen.cv.cget('width')
    h = screen.cv.cget('height')
    ox, oy = w / 2, h / 2
    text_space = (h - actual_image.height() - diff_image.height() -
                  expected_image.height())
    text_height = max(20, text_space // 3)
    font = ('Arial', text_height // 2, 'Normal')
    t.penup()
    t.goto(-ox, oy)
    t.right(90)
    t.forward(text_height)
    t.write(f'Actual', font=font)
    display_image(encode_image(actual_image), t.pos())
    t.forward(actual_image.height())
    t.forward(text_height)
    t.write(f'Diff ({diff_count} pixels)', font=font)
    display_image(encode_image(diff_image), t.pos())
    t.forward(diff_image.height())
    t.forward(text_height)
    t.write('Expected', font=font)
    display_image(encode_image(expected_image), t.pos())
    t.forward(expected_image.height())


class PixmapDiffer(LiveImageDiffer):
    @staticmethod
    def start_painter(size: LiveImage.Size,
                      fill: LiveImage.FlexibleFill = 0) -> LivePainter:
        width, height = size
        pixmap = QPixmap(width, height)
        return LiveQPainter(pixmap, QColor(fill))

    def end_painters(self, *painters: LivePainter):
        for painter in painters:
            assert isinstance(painter, LiveQPainter)
            painter.end()

    @contextmanager
    def create_qpainters(self,
                         size: LiveImage.Size,
                         fill: LiveImage.FlexibleFill = 0) -> typing.Iterator[
            typing.Tuple[QPainter, QPainter]]:
        with self.create_painters(size, fill) as (actual, expected):
            assert isinstance(actual, LiveQPainter)
            assert isinstance(expected, LiveQPainter)
            yield actual.painter, expected.painter


def encode_image(image: QImage) -> str:
    image_bytes = QByteArray()
    buffer = QBuffer(image_bytes)
    buffer.open(QIODevice.WriteOnly)  # type: ignore

    # writes pixmap into bytes in PNG format
    image.save(buffer, "PNG")  # type: ignore
    raw_bytes = buffer.data().data()
    b64_bytes = standard_b64encode(raw_bytes)
    b64_string = b64_bytes.decode('UTF-8')
    return b64_string


def decode_image(text: str) -> QImage:
    encoded_bytes = QByteArray(text.encode('utf8'))
    image_bytes = QByteArray.fromBase64(encoded_bytes)
    image = QImage.fromData(image_bytes)
    return image


def render_display(display: GameDisplay,
                   painter: QPainter,
                   is_closed: bool = True):
    """ Check scene size, render, then clear scene.

    You have to clear the scene to avoid a crash after running several unit
    tests.
    :param display: display widget whose children contain a QGraphicsView to
        render.
    :param painter: a canvas to render on
    :param is_closed: True if the display should be closed after rendering. Be
        sure to close the display before exiting the test, if it contains any
        items with reference cycles back to the scene.
    """
    __tracebackhide__ = True
    try:
        for child in display.children():
            if isinstance(child, QGraphicsView):
                view = child
                break
        else:
            raise ValueError("No QGraphicsView in display's children.")

        view.grab()  # Force layout to recalculate, if needed.
        scene_size = view.contentsRect().size()
        device = painter.device()
        assert isinstance(device, QPixmap)
        painter_size = device.size()
        if scene_size != painter_size:
            display_size = find_display_size(display, view, painter_size)
            message = (f"Try resizing display to "
                       f"{display_size.width()}x{display_size.height()}.")
            painter.drawText(QRect(0, 0,
                                   painter_size.width(), painter_size.height()),
                             Qt.AlignCenter | Qt.TextWordWrap,  # type: ignore
                             message)
            return
        assert scene_size == painter_size
        view.scene().render(painter)
    finally:
        if is_closed:
            display.close()


def find_display_size(display: GameDisplay,
                      view: QGraphicsView,
                      target_size: QSize) -> QSize:
    max_width = None
    max_height = None
    min_width = min_height = 1
    display_width = display.width()
    display_height = display.height()
    while True:
        scene_size = view.contentsRect().size()
        if scene_size.width() == target_size.width():
            min_width = max_width = display_width
        elif scene_size.width() < target_size.width():
            min_width = display_width+1
        else:
            max_width = display_width-1
        if scene_size.height() == target_size.height():
            min_height = max_height = display_height
        elif scene_size.height() < target_size.height():
            min_height = display_height+1
        else:
            max_height = display_height-1
        if max_width is None:
            display_width *= 2
        else:
            display_width = (min_width + max_width) // 2
        if max_height is None:
            display_height *= 2
        else:
            display_height = (min_height + max_height) // 2
        if min_width == max_width and min_height == max_height:
            return QSize(display_width, display_height)
        display.resize(display_width, display_height)
        view.grab()  # Force layout recalculation.
