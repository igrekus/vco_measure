from PyQt5 import uic
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot, QRegularExpression
from attr import attrs, attrib

from domain import Domain, Params
from markermodel import MarkerModel
from measuremodel import MeasureModel
from formlayout.formlayout import fedit
from phaseplotwidget import PhasePlotWidget
from vcocharwidget import VCOCharWidget


@attrs
class Settings:
    offset = attrib(type=float, default=0.0)
    freqOffset = attrib(type=float, default=0.0)
    ampOffset = attrib(type=float, default=0.0)
    curOffset = attrib(type=float, default=0.0)

    @classmethod
    def from_values(cls, data):
        return cls(offset=float(data[0]), freqOffset=float(data[1]) * 1_000_000, ampOffset=float(data[2]), curOffset=float(data[3]) / 1_000)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        # create models
        self._domain = Domain(parent=self)

        self._vcoCharWidget = VCOCharWidget(parent=self)
        self._ui.tabWidgetMain.addTab(self._vcoCharWidget, 'Характеристика ГУН')

        self._measureModel = MeasureModel(parent=self, domain=self._domain)
        self._markerModel = MarkerModel(parent=self)

        self._plotWidget = PhasePlotWidget(parent=self, domain=self._domain)
        self._ui.layoutPlot = QVBoxLayout()
        self._ui.layoutPlot.addWidget(self._ui.widgetStats)
        self._ui.layoutPlot.addWidget(self._plotWidget)
        self._ui.tabPlot.setLayout(self._ui.layoutPlot)

        # UI hack
        self._show_stats = False

        self._init()

    def _init(self):
        self._setupUi()

        self._ui.tableMeasure.setModel(self._measureModel)
        self._ui.tableMarker.setModel(self._markerModel)

        self._modeBeforeConnect()
        self.refreshView()

    def _setupUi(self):
        self._ui.editAnalyzerAddr.setValidator(QRegularExpressionValidator(QRegularExpression(
            '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')))

        self._ui.widgetStats.setVisible(self._show_stats)

        self._setupSignals()
        self._modeBeforeConnect()

    def _setupSignals(self):
        self._domain.measureFinished.connect(self.on_measurementFinished)
        self._markerModel.dataChanged.connect(self.on_markerChanged)

        self._vcoCharWidget.startMeasure.connect(self.on_vcoCharWidget_startMeasure)
        self._vcoCharWidget.exportResult.connect(self.on_vcoCharWidget_exportResult)

    # UI utility methods
    def refreshView(self):
        # TODO debounce resize event
        self.resizeTable()
        self._plotWidget.tightLayout()

    def resizeTable(self):
        self._ui.tableMeasure.resizeRowsToContents()
        self._ui.tableMeasure.resizeColumnsToContents()

        self._ui.tableMarker.resizeRowsToContents()
        self._ui.tableMarker.resizeColumnsToContents()

    def _modeBeforeConnect(self):
        self._vcoCharWidget.ready = False
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnStartMeasure.setEnabled(False)
        self._ui.btnContinue.setEnabled(False)
        self._ui.btnStartMeasure.show()
        self._ui.btnContinue.hide()
        self._ui.spinF1.setEnabled(False)
        self._ui.spinF2.setEnabled(False)
        self._ui.spinV1.setEnabled(False)
        self._ui.spinV2.setEnabled(False)
        self._ui.spinVdut.setEnabled(False)
        self._ui.spinCorr.setEnabled(False)
        self._ui.spinAver.setEnabled(False)
        self._ui.checkV1.setEnabled(False)
        self._ui.checkV2.setEnabled(False)
        self._ui.checkVdut.setEnabled(False)

    def _modeBeforeCheckSample(self):
        self._vcoCharWidget.ready = True
        self._ui.btnCheckSample.setEnabled(True)
        self._ui.btnStartMeasure.setEnabled(False)
        self._ui.btnContinue.setEnabled(False)
        self._ui.btnStartMeasure.show()
        self._ui.btnContinue.hide()
        self._ui.spinF1.setEnabled(True)
        self._ui.spinF2.setEnabled(True)
        self._ui.spinV1.setEnabled(self._ui.checkV1.isChecked())
        self._ui.spinV2.setEnabled(self._ui.checkV2.isChecked())
        self._ui.spinVdut.setEnabled(self._ui.checkVdut.isChecked())
        self._ui.spinCorr.setEnabled(True)
        self._ui.spinAver.setEnabled(True)
        self._ui.checkV1.setEnabled(True)
        self._ui.checkV2.setEnabled(True)
        self._ui.checkVdut.setEnabled(True)

    def _modeBeforeMeasure(self):
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnStartMeasure.setEnabled(True)
        self._ui.btnContinue.setEnabled(False)
        self._ui.btnStartMeasure.show()
        self._ui.btnContinue.hide()
        self._ui.spinF1.setEnabled(True)
        self._ui.spinF2.setEnabled(True)
        self._ui.spinV1.setEnabled(self._ui.checkV1.isChecked())
        self._ui.spinV2.setEnabled(self._ui.checkV2.isChecked())
        self._ui.spinVdut.setEnabled(self._ui.checkVdut.isChecked())
        self._ui.spinCorr.setEnabled(True)
        self._ui.spinAver.setEnabled(True)
        self._ui.checkV1.setEnabled(True)
        self._ui.checkV2.setEnabled(True)
        self._ui.checkVdut.setEnabled(True)

    def _modeMeaurementInProgress(self):
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnStartMeasure.setEnabled(False)
        self._ui.btnContinue.setEnabled(False)
        self._ui.btnStartMeasure.show()
        self._ui.btnContinue.hide()
        self._ui.spinF1.setEnabled(False)
        self._ui.spinF2.setEnabled(False)
        self._ui.spinV1.setEnabled(False)
        self._ui.spinV2.setEnabled(False)
        self._ui.spinVdut.setEnabled(False)
        self._ui.spinCorr.setEnabled(False)
        self._ui.spinAver.setEnabled(False)
        self._ui.checkV1.setEnabled(False)
        self._ui.checkV2.setEnabled(False)
        self._ui.checkVdut.setEnabled(False)

    def _modeBeforeContinue(self):
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnStartMeasure.setEnabled(False)
        self._ui.btnContinue.setEnabled(True)
        self._ui.btnStartMeasure.hide()
        self._ui.btnContinue.show()
        self._ui.spinF1.setEnabled(False)
        self._ui.spinF2.setEnabled(False)
        self._ui.spinV1.setEnabled(False)
        self._ui.spinV2.setEnabled(False)
        self._ui.spinVdut.setEnabled(False)
        self._ui.spinCorr.setEnabled(False)
        self._ui.spinAver.setEnabled(False)
        self._ui.checkV1.setEnabled(False)
        self._ui.checkV2.setEnabled(False)
        self._ui.checkVdut.setEnabled(False)

    def _collectParams(self):
        return Params(
            f1=self._ui.spinF1.value() * 1000,
            f2=self._ui.spinF2.value() * 1000,
            v1=self._ui.spinV1.value(),
            v2=self._ui.spinV2.value(),
            vc=self._ui.spinVdut.value(),
            corr=self._ui.spinCorr.value(),
            aver=self._ui.spinAver.value()
        )

    # ui event handlers
    def resizeEvent(self, event):
        self.refreshView()

    @pyqtSlot()
    def on_btnSearchInstruments_clicked(self):
        if not self._domain.connect():
            self._failWith('Не удалось найти инструменты, проверьте подключение.\nПодробности в логах.')
            print('instruments not found')
            return

        print('found all instruments, enabling sample test')
        self._ui.editAnalyzer.setText(self._domain.analyzerName)
        self._modeBeforeCheckSample()

    @pyqtSlot()
    def on_btnCheckSample_clicked(self):
        if not self._domain.check():
            self._failWith('Не удалось найти образец, проверьте подключение.\nПодробности в логах.')
            print('sample not detected')
            return

        print('sample found, enabling measurement')
        self._modeBeforeMeasure()
        self.refreshView()

    @pyqtSlot()
    def on_btnStartMeasure_clicked(self):
        if not self._domain.check():
            self._failWith('Не удалось найти образец, проверьте подключение.\nПодробности в логах.')
            print('sample not detected')
            return

        self._domain.measure(self._collectParams())
        self._modeMeaurementInProgress()

    @pyqtSlot()
    def on_btnContinue_clicked(self):
        self._modeBeforeCheckSample()

    @pyqtSlot(str)
    def on_editAnalyzerAddr_textChanged(self, text):
        self._domain.analyzerAddress = text

    @pyqtSlot()
    def on_btnAddMarker_clicked(self):
        try:
            self._markerModel.addMarker()

            self.on_measurementFinished()
        except Exception as ex:
            print(ex)

    @pyqtSlot()
    def on_btnDelMarker_clicked(self):
        if not self._ui.tableMarker.selectionModel().hasSelection():
            return

        targetRow = self._ui.tableMarker.selectionModel().selectedIndexes()[0].row()

        try:
            self._markerModel.delMarker(targetRow)

            self.on_measurementFinished()
        except Exception as ex:
            print(ex)

    # action triggers
    @pyqtSlot()
    def on_actSettings_triggered(self):
        data = (
            ('Параметр шума', self._domain._offset),
            ('Параметр частоты', self._domain._freqOffset / 1_000_000),
            ('Параметр мощности', self._domain._ampOffset),
            ('Параметр тока', self._domain._curOffset * 1000),
            ('Показывать частоту', self._show_stats)
        )
        # TODO сменить единицу измерения частоты отстройки
        values = fedit(data=data, title='Настройки')
        if not values:
            return

        self._domain.applySettings(Settings.from_values(values))

        self._show_stats = values[4]
        self._ui.widgetStats.setVisible(self._show_stats)

    # model signals
    def on_markerChanged(self, first, last, roles):
        if not self._domain.xs:
            return

        self.on_measurementFinished()

    def on_vcoCharWidget_startMeasure(self):
        print('vco start measure')

    def on_vcoCharWidget_exportResult(self):
        print('vco export result')

    # measurement event handlers
    @pyqtSlot()
    def on_measurementFinished(self):
        self._measureModel.init()
        self._markerModel.updateModel(self._domain.ampsForMarkers(self._markerModel.markers))

        self._plotWidget._title = ""
        # self._plotWidget._title = f'Частота: {round(self._domain._freq / 1_000_000, 2)} МГц, ' \
        #                          f'мощность: {round(self._domain._amp, 2)} дБц, ' \
        #                          f'ток потребления: {round(self._domain._cur * 1_000, 2)} мА'

        self._plotWidget._stats = self._markerModel.stats

        self._plotWidget.plot()
        self._plotWidget.addMarkers(self._markerModel.markers)

        self.refreshView()
        self._modeBeforeContinue()

    # helpers
    def _failWith(self, message):
        QMessageBox.information(self, 'Ошибка', message)
