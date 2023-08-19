from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QLabel
from PySide6.QtCore import Qt


class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框窗口
        self.setWindowTitle("Custom Window")

        # 创建一个 QLabel，模拟窗口内容
        label = QLabel("Hello, World!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

        # 创建阴影效果，实现圆角
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # 阴影模糊半径
        shadow.setColor(Qt.black)  # 阴影颜色
        label.setGraphicsEffect(shadow)


if __name__ == "__main__":
    app = QApplication([])
    window = CustomWindow()
    window.show()
    app.exec()
