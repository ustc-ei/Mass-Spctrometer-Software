import sys
from time import sleep
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import QThread, Signal, QSize, Qt
from utils import initialTheLayout, setQss
from tableWidget import TableWidgetWithButtons


# class ProgressDataTableWidget(TableWidget):
#     def __init__(self, parent: Optional[QWidget] = None):
#         super(ProgressDataTableWidget, self).__init__(parent)


class ProgressUpdateThread(QThread):
    # set the data type that siganl emits
    signal = Signal(int)

    def __init__(self, parent: Optional[QWidget]) -> None:
        """
        the basic class of progress

        use the Qthread to update the progress UI
        """
        self.running = True
        super(ProgressUpdateThread, self).__init__(parent)

    def stop(self):
        self.running = False


class DataAcqusionUpdateThread(ProgressUpdateThread):
    def __init__(self, parent: Optional[QWidget]) -> None:
        super(DataAcqusionUpdateThread, self).__init__(parent)

    def run(self) -> None:
        for i in range(101):
            sleep(0.1)
            self.signal.emit(i)
            if self.running == False:
                break


class SampleAcqusionUpdateThread(ProgressUpdateThread):
    def __init__(self, parent: Optional[QWidget]) -> None:
        super(SampleAcqusionUpdateThread, self).__init__(parent)

    def run(self) -> None:
        for i in range(101):
            sleep(0.2)
            self.signal.emit(i)
            if self.running == False:
                break


class ProgressShow(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(ProgressShow, self).__init__(parent)
        self.setupUI()
        self.setStyleSheet(setQss('./style/ProgressShow.css'))
        self.initUpdateProgressThread()
        self.initFlags()
        self.signalConnect()
        self.startThread()

    def initFlags(self):
        pass

    def initUpdateProgressThread(self):
        self.dataAcqusionThread = DataAcqusionUpdateThread(self)
        self.sampleAcqusionThread = SampleAcqusionUpdateThread(self)

    def signalConnect(self):
        self.sampleAcqusionThread.signal.connect(self.updateSampleProgressBar)
        self.dataAcqusionThread.signal.connect(self.updateDataProgressBar)

    def startThread(self):
        self.sampleAcqusionThread.start()
        self.dataAcqusionThread.start()

    def setupUI(self):
        # main Layout
        self.mainLayout = QVBoxLayout()
        # progress layout
        self.dataProgressLayout = QHBoxLayout()
        self.sampleProgressLayout = QHBoxLayout()
        self.porgressLayout = QVBoxLayout()
        # Table
        self.tableWidget = TableWidgetWithButtons(
            data="./TableWidgetTestData.csv",
            headLabels=["日期", "姓名", "省份", "市区", "地址", "邮编", "操作1", "操作2"])
        # progress
        self.progressFrame = QFrame()
        self.progressFrame.setObjectName("ProgressFrame")
        self.dataAcqusionLabel = QLabel("数据采集进度:")
        self.dataAcqusionLabel.setMinimumSize(QSize(130, 20))
        self.dataAcqusionLabel.setMaximumHeight(30)
        self.dataAcqusionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dataAcqusionLabel.setObjectName("DataAcqusion")
        self.dataAcqusionProgress = QProgressBar()
        # self.dataAcqusionProgress.setMaximumHeight(30)
        # self.dataAcqusionProgress.setMinimumWidth(400)
        self.sampleAcqusionLabel = QLabel("样品采集进度:")
        self.sampleAcqusionLabel.setMinimumSize(QSize(130, 20))
        self.sampleAcqusionLabel.setMaximumHeight(30)
        self.sampleAcqusionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sampleAcqusionLabel.setObjectName("SampleAcqusion")
        self.sampleAcqusionProgress = QProgressBar()
        # self.sampleAcqusionProgress.setMinimumWidth(400)
        # self.sampleAcqusionProgress.setMaximumHeight(30)
        # set progress Layout
        initialTheLayout(self.dataProgressLayout, [
                         self.dataAcqusionLabel, self.dataAcqusionProgress],
                         [1, 5],
                         True)
        self.dataProgressLayout.setSpacing(5)
        initialTheLayout(self.sampleProgressLayout, [
                         self.sampleAcqusionLabel, self.sampleAcqusionProgress],
                         [1, 5],
                         True)
        self.sampleProgressLayout.setSpacing(5)
        initialTheLayout(self.porgressLayout, [
            self.sampleProgressLayout, self.dataProgressLayout],
            [1, 1],
            True)
        self.porgressLayout.setSpacing(5)
        self.porgressLayout.setContentsMargins(10, 5, 5, 5)
        self.progressFrame.setLayout(self.porgressLayout)
        # set main Layout
        initialTheLayout(self.mainLayout, [self.tableWidget,
                                           self.progressFrame],
                         [5, 1],
                         True)
        self.mainLayout.setSpacing(5)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.mainLayout)

    def updateDataProgressBar(self, value: int):
        self.dataAcqusionProgress.setValue(value)
        if value == 100:
            # You cannot change the execution order
            # Otherwise, the program may crash.
            self.dataAcqusionThread.quit()
            self.dataAcqusionThread.wait()
            del self.dataAcqusionThread
            self.dataAcqusionThread = DataAcqusionUpdateThread(self)
            self.dataAcqusionThread.signal.connect(self.updateDataProgressBar)
            self.dataAcqusionThread.start()

    def updateSampleProgressBar(self, value: int):
        self.sampleAcqusionProgress.setValue(value)
        if value == 100:
            # You cannot change the execution order
            # Otherwise, the program may crash.
            self.sampleAcqusionThread.quit()
            self.sampleAcqusionThread.wait()
            del self.sampleAcqusionThread
            self.sampleAcqusionThread = SampleAcqusionUpdateThread(self)
            self.sampleAcqusionThread.signal.connect(
                self.updateSampleProgressBar)
            self.sampleAcqusionThread.start()

    def destoryAllThread(self):
        self.sampleAcqusionThread.stop()
        self.dataAcqusionThread.stop()
        self.sampleAcqusionThread.wait()
        self.dataAcqusionThread.wait()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.destoryAllThread()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ProgressShow()
    widget.show()
    app.exec()
