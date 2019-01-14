from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot


class MarkerModel(QAbstractTableModel):

    ColName, \
    ColFreq = range(2)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._headers = ['#', 'Частота', 'дБц/Гц']

        self._data = [
            ['Маркер 1', 1_000.0, 0],
            ['Маркер 2', 10_000.0, 0],
            ['Маркер 3', 100_000.0, 0]
        ]

    def init(self):
        self.beginResetModel()
        # self.initHeader(self._domain)
        # self._data = self._domain
        self.endResetModel()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._headers):
                    return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return 3

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return QVariant(self._data[row][col])

        return QVariant()

    @pyqtSlot(name='updateModel')
    def updateModel(self):
        self.initModel()

    @property
    def markers(self):
        return [d[1] for d in self._data]

