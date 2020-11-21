import turtle
from contextlib import contextmanager
from pathlib import Path

import typing
from PySide2.QtGui import QPixmap, QColor, QPainter, QImage, QPen, Qt
from PySide2.QtWidgets import QApplication

from zero_play.connect4.display import Connect4Display
from zero_play.connect4.game import Connect4State
from zero_play.game_display import GameDisplay
from zero_play.pixmap_differ import render_display, encode_image
from zero_play.tictactoe.display import TicTacToeDisplay
from zero_play.tictactoe.state import TicTacToeState


class DiagramWriter:
    app = QApplication()

    def __init__(self, display: GameDisplay, width=200, height=200):
        self.display = display
        self.width = width
        self.height = height

    def draw(self, painter: QPainter):
        render_display(self.display, painter)
        pen = QPen()
        pen.setWidth(self.width // 50)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

    @contextmanager
    def create_painter(self) -> typing.Iterator[QPainter]:
        white = QColor('white')
        pixmap = QPixmap(self.width, self.height)
        pixmap.fill(white)
        painter = QPainter(pixmap)
        try:
            yield painter
        finally:
            painter.end()

    def demo(self):
        display_image = getattr(turtle.Turtle, 'display_image', None)
        if display_image is None:
            return
        with self.create_painter() as painter:
            self.draw(painter)
            actual_image: QImage = painter.device().toImage()
            display_image(0, 0, image=encode_image(actual_image))

    def write(self, path: Path):
        print('Writing to', path)
        with self.create_painter() as painter:
            self.draw(painter)
            image: QImage = painter.device().toImage()
            image.save(str(path))


class TictactoeDiagram(DiagramWriter):
    def __init__(self):
        display = TicTacToeDisplay()
        display.update_board(TicTacToeState('''\
OX.
XO.
X.O
'''))
        display.resize(276, 224)
        super().__init__(display, 200, 200)

    def draw(self, painter: QPainter):
        super().draw(painter)
        w = self.width
        h = self.height
        painter.drawLine(w//6, h//6, w*5//6, h*5//6)


class Connect4Diagram(DiagramWriter):
    def __init__(self):
        display = Connect4Display()
        display.resize(288, 204)
        display.update_board(Connect4State('''\
.......
......X
.....XO
..XOXOX
..OXOXO
..OXXXO
'''))
        super().__init__(display, 210, 180)

    def draw(self, painter: QPainter):
        super().draw(painter)
        pen = painter.pen()
        pen.setColor(QColor('darkgrey'))
        painter.setPen(pen)
        w = self.width
        h = self.height
        painter.drawLine(w//2, h*3//4, w*13//14, h*3//12)


def main():
    rules_path = Path(__file__).parent.parent / "docs" / "rules"
    TictactoeDiagram().write(rules_path / "tictactoe.png")
    Connect4Diagram().write(rules_path / "connect4.png")


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    TictactoeDiagram().demo()
