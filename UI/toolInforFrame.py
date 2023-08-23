from typing import Optional, Union, List
import sys
from PySide6.QtWidgets import (
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QApplication,
)
from PySide6.QtGui import QPixmap, QPainterPath, QPainter, QHideEvent
from PySide6.QtCore import Qt, QSize, QPoint
from utils import *


class CircularLabel(QLabel):
    def __init__(self, pixmap_path):
        """
        圆形头像显示 label
        """
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(200, 200)
        self.pixmaps = QPixmap(pixmap_path)
        self.circular_pixmap = self.create_circular_pixmap(self.pixmaps)
        self.setPixmap(self.circular_pixmap)

    def create_circular_pixmap(self, pixmap):
        size = self.size()
        result = QPixmap(size)
        result.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        center = QPoint(size.width() // 2, size.height() // 2)
        radius = min(size.width(), size.height()) // 2
        path.addEllipse(center, radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap.scaled(
            size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        painter.end()
        return result


class Label(QLabel):
    def __init__(self, font: Optional[Font] = None, parent: Optional[QWidget] = None):
        super(Label, self).__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if font is not None:
            self.setFont(font)


class ToolInfor(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(ToolInfor, self).__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.NoDropShadowWindowHint |
                            Qt.WindowType.Popup)
        self.initFlags()
        self.setupUI()
        self.setObjectName("InfoToolTip")
        self.setFixedSize(QSize(400, 400))

    def initFlags(self):
        self.isVisibleFlag = False

    def setupUI(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.widget = QWidget()
        self.widget.setStyleSheet(
            "background-color: white;border-radius: 40px")
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # title
        self.titleFont = Font(20, ["Helvetica", "微软雅黑", "宋体"])
        self.title = Label(self.titleFont)
        self.title.setText("质谱仪软件V1.0")
        # pic
        self.authorPicHBoxLayout = QHBoxLayout()
        self.authorPic = CircularLabel("./figs/author.png")
        self.authorPicHBoxLayout.addWidget(self.authorPic)
        # author
        self.authorFont = Font(12, ["Helvetica", "微软雅黑", "宋体"])
        self.author = Label(self.authorFont)
        self.author.setText("作者: PengXiong, ZhengJin, ZiYeFeng")
        # statement
        self.statementLayout = QHBoxLayout()
        self.statementLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statementFont = Font(12, ["Helvetica", "微软雅黑", "宋体"])
        self.statement1 = Label(self.statementFont)
        self.statement1.setText("该软件全部开源, GitHub 地址为 ")
        self.statement2 = Label(self.statementFont)
        self.statement2.setOpenExternalLinks(True)
        self.statement2.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction)
        self.statement2.setText(
            '<a href="https://github.com/ustc-ei/Mass-Spctrometer-Software">GitHub Repository</a>')
        self.statementLayout.addWidget(self.statement1)
        self.statementLayout.addWidget(self.statement2)
        # add the widgets to the layout
        initialTheLayout(self.vboxlayout, [
                         self.title, self.authorPicHBoxLayout, self.author, self.statementLayout], [2, 2, 1, 1])
        # widget layout
        self.widget.setLayout(self.vboxlayout)
        # main layout
        self.mainLayout = QHBoxLayout()
        initialTheLayout(self.mainLayout, [self.widget], [1], True)
        self.setLayout(self.mainLayout)

    # def leaveEvent(self, event: QEvent) -> None:
    #     if self.isVisibleFlag:
    #         self.isVisibleFlag = False
    #     self.setVisible(self.isVisibleFlag)

    def hideEvent(self, event: QHideEvent) -> None:
        if not self.isVisibleFlag:
            self.isVisibleFlag = True

    # def focusOutEvent(self, event: QFocusEvent) -> None:
    #     if self.isVisibleFlag:
    #         self.isVisibleFlag = False
    #     self.setVisible(self.isVisibleFlag)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = ToolInfor(None)
    x.show()
    sys.exit(app.exec())
