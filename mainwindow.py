from time import sleep

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QAction
from PyQt5.QtCore import Qt, QStateMachine, QState, pyqtSignal

from instrumentmanager import InstrumentManager
from measuremodel import MeasureModel
from plotwidget import PlotWidget


class MainWindow(QMainWindow):

    instrumentsFound = pyqtSignal()
    sampleFound = pyqtSignal()
    measurementFinished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        # create models
        self._instrumentManager = InstrumentManager()
        self._mdeasureModel = MeasureModel(parent=self, instrumentManager=self._instrumentManager)
        self._plotWidget = PlotWidget(parent=self, instrumentManager=self._instrumentManager)
        self._ui.tabPlot.setLayout(self._plotWidget)

        self.initDialog()

    def setupUiSignals(self):
        self._ui.btnSearchInstruments.clicked.connect(self.onBtnSearchInstrumentsClicked)
        self._ui.btnCheckSample.clicked.connect(self.onBtnCheckSample)
        self._ui.btnMeasureStart.clicked.connect(self.onBtnMeasureStart)
        self._ui.btnMeasureStop.clicked.connect(self.onBtnMeasureStop)

        self.measurementFinished.connect(self._mdeasureModel.updateModel)
        self.measurementFinished.connect(self._plotWidget.updatePlot)

    def initDialog(self):
        self.setupUiSignals()

        self._ui.tableMeasure.setModel(self._mdeasureModel)

        self.modeSearchInstruments()

        self.refreshView()

    # UI utility methods
    def refreshView(self):
        self.resizeTable()

    def resizeTable(self):
        self._ui.tableMeasure.resizeRowsToContents()
        self._ui.tableMeasure.resizeColumnsToContents()

    def modeSearchInstruments(self):
        self._ui.btnMeasureStop.hide()
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnMeasureStart.setEnabled(False)

    def modeCheckSample(self):
        self._ui.btnCheckSample.setEnabled(True)
        self._ui.btnMeasureStart.show()
        self._ui.btnMeasureStart.setEnabled(False)
        self._ui.btnMeasureStop.hide()
        self._ui.editAnalyzer.setText(self._instrumentManager.getInstrumentNames())

    def modeReadyToMeasure(self):
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnMeasureStart.setEnabled(True)

    def modeMeasureInProgress(self):
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnMeasureStart.setVisible(False)
        self._ui.btnMeasureStop.setVisible(True)

    def modeMeasureFinished(self):
        self._ui.btnCheckSample.setEnabled(False)
        self._ui.btnMeasureStart.setVisible(False)
        self._ui.btnMeasureStop.setVisible(True)

    def collectParams(self):
        power = self._ui.spinPowerVolt.value()
        control = self._ui.spinControlVolt.value()
        f1 = self._ui.spinF1.value()
        f2 = self._ui.spinF2.value()
        df = self._ui.spinDF.value()
        return power, control, f1, f2, df

    # instrument control methods
    def search(self):
        if not self._instrumentManager.findInstruments():
            QMessageBox.information(self, "Ошибка",
                                    "Не удалось найти инструменты, проверьте подключение.\nПодробности в логах.")
            return False

        print('found all instruments, enabling sample test')
        return True

    # event handlers
    def resizeEvent(self, event):
        self.refreshView()

    # TODO: extract to a measurement manager class
    def onBtnSearchInstrumentsClicked(self):
        self.modeSearchInstruments()
        if not self.search():
            return
        self.modeCheckSample()
        self.instrumentsFound.emit()

    def failWith(self, message):
        QMessageBox.information(self, "Ошибка", message)

    def onBtnCheckSample(self):
        if not self._instrumentManager.checkSample():
            self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
            print('sample not detected')
            return

        self.modeReadyToMeasure()
        self.sampleFound.emit()
        self.refreshView()

    def onBtnMeasureStart(self):
        print('start measurement task')

        if not self._instrumentManager.checkSample():
            self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
            print('sample not detected')
            return

        self.modeMeasureInProgress()
        self._instrumentManager.measure(self.collectParams())
        self.measurementFinished.emit()
        self.modeMeasureFinished()
        self.refreshView()

    def onBtnMeasureStop(self):
        # TODO implement
        print('abort measurement task')
        self.modeCheckSample()


