from PySide6.QtCore import QByteArray, QBuffer, QIODevice, QIODeviceBase
from PySide6.QtGui import QColor, QPixmap, QPainter
from space_tracer import LivePainter, LiveImage


class LiveQPainter(LivePainter):
    WHITE = QColor('white')

    def __init__(self, pixmap: QPixmap, fill: QColor | None = WHITE):
        self.pixmap = pixmap
        self.painter = QPainter(self.pixmap)
        if fill is not None:
            self.pixmap.fill(fill)

    def set_pixel(self, position: LiveImage.Position, fill: LiveImage.Fill):
        self.painter.setPen(QColor(*fill))
        x, y = position
        self.painter.drawPoint(round(x), round(y))

    def get_pixel(self, position: LiveImage.Position) -> LiveImage.Fill:
        x, y = position
        pixmap = self.painter.device()
        assert isinstance(pixmap, QPixmap)
        colour = pixmap.toImage().pixelColor(round(x), round(y))
        return colour.toTuple()  # type: ignore

    def get_size(self) -> LiveImage.Size:
        size = self.pixmap.size()
        return size.toTuple()  # type: ignore

    def convert_to_png(self) -> bytes:
        self.end()
        image_bytes = QByteArray()
        buffer = QBuffer(image_bytes)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        try:
            image = self.pixmap.toImage()
            image.save(buffer, "PNG")  # type: ignore
            return bytes(buffer.data())  # type: ignore
        finally:
            buffer.close()

    def end(self):
        if self.painter.isActive():
            self.painter.end()
