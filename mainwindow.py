from PyQt5 import uic
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot, QRegularExpression, QModelIndex
from attr import attrs, attrib

from domain import Domain, Params
from markermodel import MarkerModel
from measuremodel import MeasureModel
from mytools.plotwidget import PlotWidget
from formlayout.formlayout import fedit
from phaseplotwidget import PhasePlotWidget


@attrs
class Settings:
    offset = attrib(type=float, default=0.0)

    @classmethod
    def from_values(cls, data):
        return cls(offset=data[0])


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        # create models
        self._domain = Domain(parent=self)

        self._measureModel = MeasureModel(parent=self, domain=self._domain)
        self._markerModel = MarkerModel(parent=self)

        self._plotWidget = PhasePlotWidget(parent=self, domain=self._domain)
        self._ui.layoutPlot = QVBoxLayout()
        self._ui.layoutPlot.addWidget(self._ui.widgetStats)
        self._ui.layoutPlot.addWidget(self._plotWidget)
        self._ui.tabPlot.setLayout(self._ui.layoutPlot)

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

        self._setupSignals()
        self._modeBeforeConnect()

    def _setupSignals(self):
        self._domain.measureFinished.connect(self.on_measurementFinished)
        self._markerModel.dataChanged.connect(self.on_markerChanged)

    # UI utility methods
    def refreshView(self):
        self.resizeTable()

    def resizeTable(self):
        self._ui.tableMeasure.resizeRowsToContents()
        self._ui.tableMeasure.resizeColumnsToContents()

        self._ui.tableMarker.resizeRowsToContents()
        self._ui.tableMarker.resizeColumnsToContents()

    def _modeBeforeConnect(self):
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
        data = [
            ('Параметр шума', self._domain._offset),
            ('Параметр частоты', self._domain._freqOffset),
            ('Параметр мощности', self._domain._ampOffset)
        ]
        # TODO сменить единицу измерения частоты отстройки
        values = fedit(data=data, title='Настройки')
        if not values:
            return

        self._domain.applySettings(Settings.from_values(values))

    # model signals
    def on_markerChanged(self, first, last, roles):
        if not self._domain.xs:
            return

        self.on_measurementFinished()

    # measurement event handlers
    @pyqtSlot()
    def on_measurementFinished(self):
        self._measureModel.init()

        self._plotWidget.plot()
        self._plotWidget.addMarkers(self._markerModel.markers)

        self._markerModel.updateModel(self._domain.ampsForMarkers(self._markerModel.markers))

        self._ui.editFreq.setText(self._domain._freq)
        self._ui.editAmp.setText(self._domain._amp)
        self._ui.editCur.setText(self._domain._cur)

        self.refreshView()
        self._modeBeforeContinue()

    # helpers
    def _failWith(self, message):
        QMessageBox.information(self, 'Ошибка', message)
