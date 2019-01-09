from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot


class MeasureModel(QAbstractTableModel):

    _default_column_count = 1
    _default_headers = ['№']

    ColRowNumber, \
    ColFreq, \
    ColAmp = range(3)

    # TODO: read params from .xlsx
    def __init__(self, parent=None, domain=None):
        super().__init__(parent)

        self._domain = domain
        self._headers = self._default_headers + self._domain.headers

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
        return self._domain.rows()

    def columnCount(self, parent=None, *args, **kwargs):
        return self._domain.cols() + 1

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if col == self.ColRowNumber:
                return row
            else:
                return QVariant(self._domain.data(row, col))

        return QVariant()

    @pyqtSlot(name='updateModel')
    def updateModel(self):
        self.initModel()
