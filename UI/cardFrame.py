import sys
from typing import List, Callable, Union

from PySide6.QtWidgets import (
    QFrame,
    QWidget,
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
    QLabel
)

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QResizeEvent, QWheelEvent
from utils import *


class CardFrame(QFrame):
    def __init__(self, title: str, parameterNums: int, parent=None):
        super(CardFrame, self).__init__(parent)
        self.titleStr = title
        self.parameterNums = parameterNums
        self.setObjectName("CardBorder")
        self.setupUI()
        self.setMinAndMaxSize()
        self.updateParameters([1, 2, 3, 4, 5])

    def updateParameters(self, data: List[Union[int, str]]):
        """
        update the parameters once you set the mass or liquid parameters
        """
        for i, item in enumerate(data):
            self.parametersValue[i].setText(str(item))

    def setupUI(self):
        self.contentFrame = QFrame()
        self.contentFrame.setObjectName("Card")
        # title
        self.title = QLabel()
        self.title.setText(self.titleStr)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        # Parameters
        self.parametersName = [QLabel()
                               for _ in range(self.parameterNums)]
        for i, parameterName in enumerate(self.parametersName):
            parameterName.setAlignment(Qt.AlignmentFlag.AlignCenter)
            parameterName.setSizePolicy(
                QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)  # type: ignore
            parameterName.setObjectName("parameterName")
            parameterName.setText(f'质谱仪参数{i + 1}:')
        self.parametersValue = [QLabel() for _ in range(self.parameterNums)]
        for parameterValue in self.parametersValue:
            parameterValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
            parameterValue.setSizePolicy(
                QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)  # type: ignore
            parameterValue.setObjectName("parameterValue")
        # Parameters Layout
        self.hBoxLayoutList = [QHBoxLayout()
                               for _ in range(self.parameterNums)]
        for layout in self.hBoxLayoutList:
            layout.setSpacing(4)
            layout.setContentsMargins(2, 0, 2, 0)
        for i in range(self.parameterNums):
            initialTheLayout(self.hBoxLayoutList[i], [
                             self.parametersName[i], self.parametersValue[i]], [1, 1])
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.title)
        initialTheLayout(self.vBoxLayout, self.hBoxLayoutList, [  # type: ignore
                         1 for _ in range(self.parameterNums)])
        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(5, 0, 5, 10)
        self.contentFrame.setLayout(self.vBoxLayout)
        # content Layout
        self.contentLayout = QHBoxLayout()
        self.contentLayout.addWidget(self.contentFrame)
        self.contentLayout.setContentsMargins(4, 10, 4, 10)
        self.setLayout(self.contentLayout)

    def setMinAndMaxSize(self):
        # Set minimum and maximum dimensions for the card
        self.setMaximumSize(QSize(300, 300))
        self.setMinimumSize(QSize(200, 200))


class Debounce:
    def __init__(self, func: Callable, delay: int):
        self.func = func
        self.delay = delay
        self.timer = None

    def __call__(self):
        print("Debounce called")
        if self.timer is not None:
            print("Stopping previous timer")
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.func(True))
        self.timer.start(self.delay)


class DynamicLayoutApp(QScrollArea):
    """
    A scroll area containing dynamically updating cards with debounce mechanism.
    """

    def __init__(self, cards: List[CardFrame]):
        super().__init__()
        self.cards: List[CardFrame] = cards
        self.setObjectName("ParametersScollArea")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.setStyleSheet(self.readQss("./style/HomePage.css"))
        self.initParameters()
        self.initFlags()
        self.initUI()

    def readQss(self, style_path) -> str:
        with open(style_path, "r") as style_file:
            Qssfile = style_file.read()
        return Qssfile

    def initParameters(self):
        # Initialize layout parameters
        self.columns = 0
        self.spacing = 5
        self.initRows = 20
        self.updateRows = 10
        self.nowIndex = 0
        self.nowRow = 0
        self.nowColumn = 0

    def initFlags(self):
        # Initialize flags and debounce mechanism
        self.isInitial = True
        debounce_delay = 50  # Debounce delay in milliseconds
        self.debounce_update_layout = Debounce(
            self.updateLayout, debounce_delay)

    def initUI(self):
        # Initialize the UI components
        self.setMinimumSize(QSize(480, 480))
        self.CardWidget = QWidget()
        self.CardWidget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(self.spacing)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.setWidget(self.CardWidget)
        self.CardWidget.setLayout(self.gridLayout)
        # Make the scroll area's content resizable
        self.setWidgetResizable(True)

    def addCard(self, index: int, row: int, col: int):
        # Add a card to the grid layout
        self.gridLayout.addWidget(self.cards[index], row, col)

    def updateRowColAndIndex(self, index: int, row: int, col: int):
        # Update the current row, column, and index values
        self.nowRow = row
        self.nowColumn = col
        self.nowIndex = index

    def clearWidgets(self):
        # Clear all widgets from the grid layout
        while self.gridLayout.count():
            widget = self.gridLayout.itemAt(0).widget()
            if widget:
                self.gridLayout.removeWidget(widget)
                widget.setParent(None)  # type: ignore

    def updateLayout(self, isInitial: bool = False):
        # Update the layout of the scroll area's content
        print("update")
        self.debounce_update_layout.timer.stop()  # type: ignore
        numColumns = self.viewport().width(
        ) // (self.cards[0].maximumWidth() + self.spacing)
        if self.ifReLayout(numColumns):
            self.clearWidgets()
            self.updateRowColAndIndex(0, 0, 0)
        maxViewNum = self.updateRows * numColumns
        if isInitial:
            maxViewNum = self.initRows * numColumns
        updateNum = min(maxViewNum, len(self.cards) - self.nowIndex)
        numRows = (updateNum + self.nowColumn) // numColumns
        for i in range(numRows):
            row = self.nowRow + i
            for j in range(numColumns):
                col = (self.nowColumn + j) % numColumns
                if self.nowIndex + i * numColumns + j < len(self.cards):
                    self.addCard(self.nowIndex + i * numColumns + j, row, col)
                if i == numRows - 1 and j == numColumns - 1:
                    self.updateRowColAndIndex(
                        self.nowIndex + updateNum, row, col + 1)
        self.columns = numColumns

    def wheelEvent(self, wheelEvent: QWheelEvent):
        # Handle wheel scrolling event
        scroll_bar = self.verticalScrollBar()
        if wheelEvent.angleDelta().y() < 0:
            if scroll_bar.value() == scroll_bar.maximum():
                self.updateLayout(False)
        super().wheelEvent(wheelEvent)

    def ifReLayout(self, numColumns) -> bool:
        # Check if the number of columns has changed
        if numColumns != self.columns:
            return True
        return False

    def resizeEvent(self, event: QResizeEvent):
        # Resize event handler
        new_width = self.viewport().width()
        self.CardWidget.setFixedWidth(new_width)
        self.debounce_update_layout()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_list = []
    for i in range(101):
        card_list.append(CardFrame(f'质谱仪参数', 5))
    dynamic_layout_app = DynamicLayoutApp(card_list)
    dynamic_layout_app.show()
    sys.exit(app.exec())
