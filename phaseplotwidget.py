from PyQt5.QtWidgets import QWidget, QVBoxLayout
from mytools.plotwidget import PlotWidget


class PhasePlotWidget(QWidget):

    def __init__(self, parent=None, domain=None):
        super().__init__(parent)

        self._domain = domain

        self._plot = PlotWidget(parent=None, toolbar=True)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._plot)

        self.setLayout(self._layout)

        self._init()

    def _init(self):
        self._plot.set_title('Фазовый шум')
        self._plot.set_xlabel('Частота, Гц')
        self._plot.set_ylabel('дБн/Гц')
        self._plot.set_xscale('log')
        # self._plot.set_xlim(pars['xlim'][0], pars['xlim'][1])
        # self._plot.set_ylim(pars['ylim'][0], pars['ylim'][1])
        self._plot.grid(b=True, which='major', color='0.5', linestyle='--')

    def clear(self):
        self._plot.clear()

    def plot(self):
        self._plot.clear()
        self._init()
        self._plot.plot(self._domain.xs, self._domain.ys)

    def addMarkers(self, markers):
        for marker in markers:
            self._plot.axvline(marker, 0, 1, linewidth=0.8, color='0.3', linestyle='-')

    # def save(self, img_path='./image'):
    #     try:
    #         os.makedirs(img_path)
    #     except OSError as ex:
    #         if ex.errno != errno.EEXIST:
    #             raise IOError('Error creating image dir.')
    #
    #     for plot, name in zip([self._plot11, self._plot12, self._plot21, self._plot22], ['stats.png', 'cutoff.png', 'delta.png', 'double-triple.png']):
    #         plot.savefig(img_path + name, dpi=400)


