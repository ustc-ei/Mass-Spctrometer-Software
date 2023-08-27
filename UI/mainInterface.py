import sys
from typing import Optional, List, Union
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QFrame,
    QSizePolicy
)

from PySide6.QtGui import QPixmap, QResizeEvent, QCloseEvent, QMoveEvent, QMouseEvent
from PySide6.QtCore import QSize, QPoint, Qt
from switchButton import SwitchButton
from toolInforFrame import ToolInfor
from utils import initialTheLayout, Font, QPixmap
from navigator import Navigator
from homePage import HomePage


class ButtonWithThePixmap(QPushButton):
    def __init__(self, text: str, objectName: str, parent: Optional[QWidget] = None):
        """
        Base class for the menu and toolInfo buttons.

        Parameters:
        * parent: The parent widget.
        * text: The text to be displayed on the button.
        """
        super(ButtonWithThePixmap, self).__init__(parent)
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
        self.pixMapSize = QSize(30, 30)

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
        # self.pixMap = self.pixMap.scaled(self.pixMapSize)
        self.setFixedSize(size)
        self.setIcon(self.pixMap)


class ToolInfoButton(ButtonWithThePixmap):
    def __init__(self, text: str, ObjectName: str, parent: Optional[QWidget] = None):
        """
        Tool Information Button class.

        Parameters:
        * parent: The parent widget.
        * text: The text displayed on the button.
        """
        super(ToolInfoButton, self).__init__(text, ObjectName, parent)
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
    def __init__(self, text: str, ObjectName: str, parent: Optional[QWidget] = None):
        """
        Menu Button class.

        Parameters:
        * parent: The parent widget.
        * text: The text displayed on the button.
        """
        super(MenuButton, self).__init__(text, ObjectName, parent)
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


