import pyqtgraph as pg
import numpy as np
from PySide6.QtWidgets import QApplication
import sys

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Find indices of top six y values
top_indices = np.argsort(y)[-6:]

# Create the application
app = QApplication(sys.argv)

# Create a PlotWidget
plot_widget = pg.PlotWidget()

# Plot the data
plot_item = plot_widget.plot(x, y, pen='b')

# Add TextItems for displaying y values above the top points
for index in top_indices:
    x_coord = x[index]
    y_coord = y[index]
    text_item = pg.TextItem(text=f'{y_coord:.2f}', anchor=(0.5, 1))
    plot_widget.addItem(text_item)
    text_item.setPos(x_coord, y_coord)

# Show the plot
plot_widget.show()

sys.exit(app.exec_())
