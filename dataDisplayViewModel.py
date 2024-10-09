from PyQt5.QtCore import Qt, QAbstractTableModel


class MyTableModel(QAbstractTableModel):
    def __init__(self, data, HEADERS):
        super().__init__()
        self.data = data
        self.headers = HEADERS

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return len(self.data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        标题定义
        """
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)
