from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
import sys

class StockTradeCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Define the purchase date
        purchaseDate = "2024-10-15"  # Replace with actual data

        # Main layout
        layout = QVBoxLayout(self)

        # Sub layout for the purchase date
        sub1_layout = QHBoxLayout()

        # Create labels
        self.purchase_date_label = QLabel("Select Purchase Date:")
        self.purchase_date = QLabel(f'{purchaseDate}')

        # Add the labels to the horizontal sub-layout
        sub1_layout.addWidget(self.purchase_date_label)
        sub1_layout.addWidget(self.purchase_date)

        # Add the sub-layout to the main layout
        layout.addLayout(sub1_layout)

        # Set the layout to the window
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockTradeCalculator()
    window.show()
    sys.exit(app.exec())
