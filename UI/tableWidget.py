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
    def __init__(self,
                 data: Union[str, pd.DataFrame],
                 headLables: List[str] = [],
                 parent: Optional[QWidget] = None):
        """
        Basic TableWidget Class

        This is the base class for the table widget.

        This class represents a table widget that displays the data you have added. 

        It allows you to view the data, but you cannot edit or delete it.

        Parameters:
        * data (Union[str, pd.DataFrame]): The CSV path or the DataFrame. 
            In the future, this will be replaced with database indexing.
        * headLabels (Sequence[str]): The headers for the table data.
        * parent: The parent widget of the table widget.

        TODO: 
        1. Replace the 'data' parameter with a database connection. You can use the sqlite3 library.
        2. 'headLabels' can be removed; use the database fields as table headers.
        """
        super(TableWidget, self).__init__(parent)
        self.headLabels = headLables
        self.data = data
        self.initData()
        self.initTableContent()
        self.initTableAttributes()
        self.setStyleSheet(setQss("./style/TableWidget.css"))

    def initTableAttributes(self):
        """
        init the attributes of the TableWidget
        """
        self.horizontalHeader().setMaximumSectionSize(250)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)

    def initFlags(self):
        """
        Initialize the Flags:

        Flags initialized in this section:
        * numColumns: Number of the 'headLabels' columns.
        * isInitial: Checks if it's the first time of adding data.
        * initRows: The initial number of rows displayed on the table.
        * updateRows: Used to update rows data on the table when the user scrolls to the end.
        * nowIndex: The current index of added data.
        * nowRows: The current row index for the added data.
        """

        self.numColumns = len(self.df.columns)
        self.isInitial = True
        self.initRows = 20
        self.updateRows = 30
        self.nowIndex = 0
        self.nowRows = 0
        self.setColumnCount(self.numColumns)
        self.setHorizontalHeaderLabels(self.headLabels)

    def updateRowIndex(self, row: int, index: int):
        """
        update the parameters of numRows, nowIndex 
        """
        self.nowRows, self.nowIndex = row, index

    def initData(self):
        """
        Initialize Displayed Data

        This section initializes the data that will be displayed in the widget.

        In the future, this will be replaced with database integration.

        For now, we use this to test the widget and its functionality.

        TODO:
        * replace it with the indexing of the database 
        * maybe you need the name of the database, table 
        """

        if isinstance(self.data, str):
            self.df = pd.read_csv(self.data)
        else:
            self.df = self.data
        self.dataLen = len(self.df)

    def initTableContent(self):
        """
        init the data displayed on the table 
        """
        self.clear()
        self.setRowCount(0)
        self.initFlags()
        self.updateTableData()
        self.isInitial = False

    def updateTableData(self):
        """
        Update Data in the Table

        This function updates the data displayed in the table.

        1. When initializing, update 'initRows' number of rows.
        2. Otherwise, when the user scrolls to the bottom, 
        update the table with 'updateRows' number of rows or remaining data.
        """

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
        """
        Monitor Wheel Event

        This function monitors the wheel event.

        Currently, it is used to update data. 

        You can add other functionalities as needed in the future.
        """

        scroll_bar = self.verticalScrollBar()
        if event.angleDelta().y() < 0:
            if scroll_bar.value() == scroll_bar.maximum():
                self.updateTableData()
        """
        It's essential to execute the parent class's operation function;
        otherwise, unexpected bugs might occur,
        as you may not be aware of what actions the parent class's function performs.
        """
        super().wheelEvent(event)


