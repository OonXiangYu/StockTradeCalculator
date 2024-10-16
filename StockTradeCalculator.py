import sys
import csv
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, \
    QVBoxLayout
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
        '''
        This method requires substantial updates.
        Each of the widgets should be suitably initialized and laid out.
        '''
        super().__init__()

        # setting up dictionary of Stocks
        self.data = self.make_data()

        # Initialize the layout
        layout = QVBoxLayout()

        # TODO: create QLabel for Stock selection
        # Stock selection label
        self.stock_label = QLabel("Select Stock:")
        layout.addWidget(self.stock_label)

        # TODO: create QComboBox and populate it with a list of Stocks
        # Stock selection ComboBox
        self.stock_combobox = QComboBox()
        self.stock_combobox.addItems(self.data.keys())
        layout.addWidget(self.stock_combobox)

        # TODO: create QLabel for Quantity selection
        # Quantity selection label
        self.quantity_label = QLabel("Quantity:")
        layout.addWidget(self.quantity_label)

        # TODO: create QSpinBox to select Stock quantity purchased
        #Quantity select SpinBox
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(0)
        self.quantity_spinbox.setMaximum(100)
        layout.addWidget(self.quantity_spinbox)

        # TODO: create CalendarWidgets for selection of purchase and sell dates
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

        # TODO: create QLabels to show the Stock purchase total
        self.stock_purchase_total = QLabel("Purchase Total :$")
        layout.addWidget(self.stock_purchase_total)

        # TODO: create QLabels to show the Stock sell total
        self.stock_sell_total = QLabel("Sell Total :$")
        layout.addWidget(self.stock_sell_total)

        # TODO: create QLabels to show the Stock profit total
        self.stock_profit_total = QLabel("Profit :$")
        layout.addWidget(self.stock_profit_total)

        self.setLayout(layout)
        self.setWindowTitle('Stock Trade Profit Calculator')
        self.show()

        # Check if 'Amazon' exists, if not, handle it gracefully
        if 'Amazon' in self.data:
            self.sellCalendarDefaultDate = sorted(self.data['Amazon'].keys())[-1]
        else:
            print("Amazon not found in the dataset. Available stocks:", self.data.keys())
            self.sellCalendarDefaultDate = QDate.currentDate()  # Default to the current date

        # TODO: Define buyCalendarDefaultDate

        # TODO: initialize the layout - 6 rows to start

        # TODO: set the calendar values
        # purchase: two weeks before most recent
        # sell: most recent

        # TODO: connecting signals to slots so that a change in one control updates the UI

        # TODO: set the window title
        # TODO: update the UI

    def updateUi(self):
        '''
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        try:
            # TODO: get selected dates from calendars

            # TODO: perform necessary calculations to calculate totals

            # TODO: update the label displaying totals
            pass  # placeholder for future code
        except Exception as e:
            print(f"Error in updateUi: {e}")

    def make_data(self):
        '''
        This code reads the stock market CSV file and generates a dictionary structure.
        :return: a dictionary of dictionaries
        '''
        data = {}
        try:
            with open('data/Transformed_Stock_Market_Dataset.csv', mode='r') as file:
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
            print(f"Stocks available: {stock_names}")  # Debugging: Print all available stock names

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

def main():
    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    sys.exit(app.exec())
# This is complete
if __name__ == '__main__':
        main()
