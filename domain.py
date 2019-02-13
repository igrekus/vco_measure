from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal
from attr import attrs, attrib
from scipy.signal import savgol_filter

from instrumentcontroller import InstrumentController


@attrs
class Params:
    f1 = attrib(type=float, default=0.0)
    f2 = attrib(type=float, default=100.0)
    v1 = attrib(type=float, default=4.70)
    v2 = attrib(type=float, default=0.0)
    vc = attrib(type=float, default=0.0)
    corr = attrib(type=int, default=20)
    aver = attrib(type=int, default=0)


class Task(QRunnable):

    def __init__(self, fn, end, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.end = end
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.fn(*self.args, **self.kwargs)
        self.end()


class Domain(QObject):

    measureFinished = pyqtSignal()

    headers = ['F, Гц', 'Шум, dBc/Hz']

    def __init__(self, parent=None):
        super().__init__(parent)

        self._instruments = InstrumentController()
        self._threadPool = QThreadPool()

        self._offset = 0.0
        self._freqOffset = 0.0
        self._ampOffset = 0.0
        self._curOffset = 0.0

        self._freqs = list()
        self._amps = list()

        self._freq = 0.0
        self._amp = 0.0
        self._cur = 0.0

    def _clear(self):
        self._freqs.clear()
        self._amps.clear()

    def applySettings(self, settings):
        self._offset = settings.offset
        self._freqOffset = settings.freqOffset
        self._ampOffset = settings.ampOffset
        self._curOffset = settings.curOffset

    def connect(self):
        print('find instruments')
        return self._instruments.find()

    def check(self):
        print('check sample presence')
        return self._instruments.test_sample()

    def measure(self, params: Params):
        print(f'run measurement with {params}')
        self._clear()
        self._threadPool.start(Task(self._measureFunc, self._processingFunc, params))

    def _measureFunc(self, params: Params):
        print(f'start measurement task')
        self._freqs, self._amps, self._freq, self._amp, self._cur = self._instruments.measure(params)
        print('end measurement task')

    def _processingFunc(self):
        print('processing stats')
        self._amps = list(map(lambda x: x + self._offset, self._amps))

        self._amp = float(self._amp) + self._ampOffset
        self._freq = float(self._freq) + self._freqOffset
        self._cur = float(self._cur) + self._curOffset

        self.measureFinished.emit()

    def rows(self):
        return len(self._amps)

    def cols(self):
        return 2

    def data(self, row, col):
        if col == 1:
            return self._freqs[row]
        elif col == 2:
            return self._amps[row]

    def ampsForMarkers(self, markers):
        return [self._amps[self._freqs.index(min(self._freqs, key=lambda x: abs(freq - x)))] for freq in markers]

    @property
    def analyzerAddress(self):
        return self._instruments.analyzer_address

    @analyzerAddress.setter
    def analyzerAddress(self, addr):
        self._instruments.analyzer_address = addr

    @property
    def analyzerName(self):
        return str(self._instruments._analyzer)

    @property
    def xs(self):
        return self._freqs

    @property
    def ys(self):
        return self._amps

    @property
    def smoothYs(self):
        return savgol_filter(self._amps, 31, 3)

