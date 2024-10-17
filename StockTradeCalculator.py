import sys
import csv

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, QVBoxLayout, QHBoxLayout, QMessageBox
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
        layout = QVBoxLayout(self)

        #assign variable
        self.purchase_total_price = 0
        self.sell_total_price = 0
        self.total_profit = 0
        self.stock_buy_price = 0
        self.stock_sell_price = 0

        # TODO: create QLabel for Stock selection
        # Stock selection label
        self.stock_label = QLabel("Select Stock:")
        layout.addWidget(self.stock_label)

        # TODO: create QComboBox and populate it with a list of Stocks
        # Stock selection ComboBox
        self.stock_combobox = QComboBox()
        self.stock_combobox.addItems(self.data.keys())
        layout.addWidget(self.stock_combobox)
        self.stock_name = self.stock_combobox.currentText()

        # TODO: Define buyCalendarDefaultDate
        self.purchaseDate = QDate.currentDate().addDays(-14)  # purchase: two weeks before most recent
        self.sellDate = QDate.currentDate()

        # Check if current stock exists, if not, handle it gracefully
        if self.stock_name in self.data:
            self.sellDefaultDate = sorted(self.data[self.stock_name].keys())[0]
            #self.sellDate = QDate(year, month, day)
            print(f'{self.sellDefaultDate}')
        else:
            print("Current stock not found in the dataset. Available stocks:", self.data.keys())
            self.sellDefaultDate = QDate.currentDate()  # Default to the current date

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
        sub1_layout = QHBoxLayout()
        self.purchase_date_label = QLabel("Select Purchase Date:")
        self.purchase_date = QLabel(f"{self.purchaseDate.toString('dd-MM-yyyy')}")
        sub1_layout.addWidget(self.purchase_date_label)
        sub1_layout.addWidget(self.purchase_date)
        sub1_layout.addStretch(1)
        layout.addLayout(sub1_layout)

        # TODO: set the purchase calendar values
        self.purchase_calendar = QCalendarWidget()
        self.purchase_calendar.setSelectedDate(self.purchaseDate)
        layout.addWidget(self.purchase_calendar)

        # Sell date selection
        sub2_layout = QHBoxLayout()
        self.sell_date_label = QLabel("Select Sell Date:")
        self.sell_date = QLabel(f"{self.sellDate.toString('dd-MM-yyyy')}")
        sub2_layout.addWidget(self.sell_date_label)
        sub2_layout.addWidget(self.sell_date)
        sub2_layout.addStretch(1)
        layout.addLayout(sub2_layout)

        # TODO: set the sell calendar values
        self.sell_calendar = QCalendarWidget()
        self.sell_calendar.setSelectedDate(self.sellDate)
        layout.addWidget(self.sell_calendar)

        # TODO: create QLabels to show the Stock purchase total
        self.stock_purchase_total = QLabel(f"Purchase Total: $ {self.purchase_total_price:.2f}")
        layout.addWidget(self.stock_purchase_total)

        # TODO: create QLabels to show the Stock sell total
        self.stock_sell_total = QLabel(f"Sell Total :${self.sell_total_price:.2f}")
        layout.addWidget(self.stock_sell_total)

        # TODO: create QLabels to show the Stock profit total
        self.stock_profit_total = QLabel(f"Profit :${self.total_profit:.2f}")
        layout.addWidget(self.stock_profit_total)

        # TODO: set the window title

        self.setLayout(layout)
        self.setWindowTitle('Stock Trade Profit Calculator')
        self.show()

        # TODO: initialize the layout - 6 rows to start

        # TODO: connecting signals to slots so that a change in one control updates the UI
        self.quantity_spinbox.valueChanged.connect(self.updateUi)
        self.stock_combobox.currentTextChanged.connect(self.updateUi)
        self.purchase_calendar.clicked.connect(self.updateUi)
        self.sell_calendar.clicked.connect(self.updateUi)

    def updateUi(self): # TODO: update the UI
        '''
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        try:
            # TODO: get selected dates from calendars
            self.selected_purchase_date = self.purchase_calendar.selectedDate()
            self.selected_sell_date = self.sell_calendar.selectedDate()

            #validation for sale date cannot earlier than purchase date
            if self.selected_sell_date <= self.selected_purchase_date: #if error occur
                self.error_msg = "The sell date cannot earlier than purchase date"
                self.show_error_message()

            else:
                self.get_price()

            if self.active:
                self.purchaseDate = self.selected_purchase_date
                self.sellDate = self.selected_sell_date

            # render new label for purchase date, sell date and both calendar
            self.purchase_date.setText(f"{self.purchaseDate.toString('dd-MM-yyyy')}")
            self.sell_date.setText(f"{self.sellDate.toString('dd-MM-yyyy')}")
            self.purchase_calendar.setSelectedDate(self.purchaseDate)
            self.sell_calendar.setSelectedDate(self.sellDate)

            # TODO: perform necessary calculations to calculate totals
            self.purchase_total_price = self.stock_buy_price  * self.quantity_spinbox.value() # purchase total price
            self.sell_total_price = self.stock_sell_price * self.quantity_spinbox.value() # sell total price
            self.total_profit = self.purchase_total_price - self.sell_total_price #total profit

            # TODO: update the label displaying totals
            self.stock_purchase_total.setText(f'Purchase Total :$ {self.purchase_total_price}') #render label of purchase total
            self.stock_sell_total.setText(f'Sell Total :$ {self.sell_total_price}')  # render label of sell total
            self.stock_profit_total.setText(f'Profit :${self.total_profit}') # render label of total profit

            pass  # placeholder for future code
        except Exception as e:
            print(f"Error in updateUi: {e}")

    def show_error_message(self):
        # Pop up an error message
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText("An error occurred!")
        error_dialog.setInformativeText(self.error_msg)
        error_dialog.setWindowTitle("Error")
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    def get_price(self):
        # setting up dictionary of Stocks and format the date
        data = self.make_data()
        self.error_index = 0
        self.stock_name = self.stock_combobox.currentText()
        purchaseDateTuple = self.string_date_into_tuple(self.selected_purchase_date.toString('dd-MM-yyyy'))
        sellDateTuple = self.string_date_into_tuple(self.selected_sell_date.toString('dd-MM-yyyy'))

        # Retrieve the stock price for the purchase date
        if self.stock_name in data and purchaseDateTuple in data[self.stock_name]:
            self.stock_buy_price = data[self.stock_name][purchaseDateTuple]
        else:
            self.error_msg = (f"No data found for {self.stock_name} on {self.selected_purchase_date.toString('dd-MM-yyyy')}") # to recover if no data found
            self.show_error_message()
            self.error_index += 1

        # Retrieve the stock price for the sell date
        if self.stock_name in data and sellDateTuple in data[self.stock_name]:
            self.stock_sell_price = data[self.stock_name][sellDateTuple]
        else:
            self.error_msg = (f"No data found for {self.stock_name} on {self.selected_sell_date.toString('dd-MM-yyyy')}") # to recover if no data found
            self.show_error_message()
            self.error_index += 1

        if self.error_index > 1:
            self.active = False
        else:
            self.active = True

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
                date_obj = datetime.strptime(date_string, "%d/%m/%Y")
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
