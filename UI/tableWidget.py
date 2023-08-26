import sys
from typing import Optional, List, Union, Tuple
from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QApplication,
    QTableWidgetItem,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QWheelEvent
import pandas as pd


class ButtonEmitRow(QPushButton):
    # emit the row data
    signal = Signal(int)

    def __init__(self, text: str, row: int):
        super(ButtonEmitRow, self).__init__(text)
        self.row = row
        self.connectSignal()
        self.setMaximumSize(QSize(150, 50))
        self.setMinimumSize(QSize(100, 30))

    def updateRow(self, row: int):
        self.row = row

    def connectSignal(self):
        self.clicked.connect(self.emitRow)

    def emitRow(self):
        self.signal.emit(self.row)


class TableWidget(QTableWidget):
    def __init__(self, data: Union[str, pd.DataFrame], parent: Optional[QWidget] = None, headLables: List[str] = []):
        super(TableWidget, self).__init__(parent)
        self.headLabels = headLables
        self.data = data
        self.initData()
        self.initFlags()
        self.initTableContent()

    def initFlags(self):
        self.numColumns = len(self.df.columns)
        self.isInitial = True
        self.initRows = 10
        self.updateRows = 20
        self.nowIndex = 0
        self.nowRows = 0

    def updateRowIndex(self, row: int, index: int):
        self.nowRows, self.nowIndex = row, index

    def initData(self):
        self.setColumnCount(len(self.headLabels))
        self.setHorizontalHeaderLabels(self.headLabels)
        if isinstance(self.data, str):
            self.df = pd.read_csv(self.data)
        else:
            self.df = self.data
        self.dataLen = len(self.df)

    def initTableContent(self):
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


class TableWidgetWithButton(TableWidget):
    def __init__(self, data: Union[str, pd.DataFrame], parent: Optional[QWidget] = None, headLables: List[str] = []):
        self.initButtonsList()
        super(TableWidgetWithButton, self).__init__(data, parent, headLables)
        self.horizontalHeader().setStretchLastSection(True)

    def initButtonsList(self):
        self.buttons: List[Tuple[ButtonEmitRow, ButtonEmitRow]] = []

    def insertSelectButton(self, row: int, col: int) -> ButtonEmitRow:
        widget = QWidget()
        layout = QHBoxLayout()
        btn = ButtonEmitRow("采用", row)
        btn.setObjectName("TableWidgetSelectButton")
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self.setCellWidget(row, col, widget)
        btn.signal.connect(self.selectRowData)
        return btn

    def insertDeleteButton(self, row: int, col: int) -> ButtonEmitRow:
        widget = QWidget()
        layout = QHBoxLayout()
        btn = ButtonEmitRow("删除", row)
        btn.setObjectName("TableWidgetDeleteButton")
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self.setCellWidget(row, col, widget)
        btn.signal.connect(self.deleteRowData)
        return btn

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
            selectedButton = self.insertSelectButton(rowCount, self.numColumns)
            deleteButton = self.insertDeleteButton(
                rowCount, self.numColumns + 1)
            self.buttons.append((selectedButton, deleteButton))
        self.updateRowIndex(self.nowRows + numRows, self.nowIndex + numRows)

    def selectRowData(self, row: int):
        reData = []
        for col in range(self.numColumns):
            item = self.item(row, col)
            reData.append(item.text())

    def deleteRowData(self, row: int):
        self.removeRow(row)
        del self.buttons[row]
        self.nowRows -= 1
        for i in range(row, self.nowRows):
            for btn in self.buttons[i]:
                btn.updateRow(btn.row - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = TableWidgetWithButton("./TableWidgetTestData.csv",
                                  headLables=["日期", "姓名", "省份", "市区", "地址", "邮编", "操作1", "操作2"])
    widget = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(table)
    widget.setLayout(layout)
    widget.show()
    app.exec()
