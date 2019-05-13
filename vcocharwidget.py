from PyQt5 import uic
from PyQt5.QtChart import QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QPointF, Qt
from PyQt5.QtGui import QPainter, QFont
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
        self._axis_x = QValueAxis()
        self._axis_y = QValueAxis()

        self.series = QLineSeries(self)

        self._chart.addSeries(self.series)
        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)

        self.series.attachAxis(self._axis_x)
        self.series.attachAxis(self._axis_y)

        self._axis_x.setTickCount(5)
        self._axis_x.setRange(0, 10)

        self._axis_y.setTickCount(5)
        self._axis_y.setRange(0, 10)

        self._chart.legend().hide()

    def plot(self, xs, ys):
        self.series.replace([QPointF(x, y) for x, y in zip(xs, ys)])

    @property
    def axes_titles(self):
        return self._axis_x.titleText(), self._axis_y.titleText()

    @axes_titles.setter
    def axes_titles(self, value):
        x, y = value
        self._axis_x.setTitleText(x)
        self._axis_y.setTitleText(y)

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

    startMeasure = pyqtSignal()
    exportResult = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._ui = uic.loadUi('vcocharwidget.ui', self)

        self._params = VCOCharParams()

        self._plotFreq = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotFreq, 0, 0)
        self._plotFreq.axes_titles = 'Упр. нарпяжение, В', 'Частота, МГц'

        self._plotKvco = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotKvco, 0, 1)
        self._plotKvco.axes_titles = 'Упр. нарпяжение, В', 'Kvco, МГц/В'

        self._plotSupply1Current = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotSupply1Current, 1, 0)
        self._plotSupply1Current.axes_titles = 'Упр. нарпяжение, В', 'Ток источника, мА'

        self._plotPower = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotPower, 1, 1)
        self._plotPower.axes_titles = 'Упр. нарпяжение, В', 'Мощность, дБм'

        self._plotPushing = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotPushing, 2, 0)
        self._plotPushing.axes_titles = 'Упр. нарпяжение, В', 'Pushing, МГц/В'

        self._plotPhaseNoise = CharPlotWidget(self)
        self._ui.plotGrid.addWidget(self._plotPhaseNoise, 2, 1)
        self._plotPhaseNoise.axes_titles = 'Упр. нарпяжение, В', 'Фазовый шум при частоте, дБц/Гц'
        self._plotPhaseNoise.legend.show()

        self._ready = False

    def plotResult(self, result):
        self._plotFreq.plot(xs=result.tune_voltage, ys=result.frequency)
        self._plotKvco.plot(xs=result.tune_voltage, ys=result.kvco)
        self._plotSupply1Current.plot(xs=result.tune_voltage, ys=result.supply_current)
        self._plotPower.plot(xs=result.tune_voltage, ys=result.power)
        self._plotPushing.plot(xs=result.tune_voltage, ys=result.pushing)
        self._plotPhaseNoise.plot(xs=result.tune_voltage, ys=result.noise)

    # event handlers
    @pyqtSlot()
    def on_btnMeasure_clicked(self):
        self.startMeasure.emit()

    @pyqtSlot()
    def on_btnExport_clicked(self):
        self.exportResult.emit()

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

    @property
    def params(self):
        return self._params
