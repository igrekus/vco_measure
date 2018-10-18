from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot


class MeasureModel(QAbstractTableModel):
    _default_column_count = 1

    _default_headers = ['№'] * _default_column_count

    # TODO: read params from .xlsx
    def __init__(self, parent=None, instrumentManager=None):
        super().__init__(parent)

        self._data = list()
        self._headers = self._default_headers
        self._columnCount = self._default_column_count

        self._instrumentManager = instrumentManager

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()

    def initModel(self):
        self.beginResetModel()
        self.initHeader(self._instrumentManager._captions)
        self._data = self._instrumentManager._measure_data
        self.endResetModel()

    def initHeader(self, headers):
        self._headers = headers
        self._columnCount = len(headers)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._headers):
                    return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        # FIXME: row counter
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return self._columnCount

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if not self._data:
                return QVariant()
            return QVariant(self._data[row][col])

        return QVariant()

    @pyqtSlot(name='updateModel')
    def updateModel(self):
        self.initModel()
