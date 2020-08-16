import typing
from contextlib import contextmanager
from pathlib import Path
import turtle

from PySide2.QtCore import QByteArray, QBuffer, QIODevice, QTextCodec
from PySide2.QtGui import QPixmap, QPainter, QColor, QImage


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
    display_image(ox + t.xcor(), oy - t.ycor(),
                  image=encode_image(actual_image))
    t.forward(actual_image.height())
    t.forward(text_height)
    t.write(f'Diff ({diff_count} pixels)', font=font)
    display_image(ox + t.xcor(), oy - t.ycor(),
                  image=encode_image(diff_image))
    t.forward(diff_image.height())
    t.forward(text_height)
    t.write('Expected', font=font)
    display_image(ox + t.xcor(), oy - t.ycor(),
                  image=encode_image(expected_image))
    t.forward(expected_image.height())


class PixmapDiffer:
    def __init__(self):
        self.name = None
        self.actual_pixmap = self.expected_pixmap = None
        self.actual = self.expected = None
        self.different_pixels = 0
        self.diff_min_x = self.diff_min_y = None
        self.diff_max_x = self.diff_max_y = None

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
            name: str) -> typing.Iterator[typing.Tuple[QPainter, QPainter]]:
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
        self.actual = QPainter(self.actual_pixmap)
        self.actual.fillRect(0, 0, width, height, white)
        self.expected_pixmap = QPixmap(width, height)
        self.expected = QPainter(self.expected_pixmap)
        self.expected.fillRect(0, 0, width, height, white)

        return self.actual, self.expected

    def end(self):
        if self.actual.isActive():
            self.actual.end()
        if self.expected.isActive():
            self.expected.end()

    def assert_equal(self):
        __tracebackhide__ = True
        self.end()
        self.different_pixels = 0
        actual_image: QImage = self.actual.device().toImage()
        expected_image: QImage = self.expected.device().toImage()
        diff_pixmap = QPixmap(actual_image.width(), actual_image.height())
        diff = QPainter(diff_pixmap)
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
        diff_section_painter.drawPixmap(0, 0,
                                        diff_width, diff_height,
                                        QPixmap.fromImage(diff_image),
                                        self.diff_min_x, self.diff_min_y,
                                        diff_width, diff_height)
        diff_section_painter.end()
        # To see an image dumped in the Travis CI log, copy the text from the
        # log, and paste it in test_pixmap_differ.test_decode_image.
        print(f'Encoded image of differing section '
              f'({self.diff_min_x}, {self.diff_min_y}) - '
              f'({self.diff_max_x}, {self.diff_max_y}):')
        print(encode_image(diff_section))
        message = f'Found {self.different_pixels} different pixels, '
        message += f'see' if is_saved else 'could not write'
        message += f' {diff_path.relative_to(Path(__file__).parent)}.'
        assert self.different_pixels == 0, message

    def diff_colour(self,
                    actual_colour: QColor,
                    expected_colour: QColor,
                    x: int,
                    y: int):
        if actual_colour == expected_colour:
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
    encoded_bytes = image_bytes.toBase64()
    codec = QTextCodec.codecForName(b"UTF-8")
    encoded_string = codec.toUnicode(encoded_bytes)
    return encoded_string


def decode_image(text: str) -> QImage:
    encoded_bytes = QByteArray(text.encode('utf8'))
    image_bytes = QByteArray.fromBase64(encoded_bytes)
    image = QImage.fromData(image_bytes)
    return image
