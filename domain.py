from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal
from attr import attrs, attrib

from instrumentcontroller import InstrumentController


@attrs
class Params:
    f1 = attrib(type=float, default=0.0)
    f2 = attrib(type=float, default=100.0)
    df = attrib(type=float, default=10.0)
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

        self._freqs = list()
        self._amps = list()

    def _clear(self):
        self._freqs.clear()
        self._amps.clear()

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
        self._freqs, self._amps = self._instruments.measure(params)
        print('end measurement task')

    def _processingFunc(self):
        print('processing stats')
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


