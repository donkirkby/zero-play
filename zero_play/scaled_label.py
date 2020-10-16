from PySide2.QtCore import QMargins
from PySide2.QtGui import QResizeEvent, QFontMetrics, Qt
from PySide2.QtWidgets import QLabel


class ScaledLabel(QLabel):
    def resizeEvent(self, event: QResizeEvent):
        # This flag is used for pixmaps, but I thought it might be useful to
        # be able to disable font scaling.
        if not self.hasScaledContents():
            return
        self.update_margins()

        target_rect = self.contentsRect()
        text = self.text()

        # Use binary search to efficiently find the biggest font that will fit.
        max_size = self.height()
        min_size = 1
        font = self.font()
        while min_size < max_size:
            new_size = (min_size + max_size) // 2
            font.setPointSize(new_size)
            metrics = QFontMetrics(font)

            # Be careful which overload of boundingRect() you call.
            rect = metrics.boundingRect(target_rect, Qt.AlignLeft, text)
            if (target_rect.width() < rect.width() or
                    target_rect.height() < rect.height()):
                max_size = new_size - 1
            elif (rect.width() == target_rect.width() or
                  rect.height() == target_rect.height()):
                min_size = max_size = new_size
            else:
                min_size = new_size + 1

        font.setPointSize(min_size)
        self.setFont(font)

    def update_margins(self):
        pixmap = self.pixmap()
        if pixmap is None:
            return
        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()
        target_rect = self.contentsRect()
        margins = self.contentsMargins()
        target_width = target_rect.width() + margins.left() + margins.right()
        target_height = target_rect.height() + margins.top() + margins.bottom()
        if pixmap_width == 0 or pixmap_height == 0:
            new_margins = QMargins()
        elif target_width * pixmap_height < target_height * pixmap_width:
            m = target_height - pixmap_height * target_width // pixmap_width
            # noinspection PyUnresolvedReferences
            vertical_alignment = self.alignment() & Qt.AlignVertical_Mask
            if vertical_alignment == Qt.AlignTop:
                new_margins = QMargins(0, 0, 0, m)
            elif vertical_alignment == Qt.AlignBottom:
                new_margins = QMargins(0, m, 0, 0)
            else:
                assert vertical_alignment == Qt.AlignVCenter, vertical_alignment
                new_margins = QMargins(0, m//2, 0, m//2)
        else:
            m = target_width - pixmap_width * target_height // pixmap_height
            # noinspection PyUnresolvedReferences
            horizontal_alignment = self.alignment() & Qt.AlignHorizontal_Mask
            if horizontal_alignment == Qt.AlignLeft:
                new_margins = QMargins(0, 0, m, 0)
            elif horizontal_alignment == Qt.AlignRight:
                new_margins = QMargins(m, 0, 0, 0)
            else:
                assert horizontal_alignment == Qt.AlignHCenter, horizontal_alignment
                new_margins = QMargins(m//2, 0, m//2, 0)
        if new_margins != margins:
            self.setContentsMargins(new_margins)
