from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget

app = QApplication([])

# 创建主窗口和布局
window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

# 创建一个 QComboBox 控件
combo_box = QComboBox()

combo_box.setStyleSheet("""
/* 设置 QComboBox 圆角 */
QComboBox {
    border: 1px solid gray;
    border-radius: 10px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}

/* 设置 QComboBox 下拉列表 QAbstractItemView 圆角 */
QComboBox QAbstractItemView {
    border: 1px solid gray;
    border-radius: 10px;
    background-color: white;
    /* 避免黑框 */
    outline: none;
    margin-top: 20px;
}

/* 设置下拉列表项的样式 */
QComboBox QAbstractItemView::item {
    padding: 4px 8px;
}

/* 设置下拉列表项的样式（鼠标悬停时） */
QComboBox QAbstractItemView::item:hover {
    background-color: lightgray;
}

/* 设置下拉列表项的样式（选中状态） */
QComboBox QAbstractItemView::item:selected {
    background-color: gray;
    color: white;
}


""")
# 添加选项
combo_box.addItem("Option 1")
combo_box.addItem("Option 2")
combo_box.addItem("Option 3")

# 设置初始选中的选项
initial_index = 1  # 设置初始选中 Option 2
combo_box.setCurrentIndex(initial_index)

# 将 QComboBox 添加到布局中
layout.addWidget(combo_box)

# 将布局设置为主窗口的中央部件
window.setCentralWidget(central_widget)

window.show()
app.exec()
