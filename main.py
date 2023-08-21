from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QPainter, QColor, QPaintEvent
import sys


class SwitchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 50)
        self.isSwitchOn = False
        self.originIsSwitch = False

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(221, 221, 221))
        painter.setBrush(QColor(255, 255, 255))

        if self.isSwitchOn:
            painter.setPen(QColor(140, 225, 149))
            painter.setBrush(QColor(255, 255, 255))

        rect = event.rect()
        painter.drawRoundedRect(rect, self.height() // 2, self.height() // 2)

    def enterEvent(self, event):
        self.originIsSwitch = self.isSwitchOn
        self.isSwitchOn = not self.isSwitchOn
        self.update()

    def leaveEvent(self, event):
        if self.isSwitchOn != self.originIsSwitch:
            self.isSwitchOn = not self.isSwitchOn
            self.originIsSwitch = self.originIsSwitch
        self.update()

    def mousePressEvent(self, event):
        self.isSwitchOn = not self.originIsSwitch
        self.originIsSwitch = self.isSwitchOn
        print(self.isSwitchOn)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    vbox = QVBoxLayout()
    btn = SwitchButton()
    vbox.addWidget(btn)
    widget.setLayout(vbox)
    widget.show()
    sys.exit(app.exec())
