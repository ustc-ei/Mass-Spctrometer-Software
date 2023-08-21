import sys
from typing import Optional, List
from enum import Enum
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPaintEvent,
    QPen,
    QFont
)
from PySide6.QtCore import QRect, Qt, QSize, QPoint


class Font(QFont):
    def __init__(self, fontSize: int, fontFamiles: List[str], boldIf: bool = True):
        super(Font, self).__init__()
        self.setPointSize(fontSize)
        self.setFamilies(fontFamiles)
        self.setBold(boldIf)


class SwitchButton(QPushButton):
    def __init__(self, parent: Optional[QWidget] = None):
        super(SwitchButton, self).__init__(parent)
        self.setColor()
        self.initPainterFlags()
        self.initPaintRectAndCircle()
        self.setPoint()
        self.clicked.connect(self.triggleSwitch)



    def initPaintRectAndCircle(self):
        self.setFixedSize(125, 50)
        self.paintRect = QRect(0, 0, self.width(), self.height())
        self.circleSize = QSize(int(0.95*self.height()),
                                int(0.95*self.height()))
        textSize = QSize(40, (self.height() - 5) // 2)
        # print(textSize)
        textOnPoint = QPoint(20, 10)
        textOffPoint = QPoint(
            self.width() - textSize.width() - 20, 10)
        self.switchOntextRect = QRect(
            textOnPoint.x(), textOnPoint.y(), textSize.width(), textSize.height())
        self.switchOfftextRect = QRect(
            textOffPoint.x(), textOffPoint.y(), textSize.width(), textSize.height())
        self.textAlignment = Qt.AlignmentFlag.AlignLeft

    def initPainterFlags(self):
        self.originIsSwitch = False
        self.isSwitchOn = False

    def setColor(self):
        self.switchOffRectPenColor = QColor(221, 221, 221)
        self.switchOffRectBrushColor = QColor(255, 255, 255)
        self.switchOffCircleBrushColor = QColor(221, 221, 221)
        self.switchOnRectPenColor = QColor(140, 225, 149)
        self.switchOnRectBrushColor = QColor(255, 255, 255)
        self.switchOnCircleBrushColor = QColor(140, 225, 149)
        self.textColor = QColor(189, 221, 212)

    def setPoint(self):
        width = 1
        self.switchOffCirclePoint = QPoint(
            width, int(0.05 * self.height() // 2))
        self.switchOnCirclePoint = QPoint(
            self.width() - width - self.circleSize.width(), int(0.05*self.height()//2))

    def paintEvent(self, event: QPaintEvent) -> None:
        # set painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        # paint rect
        self.paintSwitchOffRect(painter)
        if self.isSwitchOn:
            self.paintSwitchOnRect(painter)
        painter.drawRoundedRect(
            self.paintRect, self.height() // 2, self.height() // 2)
        # paint circle
        self.paintSwitchOffCircle(painter)
        if self.isSwitchOn:
            self.paintSwitchOnCircle(painter)
        if not self.isSwitchOn:
            painter.drawEllipse(self.switchOffCirclePoint.x(), self.switchOffCirclePoint.y(
            ), self.circleSize.width(), self.circleSize.height())
        else:
            painter.drawEllipse(self.switchOnCirclePoint.x(), self.switchOnCirclePoint.y(
            ), self.circleSize.width(), self.circleSize.height())
        # paint text
        painter.setPen(QColor(189, 221, 212))
        painter.setFont(Font(14, ["Helvetica", "微软雅黑", "宋体"], True))
        if self.isSwitchOn:
            painter.drawText(self.switchOntextRect, "关闭", self.textAlignment)
        else:
            painter.drawText(self.switchOfftextRect, "开启", self.textAlignment)

    def paintSwitchOffRect(self, painter: QPainter):
        painter.setBrush(self.switchOffRectBrushColor)
        painter.setPen(Qt.PenStyle.NoPen)

    def paintSwitchOnRect(self, painter: QPainter):
        painter.setBrush(self.switchOnRectBrushColor)
        painter.setPen(Qt.PenStyle.NoPen)

    def paintSwitchOffCircle(self, painter: QPainter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.switchOffCircleBrushColor)

    def paintSwitchOnCircle(self, painter: QPainter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.switchOnCircleBrushColor)

    def enterEvent(self, event):
        self.originIsSwitch = self.isSwitchOn
        self.isSwitchOn = not self.isSwitchOn
        self.update()

    def leaveEvent(self, event):
        if self.isSwitchOn != self.originIsSwitch:
            self.isSwitchOn = not self.isSwitchOn
            self.originIsSwitch = self.originIsSwitch
        self.update()

    def paintText(self, painter: QPainter):
        painter.setPen(QPen(self.textColor))

    def triggleSwitch(self, event):
        self.isSwitchOn = not self.originIsSwitch
        self.originIsSwitch = self.isSwitchOn
        # print(self.isSwitchOn)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    vbox = QVBoxLayout()
    btn = SwitchButton()
    vbox.addWidget(btn)
    widget.setLayout(vbox)
    widget.show()
    app.exec()
