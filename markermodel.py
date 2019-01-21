from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant


class MarkerModel(QAbstractTableModel):

    ColName, \
    ColFreq, \
    ColAmp = range(3)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._headers = ['#', 'Частота', 'дБц/Гц']

        self._markerIndex = 4

        self._data = [
            ['1', 1_000.0, 0],
            ['2', 10_000.0, 0],
            ['3', 100_000.0, 0]
        ]

    def init(self, amps=None):
        if amps is not None:
            self.beginResetModel()
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

    def setData(self, index, value, role):
        if index.column() == 1 and role == Qt.EditRole:
            row = index.row()
            col = index.column()
            new_value = 0
            try:
                new_value = float(value)
            except Exception as ex:
                print(ex)

            self._data[row][col] = new_value
            self.dataChanged.emit(index, index, [])
            return True

        return False

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return QVariant(self._data[row][col])
        elif role == Qt.EditRole:
            if col == self.ColFreq:
                return QVariant(self._data[row][col])

        return QVariant()

    def flags(self, index):
        f = super().flags(index)
        if index.column() == self.ColFreq:
            return f | Qt.ItemIsEditable
        return f

    def updateModel(self, amps):
        self.beginResetModel()

        for index, amp in enumerate(amps):
            self._data[index][2] = round(amp, 2)

        self.endResetModel()

    def addMarker(self):
        self.beginResetModel()
        self._data.append([str(self._markerIndex), 10_000.0, 0])
        self._markerIndex += 1
        self.endResetModel()

    def delMarker(self, row: int):
        self.beginResetModel()
        del self._data[row]
        self.endResetModel()

    @property
    def markers(self):
        return [d[1] for d in self._data]

    @property
    def stats(self):
        return [f'{d[0]}: {round(d[1]/1_000, 1)} кГц = {round(d[2], 2)} дБц/Гц' for d in self._data]
