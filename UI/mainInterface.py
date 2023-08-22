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
    QFrame,
    QListWidgetItem,
    QSizePolicy
)

from PySide6.QtGui import QPixmap, QFont, QResizeEvent, QCloseEvent, QMoveEvent
from PySide6.QtCore import QSize, QPoint, QItemSelection
from switchButton import SwitchButton
from toolInforFrame import ToolInfor


class PixMap(QPixmap):
    def __init__(self, iconPath: str, size: QSize):
        super(PixMap, self).__init__()
        self.load(iconPath)


class Font(QFont):
    def __init__(self, fontSize: int, fontFamiles: List[str], isBold: bool = False):
        super(Font, self).__init__()
        self.setPointSize(fontSize)
        self.setFamilies(fontFamiles)
        self.setBold(isBold)


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
        self.setObjectName("MainInterface")
        self.setMinimumSize(QSize(500, 500))
        self.setQss("./style/MainInterface.css")
        self.setupUI()
        self.initFlags()

    def initFlags(self):
        self.menuButton.clicked.connect(self.toggleState)
        self.navigatorListWidget.setCurrentRow(0)
        self.moveFlag = False

    def initialTheLayout(self, layout: Union[QVBoxLayout, QHBoxLayout],
                         widgets: List[Union[QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem]],
                         stretch: List[int],
                         SpacintAndMarginIf: bool):
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

    def setQss(self, style_path):
        with open(style_path, "r") as style_file:
            self.setStyleSheet(style_file.read())

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
        self.navigatorListWidget = Navigator(self)
        self.navigatorSpacerItem = QSpacerItem(20, 40)
        self.toolInfoButton = ToolInfoButton("软件相关信息", "ToolInfoButton", self)
        # add the left navigator widgets
        self.initialTheLayout(self.navigatorVboxLayout, [
                              self.menuButton, self.navigatorListWidget, self.navigatorSpacerItem, self.toolInfoButton],
                              [1, 5, 1, 1],
                              True)
        self.navigatorVboxLayout.setSpacing(3)
        self.navigatorVboxLayout.setContentsMargins(0, 0, 0, 2)
        self.leftFrame.setLayout(self.navigatorVboxLayout)
        # right layout
        self.stackwidgetsLayout = QVBoxLayout()
        self.stackwidget = QStackedWidget()
        # 1. toggle layout
        self.toggleSwitchLayout = QHBoxLayout()
        self.spacerItem1 = QSpacerItem(40, 5, QSizePolicy.Policy.Expanding)
        self.spacerItem2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum)
        self.styleToggleSwitchButton = SwitchButton()
        # add the right stackWidgets widgtes
        self.initialTheLayout(self.toggleSwitchLayout, [
                              self.spacerItem1, self.styleToggleSwitchButton, self.spacerItem2],
                              [3, 1, 1],
                              True)
        self.toggleSwitchLayout.setContentsMargins(0, 10, 0, 0)
        # 2. add the stackWidget
        self.initialTheLayout(self.stackwidgetsLayout, [
                              self.toggleSwitchLayout, self.stackwidget],
                              [1, 5],
                              True)
        # main layout
        self.mainHboxLayout = QHBoxLayout()
        # add the main sub-layouts
        self.initialTheLayout(self.mainHboxLayout, [
                              self.leftFrame, self.stackwidgetsLayout],
                              [1, 3],
                              True)
        self.setLayout(self.mainHboxLayout)
        # Info Tool Frame
        self.toolInfoFrame = ToolInfor()
        self.toolInfoFrame.isVisibleFlag = False
        self.toolInfoButton.clicked.connect(self.changeToolInfoFrameVisible)

    def changeToolInfoFrameVisible(self):
        if self.toolInfoFrame.isVisibleFlag:
            self.toolInfoFrame.setVisible(False)
        else:
            self.toolInfoFrame.setVisible(True)
            pos = self.toolInfoButton.pos() + self.pos()
            size = self.toolInfoButton.size() + QSize(0, -self.toolInfoFrame.widget.height())
            self.toolInfoFrame.move(pos + QPoint(size.width(), size.height()))
        self.toolInfoFrame.isVisibleFlag = not self.toolInfoFrame.isVisibleFlag

    def shinkNavigationBar(self):
        self.toolInfoButton.changeWithoutText()
        self.navigatorListWidget.clearText()
        self.navigatorListWidget.setFixedWidth(
            self.toolInfoButton.iconMapSize.width())
        self.leftFrame.setFixedWidth(
            self.toolInfoButton.iconMapSize.width())

    def expandNavigationBar(self):
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

    def moveEvent(self, event: QMoveEvent) -> None:
        if self.toolInfoFrame.isVisibleFlag:
            self.toolInfoFrame.isVisibleFlag = False
            self.toolInfoFrame.setVisible(False)
    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     if event.buttons() == Qt.MouseButton.LeftButton:
    #         self.moveFlag = True
    #         self.mouseOriginPoint = event.pos()
    #         self.originPoint = self.pos()

    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     if event.buttons() == Qt.MouseButton.LeftButton:
    #         self.moveFlag = False

    # def mouseMoveEvent(self, event: QMouseEvent) -> None:
    #     diff = event.pos() - self.mouseOriginPoint
    #     if self.moveFlag:
    #         if diff.manhattanLength() > 5:  # 设置阈值，避免过于频繁的移动
    #             self.move(self.pos() + diff)
    #             if self.toolInfoFrame.isVisibleFlag:
    #                 self.toolInfoFrame.move(
    #                     self.toolInfoFrame.pos() + diff)


class Navigator(QListWidget):
    def __init__(self, parent: Optional[Union[QWidget, MainInterface]] = None) -> None:
        super(Navigator, self).__init__(parent)
        self._parent = parent
        self.setMaximumWidth(200)
        self.itemNames = ["首页", "仪器配置", "仪器控制", "数据采集", "定性分析"]
        self.itemFigs = ["./figs/首页.svg", "./figs/仪器配置.svg", "./figs/仪器控制.svg",
                         "./figs/数据采集.svg", "./figs/定性分析.svg"]
        self.itemSelectedFont = Font(15, ["Helvetica", "微软雅黑", "宋体"], True)
        self.itemNoSelectedFont = Font(15, ["Helvetica", "微软雅黑", "宋体"])
        self.setupUI()

    def setupUI(self):
        for index, itemName in enumerate(self.itemNames):
            self.setIconSize(QSize(30, 30))
            icon = PixMap(self.itemFigs[index], QSize(30, 30))
            item = QListWidgetItem()
            item.setIcon(icon)
            item.setText(itemName)
            item.setFont(self.itemNoSelectedFont)
            self.addItem(item)

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
        # typing
        # self._parent.stackwidget.setCurrentWidget(  # type: ignore
        #     self.item(selected.indexes()[0].row()))  # type: ignore


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = MainInterface()
    x.show()
    sys.exit(app.exec())
