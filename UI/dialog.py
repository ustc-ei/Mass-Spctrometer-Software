import sys
from typing import Optional, Callable, Tuple, Any
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QWidget,
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QPushButton
)
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QMouseEvent, QPixmap
from utils import initialTheLayout


class DialogButton(QPushButton):
    def __init__(self, text: str):
        super(DialogButton, self).__init__(text)
        self.setMaxMinSize()
        self.setObjectName("DialogButton")

    def setMaxMinSize(self):
        self.setSizePolicy(QSizePolicy.Policy.Minimum,
                           QSizePolicy.Policy.Minimum)
        self.setMaximumSize(QSize(100, 30))
        self.setMinimumSize(QSize(80, 20))


class CloseButtonWithPixmap(QPushButton):
    def __init__(self, pixmapPath: str, parent: Optional[QWidget] = None):
        """
        Parameters:
        * parent: The parent widget.
        """
        super(CloseButtonWithPixmap, self).__init__(parent)
        # Set icon of the button
        self.pixmap = QPixmap()
        self.pixmap.load(pixmapPath)
        self.setIconSize(QSize(30, 30))
        self.setFixedSize(QSize(30, 30))
        self.setIcon(self.pixmap)


class BasicDialog(QDialog):
    def __init__(self,  toolTipStr: str, opFunc: Callable, opFuncArgs: Tuple, parent: Optional[QWidget] = None) -> None:
        super(BasicDialog, self).__init__(parent)
        self.toolTipStr = toolTipStr
        self.opFunc = opFunc
        self.opFuncArgs = opFuncArgs
        self.setupUI()
        self.setStyleSheet(self.setQss("./style/Dialog.css"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setMinMaxSize()
        self.connectSignal()

    def setupUI(self):
        # main frame
        self.mainFrame = QFrame()
        self.mainFrame.setObjectName("DialogMain")
        self.mainLayout = QHBoxLayout()
        initialTheLayout(self.mainLayout, [self.mainFrame], [1], True)
        self.setLayout(self.mainLayout)
        # title Frame
        self.titleFrame = QFrame()
        self.titleFrame.setMaximumHeight(30)
        self.titleFrame.setObjectName("DialogTitle")
        self.closeButton = CloseButtonWithPixmap("./figs/关闭_close.svg")
        self.titleFrameLayout = QHBoxLayout()
        self.titleFrameLayoutSpcerItem = QSpacerItem(
            20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        initialTheLayout(self.titleFrameLayout, [
                         self.titleFrameLayoutSpcerItem, self.closeButton], [5, 1], True)
        self.titleFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.titleFrame.setLayout(self.titleFrameLayout)
        # center text
        self.toolText = QLabel()
        self.toolText.setText(self.toolTipStr)
        self.toolText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # buttons
        self.buttonLayout = QHBoxLayout()
        self.buttonsSpacerItem = QSpacerItem(
            20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonSure = DialogButton("确定")
        self.buttonCancel = DialogButton("取消")
        initialTheLayout(self.buttonLayout, [
                         self.buttonsSpacerItem, self.buttonSure, self.buttonCancel], [2, 1, 1], True)
        self.buttonLayout.setSpacing(5)
        self.buttonLayout.setContentsMargins(0, 0, 10, 0)
        # set main Frame Layout
        self.mainFrameLayout = QVBoxLayout()
        self.mainFrameLayoutSpacerItem = QSpacerItem(
            5, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        initialTheLayout(self.mainFrameLayout, [
                         self.titleFrame,
                         self.toolText,
                         self.mainFrameLayoutSpacerItem,
                         self.buttonLayout],
                         [1, 3, 2, 1],
                         True)
        self.mainFrame.setLayout(self.mainFrameLayout)

    def connectSignal(self):
        self.closeButton.clicked.connect(self.close)
        self.buttonSure.clicked.connect(self.exectuateOpFunc)
        self.buttonCancel.clicked.connect(self.close)

    def exectuateOpFunc(self):
        self.opFunc(*self.opFuncArgs)
        self.close()

    def setMinMaxSize(self):
        self.setMinimumSize(QSize(300, 300))

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


def testFunc(a: int, b: int) -> int:
    result = a + b
    print(result)
    return result


if __name__ == "__main__":
    app = QApplication(sys.argv)  # type: ignore
    widget = BasicDialog("测试", testFunc, (1, 2))
    widget.show()
    app.exec()
