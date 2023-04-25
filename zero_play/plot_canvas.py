import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6 import QtWidgets

plt.switch_backend('QtAgg')


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None) -> None:
        fig = Figure()
        self.axes: Axes = fig.add_subplot(111)

        super().__init__(fig)
        self.setParent(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.updateGeometry()
