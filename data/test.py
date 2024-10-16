import sys
import csv
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, QVBoxLayout
from datetime import datetime


class StockTradeProfitCalculator(QDialog):
    '''
    Provides the following functionality:

    - Allows the selection of the stock to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    '''

    def __init__(self):
        super().__init__()

        # setting up dictionary of Stocks
        self.data = self.make_data()

        # Initialize the layout
        layout = QVBoxLayout()

        # Stock selection label
        self.stock_label = QLabel("Select Stock:")
        layout.addWidget(self.stock_label)

        # Stock selection ComboBox
        self.stock_combobox = QComboBox()
        self.stock_combobox.addItems(self.data.keys())
        layout.addWidget(self.stock_combobox)

        # Quantity selection
        self.quantity_label = QLabel("Select Quantity:")
        layout.addWidget(self.quantity_label)

        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setRange(1, 10000)  # Arbitrary range, adjust as needed
        layout.addWidget(self.quantity_spinbox)

        # Purchase date selection
        self.purchase_date_label = QLabel("Select Purchase Date:")
        layout.addWidget(self.purchase_date_label)

        self.purchase_calendar = QCalendarWidget()
        layout.addWidget(self.purchase_calendar)

        # Sell date selection
        self.sell_date_label = QLabel("Select Sell Date:")
        layout.addWidget(self.sell_date_label)

        self.sell_calendar = QCalendarWidget()
        layout.addWidget(self.sell_calendar)

        # Labels to show totals
        self.purchase_total_label = QLabel("Purchase Total: 0")
        layout.addWidget(self.purchase_total_label)

        self.sell_total_label = QLabel("Sell Total: 0")
        layout.addWidget(self.sell_total_label)

        self.profit_total_label = QLabel("Profit Total: 0")
        layout.addWidget(self.profit_total_label)

        # Set the layout for the dialog
        self.setLayout(layout)

        # Set window title
        self.setWindowTitle("Stock Trade Profit Calculator")

        # Connect signals to slots
        self.stock_combobox.currentIndexChanged.connect(self.updateUi)
        self.quantity_spinbox.valueChanged.connect(self.updateUi)
        self.purchase_calendar.selectionChanged.connect(self.updateUi)
        self.sell_calendar.selectionChanged.connect(self.updateUi)

        # Initialize the UI
        self.updateUi()

    def updateUi(self):
        '''
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        try:
            stock = self.stock_combobox.currentText()
            quantity = self.quantity_spinbox.value()

            # Get the selected dates
            purchase_date = self.purchase_calendar.selectedDate()
            sell_date = self.sell_calendar.selectedDate()

            # Convert QDate to tuple (year, month, day)
            purchase_tuple = (purchase_date.year(), purchase_date.month(), purchase_date.day())
            sell_tuple = (sell_date.year(), sell_date.month(), sell_date.day())

            # Fetch stock prices for the selected dates
            purchase_price = self.data.get(stock, {}).get(purchase_tuple, 0)
            sell_price = self.data.get(stock, {}).get(sell_tuple, 0)

            # Calculate totals
            purchase_total = purchase_price * quantity
            sell_total = sell_price * quantity
            profit_total = sell_total - purchase_total

            # Update labels
            self.purchase_total_label.setText(f"Purchase Total: {purchase_total:.2f}")
            self.sell_total_label.setText(f"Sell Total: {sell_total:.2f}")
            self.profit_total_label.setText(f"Profit Total: {profit_total:.2f}")

        except Exception as e:
            print(f"Error in updateUi: {e}")

    def make_data(self):
        '''
        Reads the stock market CSV file and generates a dictionary structure.
        :return: a dictionary of dictionaries
        '''
        data = {}
        try:
            with open('Transformed_Stock_Market_Dataset.csv', mode='r') as file:
                reader = csv.DictReader(file)
                stock_names = reader.fieldnames[1:]  # All columns except 'Date' are stock names

                for row in reader:
                    date_string = row['Date']
                    date_tuple = self.string_date_into_tuple(date_string)

                    for stock in stock_names:
                        price = row[stock].replace(',', '')
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0

                        if stock not in data:
                            data[stock] = {}

                        data[stock][date_tuple] = price

            print("Data loaded successfully.")
            print(f"Stocks available: {stock_names}")

        except Exception as e:
            print(f"Error reading data: {e}")
        return data

    def string_date_into_tuple(self, date_string):
        '''
        Converts a date in string format (e.g., "2024-02-02") into a tuple (year, month, day).
        :return: tuple representing the date
        '''
        try:
            if '-' in date_string:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            else:
                date_obj = datetime.strptime(date_string, "%m/%d/%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print(f"Error parsing date: {date_string}")
            return None


# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    sys.exit(app.exec())
