from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent, QFontMetrics, Qt
from PySide6.QtWidgets import QRadioButton


class ScaledRadioButton(QRadioButton):
    def resizeEvent(self, event: QResizeEvent):
        target_rect = self.contentsRect()
        text = self.text()
        icon = self.icon()
        icon_spacing = 4  # Constant?

        # Use binary search to efficiently find the biggest font that will fit.
        min_fail = self.height()  # Smallest known to fail.
        max_size = min_fail  # Largest left in search space.
        min_size = 1  # Smallest left in search space.
        max_pass = min_size  # Largest known to pass.
        font = self.font()
        while max_pass+1 < min_fail:
            new_size = (min_size + max_size) // 2
            indicator_width = new_size
            indicator_spacing = new_size // 2
            font.setPointSize(new_size)
            metrics = QFontMetrics(font)

            # Be careful which overload of boundingRect() you call.
            rect = metrics.boundingRect(target_rect, Qt.AlignLeft, text)
            full_width = indicator_width + indicator_spacing + rect.width()
            height = rect.height()
            if icon:
                icon_size = new_size * 3 // 2
                full_width += icon_size
                if text:
                    full_width += icon_spacing
                height = max(height, icon_size)

            if (target_rect.width() < full_width or
                    target_rect.height() < height):
                min_fail = new_size
                max_size = new_size - 1
            elif (full_width == target_rect.width() or
                  height == target_rect.height()):
                max_pass = min_size = max_size = new_size
                min_fail = new_size+1
            else:
                max_pass = new_size
                min_size = new_size+1

        indicator_width = max_pass
        indicator_spacing = max_pass // 2
        if icon:
            icon_size = max_pass*3//2
            self.setIconSize(QSize(icon_size, icon_size))
        font.setPointSize(max_pass)
        self.setFont(font)
        self.setStyleSheet(f'QRadioButton::indicator {{width: {indicator_width}}} '
                           f'QRadioButton {{spacing: {indicator_spacing}}}')
