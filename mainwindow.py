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

        self._plotWidget = PlotWidget(parent=self, toolbar=True)
        self._ui.layoutPlot = QVBoxLayout()
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
        self._ui.spinDF.setEnabled(False)
        self._ui.spinV1.setEnabled(False)
        self._ui.spinV2.setEnabled(False)
        self._ui.spinVdut.setEnabled(False)
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
        self._ui.spinDF.setEnabled(True)
        self._ui.spinV1.setEnabled(self._ui.checkV1.isChecked())
        self._ui.spinV2.setEnabled(self._ui.checkV2.isChecked())
        self._ui.spinVdut.setEnabled(self._ui.checkVdut.isChecked())
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
        self._ui.spinDF.setEnabled(True)
        self._ui.spinV1.setEnabled(self._ui.checkV1.isChecked())
        self._ui.spinV2.setEnabled(self._ui.checkV2.isChecked())
        self._ui.spinVdut.setEnabled(self._ui.checkVdut.isChecked())
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
        self._ui.spinDF.setEnabled(False)
        self._ui.spinV1.setEnabled(False)
        self._ui.spinV2.setEnabled(False)
        self._ui.spinVdut.setEnabled(False)
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
        self._ui.spinDF.setEnabled(False)
        self._ui.spinV1.setEnabled(False)
        self._ui.spinV2.setEnabled(False)
        self._ui.spinVdut.setEnabled(False)
        self._ui.checkV1.setEnabled(False)
        self._ui.checkV2.setEnabled(False)
        self._ui.checkVdut.setEnabled(False)

    def _collectParams(self):
        return Params(
            f1=self._ui.spinF1.value(),
            f2=self._ui.spinF2.value(),
            df=self._ui.spinDF.value(),
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
        print('del')

    # action triggers
    @pyqtSlot()
    def on_actSettings_triggered(self):
        data = [
            ('Оффсет', self._domain._offset)
        ]
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

        def setup_plot(plot):
            plot.subplots_adjust(bottom=0.150)
            plot.set_title('Фазовый шум')
            plot.set_xlabel('Частота, Гц')
            plot.set_xscale('log')
            plot.set_ylabel('дБц/Гц')
            # plot.set_xlim(pars['xlim'][0], pars['xlim'][1])
            # plot.set_ylim(pars['ylim'][0], pars['ylim'][1])
            plot.grid(b=True, which='major', color='0.5', linestyle='--')

        def add_markers(plot):
            for marker in self._markerModel.markers:
                plot.axvline(marker, 0, 1, linewidth=0.8, color='0.3', linestyle='-')

        self._measureModel.init()
        self._plotWidget.clear()
        setup_plot(self._plotWidget)
        self._plotWidget.plot(self._domain.xs, self._domain.ys)
        add_markers(self._plotWidget)

        self._markerModel.updateModel(self._domain.ampsForMarkers(self._markerModel.markers))

        self.refreshView()

        self._modeBeforeContinue()

    # helpers
    def _failWith(self, message):
        QMessageBox.information(self, 'Ошибка', message)
