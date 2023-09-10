from typing import Optional, Sequence, Union, Tuple, List
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSpacerItem,
    QStackedWidget,
    QListView,
    QSizePolicy,
    QFrame,
    QTabWidget
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, QPoint
from utils import initialTheLayout, setQss, Font
from navigator import Navigator
from tableWidget import TableWidget
from searchBar import CodeCompleter


class GraphWidget(pg.GraphicsLayoutWidget):
    def __init__(self, graphTitle, parent=None, show=True, size=None, title=None, **kargs):
        super().__init__(parent, show, size, title, **kargs)
        self.title = graphTitle
        self.initFlags()
        self.init()

    def initFlags(self):
        self.maxValuePointNum = 6

    def getMaxValuePos(self):
        argIndex = np.argsort(-self.data["y"])  # type: ignore
        return self.data["x"][argIndex[:self.maxValuePointNum]], self.data["y"][argIndex[:self.maxValuePointNum]]

    def init(self):
        # 添加 label, 准备放十字基准线的数据
        self.label = pg.LabelItem(justify='right')
        self.addItem(self.label)

        # p1, 放置可缩放的质谱数据图
        self.p1 = self.addPlot(row=1, col=0)
        self.p1.avgPen = pg.mkPen('#FFFFFF')
        self.p1.avgShadowPen = pg.mkPen('#8080DD', width=10)
        self.p1.setLabel(axis="left", text="峰强度值")
        self.p1.setLabel(axis="bottom", text="质荷比")
        self.p1.setTitle(self.title)

        # 在 p1 中添加基准线
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vline, ignoreBounds=True)  # type: ignore
        self.p1.addItem(self.hline, ignoreBounds=True)  # type: ignore

        # p2, 作为完整的质谱图作为参考图
        self.p2 = self.addPlot(row=2, col=0)
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.p2.addItem(self.region, ignoreBounds=True)

        self.p1.setAutoVisible(y=True)
        self.region.setRegion([1000, 2000])

    def connectSignal(self):
        self.region.sigRegionChanged.connect(self.update)
        self.p1.scene().sigMouseMoved.connect(self.mouseMoved)
        self.p1.sigRangeChanged.connect(self.updateRegion)

    def updateCurve(self, x: Union[Sequence[float], np.ndarray], y: Union[Sequence[float], np.ndarray], color: str):
        self.data = {"x": x, "y": y}
        self.connectSignal()

        self.p1.plot(x, y, pen="r")
        self.p2.plot(x, y, pen="g", fillLevel=-0.3, brush=(50, 50, 200, 100))

        p2d = self.p2.plot(x, y, pen="w")
        self.region.setClipItem(p2d)

        xValue, yValue = self.getMaxValuePos()

        # 添加最高点的位置
        self.labels: List[pg.LabelItem] = []
        for i in range(len(xValue)):  # type: ignore
            label = pg.TextItem()
            self.p1.addItem(label)
            font = Font(12, ["Helvetica", "Times NewRoman", "微软雅黑", "宋体"])
            label.setFont(font)
            label.setPos(xValue[i],  # type: ignore
                         yValue[i] + 0.1)  # type: ignore
            label.setText(
                "%0.1f" % (yValue[i]))  # type: ignore

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.p1.setXRange(minX, maxX, padding=0)

    def searchIndex(self, x: float) -> np.intp:
        diff: np.ndarray = np.absolute(self.data["x"] - x)  # type: ignore
        index = diff.argmin()
        return index

    def mouseMoved(self, event: QMouseEvent):
        pos = event
        # 如果鼠标在 p1 图内
        if self.p1.sceneBoundingRect().contains(pos):
            # 将鼠标坐标转换为绘图的坐标
            mousePoint: QPoint = self.p1.vb.mapSceneToView(pos)
            index = self.searchIndex(mousePoint.x())
            if index >= 0:
                self.label.setText("<span style='font-size: 12pt'>x=%0.1f,  <span style='color: red'>y1=%0.1f</span>" %
                                   (self.data["x"][index], self.data["y"][index]))
                self.vline.setPos(self.data["x"][index])
                self.hline.setPos(self.data["y"][index])


class TIC_XIC_Widget(QWidget):
    def __init__(self, title: str, parent: Optional[QWidget] = None) -> None:
        super(TIC_XIC_Widget, self).__init__(parent)
        # 图像的标题
        self.graphTitle = title
        self.setupUI()
        self.searchBar.setPopulateCompleter(
            self.dataTableWidget.getDataGrip("省份"))

    def setupUI(self):
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName("GraphTabWidget")
        initialTheLayout(self.mainLayout, [self.tabWidget], [1], True)
        # graph
        self.graphWidget = GraphWidget(self.graphTitle)
        # data
        self.dataPage = QWidget()
        self.dataPage.setObjectName("DataPage")
        self.dataPageMainLayout = QVBoxLayout()
        self.dataPage.setLayout(self.dataPageMainLayout)
        self.searchBarLayout = QHBoxLayout()
        self.searchBarSpacerItem = QSpacerItem(
            5, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.searchBar = CodeCompleter()
        initialTheLayout(self.searchBarLayout, [
                         self.searchBar, self.searchBarSpacerItem], [1, 4], True)
        self.dataTableWidget = TableWidget(
            data="./TableWidgetTestData.csv",
            headLables=["日期", "姓名", "省份", "市区", "地址", "邮编"])
        initialTheLayout(self.dataPageMainLayout, [
                         self.searchBarLayout, self.dataTableWidget], [1, 4], True)
        self.tabWidget.addTab(self.graphWidget, "图像展示")
        self.tabWidget.addTab(self.dataPage, "数据展示")


class MassGraph(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super(MassGraph, self).__init__(parent)
        self.setupUI()
        self.initFlags()
        self.setStyleSheet(setQss("./style/MassGraph.css"))
        self.updateXicPlot()
        self.updateTicPlot()

    def initFlags(self):
        self.navigator.setCurrentRow(0)

    def updateTicPlot(self):
        self.TicGraphWidget.graphWidget.updateCurve(np.linspace(
            0, 10, 1000), np.random.rand(1000), "white")

    def updateXicPlot(self):
        self.XicGraphWidget.graphWidget.updateCurve(np.linspace(
            0, 10, 120), np.random.normal(size=120)+10, "white")

    def setupUI(self):
        # mainLayout
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        # Navigator Layout
        self.navigator = Navigator(names=['TIC', 'XIC'], parent=self)
        self.navigator.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.navigator.setObjectName("MassGraphPageNavigator")
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
        self.navigatorFrame = QFrame()
        self.navigatorFrame.setObjectName("MassGraphPageNavigatorFrame")
        self.navigatorFrame.setLayout(self.navigatorLayout)
        # stackwidget
        self.stackWidget = QStackedWidget()
        self.TicGraphWidget = TIC_XIC_Widget("TIC 图像")
        self.XicGraphWidget = TIC_XIC_Widget("XIC 图像")
        self.stackWidget.addWidget(self.TicGraphWidget)
        self.stackWidget.addWidget(self.XicGraphWidget)
        initialTheLayout(self.mainLayout, [
                         self.navigatorFrame, self.stackWidget], [1, 5], True)
        self.mainLayout.setSpacing(4)
        self.mainLayout.setContentsMargins(2, 4, 2, 2)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MassGraph()
    w.show()
    app.exec()
