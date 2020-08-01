from PySide2.QtGui import QPixmap, QPainter, QColor

# noinspection PyUnresolvedReferences
from tests.pixmap_differ import pixmap_differ, encode_image, decode_image

ENCODED_BLUE_GREEN_RECT = 'iVBORw0KGgoAAAANSUhEUgAAAAQAAAACCAIAAADwyuo0AAAACX' \
                          'BIWXMAAA7EAAAOxAGVKw4bAAAAGElEQVQImWNkYPjPwMDA0MDI' \
                          'wMDAxIAEACBIAYQpweBiAAAAAElFTkSuQmCC'


def create_blue_green_rect():
    pixmap = QPixmap(4, 2)
    painter = QPainter(pixmap)
    try:
        painter.fillRect(0, 0, 2, 2, QColor('blue'))
        painter.fillRect(2, 0, 2, 2, QColor('green'))
    finally:
        painter.end()
    return pixmap


def test_encode_image(pixmap_differ):
    pixmap = create_blue_green_rect()

    text = encode_image(pixmap.toImage())

    assert text == ENCODED_BLUE_GREEN_RECT


def test_decode_image(pixmap_differ):
    # To see an image dumped in the Travis CI log, replace
    # ENCODED_BLUE_GREEN_RECT with "TheEncodedText==" from the log.
    text = ENCODED_BLUE_GREEN_RECT
    image = decode_image(text)

    expected_pixmap = create_blue_green_rect()
    width = max(4, image.width())
    height = max(2, image.height())

    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(width, height, 'decode_image') as (
            actual,
            expected):
        actual.drawPixmap(0, 0, QPixmap(image))

        expected.drawPixmap(0, 0, expected_pixmap)
