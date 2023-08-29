import sys
from typing import Optional, Callable, Tuple, List, Any
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
    QPushButton,
    QLineEdit
)
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QMouseEvent, QPixmap, QFocusEvent, QCursor
from utils import initialTheLayout, setQss


class DialogButton(QPushButton):
    def __init__(self, text: str):
        super(DialogButton, self).__init__(text)
        self.setMaxMinSize()
        self.setObjectName("DialogButton")

    def setMaxMinSize(self):
        self.setSizePolicy(QSizePolicy.Policy.Minimum,
                           QSizePolicy.Policy.Minimum)
        self.setMaximumSize(QSize(100, 40))
        self.setMinimumSize(QSize(80, 30))


class _CloseButtonWithPixmap(QPushButton):
    def __init__(self, pixmapPath: str, parent: Optional[QWidget] = None):
        """
        Parameters:
        * parent: The parent widget.
        """
        super(_CloseButtonWithPixmap, self).__init__(parent)
        # Set icon of the button
        self.pixmap = QPixmap()
        self.pixmap.load(pixmapPath)
        self.setIconSize(QSize(30, 30))
        self.setFixedSize(QSize(30, 30))
        self.setIcon(self.pixmap)


class _BasicDialog(QDialog):
    def __init__(self,  toolTipStr: str, parent: Optional[QWidget] = None) -> None:
        super(_BasicDialog, self).__init__(parent)
        self.toolTipStr = toolTipStr
        self.setStyleSheet(setQss("./style/Dialog.css"))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setMinMaxSize()
        self.initUI()

    def initUI(self):
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
        self.buttonClose = _CloseButtonWithPixmap("./figs/关闭.svg")
        self.titleFrameLayout = QHBoxLayout()
        self.titleFrameLayoutSpcerItem = QSpacerItem(
            20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        initialTheLayout(self.titleFrameLayout, [
                         self.titleFrameLayoutSpcerItem, self.buttonClose], [5, 1], True)
        self.titleFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.titleFrame.setLayout(self.titleFrameLayout)
        # main Frame Layout
        self.mainFrameLayout = QVBoxLayout()
        self.mainFrameLayoutSpacerItem = QSpacerItem(
            5, 30, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # tool text
        self.toolText = QLabel()
        self.toolText.setObjectName("ToolText")
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
        self.buttonLayout.setContentsMargins(0, 0, 10, 8)

    def setMinMaxSize(self):
        self.setMinimumSize(QSize(300, 300))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moveFlag = True
            self.mouseOriginGlobalPos = QCursor().pos()
            self.windowOriginalPos = self.pos()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moveFlag = False
            self.mouseOriginGlobalPos = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.moveFlag and self.mouseOriginGlobalPos is not None:
            diff = QCursor().pos() - self.mouseOriginGlobalPos
            if diff.manhattanLength() > 5:  # 设置阈值，避免过于频繁的移动
                new_pos = self.windowOriginalPos + diff
                self.move(new_pos)
        super().mouseMoveEvent(event)


class _SelectDeleteBasicDialog(_BasicDialog):
    def __init__(self, toolTipStr: str, opFunc: Callable, opFuncArgs: Tuple, parent: Optional[QWidget] = None) -> None:
        super(_SelectDeleteBasicDialog, self).__init__(toolTipStr, parent)
        self.opFunc = opFunc
        self.opFuncArgs = opFuncArgs
        self.setupUI()
        self.connectSignal()

    def setupUI(self):
        # set main Frame Layout
        initialTheLayout(self.mainFrameLayout, [
                         self.titleFrame,
                         self.toolText,
                         self.mainFrameLayoutSpacerItem,
                         self.buttonLayout],
                         [1, 3, 2, 1],
                         True)
        self.mainFrame.setLayout(self.mainFrameLayout)

    def connectSignal(self):
        self.buttonClose.clicked.connect(self.close)
        self.buttonSure.clicked.connect(self.exectuateOpFunc)
        self.buttonCancel.clicked.connect(self.close)

    def exectuateOpFunc(self):
        self.opFunc(*self.opFuncArgs)
        self.close()


class SelectDialog(_SelectDeleteBasicDialog):
    def __init__(self, toolTipStr: str, opFunc: Callable, opFuncArgs: Tuple, parent: Optional[QWidget] = None) -> None:
        super().__init__(toolTipStr, opFunc, opFuncArgs, parent)


class DeleteDialog(_SelectDeleteBasicDialog):
    def __init__(self, toolTipStr: str, opFunc: Callable, opFuncArgs: Tuple, parent: Optional[QWidget] = None) -> None:
        super().__init__(toolTipStr, opFunc, opFuncArgs, parent)


class _AddEditBasicDialog(_BasicDialog):
    def __init__(self,
                 toolTipStr: str,
                 Func: Callable[[int, Tuple[str]], None],
                 FuncArgs: Tuple[Any],
                 Names: Tuple[str],
                 parent: Optional[QWidget] = None) -> None:

        super().__init__(toolTipStr, parent)
        self.Func = Func
        self.FuncArgs = FuncArgs
        self.Names = Names
        self.initFlags()
        self.setupUI()

    def initFlags(self):
        self.editNums = len(self.Names)

    def setupUI(self):
        self.editsLayout = QVBoxLayout()
        self.editLayoutList = []
        self.editBoxs: List[LineEdit] = []
        for i in range(self.editNums):
            layout = QHBoxLayout()
            name = QLabel(self.Names[i] + ": ")
            name.setObjectName("EditName")
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lineEdit = LineEdit(name, "")
            self.editBoxs.append(lineEdit)
            initialTheLayout(layout, [name, lineEdit], [1, 4], True)
            layout.setSpacing(2)
            self.editLayoutList.append(layout)
        initialTheLayout(self.editsLayout, self.editLayoutList, [
                         1 for _ in range(len(self.editLayoutList))], True)
        self.editsLayout.setSpacing(5)
        self.SpacerItem = QSpacerItem(
            2, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        initialTheLayout(self.mainFrameLayout,
                         [
                             self.titleFrame,
                             self.toolText,
                             self.SpacerItem,
                             self.editsLayout,
                             self.mainFrameLayoutSpacerItem,
                             self.buttonLayout
                         ],
                         [1, 1, 1, 4, 1, 1],
                         True
                         )
        self.mainFrame.setLayout(self.mainFrameLayout)


class AddDialog(_AddEditBasicDialog):
    def __init__(self,
                 toolTipStr: str,
                 Func: Callable[[int, Tuple[str]], None],
                 FuncArgs: Tuple[Any],
                 Names: Tuple[str],
                 parent: Optional[QWidget] = None) -> None:
        super(AddDialog, self).__init__(
            toolTipStr, Func, FuncArgs, Names, parent)
        self.connectSignal()
        self.addPlaceholderText()

    def connectSignal(self):
        self.buttonSure.clicked.connect(self.addData)
        self.buttonCancel.clicked.connect(self.close)
        self.buttonClose.clicked.connect(self.close)

    def addData(self):
        data: List[str] = []
        for edit in self.editBoxs:
            data.append(edit.text())
        self.Func(*self.FuncArgs, tuple(data))
        self.close()

    def addPlaceholderText(self):
        for idx, lineEdit in enumerate(self.editBoxs):
            lineEdit.setPlaceholderText("请输入 " + self.Names[idx])


class EditDialog(_AddEditBasicDialog):
    def __init__(self,
                 toolTipStr: str,
                 Func: Callable[[int, Tuple[str]], None],
                 FuncArgs: Tuple[Any],
                 Names: Tuple[str],
                 initData: Tuple[str],
                 parent: Optional[QWidget] = None) -> None:
        super(EditDialog, self).__init__(
            toolTipStr, Func, FuncArgs, Names, parent)
        self.initData = initData
        self.addPlaceholderText()
        self.connectSignal()

    def addPlaceholderText(self):
        for idx, lineEdit in enumerate(self.editBoxs):
            lineEdit.setPlaceholderText(self.initData[idx])

    def connectSignal(self):
        self.buttonSure.clicked.connect(self.editData)
        self.buttonCancel.clicked.connect(self.close)
        self.buttonClose.clicked.connect(self.close)

    def editData(self):
        data: List[str] = []
        for edit in self.editBoxs:
            if edit.text() != "":
                data.append(edit.text())
            else:
                data.append(edit.placeholderText())
        self.Func(*self.FuncArgs, tuple(data))
        self.close()


class LineEdit(QLineEdit):
    def __init__(self, label: QLabel, placeholderText: str = "", parent: Optional[QWidget] = None):
        super(LineEdit, self).__init__(parent)
        self.label = label
        if placeholderText != "":
            self.setPlaceholderText(placeholderText)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName("Edit")

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.label.setEnabled(False)
        return super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.label.setEnabled(True)
        return super().focusOutEvent(event)


def testFunc(a: int, b: int) -> int:
    result = a + b
    print(result)
    return result


def testEditFunc(a: int, data: Tuple[str]):
    print(a)
    print(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # type: ignore
    # widget = SelectDialog("测试", testFunc, (1, 2))
    widget = AddDialog("测试", testEditFunc, (1, ),
                       tuple(["a", "b", "c", "d", "e"]))
    widget.show()
    app.exec()
