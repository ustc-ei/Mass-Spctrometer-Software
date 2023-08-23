from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import QSize, QItemSelection
from utils import Font, PixMap


class Navigator(QListWidget):
    def __init__(self, names: List[str], isHaveIcon=False, pixmapPath: List[str] = [], parent: Optional[QWidget] = None) -> None:
        super(Navigator, self).__init__(parent)
        self._parent = parent
        self.itemNames = names
        self.itemPixmapPath = pixmapPath
        self.isHaveIcon = isHaveIcon
        self.itemSelectedFont = Font(15, ["Helvetica", "微软雅黑", "宋体"], True)
        self.itemNoSelectedFont = Font(15, ["Helvetica", "微软雅黑", "宋体"])
        self.setupUI()

    def updateItemsIcon(self, item: QListWidgetItem, iconPath: str):
        icon = PixMap(iconPath, QSize(30, 30))
        item.setIcon(icon)

    def updateItemsText(self, item: QListWidgetItem, text: str):
        item.setText(text)
        item.setFont(self.itemNoSelectedFont)

    def setupUI(self):
        if self.isHaveIcon:
            self.setIconSize(QSize(30, 30))
        for i, itemName in enumerate(self.itemNames):
            item = QListWidgetItem()
            self.addItem(item)
            if self.isHaveIcon:
                self.updateItemsIcon(item, self.itemPixmapPath[i])
            self.updateItemsText(item, itemName)

    def clearText(self):
        for i in range(self.count()):
            self.item(i).setText("")

    def recoverText(self):
        for i in range(self.count()):
            self.item(i).setText(self.itemNames[i])

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        if deselected.indexes():
            self.item(deselected.indexes()[0].row()).setFont(
                self.itemNoSelectedFont)
        self.item(selected.indexes()[0].row()).setFont(self.itemSelectedFont)
        # toggle the current widget of the stackwidgets
        if selected.indexes()[0].row() == 0:
            self._parent.stackWidget.setCurrentIndex(  # type: ignore
                selected.indexes()[0].row())  # type: ignore
