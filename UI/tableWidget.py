import sys
from enum import Enum
from typing import Optional, List, Union, Tuple
from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QApplication,
    QTableWidgetItem,
    QHBoxLayout,
    QPushButton,
    QHeaderView
)
from PySide6.QtCore import Qt, Signal, QSize, QItemSelection
from PySide6.QtGui import QWheelEvent
import pandas as pd
from dialog import SelectDialog, DeleteDialog, EditDialog
from utils import initialTheLayout, setQss


class ButtonEmitRow(QPushButton):
    # emit the row data
    signal = Signal(int)

    def __init__(self, row: int, text: str = ""):
        super(ButtonEmitRow, self).__init__(text)
        self.row = row
        self.connectSignal()
        self.setMaximumSize(QSize(100, 50))
        self.setMinimumSize(QSize(80, 30))

    def updateRow(self, row: int):
        self.row = row

    def connectSignal(self):
        self.clicked.connect(self.emitRow)

    def emitRow(self):
        self.signal.emit(self.row)


class TableWidget(QTableWidget):
    def __init__(self, data: Union[str, pd.DataFrame], parent: Optional[QWidget] = None, headLables: List[str] = []):
        """
        TODO: 
        1. 将 data 参数更换为数据库, 进行数据库连接, 可以使用 sqlite3 库
        2. headLabels 可以删掉了, 将数据库的字段作为表头
        """
        super(TableWidget, self).__init__(parent)
        self.headLabels = headLables
        self.data = data
        self.initData()
        self.initTableContent()
        self.initTableAttributes()
        self.setStyleSheet(setQss("./style/TableWidget.css"))

    def initTableAttributes(self):
        self.horizontalHeader().setMaximumSectionSize(250)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)

    def initFlags(self):
        self.numColumns = len(self.df.columns)
        self.isInitial = True
        self.initRows = 10
        self.updateRows = 20
        self.nowIndex = 0
        self.nowRows = 0
        self.setColumnCount(self.numColumns)
        self.setHorizontalHeaderLabels(self.headLabels)

    def updateRowIndex(self, row: int, index: int):
        self.nowRows, self.nowIndex = row, index

    def initData(self):
        if isinstance(self.data, str):
            self.df = pd.read_csv(self.data)
        else:
            self.df = self.data
        self.dataLen = len(self.df)

    def initTableContent(self):
        self.initFlags()
        self.updateTableData()
        self.isInitial = False

    def updateTableData(self):
        numRows = self.updateRows
        if self.isInitial:
            numRows = self.initRows
        numRows = min(numRows, self.dataLen - self.nowIndex)
        for row in range(numRows):
            rowCount = self.rowCount()
            self.insertRow(rowCount)
            for col in range(len(self.df.columns)):
                item = QTableWidgetItem()
                item.setText(str(self.df.iloc[self.nowIndex + row, col]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(rowCount, col, item)
        self.updateRowIndex(self.nowRows + numRows, self.nowIndex + numRows)

    def wheelEvent(self, event: QWheelEvent) -> None:
        scroll_bar = self.verticalScrollBar()
        if event.angleDelta().y() < 0:
            if scroll_bar.value() == scroll_bar.maximum():
                self.updateTableData()
        super().wheelEvent(event)


class TableWidgetWithButtons(TableWidget):
    # class buttonType(Enum):
    #     Select = 0
    #     Edit = 1
    #     Delete = 2

    def __init__(self,
                 data: Union[str, pd.DataFrame],
                 parent: Optional[QWidget] = None,
                 headLabels: List[str] = []):
        """
        TODO: 同上, 将其修改为数据库连接, 使用 sqlite3
        tableWidget with buttons
        """
        self.initButtonsList()
        super(TableWidgetWithButtons, self).__init__(data, parent, headLabels)
        self.connectSignal()

    def initTableAttributes(self):
        self.horizontalHeader().setMinimumSectionSize(100)
        self.horizontalHeader().setMaximumSectionSize(250)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setColumnWidth(self.numColumns, 240)

    def initButtonsList(self):
        self.buttons: List[Tuple[ButtonEmitRow,
                                 ButtonEmitRow, ButtonEmitRow]] = []

    def connectSignal(self):
        self.horizontalHeader().sectionResized.connect(self.selectionSizeIfChanged)

    def initFlags(self):
        self.numColumns = len(self.df.columns)
        self.isInitial = True
        self.initRows = 10
        self.updateRows = 20
        self.nowIndex = 0
        self.nowRows = 0
        self.setColumnCount(self.numColumns + 1)
        self.headLabels.extend(["操作"])
        self.setHorizontalHeaderLabels(self.headLabels)

    def insertButton(self, row: int, col: int) -> Tuple[ButtonEmitRow, ButtonEmitRow, ButtonEmitRow]:
        widget = QWidget()
        layout = QHBoxLayout()
        selectedBtn = ButtonEmitRow(row, "选择")
        selectedBtn.setObjectName("TableWidgetSelectButton")
        selectedBtn.signal.connect(self.selectSureDialog)
        editBtn = ButtonEmitRow(row, "编辑")
        editBtn.setObjectName("TableWidgetEditButton")
        editBtn.signal.connect(self.editSureDialog)
        deleteBtn = ButtonEmitRow(row, "删除")
        deleteBtn.setObjectName("TableWidgetDeleteButton")
        deleteBtn.signal.connect(self.deleteSureDialog)
        initialTheLayout(
            layout, [selectedBtn, editBtn, deleteBtn], [1, 1, 1], True)
        layout.setSpacing(3)
        layout.setContentsMargins(2, 1, 5, 0)
        widget.setLayout(layout)
        self.setCellWidget(row, col, widget)
        return tuple([selectedBtn, editBtn, deleteBtn])

    def updateTableData(self):
        numRows = self.updateRows
        if self.isInitial:
            numRows = self.initRows
        numRows = min(numRows, self.dataLen - self.nowIndex)
        for row in range(numRows):
            rowCount = self.rowCount()
            self.insertRow(rowCount)
            for col in range(self.numColumns):
                item = QTableWidgetItem()
                item.setText(str(self.df.iloc[self.nowIndex + row, col]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(rowCount, col, item)
            btns = self.insertButton(rowCount, self.numColumns)
            self.buttons.append(btns)
        self.setStyleSheet(setQss('./style/TableWidget.css'))
        self.updateRowIndex(self.nowRows + numRows, self.nowIndex + numRows)

    def selectSureDialog(self, row: int):
        self.dialog = SelectDialog(
            f"你确定要选择{row + 1}行的数据吗？", self.selectRowData, (row, ))
        self.dialog.show()

    def selectRowData(self, row: int):
        reData = []
        for col in range(self.numColumns):
            item = self.item(row, col)
            reData.append(item.text())

    def deleteSureDialog(self, row: int):
        self.dialog = DeleteDialog(
            f"你确定要删除{row + 1}行的数据吗？", self.deleteRowData, (row, ))
        self.dialog.show()

    def deleteRowData(self, row: int):
        self.removeRow(row)
        del self.buttons[row]
        self.nowRows -= 1
        for i in range(row, self.nowRows):
            for btn in self.buttons[i]:
                btn.updateRow(btn.row - 1)
        # TODO: 更改数据库中数据

    def editSureDialog(self, row: int):
        data = []
        for col in range(self.numColumns):
            data.append(self.item(row, col).text())

        self.dialog = EditDialog(
            f"正在编辑第{row + 1}行的数据", self.editRowData, (row, ), tuple(self.headLabels[:self.numColumns]), tuple(data))
        self.dialog.show()

    def editRowData(self, row: int, data: Tuple):
        for col in range(self.numColumns):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setText(data[col])
            self.setItem(row, col, item)
        # TODO: 更改数据库中数据

    def selectionSizeIfChanged(self, logicalIndex: int, oldSize: int, newSize: int) -> None:
        if logicalIndex == self.numColumns:
            if newSize < 240:
                self.horizontalHeader().resizeSection(logicalIndex, 240)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = TableWidgetWithButtons("./TableWidgetTestData.csv",
                                   headLabels=["日期", "姓名", "省份", "市区", "地址", "邮编"])
    widget = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(table)
    widget.setLayout(layout)
    widget.show()
    app.exec()
