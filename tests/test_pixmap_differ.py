import turtle
from unittest.mock import Mock

import pytest
from PySide2.QtGui import QPixmap, QPainter, QColor

from zero_play.pixmap_differ import encode_image, decode_image

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


def test_diff_found(pixmap_differ, monkeypatch):
    mock_turtle = Mock('MockTurtle')
    mock_turtle.display_image = Mock('MockTurtle.display_image')
    mock_turtle.return_value.screen.cv.cget.return_value = 100
    mock_turtle.return_value.xcor.return_value = 0
    mock_turtle.return_value.ycor.return_value = 0
    monkeypatch.setattr(turtle, 'Turtle', mock_turtle)
    expected_pixmap = create_blue_green_rect()

    with pytest.raises(AssertionError, match='Found 8 different pixels'):
        actual: QPainter
        expected: QPainter
        with pixmap_differ.create_painters(4, 2, 'diff_found') as (actual,
                                                                   expected):
            expected.drawPixmap(0, 0, expected_pixmap)

            # Do nothing to actual, so error should be raised.

    # actual, diff, and expected
    assert len(mock_turtle.display_image.call_args_list) == 3


def test_encode_image(pixmap_differ):
    expected_pixmap = create_blue_green_rect()

    text = encode_image(expected_pixmap.toImage())
    actual: QPainter
    expected: QPainter
    with pixmap_differ.create_painters(4, 2, 'encode_image') as (
            actual,
            expected):
        image = decode_image(text)
        actual.drawPixmap(0, 0, QPixmap(image))

        expected.drawPixmap(0, 0, expected_pixmap)


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
