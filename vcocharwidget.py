from PyQt5 import uic
from PyQt5.QtChart import QChartView, QLineSeries
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from attr import attrs, attrib


@attrs
class VCOCharParams:
    v_sup1_on = attrib(default=True)
    v_sup1 = attrib(default=4.7)
    v_sup2_on = attrib(default=False)
    v_sup2 = attrib(default=0.0)
    v_dut_start = attrib(default=0.0)
    v_dut_end = attrib(default=3.0)
    v_dut_step = attrib(default=1.0)
    f_offset1 = attrib(default=10_000.0)
    f_offset2 = attrib(default=100_000.0)
    f_offset3 = attrib(default=1000_000.0)
    f_offset4 = attrib(default=0.0)


class CharPlotWidget(QChartView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setRenderHint(QPainter.Antialiasing)

        self._chart = self.chart()

        self.series = QLineSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(9, 5)

        self._chart.addSeries(self.series)
        self._chart.legend().hide()
        self._chart.createDefaultAxes()

    @property
    def title(self):
        return self._chart.title()

    @title.setter
    def title(self, value):
        self._chart.setTitle(value)

    @property
    def legend(self):
        return self._chart.legend()


class VCOCharWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._ui = uic.loadUi('vcocharwidget.ui', self)

        self._params = VCOCharParams()

        self._plotFreq = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotFreq, 0, 0)
        self._plotFreq.title = 'FV char'

        self._plotKvco = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotKvco, 0, 1)
        self._plotKvco.title = 'Kv'

        self._plotSupply1Current = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotSupply1Current, 1, 0)
        self._plotSupply1Current.title = 'Supply current'

        self._plotPower = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotPower, 1, 1)
        self._plotPower.title = 'Power'

        self._plotPushing = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotPushing, 2, 0)
        self._plotPushing.title = 'Pushing'

        self._plotPhaseNoise = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotPhaseNoise, 2, 1)
        self._plotPhaseNoise.title = 'SSB phase noise at offset'
        self._plotPhaseNoise.legend.show()

        self._ready = False

    # event handlers
    @pyqtSlot()
    def on_btnMeasure_clicked(self):
        print('measure')

    @pyqtSlot()
    def on_btnExport_clicked(self):
        print('export')

    @pyqtSlot(bool)
    def on_checkV1_toggled(self, value):
        self._params.v_sup1_on = value

    @pyqtSlot(bool)
    def on_checkV2_toggled(self, value):
        self._params.v_sup2_on = value

    @pyqtSlot(float)
    def on_spinV1_valueChanged(self, value):
        self._params.v_sup1 = value

    @pyqtSlot(float)
    def on_spinV2_valueChanged(self, value):
        self._params.v_sup2 = value

    @pyqtSlot(float)
    def on_spinDutVstart_valueChanged(self, value):
        self._params.v_dut_start = value

    @pyqtSlot(float)
    def on_spinDutVend_valueChanged(self, value):
        self._params.v_dut_end = value

    @pyqtSlot(float)
    def on_spinDutVstep_valueChanged(self, value):
        self._params.v_dut_step = value

    @pyqtSlot(float)
    def on_spinOffsetF1_valueChanged(self, value):
        self._params.f_offset1 = value * 1_000

    @pyqtSlot(float)
    def on_spinOffsetF2_valueChanged(self, value):
        self._params.f_offset2 = value * 1_000

    @pyqtSlot(float)
    def on_spinOffsetF3_valueChanged(self, value):
        self._params.f_offset3 = value * 1_000

    @pyqtSlot(float)
    def on_spinOffsetF4_valueChanged(self, value):
        self._params.f_offset4 = value * 1_000

    # props
    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, value):
        self._ui.btnMeasure.setEnabled(value)
        self._ready = value
