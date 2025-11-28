import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt



class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers = None) -> None:
        super().__init__()
        self.setObjectName("table-view")
        self._headers = headers
        self._data = data
   
    def headerData(self, section, orientation, role): # type: ignore
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section] # type: ignore
            else:
                return str(section + 1)

    def data(self, index, role): # type: ignore
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        

    def rowCount(self, index = None) -> int: # type: ignore
        return len(self._data)
    
    def add_row(self, row_data):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(row_data)
        self.endInsertRows()

    def columnCount(self, index) -> int: # type: ignore
        return len(self._data[0])
