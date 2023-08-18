import sys
from typing import Optional, List, Union
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QListWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QFrame
)

from PySide6.QtGui import QPixmap, QFont, QResizeEvent
from PySide6.QtCore import QSize


class ButtonWithThePixmap(QPushButton):
    def __init__(self, text: str, parent: Optional[QWidget] = None):
        """
        Base class for the menu and toolInfo buttons.

        Parameters:
        * parent: The parent widget.
        * text: The text to be displayed on the button.
        """
        super(ButtonWithThePixmap, self).__init__(parent)
        # Set the button's font
        font = QFont()
        font.setPointSize(15)
        font.setFamilies(["Helvetica", "微软雅黑", "宋体"])
        self.setFont(font)

        # Set the button's general properties
        self.name = text
        self.fixedSize = QSize(200, 50)
        self.setMaximumSize(self.fixedSize)
        self.setStyleSheet("text-align:left")

        # Set the pixmap's general properties
        self.pixMap = QPixmap()
        self.pixMapSize = QSize(30, 30)

        # Set icon of the button
        self.iconMapSize = QSize(50, 50)
        self.setIconSize(self.pixMapSize)

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
        self.pixMap = self.pixMap.scaled(self.pixMapSize)
        self.setFixedSize(size)
        self.setIcon(self.pixMap)


class ToolInfoButton(ButtonWithThePixmap):
    def __init__(self, text: str, parent: Optional[QWidget] = None):
        """
        Tool Information Button class.

        Parameters:
        * parent: The parent widget.
        * text: The text displayed on the button.
        """
        super(ToolInfoButton, self).__init__(text, parent)
        self.pixMapPath = "./figs/信息.svg"
        self.changeThePixmapAndText(self.pixMapPath, self.name, self.fixedSize)

    def recoverToInitial(self):
        """
        Recover to the initial state
        """
        self.changeThePixmapAndText(self.pixMapPath, self.name, self.fixedSize)

    def changeWithoutText(self):
        """
        clear the text on the button
        """
        self.changeThePixmapAndText(self.pixMapPath, "", self.iconMapSize)


class MenuButton(ButtonWithThePixmap):
    def __init__(self, text: str, parent: Optional[QWidget] = None):
        """
        Menu Button class.

        Parameters:
        * parent: The parent widget.
        * text: The text displayed on the button.
        """
        super(MenuButton, self).__init__(text, parent)
        self.pixMapsPath = ["./figs/菜单收起.svg",
                            "./figs/菜单展开.svg"]
        self.pixMapFlag = False
        self.changeThePixmapAndText(
            self.pixMapsPath[0], self.name, self.fixedSize)
        self.clicked.connect(lambda: self.toggleState())

    def toggleState(self, clicked: bool = True):
        """
        Toggle the button's state when clicked.

        The button is initially configured with the pixmap on the left side and the text on the right side.
        When the button is clicked, the pixmap changes, and the text is cleared.
        Clicking the button again will revert it to its original state.

        This function is used to simulate a toggle switch, where the button's appearance alternates between two states
        as a visual indicator of its state change.
        """
        if not self.pixMapFlag:
            self.changeThePixmapAndText(
                self.pixMapsPath[1], "", self.iconMapSize)
        else:
            self.changeThePixmapAndText(
                self.pixMapsPath[0], self.name, self.fixedSize)
        if clicked:
            self.pixMapFlag = not self.pixMapFlag


class Navigator(QListWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(Navigator, self).__init__(parent)
        self.setMaximumWidth(200)


class MainInterface(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        main interface class
        """
        super().__init__(parent)
        self.setupUI()
        self.menuButton.clicked.connect(self.toggleState)

    def initialTheLayout(self, layout: Union[QVBoxLayout, QHBoxLayout], widgets: List[Union[QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem]], stretch: List[int]):
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

    def setupUI(self):
        """
        Initial the UI interface 
        """
        # left layout
        self.navigatorVboxLayout = QVBoxLayout()
        self.navigatorVboxLayout.maximumSize()
        self.menuButton = MenuButton("菜单栏", self)
        self.navigatorListWidget = Navigator(self)
        self.navigatorSpacerItem = QSpacerItem(20, 40)
        self.toolInfoButton = ToolInfoButton("软件相关信息", self)
        # add the left navigator widgets
        self.initialTheLayout(self.navigatorVboxLayout, [
                              self.menuButton, self.navigatorListWidget, self.navigatorSpacerItem, self.toolInfoButton], [1, 5, 1, 1])
        # right layout
        self.stackwidgetsLayout = QVBoxLayout()
        self.stackwidget = QStackedWidget()
        # 1. toggle layout
        self.toggleSwitchLayout = QHBoxLayout()
        self.toggleFrame = QFrame()
        self.styleToggleSwitchButton = QPushButton()
        # add the right stackWidgets widgtes
        self.initialTheLayout(self.toggleSwitchLayout, [
                              self.toggleFrame, self.styleToggleSwitchButton], [3, 1])
        # 2. add the stackWidget
        self.initialTheLayout(self.stackwidgetsLayout, [
                              self.toggleSwitchLayout, self.stackwidget], [1, 5])
        # main layout
        self.mainHboxLayout = QHBoxLayout()
        # add the main sub-layouts
        self.initialTheLayout(self.mainHboxLayout, [
                              self.navigatorVboxLayout, self.stackwidgetsLayout], [1, 3])
        self.setLayout(self.mainHboxLayout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Resize event handler.

        This function is automatically called when the widget is resized.

        Parameters:
        * event: The QResizeEvent containing information about the resizing.

        In this function, we adjust the state of the menuButton based on the width of the window.
        """
        if event.size().width() < 600:
            if not self.menuButton.pixMapFlag:
                self.menuButton.toggleState(False)
                self.toolInfoButton.changeWithoutText()
                self.menuButton.pixMapFlag = not self.menuButton.pixMapFlag
                self.navigatorListWidget.setFixedWidth(
                    self.toolInfoButton.iconMapSize.width())

        elif event.size().width() > 1000:
            if self.menuButton.pixMapFlag:
                self.menuButton.toggleState(False)
                self.toolInfoButton.recoverToInitial()
                self.menuButton.pixMapFlag = not self.menuButton.pixMapFlag
                self.navigatorListWidget.setFixedWidth(
                    self.toolInfoButton.fixedSize.width())

    def toggleState(self):
        """
        Toggle the state of button and listwidget when clicked.
        """
        if self.menuButton.pixMapFlag:
            self.toolInfoButton.changeWithoutText()
            self.navigatorListWidget.setFixedWidth(
                self.toolInfoButton.iconMapSize.width())
        else:
            self.toolInfoButton.recoverToInitial()
            self.navigatorListWidget.setFixedWidth(
                self.toolInfoButton.fixedSize.width())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = MainInterface()
    x.show()
    sys.exit(app.exec())
