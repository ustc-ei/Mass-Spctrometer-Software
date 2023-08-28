import sys
from typing import Optional, List, Sequence
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
    QFrame
)
from tableWidget import TableWidgetWithButtons
from utils import ButtonWithPixmap, initialTheLayout, setQss


class ComboBox(QComboBox):
    def __init__(self, text: Sequence[str], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.text = text
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.initSelectData()
        self.setMaxMinSize()

    def initSelectData(self):
        self.addItems(self.text)

    def setMaxMinSize(self):
        self.setMaximumSize(QSize(120, 35))
        self.setMinimumSize(QSize(100, 35))


class InstrumentSetting(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(InstrumentSetting, self).__init__(parent)
        self.initFlags()
        self.setupUI()
        self.initState()
        self.connectSignal()
        self.setStyleSheet(setQss("./style/InstrumentSetting.css"))

    def connectSignal(self):
        self.addButton.clicked.connect(self.addData)
        self.upSortButton.clicked.connect(self.sortDownUp)
        self.downSortButton.clicked.connect(self.sortUpDown)

    def initFlags(self):
        self.changeStateWidgetList: List[QWidget] = []

    def initState(self):
        for widget in self.changeStateWidgetList:
            widget.setEnabled(False)

    def changeState(self):
        for widget in self.changeStateWidgetList:
            widget.setEnabled(True)

    def setupUI(self):
        # main Layout
        self.mainLayout = QVBoxLayout()
        # parameters layout
        self.labelFrame = QFrame()
        self.massLabel = QLabel("质谱仪")
        self.massLabel.setObjectName("MassLabel")
        self.changeStateWidgetList.append(self.massLabel)
        self.liquidLabel = QLabel("液相仪")
        self.liquidLabel.setObjectName("LiquidLabel")
        self.changeStateWidgetList.append(self.liquidLabel)
        self.massParametersLabel = QLabel()
        self.massParametersLabel.setObjectName("MassParameters")
        self.changeStateWidgetList.append(self.liquidLabel)
        self.liquidParametersLabel = QLabel()
        self.liquidParametersLabel.setObjectName("LiquidParameters")
        self.changeStateWidgetList.append(self.liquidParametersLabel)
        self.parametersLayout = QVBoxLayout()
        self.massLayout = QHBoxLayout()
        self.liquidLayout = QHBoxLayout()
        initialTheLayout(self.massLayout, [
                         self.massLabel, self.massParametersLabel], [1, 3], True)
        initialTheLayout(self.liquidLayout, [
                         self.liquidLabel, self.liquidParametersLabel], [1, 3], True)
        initialTheLayout(self.parametersLayout, [
                         self.massLayout, self.liquidLayout], [1, 1], True)
        self.parametersLayout.setContentsMargins(20, 5, 0, 5)
        self.labelFrame.setLayout(self.parametersLayout)
        self.labelFrame.setMaximumHeight(80)
        self.labelFrame.setMinimumHeight(50)
        # Buttons Layout
        self.addButton = ButtonWithPixmap(
            "./figs/添加.svg", "添加数据", "AddDataButton")
        # sort Layout
        self.toolText = QLabel("选择排序列和排序方式:")
        self.toolText.setObjectName("ToolText")
        self.toolText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sortColumnComboBox = ComboBox(
            ["日期", "姓名", "省份", "市区", "地址", "邮编"])
        self.upSortButton = ButtonWithPixmap(
            "./figs/上.svg", "从小到大", "upSortButton")
        self.downSortButton = ButtonWithPixmap(
            "./figs/下.svg", "从大到小", "downSortButton")
        self.sortSpacerItem1 = QSpacerItem(
            10, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.sortSpacerItem2 = QSpacerItem(
            15, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.sortLayout = QHBoxLayout()
        initialTheLayout(self.sortLayout, [
            self.sortSpacerItem1,
            self.toolText,
            self.sortColumnComboBox,
            self.upSortButton,
            self.downSortButton,
            self.sortSpacerItem2],
            [1, 2, 2, 2, 2, 1],
            True)
        self.sortLayout.setSpacing(10)
        self.sortLayout.setContentsMargins(2, 0, 5, 0)
        # set Button Layout
        self.buttonsSpacerItem = QSpacerItem(
            20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.buttonsLayout = QHBoxLayout()
        initialTheLayout(self.buttonsLayout, [
                         self.addButton,
                         self.buttonsSpacerItem,
                         self.sortLayout
                         ],
                         [1, 2, 1],
                         True)
        self.buttonsLayout.setContentsMargins(5, 0, 5, 0)
        # set main Layout
        self.settingTableWidget = TableWidgetWithButtons(
            data="./TableWidgetTestData.csv",
            headLabels=["日期", "姓名", "省份", "市区", "地址", "邮编"])
        initialTheLayout(self.mainLayout, [
                         self.labelFrame,
                         self.buttonsLayout,
                         self.settingTableWidget
                         ],
                         [2, 1, 4],
                         True)
        self.setLayout(self.mainLayout)
        self.mainLayout.setSpacing(2)

    def addData(self):
        """
        TODO: 添加数据
        """

    def sortUpDown(self, columnName: str):
        """
        TODO: 将数据按照 ComboBox 选择的列从大到小排序
        """

    def sortDownUp(self, columnName: str):
        """
        TODO: 将数据按照 ComboBox 选择的列从小到大排序
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InstrumentSetting()
    widget.show()
    app.exec()
