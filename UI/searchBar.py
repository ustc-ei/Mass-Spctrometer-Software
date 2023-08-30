from typing import List, Optional, Sequence
import PySide6.QtGui
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter, QListView
from PySide6.QtCore import Qt, QStringListModel, QObject, QEvent
from utils import setQss, Font


class ListView(QListView):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(ListView, self).__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setFont(Font(15, ["Helvetica", "微软雅黑", "宋体"]))


class Completer(QCompleter):
    def __init__(self, parent: Optional[QWidget] = None):
        super(Completer, self).__init__(parent)
        self.setFilterMode(Qt.MatchFlag.MatchContains)


class CodeCompleter(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.populateCompleter()
        self.setStyleSheet(setQss('./style/SearchBar.css'))

    def setupUI(self):
        layout = QVBoxLayout(self)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("SearchEditLine")
        layout.addWidget(self.lineEdit)

        self.completer = Completer(self)
        self.listView = ListView(self)
        self.listView.setStyleSheet(setQss('./style/ToolListView.css'))
        self.completer.setPopup(self.listView)
        self.completer.setCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive)  # 设置大小写不敏感
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.lineEdit.setCompleter(self.completer)

    def populateCompleter(self):
        suggestions = ["湖南", "河北", "河南",
                       "arape", "aiwi", "arange", "aear", "atrawberry"]
        self.model.setStringList(suggestions)


if __name__ == "__main__":
    app = QApplication([])
    window = CodeCompleter()
    window.show()
    app.exec()
