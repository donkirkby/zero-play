import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6 import QtWidgets

plt.switch_backend('QtAgg')


class PlotCanvas(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.axes: Axes = fig.add_subplot(111)
        layout_canvas = QtWidgets.QVBoxLayout(self)
        layout_canvas.addWidget(self.canvas)
