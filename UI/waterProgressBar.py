from typing import Optional
from time import sleep
import math
import random
from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QBrush,
    QColor,
    QPen,
    QPainterPath,
    QFontMetrics,
    QCloseEvent
)
from PySide6.QtCore import (
    Qt,
    QSize,
    QThread,
    Signal,
    QTimer,
    QPoint,
    QRect
)
from utils import Font


class UpdateWaterThread(QThread):
    signal = Signal(float)

    def __init__(self, beginVlue: float, endValue: float, parent: Optional[QWidget] = None) -> None:
        super(UpdateWaterThread, self).__init__(parent)
        self.beginValue = beginVlue
        self.endValue = endValue
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.beginValue <= self.endValue:
            self.beginValue += random.random()
            self.signal.emit(self.beginValue)
            sleep(0.1)


class WaterProgressBar(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(WaterProgressBar, self).__init__(parent)
        self.initFlags()
        self.initThreadTimer()
        self.setMinMaxSize()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.destoryThread()

    def setMinMaxSize(self):
        self.setMinimumSize(QSize(200, 200))

    def destoryThread(self):
        self.valueThread.quit()
        self.valueThread.wait()

    # 更新水波偏移的 offset
    def updateOffset(self, offset: float):
        self.offset = offset
        self.update()

    # 更新 value
    def updateValue(self, value: float):
        self.value = value
        self.update()

    # 初始化 thread 和 timer
    def initThreadTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(
            lambda: self.updateOffset(self.offset + 0.6))
        self.timer.start(200)
        self.valueThread = UpdateWaterThread(0, 100)
        self.valueThread.signal.connect(self.updateValue)
        self.valueThread.start()

    # 初始化一些设置
    # 1. 画笔和填充色
    # 2. 水波纹三角函数的振幅, 初始偏移量
    # 3. 文本的 font
    # 4. 初始化一些数学计算的函数、常量
    def initFlags(self):
        # 圆形内容设置
        self.borderWidth = 4
        self.backgroundBrush = QBrush(QColor(255, 255, 255))
        self.borderPen = QPen(QColor(221, 221, 221))
        self.valueBrush = QBrush(QColor(135, 206, 235))
        # 水波纹设置
        self.valueWater1Color = QColor(135, 206, 235, 100)
        self.valueWater2Color = QColor(135, 206, 235, 200)
        self.borderPen.setWidth(self.borderWidth)
        self.PI = math.pi
        self.sin = math.sin
        self.value = 0
        self.maxValue = 100
        self.minValue = 0
        self.waterHeight = 10
        self.offset = 1
        # 文本设置
        self.valueFont = Font(20, ["Helvetica", "微软雅黑", "宋体"], True)
        self.valuefontMetrics = QFontMetrics(self.valueFont)
        self.valuePen = QPen(QColor(221, 221, 221))

    def drawValue(self, painter: QPainter):
        text = "{:.2f}%".format(
            (self.value / (self.maxValue - self.minValue) * 100))
        textFontRect = self.valuefontMetrics.tightBoundingRect(text)
        textWidth, textHeight = textFontRect.width(), textFontRect.height()
        textDrawTopLeftPoint = QPoint(
            self.width() // 2, self.height() // 2) + QPoint(-textWidth // 2, -textHeight // 2)
        textDrawRect = QRect(textDrawTopLeftPoint,
                             QSize(textWidth, textHeight) + QSize(20, 20))
        painter.save()
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(self.valueFont)
        painter.drawText(textDrawRect, text, Qt.AlignmentFlag.AlignLeft)
        painter.restore()

    def drawBackground(self, painter: QPainter):
        width = self.width()
        height = self.height()
        # 确定圆的直径
        side = min(width, height) - 2 * self.borderWidth
        # 确定圆内切正方形的左上角的相对坐标
        startX = (width - side) // 2
        startY = (height - side) // 2
        painter.save()
        painter.setBrush(self.backgroundBrush)
        if self.borderWidth == 0:
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            painter.setPen(self.borderPen)
        painter.drawEllipse(startX, startY, side, side)
        painter.restore()

    def drawProcess(self, painter: QPainter):
        width = self.width()
        height = self.height()
        # 确定圆的直径
        side = min(width, height) - 2 * self.borderWidth
        # 确定圆内切正方形框的终点与起点位
        startX = (width - side) // 2
        startY = (height - side) // 2
        endX = startX + side
        endY = startY + side
        # 确定百分比
        percent = (self.value * 1.0) / (self.maxValue - self.minValue)
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.valueBrush)
        # 添加圆形闭合曲线, 后续可以和波纹曲线进行相交处理, 确定相交后的填充色
        circlePath = QPainterPath()
        circlePath.addEllipse(startX, startY, side, side)
        # 绘制水波纹
        """
        使用 y = Asin(wx + phi) + k 模拟水波纹
        A 振幅可作为水柱的高度
        w 越大, 水波越密集
        k 标识 y 轴偏移量, 可以理解为进度, 取值是百分比
        """
        # 正弦函数波
        # 周期可以自己拟定
        w = 2 * self.PI / (endX - startX)
        A = self.waterHeight
        k = endY * (1.0 - percent)
        water1 = QPainterPath()
        water2 = QPainterPath()
        water1.moveTo(startX, endY)
        water2.moveTo(startX, endY)
        i = startX
        while i < endX:
            waterY1 = A * self.sin(w * (i - startX) + self.offset) + k
            waterY2 = A * self.sin(w * (i - startX) +
                                   self.offset + (endX / 2 * w)) + k
            water1.lineTo(i, waterY1)
            water2.lineTo(i, waterY2)
            i += 1
        if self.value == self.minValue:
            waterY1 = endY
        if self.value == self.maxValue:
            waterY1 = startY
        water1.lineTo(endX, endY)
        water2.lineTo(endX, endY)
        path = QPainterPath()
        path = circlePath.intersected(water1)
        painter.setBrush(self.valueWater1Color)
        painter.drawPath(path)
        path = circlePath.intersected(water2)
        painter.setBrush(self.valueWater2Color)
        painter.drawPath(path)
        painter.restore()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        self.drawBackground(painter)
        self.drawProcess(painter)
        self.drawValue(painter)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = QWidget()
    layout = QGridLayout()
    widget.setLayout(layout)
    w = WaterProgressBar()
    layout.addWidget(w)
    widget.show()
    app.exec()
