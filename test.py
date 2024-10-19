from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDialog, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import sys

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot_bar_chart(self, categories, values):
        self.axes.clear()  # Clear previous plot
        self.axes.bar(categories, values)  # Plot with floating-point values
        self.draw()

class GraphWindow(QMainWindow):
    def __init__(self, categories, values):
        super().__init__()
        self.setWindowTitle("Bar Chart with Double Values")
        self.setGeometry(200, 200, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.canvas = MatplotlibCanvas(self)
        layout.addWidget(self.canvas)

        # Plot the bar chart
        self.canvas.plot_bar_chart(categories, values)

class StockTradeProfitCalculator(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Trade Profit Calculator")
        self.setGeometry(100, 100, 400, 200)

        # Create a button to show the bar chart
        self.show_chart_button = QPushButton("Show Bar Chart", self)
        self.show_chart_button.clicked.connect(self.show_bar_chart)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.show_chart_button)
        self.setLayout(layout)

        # Example data (you may replace these with real data)
        self.categories = ['Stock A', 'Stock B', 'Stock C']
        self.values = [-12.5, 15.3, 9.8]

    def show_bar_chart(self):
        # Create and show the graph window with categories and values
        self.graph_window = GraphWindow(self.categories, self.values)
        self.graph_window.show()


def main():
    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    sys.exit(app.exec())
# This is complete
if __name__ == '__main__':
    main()

