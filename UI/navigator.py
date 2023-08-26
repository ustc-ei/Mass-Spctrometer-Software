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
        """
        Custom navigation widget that displays a list of items.

        Parameters:
        * names: List of item names.
        * isHaveIcon: Whether the items have icons.
        * pixmapPath: List of pixmap paths for icons (if isHaveIcon is True).
        * parent: Parent widget (default is None).
        """
        super(Navigator, self).__init__(parent)
        self._parent = parent
        self.itemNames = names
        self.itemPixmapPath = pixmapPath
        self.isHaveIcon = isHaveIcon
        self.itemSelectedFont = Font(15, ["Helvetica", "微软雅黑", "宋体"], True)
        self.itemNoSelectedFont = Font(15, ["Helvetica", "微软雅黑", "宋体"])
        self.setupUI()

    def updateItemsIcon(self, item: QListWidgetItem, iconPath: str):
        """
        Update the icon of a QListWidgetItem.

        Parameters:
        * item: The QListWidgetItem to update.
        * iconPath: Path to the icon pixmap.
        """
        icon = PixMap(iconPath, QSize(30, 30))
        item.setIcon(icon)

    def updateItemsText(self, item: QListWidgetItem, text: str):
        """
        Update the text of a QListWidgetItem.

        * item: The QListWidgetItem to update.
        * text: The new text.
        """
        item.setText(text)
        item.setFont(self.itemNoSelectedFont)

    def setupUI(self):
        """
        Set up the user interface for the navigator.
        """
        if self.isHaveIcon:
            self.setIconSize(QSize(30, 30))
        for i, itemName in enumerate(self.itemNames):
            item = QListWidgetItem()
            self.addItem(item)
            if self.isHaveIcon:
                self.updateItemsIcon(item, self.itemPixmapPath[i])
            self.updateItemsText(item, itemName)

    def clearText(self):
        """
        Clear the text of all items.
        """
        for i in range(self.count()):
            self.item(i).setText("")

    def recoverText(self):
        """
        Restore the original text of all items.
        """
        for i in range(self.count()):
            self.item(i).setText(self.itemNames[i])

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        """
        Handle the selection change event.

        Parameters:
        * selected: Selected items.
        * deselected: Deselected items.
        """
        if deselected.indexes():
            self.item(deselected.indexes()[0].row()).setFont(
                self.itemNoSelectedFont)
        self.item(selected.indexes()[0].row()).setFont(self.itemSelectedFont)
        # toggle the current widget of the stackwidgets
        # if selected.indexes()[0].row() == 0:
        self._parent.stackWidget.setCurrentIndex(  # type: ignore
                selected.indexes()[0].row())  # type: ignore
