from enum import Enum
from typing import Optional, List, Sequence, Tuple
from PySide6.QtCore import QSize, Qt, Signal
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
from dialog import AddDialog


class SORT_TYPES(Enum):
    """
    Enum class representing different sorting types for buttons.

    Attributes:
    * UpDown: Represents ascending to descending sorting.
    * DownUp: Represents descending to ascending sorting.
    """
    UpDown = 1
    DownUp = 2


class SortButton(ButtonWithPixmap):
    signal = Signal(SORT_TYPES)
    """
    the signal is used to sent the type of sorting
    """

    def __init__(self,
                 sortType: SORT_TYPES,
                 pixMapPath: str,
                 text: str = "",
                 objectName: str = "",
                 parent: Optional[QWidget] = None):
        """
        Sort Button

        This button allows you to select the sorting type.

        Parameters:
            sortType (SORT_TYPES): The type of sorting.
            pixMapPath (str): The path to the picture.
            text (str): The text displayed on the button.
            objectName (str): The object name of the button.
            parent (Optional[QWidget]): The parent widget of the button.
        """
        super().__init__(pixMapPath, text, objectName, parent)
        self.sortType = sortType
        self.connectSignal()

    def connectSignal(self):
        """
        Connect the signal and slot function:
        """
        self.clicked.connect(self.emitData)

    def emitData(self):
        """
        """
        self.signal.emit(self.sortType)


class ComboBox(QComboBox):
    def __init__(self,
                 text: Sequence[str],
                 parent: Optional[QWidget] = None) -> None:
        """
        ComboBox

        user-designed QComboBox, you can overload the functions to achieve the goal 

        Parameters:
        * text(Sequence[str]): the initial text of the items 
        * parent: Optional[QWidget]: the parent of the ComboBox
        """
        super().__init__(parent)
        self.text = text
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.initSelectData()
        self.setMaxMinSize()

    def initSelectData(self):
        """
        add the items
        """
        self.addItems(self.text)

    def setMaxMinSize(self):
        """
        set the maxiumSize and the minimumSize
        """
        self.setMaximumSize(QSize(120, 35))
        self.setMinimumSize(QSize(100, 35))


class InstrumentSetting(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Instrument Setting

        This is the instrument setting page.

        In this page, users can configure parameters for mass or liquid.

        Actions:
        1. Add setting parameters.
        2. Edit existing parameters.
        3. Delete parameters.
        4. Select specific parameters.
        5. View all parameters that the user has configured.
        """

        super(InstrumentSetting, self).__init__(parent)
        self.initFlags()
        self.setupUI()
        self.initState()
        self.connectSignal()
        self.setStyleSheet(setQss("./style/InstrumentSetting.css"))

    def connectSignal(self):
        """
        Connect the Signal and Slot Functions:

        1. Add Parameters
        2. Select Column and Sort Type
        """

        self.addButton.clicked.connect(self.addSureDialog)
        self.upSortButton.signal.connect(self.sortColumnSelect)
        self.downSortButton.signal.connect(self.sortColumnSelect)

    def initFlags(self):
        """
        init the flags
        """
        self.changeStateWidgetList: List[QWidget] = []

    def initState(self):
        """
        init the labels to be disabled.
        """
        for widget in self.changeStateWidgetList:
            widget.setEnabled(False)

    def changeState(self):
        """
        Change the Labels' State

        If you haven't selected the setting parameters, 

        the labels will appear disabled.

        Otherwise, the labels will be enabled.
        """
        for widget in self.changeStateWidgetList:
            widget.setEnabled(True)

    def setupUI(self):
        """
        Create UI Interface

        This section is responsible for creating the user interface.

        Here, you will design and layout the graphical elements that form the user interface of the application.
        """

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
        self.upSortButton = SortButton(SORT_TYPES.UpDown,
                                       "./figs/上.svg",
                                       "从小到大",
                                       "upSortButton")
        self.downSortButton = SortButton(SORT_TYPES.DownUp,
                                         "./figs/下.svg",
                                         "从大到小",
                                         "downSortButton")
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

    def addSureDialog(self):
        """
        Add Sure Dialog

        Opens a dialog for adding new data.

        This function is triggered when the user intends to add a new data entry. 

        It displays a dialog box where the user can input data.
        """
        self.dialog = AddDialog(
            "添加一条新记录",
            self.addRowData,  # type: ignore
            (),  # type: ignore
            tuple(self.settingTableWidget.headLabels))
        self.dialog.show()

    def addRowData(self, data: Tuple[str]):
        """
        Add Row Data

        Adds a new data row to the table.

        This function adds a new row of data to the table. 

        It is called after the user has entered data in the dialog.

        Parameters:
        * data (Tuple[str]): The data to be added.
        """
        self.settingTableWidget.updateDfData(data)

    def sortUpDown(self, column: str):
        """
        Sort Up-Down

        Sorts the data in descending order based on the selected column.

        This function sorts the data in descending order based on the selected column. 

        It is triggered when the user click the "UpDown" sorting button.

        Paramters:
        * column (str): The column by which the data should be sorted.

        """
        self.settingTableWidget.sortDataUpDown(column)

    def sortDownUp(self, column: str):
        """
        Sort Down-Up

        Sorts the data in ascending order based on the selected column.

        This function sorts the data in ascending order based on the selected column. 

        It is triggered when the user click the "DownUp" sorting button.

        Parameters:
        * column (str): The column by which the data should be sorted.
        """
        self.settingTableWidget.sortDataDownUp(column)

    def sortColumnSelect(self, sortType: SORT_TYPES):
        """
        Sort Column Select

        Initiates the sorting process based on user-selected column and sorting type.

        This function handles sorting based on the user-selected column and sorting type. 

        It triggers the appropriate sorting function.

        Parameters:
        * sortType (SORT_TYPES): The selected sorting type.
        """
        column = self.sortColumnComboBox.currentText()
        if sortType == SORT_TYPES.UpDown:
            self.sortUpDown(column)
        elif sortType == SORT_TYPES.DownUp:
            self.sortDownUp(column)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = InstrumentSetting()
    widget.show()
    app.exec()
