import typing

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget, QSizePolicy


class ProcessDisplay(QWidget):
    default_font = 'Sans Serif,9,-1,5,50,0,0,0,0,0'

    def __init__(self) -> None:
        super().__init__()
        self.worker_thread: typing.Optional[QThread] = None
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

    def close(self):
        self.stop_workers()

    def stop_workers(self):
        if self.worker_thread is not None:
            try:
                self.worker_thread.quit()
            except RuntimeError:
                # already quit.
                pass
