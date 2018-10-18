from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavToolbar


class PlotWidget(QVBoxLayout):

    def __init__(self, parent=None, instrumentManager=None):
        QVBoxLayout.__init__(self)

        self.figure = plt.figure(1)
        canvas = FigureCanvas(self.figure)
        toolbar = NavToolbar(canvas, parent=parent)

        self.addWidget(canvas)
        self.addWidget(toolbar)

        self._instrumentManager = instrumentManager

    @pyqtSlot(name='updatePlot')
    def updatePlot(self):
        print('update plot')
        freqs = list()
        amps = list()
        for freq, amp in self._instrumentManager._measure_data:
            freqs.append(freq)
            amps.append(amp)

        self.figure.clear()
        self.figure.gca().plot(freqs, amps)
        self.figure.canvas.draw()



