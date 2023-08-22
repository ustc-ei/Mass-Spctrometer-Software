import sys
from typing import List
from PySide6.QtWidgets import (
    QFrame,
    QWidget,
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QScrollArea
)
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QResizeEvent


class CardFrame(QFrame):
    def __init__(self, buttonText: str, parent=None):
        super(CardFrame, self).__init__(parent)
        self.buttonText = buttonText
        self.setupUI()
        self.setMinAndMaxSize()

    def setupUI(self):
        self.qhBoxLayout = QHBoxLayout()
        self.button = QPushButton()
        self.button.setText(self.buttonText)
        self.button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.qhBoxLayout.setSpacing(0)
        self.qhBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.qhBoxLayout.addWidget(self.button)
        self.setLayout(self.qhBoxLayout)

    def setMinAndMaxSize(self):
        self.setMaximumSize(QSize(150, 50))
        self.setMinimumSize(QSize(100, 50))


class DynamicLayoutApp(QScrollArea):
    def __init__(self, cards):
        super().__init__()
        self.cards: List[CardFrame] = cards
        self.initParameters()
        self.initUI()

    def initParameters(self):
        self.columns = 0
        self.spacing = 2
        self.maxViewRow = 20
        self.nowIndex = 0
        self.nowRow = 0
        self.nowColumn = 0
        self.update_timer = None

    def initUI(self):
        self.setMinimumSize(QSize(480, 480))
        self.CardWidget = QWidget()
        self.CardWidget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(self.spacing)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.CardWidget)
        self.CardWidget.setLayout(self.gridLayout)
        self.setWidgetResizable(True)
        self.updateLayout()

    def addCard(self, index: int, row: int, col: int):
        self.gridLayout.addWidget(self.cards[index], row, col)

    def updateRowColAndIndex(self, index: int, row: int, col: int):
        self.nowRow = row
        self.nowColumn = col
        self.nowIndex = index

    def clearWidgets(self):
        while self.gridLayout.count():
            widget = self.gridLayout.itemAt(0).widget()
            if widget:
                self.gridLayout.removeWidget(widget)
                widget.setParent(None)  # type: ignore

    def updateLayout(self):
        numColumns = self.viewport().width(
        ) // (self.cards[0].maximumWidth() + self.spacing)
        if self.ifReLayout(numColumns):
            self.clearWidgets()
            self.updateRowColAndIndex(0, 0, 0)
        maxViewNum = self.maxViewRow * numColumns
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

    def ifReLayout(self, numColumns) -> bool:
        if numColumns != self.columns:
            return True
        return False

    def resizeEvent(self, event: QResizeEvent):
        new_width = self.viewport().width()
        self.CardWidget.setFixedWidth(new_width)

        if self.update_timer is not None:
            self.update_timer.stop()
            self.update_timer.deleteLater()
            self.update_timer = None

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.debounce_update_layout)
        self.update_timer.start(200)

    def debounce_update_layout(self):
        self.update_timer.stop()  # type: ignore
        self.updateLayout()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    card_list = []
    for i in range(6000):
        card_list.append(CardFrame(str(i)))
    dynamic_layout_app = DynamicLayoutApp(card_list)
    dynamic_layout_app.show()
    sys.exit(app.exec())
