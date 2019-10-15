import ast
import os

from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal
from attr import attrs, attrib
from scipy.signal import savgol_filter

from instrumentcontroller import InstrumentController
from vcocharmeasurement import VCOCharMeasurement


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
    vcoCharMeasurementFinished = pyqtSignal()

    headers = ['F, Hz', 'Noise, dBc/Hz']

    def __init__(self, parent=None):
        super().__init__(parent)

        self._instruments = InstrumentController()
        self._threadPool = QThreadPool()

        self._vcoCharMeasurement = VCOCharMeasurement()

        self._offset = 0.0
        self._offsetF1 = 0.0
        self._offsetF2 = 0.0
        self._offsetF3 = 0.0
        self._offsetF4 = 0.0
        self._offsetF5 = 0.0
        self._freqOffset = 0.0
        self._ampOffset = 0.0
        self._curOffset = 0.0
        self._markerOffset = [0.0] * 5

        self._freqs = list()
        self._raw_amps = list()
        self._amps = list()
        self._smoothAmps = list()

        self._freq = 0.0
        self._amp = 0.0
        self._cur = 0.0

        self._loadParams()

    def _clear(self):
        self._freqs.clear()
        self._amps.clear()

    def _loadParams(self):
        param_file = 'param.ini'
        if not os.path.isfile(param_file):
            return
        with open(param_file) as f:
            for line in f.readlines():
                label, value = line.strip().split('=')
                if label == 'off1':
                    self._offsetF1 = float(value)
                elif label == 'off2':
                    self._offsetF2 = float(value)
                elif label == 'off3':
                    self._offsetF3 = float(value)
                elif label == 'off4':
                    self._offsetF4 = float(value)
                elif label == 'off5':
                    self._offsetF5 = float(value)
                elif label == 'freq':
                    self._freqOffset = float(value)
                elif label == 'amp':
                    self._ampOffset = float(value)
                elif label == 'cur':
                    self._curOffset = float(value)
                elif label == 'mark':
                    self._markerOffset = ast.literal_eval(value)

    def applySettings(self, settings):
        self._markerOffset.clear()
        self._offsetF1 = settings.offsetF1
        self._offsetF2 = settings.offsetF2
        self._offsetF3 = settings.offsetF3
        self._offsetF4 = settings.offsetF4
        self._offsetF5 = settings.offsetF5
        self._freqOffset = settings.freqOffset
        self._ampOffset = settings.ampOffset
        self._curOffset = settings.curOffset
        self._markerOffset = settings.markerOffset
        with open('param.ini', mode='wt', encoding='utf-8') as f:
            f.writelines([
                f'off1={self._offsetF1}\n',
                f'off2={self._offsetF2}\n',
                f'off3={self._offsetF3}\n',
                f'off4={self._offsetF4}\n',
                f'off5={self._offsetF5}\n',
                f'freq={self._freqOffset}\n',
                f'amp={self._ampOffset}\n',
                f'cur={self._curOffset}\n',
                f'mark={self._markerOffset}\n',
            ])

    def connect(self):
        print('find instruments')
        return self._instruments.find()

    def check(self):
        print('check sample presence')
        return self._instruments.test_sample()

    def ref_measure_vco_char(self, params):
        self._vcoCharMeasurement.measure_action = self._instruments.ref_measure_vco_char
        self._vcoCharMeasurement.params = params

        self._vcoCharMeasurement.measure()
        self._vcoCharMeasurement.process()

        self.vcoCharMeasurementFinished.emit()

    def measure(self, params: Params):
        print(f'run measurement with {params}')
        self._clear()
        self._threadPool.start(Task(self._measureFunc, self._processingFunc, params))

    def _measureFunc(self, params: Params):
        print(f'start measurement task')
        self._freqs, self._raw_amps, self._freq, self._amp, self._cur = self._instruments.measure(params)
        print('end measurement task')

    def _processingFunc(self):
        print('processing stats')
        self._amps = list(map(lambda x: x + self._offset, self._raw_amps))
        self._smoothAmps = savgol_filter(self._amps, 31, 3)

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
        if not self._freqs:
            return []
        amps = [self._smoothAmps[self._freqs.index(min(self._freqs, key=lambda x: abs(freq - x)))] for freq in markers]
        amps = [amp + offset for amp, offset in zip(amps, self._markerOffset)]
        return amps

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
        return self._smoothAmps

    @property
    def freq(self):
        return float(self._freq) + self._freqOffset

    @property
    def amp(self):
        return float(self._amp) + self._ampOffset

    @property
    def cur(self):
        return float(self._cur) + self._curOffset

