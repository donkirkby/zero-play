import typing
from base64 import standard_b64encode
from contextlib import contextmanager
from pathlib import Path
import turtle

from PySide6.QtCore import (QByteArray, QBuffer, QIODevice, QSize,
                            QRect)
from PySide6.QtGui import QPixmap, QPainter, QColor, QImage, Qt
from PySide6.QtWidgets import QGraphicsView

from zero_play.game_display import GameDisplay


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


class PixmapDiffer:
    def __init__(self):
        self.name = None
        self.actual_pixmap = self.expected_pixmap = None
        self.actual = self.expected = None
        self.different_pixels = 0
        self.diff_min_x = self.diff_min_y = None
        self.diff_max_x = self.diff_max_y = None
        self.max_diff = 0

        self.names = set()

        self.work_dir: Path = (Path(__file__).parent.parent /
                               'tests' / 'pixmap_diffs')
        self.work_dir.mkdir(exist_ok=True)
        for work_file in self.work_dir.iterdir():
            if work_file.name == 'README.md':
                continue
            assert work_file.suffix == '.png'
            work_file.unlink()

    @contextmanager
    def create_painters(
            self,
            width: int,
            height: int,
            name: str,
            max_diff: int = 0) -> typing.Iterator[typing.Tuple[QPainter, QPainter]]:
        self.max_diff = max_diff
        try:
            yield self.start(width, height, name)
        finally:
            self.end()
        self.assert_equal()

    def start(self,
              width: int,
              height: int,
              name: str) -> typing.Tuple[QPainter, QPainter]:
        """ Create painters for the actual and expected images.

        Caller must either call end() or assert_equal() to properly clean up
        the painters and pixmaps. Caller may either paint through the returned
        painters, or call the end() method and create a new painter on the
        same device. Order matters, though!
        """
        assert name not in self.names, f'Duplicate name: {name!r}.'
        self.names.add(name)
        self.name = name

        white = QColor('white')
        self.actual_pixmap = QPixmap(width, height)
        self.actual_pixmap.fill(white)
        self.actual = QPainter(self.actual_pixmap)
        self.expected_pixmap = QPixmap(width, height)
        self.expected_pixmap.fill(white)
        self.expected = QPainter(self.expected_pixmap)

        return self.actual, self.expected

    def end(self):
        if self.actual and self.actual.isActive():
            self.actual.end()
        if self.expected and self.expected.isActive():
            self.expected.end()

    def assert_equal(self):
        __tracebackhide__ = True
        self.end()
        self.different_pixels = 0
        actual_image: QImage = self.actual.device().toImage()
        expected_image: QImage = self.expected.device().toImage()
        diff_pixmap = QPixmap(actual_image.width(), actual_image.height())
        diff = QPainter(diff_pixmap)
        try:
            white = QColor('white')
            diff.fillRect(0, 0, actual_image.width(), actual_image.height(), white)
            for x in range(actual_image.width()):
                for y in range(actual_image.height()):
                    actual_colour = actual_image.pixelColor(x, y)
                    expected_colour = expected_image.pixelColor(x, y)
                    diff.setPen(self.diff_colour(actual_colour,
                                                 expected_colour,
                                                 x,
                                                 y))
                    diff.drawPoint(x, y)
        finally:
            diff.end()
        diff_image: QImage = diff.device().toImage()

        display_diff(actual_image,
                     diff_image,
                     expected_image,
                     self.different_pixels)

        if self.different_pixels == 0:
            return
        actual_image.save(str(self.work_dir / (self.name + '_actual.png')))
        expected_image.save(str(self.work_dir / (self.name + '_expected.png')))
        diff_path = self.work_dir / (self.name + '_diff.png')
        is_saved = diff_image.save(str(diff_path))
        diff_width = self.diff_max_x - self.diff_min_x + 1
        diff_height = self.diff_max_y - self.diff_min_y + 1
        diff_section = QImage(diff_width, diff_height, QImage.Format_RGB32)
        diff_section_painter = QPainter(diff_section)
        try:
            diff_section_painter.drawPixmap(0, 0,
                                            diff_width, diff_height,
                                            QPixmap.fromImage(diff_image),
                                            self.diff_min_x, self.diff_min_y,
                                            diff_width, diff_height)
        finally:
            diff_section_painter.end()
        message = f'Found {self.different_pixels} different pixels.'
        assert self.different_pixels == 0, message

    def diff_colour(self,
                    actual_colour: QColor,
                    expected_colour: QColor,
                    x: int,
                    y: int):
        diff_size = (abs(actual_colour.red() - expected_colour.red()) +
                     abs(actual_colour.green() - expected_colour.green()) +
                     abs(actual_colour.blue() - expected_colour.blue()))
        if diff_size <= self.max_diff:
            diff_colour = actual_colour.toRgb()
            diff_colour.setAlpha(diff_colour.alpha() // 3)
            return diff_colour
        if self.different_pixels == 0:
            self.diff_min_x = self.diff_max_x = x
            self.diff_min_y = self.diff_max_y = y
        else:
            self.diff_min_x = min(self.diff_min_x, x)
            self.diff_max_x = max(self.diff_max_x, x)
            self.diff_min_y = min(self.diff_min_y, y)
            self.diff_max_y = max(self.diff_max_y, y)

        self.different_pixels += 1
        # Colour
        dr = 0xff
        dg = (actual_colour.green() + expected_colour.green()) // 5
        db = (actual_colour.blue() + expected_colour.blue()) // 5

        # Opacity
        da = 0xff
        return QColor(dr, dg, db, da)


def encode_image(image: QImage) -> str:
    image_bytes = QByteArray()
    buffer = QBuffer(image_bytes)
    buffer.open(QIODevice.WriteOnly)

    # writes pixmap into bytes in PNG format
    image.save(buffer, "PNG")  # type: ignore
    raw_bytes = bytes(buffer.data())
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
        painter_size = painter.device().size()
        if scene_size != painter_size:
            display_size = find_display_size(display, view, painter_size)
            message = (f"Try resizing display to "
                       f"{display_size.width()}x{display_size.height()}.")
            painter.drawText(QRect(0, 0,
                                   painter_size.width(), painter_size.height()),
                             Qt.AlignCenter | Qt.TextWordWrap,
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
