from typing import List, Union, Optional
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QPushButton
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


class ButtonWithPixmap(QPushButton):
    def __init__(self,
                 pixMapPath: str,
                 text: str = "",
                 objectName: str = "",
                 parent: Optional[QWidget] = None):
        super(ButtonWithPixmap, self).__init__(parent)
        if text != "":
            self.setText(text)
        if objectName != "":
            self.setObjectName(objectName)
        self.setIconSize(QSize(50, 30))
        self.setIcon(QPixmap(pixMapPath))
        self.setMaxMinSize()

    def setMaxMinSize(self):
        self.setMaximumSize(QSize(100, 35))
        self.setMinimumSize(QSize(90, 30))


class ButtonWithPixmapChange(QPushButton):
    def __init__(self, text: str, objectName: str, parent: Optional[QWidget] = None):
        """
        Base class for the menu and toolInfo buttons.

        Parameters:
        * parent: The parent widget.
        * text: The text to be displayed on the button.
        """
        super(ButtonWithPixmapChange, self).__init__(parent)
        self.setObjectName(objectName)
        # Set the button's font
        font = Font(15, ["Helvetica", "微软雅黑", "宋体"])
        self.setFont(font)

        # Set the button's general properties
        self.name = text
        self.fixedSize = QSize(170, 50)
        self.setMaximumSize(self.fixedSize)
        self.setStyleSheet("text-align:left")

        # Set the pixmap's general properties
        self.pixMap = QPixmap()
        # Set icon of the button
        self.iconMapSize = QSize(50, 50)
        self.setIconSize(self.iconMapSize)

        # Set size of the button
        self.setFixedSize(self.fixedSize)

    def changeThePixmapAndText(self, pixMapPath: str, text: str, size: QSize):
        """
        Change the pixmap and text of the button, simulating a drawer switch.

        Parameters:
        - pixMapPath: URL path to the pixmap.
        - text: The text to be displayed on the button.
        - size: The desired button size.
        """
        self.pixMap.load(pixMapPath)
        self.setText(text)
        self.setFixedSize(size)
        self.setIcon(self.pixMap)


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


def setQss(style_path) -> str:
    """
    Read and return the content of a QSS style file.

    Parameters:
    * style_path: The path to the QSS style file.

    return: The content of the QSS style file.
    """
    with open(style_path, "r") as style_file:
        Qssfile = style_file.read()
    return Qssfile
