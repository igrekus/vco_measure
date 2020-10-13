from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog

from domain import Settings


class OffsetDialog(QDialog):

    def __init__(self, parent=None, settings=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self._ui = uic.loadUi('offsetdialog.ui', self)

        self._ui.spinF1.setValue(settings.offsetF1)
        self._ui.spinF2.setValue(settings.offsetF2)
        self._ui.spinF3.setValue(settings.offsetF3)
        self._ui.spinF4.setValue(settings.offsetF4)
        self._ui.spinF5.setValue(settings.offsetF5)

        self._ui.spinFreq.setValue(settings.freqOffset)
        self._ui.spinAmp.setValue(settings.ampOffset)
        self._ui.spinCurr.setValue(settings.curOffset)

        self._ui.spinM1_1.setValue(settings.markerOffset[0][0])
        self._ui.spinM2_1.setValue(settings.markerOffset[1][0])
        self._ui.spinM3_1.setValue(settings.markerOffset[2][0])
        self._ui.spinM4_1.setValue(settings.markerOffset[3][0])
        self._ui.spinM5_1.setValue(settings.markerOffset[4][0])

        self._ui.spinM1_2.setValue(settings.markerOffset[0][1])
        self._ui.spinM2_2.setValue(settings.markerOffset[1][1])
        self._ui.spinM3_2.setValue(settings.markerOffset[2][1])
        self._ui.spinM4_2.setValue(settings.markerOffset[3][1])
        self._ui.spinM5_2.setValue(settings.markerOffset[4][1])

        self._ui.spinM1_3.setValue(settings.markerOffset[0][2])
        self._ui.spinM2_3.setValue(settings.markerOffset[1][2])
        self._ui.spinM3_3.setValue(settings.markerOffset[2][2])
        self._ui.spinM4_3.setValue(settings.markerOffset[3][2])
        self._ui.spinM5_3.setValue(settings.markerOffset[4][2])

        self._ui.spinM1_4.setValue(settings.markerOffset[0][3])
        self._ui.spinM2_4.setValue(settings.markerOffset[1][3])
        self._ui.spinM3_4.setValue(settings.markerOffset[2][3])
        self._ui.spinM4_4.setValue(settings.markerOffset[3][3])
        self._ui.spinM5_4.setValue(settings.markerOffset[4][3])

        self._ui.spinM1_5.setValue(settings.markerOffset[0][4])
        self._ui.spinM2_5.setValue(settings.markerOffset[1][4])
        self._ui.spinM3_5.setValue(settings.markerOffset[2][4])
        self._ui.spinM4_5.setValue(settings.markerOffset[3][4])
        self._ui.spinM5_5.setValue(settings.markerOffset[4][4])

        self._settings = settings

    @pyqtSlot()
    def accept(self):
        self._collectData()
        super().accept()

    def _collectData(self):
        print('collecting data')
        ui = self._ui
        self._settings = Settings(
            markerOffset=[
                [ui.spinM1_1.value(), ui.spinM1_2.value(), ui.spinM1_3.value(), ui.spinM1_4.value(), ui.spinM1_5.value()],
                [ui.spinM2_1.value(), ui.spinM2_2.value(), ui.spinM2_3.value(), ui.spinM2_4.value(), ui.spinM2_5.value()],
                [ui.spinM3_1.value(), ui.spinM3_2.value(), ui.spinM3_3.value(), ui.spinM3_4.value(), ui.spinM3_5.value()],
                [ui.spinM4_1.value(), ui.spinM4_2.value(), ui.spinM4_3.value(), ui.spinM4_4.value(), ui.spinM4_5.value()],
                [ui.spinM5_1.value(), ui.spinM5_2.value(), ui.spinM5_3.value(), ui.spinM5_4.value(), ui.spinM5_5.value()],
            ],
            offsetF1=ui.spinF1.value(),
            offsetF2=ui.spinF2.value(),
            offsetF3=ui.spinF3.value(),
            offsetF4=ui.spinF4.value(),
            offsetF5=ui.spinF5.value(),
            freqOffset=ui.spinFreq.value(),
            ampOffset=ui.spinAmp.value(),
            curOffset=ui.spinCurr.value()
        )

    @property
    def settings(self):
        return self._settings
