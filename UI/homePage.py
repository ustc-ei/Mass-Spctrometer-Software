import sys
from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QStackedWidget,
    QListView,
    QFrame
)

from PySide6.QtCore import Qt
from navigator import Navigator
from utils import initialTheLayout
from cardFrame import DynamicLayoutApp, CardFrame


class HomePage(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(HomePage, self).__init__(parent)
        self.setupUI()
        self.setStyleSheet(self.readQss("./style/HomePage.css"))
        self.initFlags()

    def readQss(self, style_path) -> str:
        with open(style_path, "r") as style_file:
            Qssfile = style_file.read()
        return Qssfile

    def initFlags(self):
        self.navigator.setCurrentRow(0)

    def setupUI(self):
        self.mainLayout = QVBoxLayout()
        # Navigator Layout
        self.navigator = Navigator(names=['参数展示', '进度展示'], parent=self)
        self.navigator.setObjectName("HomePageNavigator")
        self.navigator.setFlow(QListView.Flow.LeftToRight)
        self.navigator.setFixedWidth(300)
        self.navigator.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.navigator.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.navigatorLayout = QHBoxLayout()
        self.spacerItem1 = QSpacerItem(
            20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.spacerItem2 = QSpacerItem(
            20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        initialTheLayout(self.navigatorLayout, [
                         self.spacerItem1, self.navigator, self.spacerItem2], [2, 1, 2], True)
        self.navigatorLayout.setContentsMargins(5, 2, 5, 2)
        self.navigatorLayout.setSpacing(5)
        self.navigatorFrame = QFrame()
        self.navigatorFrame.setMaximumHeight(50)
        self.navigatorFrame.setObjectName("NavigatorFrame")
        self.navigatorFrame.setLayout(self.navigatorLayout)
        # QStackWidget
        self.stackWidget = QStackedWidget()
        self.cardFrames = self.generateCards(
            500, ["质谱仪参数" for i in range(500)])
        self.parametersWidget = DynamicLayoutApp(self.cardFrames)
        self.stackWidget.addWidget(self.parametersWidget)
        # set main Layout
        initialTheLayout(self.mainLayout, [
                         self.navigatorFrame, self.stackWidget], [1, 5], True)
        self.setLayout(self.mainLayout)

    def generateCards(self, nums: int, parametersTitle: List[str]) -> List[CardFrame]:
        cards: List[CardFrame] = []
        for i in range(nums):
            cards.append(CardFrame(parametersTitle[i], 5))
        return cards


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = HomePage()
    widget.show()
    app.exec()
