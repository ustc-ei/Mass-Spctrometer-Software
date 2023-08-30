from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QCompleter, QLineEdit, QVBoxLayout, QWidget


class HighlightCompleter(QCompleter):
    def __init__(self, model):
        super().__init__(model)
        self.activated.connect(self.handleActivated)

    def handleActivated(self, index):
        item = self.model().itemFromIndex(index)
        if item:
            original_text = item.text()
            highlighted_text = f'<span style="background-color: yellow;">{original_text}</span>'
            self.popup().setHtml(
                f'<html><head/><body>{highlighted_text}</body></html>')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.lineEdit = QLineEdit()
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

        suggestions = ["apple", "banana", "cherry",
                       "grape", "kiwi", "orange", "pear", "strawberry"]
        self.model = QStandardItemModel()
        for suggestion in suggestions:
            item = QStandardItem(suggestion)
            self.model.appendRow(item)
        self.completer = HighlightCompleter(self.model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # 不区分大小写
        self.lineEdit.setCompleter(self.completer)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
