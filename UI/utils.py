from typing import List, Union
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import QSize

# ["Helvetica", "微软雅黑", "宋体"]


class Font(QFont):
    def __init__(self, fontSize: int, fontFamiles: List[str], isBold: bool = False):
        super(Font, self).__init__()
        self.setPointSize(fontSize)
        self.setFamilies(fontFamiles)
        self.setBold(isBold)


class PixMap(QPixmap):
    def __init__(self, iconPath: str, size: QSize):
        super(PixMap, self).__init__()
        self.load(iconPath)


def initialTheLayout(layout: Union[QVBoxLayout, QHBoxLayout],
                     widgets: List[Union[QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem]],
                     stretch: List[int],
                     SpacintAndMarginIf: bool = False):
    """
    Initialize the layout by adding widgets and setting their stretching factors.

    Parameters:
    * layout: The QVBoxLayout or QHBoxLayout to be initialized.
    * widgets: A list of widgets or layouts to be added to the layout.
    * stretch: A list of stretching factors corresponding to each widget/layout.
    """
    for index, item in enumerate(widgets):
        if isinstance(item, QWidget):
            layout.addWidget(item, stretch[index])
        elif isinstance(item, QSpacerItem):
            layout.addItem(item)
        else:
            layout.addLayout(item, stretch[index])
    if SpacintAndMarginIf:
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
