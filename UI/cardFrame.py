import sys
from typing import Optional, List, Callable
import threading
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
from PySide6.QtGui import QResizeEvent, QWheelEvent


class CardFrame(QFrame):
    def __init__(self, buttonText: str, parent=None):
        super(CardFrame, self).__init__(parent)
        self.buttonText = buttonText
        self.setupUI()
        self.setMinAndMaxSize()

    def setupUI(self):
        # Create a horizontal layout for the card
        self.qhBoxLayout = QHBoxLayout()
        self.button = QPushButton()
        self.button.setText(self.buttonText)
        # Set button's size policy to expanding in both dimensions
        self.button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.qhBoxLayout.setSpacing(0)
        self.qhBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.qhBoxLayout.addWidget(self.button)
        self.setLayout(self.qhBoxLayout)

    def setMinAndMaxSize(self):
        # Set minimum and maximum dimensions for the card
        self.setMaximumSize(QSize(150, 50))
        self.setMinimumSize(QSize(100, 50))


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
        self.timer.timeout.connect(self.func)
        self.timer.start(self.delay)


class DynamicLayoutApp(QScrollArea):
    """
    A scroll area containing dynamically updating cards with debounce mechanism.
    """

    def __init__(self, cards):
        super().__init__()
        self.cards: List[CardFrame] = cards
        self.initParameters()
        self.initFlags()
        self.initUI()

    def initParameters(self):
        # Initialize layout parameters
        self.columns = 0
        self.spacing = 2
        self.maxViewRow = 20
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
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
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

    def updateLayout(self):
        # Update the layout of the scroll area's content
        print("update")
        self.debounce_update_layout.timer.stop()  # type: ignore
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

    def wheelEvent(self, wheelEvent: QWheelEvent):
        # Handle wheel scrolling event
        scroll_bar = self.verticalScrollBar()
        if wheelEvent.angleDelta().y() < 0:
            if scroll_bar.value() == scroll_bar.maximum():
                self.updateLayout()
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
    for i in range(6000):
        card_list.append(CardFrame(str(i)))
    dynamic_layout_app = DynamicLayoutApp(card_list)
    dynamic_layout_app.show()
    sys.exit(app.exec())