class MainInterface(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        main interface class
        """
        super().__init__(parent)
        self.setWindowTitle("Mass-Spctrometer-Software")
        self.setObjectName("MainInterface")
        self.setMinimumSize(QSize(500, 500))
        self.setupUI()
        self.setStyleSheet(self.setQss("./style/MainInterface.css"))
        self.initFlags()

    def initFlags(self):
        """
        Initialize flags and debounce mechanism
        """
        self.navigatorListWidget.setCurrentRow(0)
        self.menuButton.clicked.connect(self.toggleState)
        self.moveFlag = False

    def setQss(self, style_path) -> str:
        """
        Read and return the content of a QSS style file.

        Parameters:
        * style_path: The path to the QSS style file.

        return: The content of the QSS style file.
        """
        with open(style_path, "r") as style_file:
            Qssfile = style_file.read()
        return Qssfile

    def setupUI(self):
        """
        Initial the UI interface 
        """
        # left layout
        self.leftFrame = QFrame(self)
        self.leftFrame.setObjectName("LeftFrame")
        self.navigatorVboxLayout = QVBoxLayout()
        self.navigatorVboxLayout.maximumSize()
        self.menuButton = MenuButton("菜单栏", "MenuButton", self)
        self.navigatorItemsName = ["首页", "仪器配置", "仪器控制", "数据采集", "定性分析"]
        self.navigatorItemsPixPath = ["./figs/首页.svg", "./figs/仪器配置.svg", "./figs/仪器控制.svg",
                                      "./figs/数据采集.svg", "./figs/定性分析.svg"]
        self.navigatorListWidget = Navigator(
            self.navigatorItemsName, True, self.navigatorItemsPixPath, self)
        self.navigatorListWidget.setObjectName("MainLeftNavigator")
        self.navigatorListWidget.setMaximumWidth(200)
        self.navigatorSpacerItem = QSpacerItem(20, 40)
        self.toolInfoButton = ToolInfoButton("软件相关信息", "ToolInfoButton", self)
        # add the left navigator widgets
        initialTheLayout(self.navigatorVboxLayout, [
            self.menuButton, self.navigatorListWidget, self.navigatorSpacerItem, self.toolInfoButton],
            [1, 5, 1, 1],
            True)
        self.navigatorVboxLayout.setSpacing(3)
        self.navigatorVboxLayout.setContentsMargins(0, 0, 0, 2)
        self.leftFrame.setLayout(self.navigatorVboxLayout)
        # right layout
        self.stackwidgetsLayout = QVBoxLayout()
        self.stackWidget = QStackedWidget()
        self.homePage = HomePage()
        self.stackWidget.addWidget(self.homePage)
        # 1. toggle layout
        self.toggleSwitchLayout = QHBoxLayout()
        self.spacerItem1 = QSpacerItem(40, 5, QSizePolicy.Policy.Expanding)
        self.spacerItem2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum)
        self.styleToggleSwitchButton = SwitchButton()
        # add the right stackWidgets widgtes
        initialTheLayout(self.toggleSwitchLayout, [
            self.spacerItem1, self.styleToggleSwitchButton, self.spacerItem2],
            [3, 1, 1],
            True)
        self.toggleSwitchLayout.setContentsMargins(0, 10, 0, 0)
        # 2. add the stackWidget
        initialTheLayout(self.stackwidgetsLayout, [
            self.toggleSwitchLayout, self.stackWidget],
            [1, 5],
            True)
        # main layout
        self.mainHboxLayout = QHBoxLayout()
        # add the main sub-layouts
        initialTheLayout(self.mainHboxLayout, [
            self.leftFrame, self.stackwidgetsLayout],
            [1, 3],
            True)
        self.setLayout(self.mainHboxLayout)
        # Info Tool Frame
        self.toolInfoFrame = ToolInfor()
        self.toolInfoFrame.isVisibleFlag = False
        self.toolInfoButton.clicked.connect(self.changeToolInfoFrameVisible)

    def changeToolInfoFrameVisible(self):
        """
        change the visibility of the toolInfoFrame
        """
        if self.toolInfoFrame.isVisibleFlag:
            self.toolInfoFrame.setVisible(False)
        else:
            self.toolInfoFrame.setVisible(True)
            pos = self.toolInfoButton.pos() + self.pos() # type: ignore
            size = self.toolInfoButton.size() + QSize(0, -self.toolInfoFrame.widget.height())
            self.toolInfoFrame.move(pos + QPoint(size.width(), size.height()))
        self.toolInfoFrame.isVisibleFlag = not self.toolInfoFrame.isVisibleFlag

    def shinkNavigationBar(self):
        """
        shink the navigationBar
        """
        self.toolInfoButton.changeWithoutText()
        self.navigatorListWidget.clearText()
        self.navigatorListWidget.setFixedWidth(
            self.toolInfoButton.iconMapSize.width())
        self.leftFrame.setFixedWidth(
            self.toolInfoButton.iconMapSize.width())

    def expandNavigationBar(self):
        """
        expand the navigationBar
        """
        self.toolInfoButton.recoverToInitial()
        self.navigatorListWidget.recoverText()
        self.navigatorListWidget.setFixedWidth(
            self.toolInfoButton.fixedSize.width())
        self.leftFrame.setFixedWidth(
            self.toolInfoButton.fixedSize.width())

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Resize event handler.

        This function is automatically called when the widget is resized.

        Parameters:
        * event: The QResizeEvent containing information about the resizing.

        In this function, we adjust the state of the menuButton based on the width of the window.
        """
        if event.size().width() < 600 or event.size().height() < 600:
            if not self.menuButton.pixMapFlag:
                self.menuButton.toggleState(False)
                self.menuButton.pixMapFlag = not self.menuButton.pixMapFlag
                self.shinkNavigationBar()

        elif event.size().width() > 800 or event.size().height() > 800:
            if self.menuButton.pixMapFlag:
                self.menuButton.toggleState(False)
                self.menuButton.pixMapFlag = not self.menuButton.pixMapFlag
                self.expandNavigationBar()
        if self.toolInfoFrame.isVisibleFlag:
            self.toolInfoFrame.isVisibleFlag = False
            self.toolInfoFrame.setVisible(False)

    def toggleState(self):
        """
        Toggle the state of button and listwidget when clicked.
        """
        if self.menuButton.pixMapFlag:
            self.shinkNavigationBar()
        else:
            self.expandNavigationBar()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.toolInfoFrame.close()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moveFlag = True
            self.mouseOriginPoint = QPoint(
                event.position().x(), event.position().y())  # type: ignore
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moveFlag = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        diff = QPoint(event.position().x(), event.position().y()  # type: ignore
                      ) - self.mouseOriginPoint
        if self.moveFlag:
            if diff.manhattanLength() > 5:  # 设置阈值，避免过于频繁的移动
                self.move(self.pos() + diff)  # type: ignore


if __name__ == "__main__":
    app = QApplication(sys.argv)  # type: ignore
    x = MainInterface()
    x.show()
    app.exec()