class TableWidgetWithButtons(TableWidget):
    def __init__(self,
                 data: Union[str, pd.DataFrame],
                 parent: Optional[QWidget] = None,
                 headLabels: List[str] = []):
        """
        TableWidget with Operation Buttons Class

        This class represents a table widget that displays the data you have added, along with operation buttons. 

        It allows you to edit, delete, or select the data.

        Parameters:
        * data (Union[str, pd.DataFrame]): The CSV path or the DataFrame. 
            In the future, this will be replaced with database indexing.
        * headLabels (Sequence[str]): The headers for the table data.
        * parent: The parent widget of the table widget.

        TODO: 
        1. Replace the 'data' parameter with a database connection. You can use the sqlite3 library.
        2. 'headLabels' can be removed; use the database fields as table headers.
        """
        super(TableWidgetWithButtons, self).__init__(data, headLabels, parent)
        self.connectSignal()

    def initTableAttributes(self):
        """
        init the attributes of the TableWidget
        """
        self.horizontalHeader().setMinimumSectionSize(100)
        self.horizontalHeader().setMaximumSectionSize(250)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setColumnWidth(self.numColumns, 240)

    def connectSignal(self):
        self.horizontalHeader().sectionResized.connect(self.selectionSizeIfChanged)

    def initFlags(self):
        self.numColumns = len(self.df.columns)
        self.isInitial = True
        self.initRows = 20
        self.updateRows = 30
        self.nowIndex = 0
        self.nowRows = 0
        self.setColumnCount(self.numColumns + 1)
        labels = self.headLabels + ["操作"]
        self.setHorizontalHeaderLabels(labels)
        """
        Initialize the Button List
    
        This function initializes the list used to store buttons.
        
        When deleting data, you need to update the stored row data in the buttons displayed in the table to avoid errors.
        """
        self.buttons: List[Tuple[ButtonEmitRow,
                                 ButtonEmitRow, ButtonEmitRow]] = []

    def insertButton(self, row: int, col: int) -> Tuple[ButtonEmitRow, ButtonEmitRow, ButtonEmitRow]:
        """
        Insert Select, Delete, and Edit Buttons with Row Data

        Parameters:
        * row: The row where you are adding the data.
        * col: The column where you are adding the buttons
        """

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

    def updateDfData(self, data: Tuple[str]):
        """
        Add One Row of Data to the DataFrame

        This function adds one row of data to the DataFrame.

        Note: You also need to update the length of the data.
        """

        self.df.loc[self.dataLen] = data  # type: ignore
        self.dataLen += 1
        """
        TODO: update the data in the database 
        """

    def updateTableData(self):
        """
        Update Data in the Table

        This function updates the data displayed in the table.

        1. When initializing, update 'initRows' number of rows.
        2. Otherwise, when the user scrolls to the bottom, 
        update the table with 'updateRows' number of rows or remaining data.
        """
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
        """
        Select Sure Dialog

        Opens a dialog to confirm selecting a specific row's data.

        This function opens a dialog to confirm whether the user wants to select the data from a specific row.

        Parameters:
        * row (int): The row index.
        """
        self.dialog = SelectDialog(
            f"你确定要选择{row + 1}行的数据吗？", self.selectRowData, (row, ))
        self.dialog.show()

    def selectRowData(self, row: int):
        """
        Select Row Data

        This function retrieves the data from what user input and performs the select operation.

        Parameters:
        * row (int): The row index.
        """
        reData = []
        for col in range(self.numColumns):
            item = self.item(row, col)
            reData.append(item.text())

    def deleteSureDialog(self, row: int):
        """
        Delete Sure Dialog

        Opens a dialog to confirm deleting a specific row's data.

        This function opens a dialog to confirm whether the user wants to delete the data from a specific row.

        Parameters:
        * row (int): The row index.
        """
        self.dialog = DeleteDialog(
            f"你确定要删除{row + 1}行的数据吗？", self.deleteRowData, (row, ))
        self.dialog.show()

    def deleteRowData(self, row: int):
        """
        Delete Row Data

        This function deletes the data from the selected row and updates the table and buttons accordingly.

        Parameters:
        * row (int): The row index.
        """
        self.removeRow(row)
        del self.buttons[row]
        self.nowRows -= 1
        for i in range(row, self.nowRows):
            for btn in self.buttons[i]:
                btn.updateRow(btn.row - 1)
        """
        TODO: update the data in the database 
        """

    def editSureDialog(self, row: int):
        """
        Edit Sure Dialog

        Opens a dialog to confirm editing a specific row's data.

        This function opens a dialog to confirm whether the user wants to edit the data from a specific row.

        Parameters:
        * row (int): The row index.

        """
        data = []
        for col in range(self.numColumns):
            data.append(self.item(row, col).text())

        self.dialog = EditDialog(
            f"正在编辑第{row + 1}行的数据", self.editRowData, (row, ), tuple(self.headLabels[:self.numColumns]), tuple(data))
        self.dialog.show()

    def editRowData(self, row: int, data: Tuple):
        """
        Edit Row Data

        This function edits the data in the selected row and updates the table accordingly.

        Parameters:
        * row (int): The row index.
        * data (Tuple): The edited data.
        """
        for col in range(self.numColumns):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setText(data[col])
            self.setItem(row, col, item)
        """
        TODO: update the data in the database 
        """

    def selectionSizeIfChanged(self, logicalIndex: int, oldSize: int, newSize: int) -> None:
        """
        Selection Size If Changed

        This function handles resizing the selection based on changes in logical index and size.

        Parameters:
        * logicalIndex (int): The logical index.
        * oldSize (int): The old size.
        * newSize (int): The new size.
        """
        if logicalIndex == self.numColumns:
            if newSize < 240:
                self.horizontalHeader().resizeSection(logicalIndex, 240)

    def sortDataUpDown(self, column: str):
        """
        Sort Data Up-Down

        This function sorts the data in ascending order based on the selected column and updates the table.

        Parameters:
        * column (str): The column by which to sort.

        TODO: Extend the Function

        extend the existing functionality to accommodate user selection of multiple columns for sorting.

        Additional UI components may be required, such as adding other ComboBoxes to allow selection of multiple columns.
        """
        self.df = self.df.sort_values(by=column, ascending=True)
        self.initTableContent()

    def sortDataDownUp(self, column: str):
        """
        Sort Data Down-Up

        This function sorts the data in descending order based on the selected column and updates the table.

        Parameters:
        * column (str): The column by which to sort.

        TODO: Extend the Function

        extend the existing functionality to accommodate user selection of multiple columns for sorting.

        Additional UI components may be required, such as adding other ComboBoxes to allow selection of multiple columns
        """
        self.df = self.df.sort_values(by=column, ascending=False)
        self.initTableContent()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    table = TableWidgetWithButtons("./TableWidgetTestData.csv",
                                   headLabels=["日期", "姓名", "省份", "市区", "地址", "邮编"])
    widget = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(table)
    widget.setLayout(layout)
    widget.show()
    app.exec()
