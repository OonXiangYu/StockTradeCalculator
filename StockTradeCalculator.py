import sys
import csv

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QSpinBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QMessageBox, QPushButton, QCheckBox
from datetime import datetime
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

# Create a simple Matplotlib canvas class
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot_bar_chart(self, categories, profits, bg_colour='black'):
        self.axes.clear()  # Clear previous plot
        self.axes.set_facecolor(bg_colour)  # Set background color
        self.axes.bar(categories, profits)
        self.axes.set_title('Profit Bar Chart')
        self.axes.set_xlabel('Categories')
        self.axes.set_ylabel('Values')
        self.axes.tick_params(axis='x', labelsize=6) # Font size
        self.draw()

    def plot_line_graph(self, stockName, dates, prices):
        dates = [datetime(year, month, day) for year, month, day in dates]

        self.axes.plot(dates, prices, linestyle='-', color='b')
        self.axes.set_title(f"Growth Line Graph of {stockName} per Unit")
        self.axes.set_xlabel('Date')
        self.axes.set_ylabel('Price')

        # Format the x-axis to show dates nicely
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.xaxis.set_major_locator(mdates.DayLocator())# Set major ticks to be every day

        # Rotate date labels for better readability
        self.figure.autofmt_xdate()

        self.axes.tick_params(axis='x', labelsize=6) # Font size

        self.draw()


class GraphWindow(QMainWindow):
    def __init__(self, categories, purchase_date_parameter, sell_date_parameter, quantity,bg_colour='black'):
        super().__init__()
        self.setWindowTitle("Bar Chart for Comparison")
        self.setGeometry(200, 200, 600, 400)

        # Setting up dictionary of Stocks
        self.data_getter = StockDataReader()
        self.data = self.data_getter.make_data()

        # Assign variable
        self.purchase_date = purchase_date_parameter
        self.sell_date = sell_date_parameter
        self.amount = quantity
        self.category_profit = {}  # Dictionary to hold category and profit pairs
        self.category_profit[categories] = self.get_price(categories, quantity)

        # Layout of graph
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        checkboxes_layout = QHBoxLayout()

        # Add the checkbox except the stock you selected on the calculator
        for stock_name in self.data.keys():
            if stock_name != categories:
                checkbox = QCheckBox(stock_name, self)
                checkboxes_layout.addWidget(checkbox)  # Add the checkbox to the layout
                checkbox.stateChanged.connect(self.checkBox_state_changed) # Connect to event

        layout.addLayout(checkboxes_layout)

        self.canvas = MatplotlibCanvas(self)
        layout.addWidget(self.canvas)

        # Plot the bar chart
        self.update_plot()

    def checkBox_state_changed(self):
        sender = self.sender()  # Get the checkbox that triggered the event
        category = sender.text()

        if sender.isChecked():
            self.category_profit[category] = self.get_price(category, self.amount)
            self.update_plot() # Update chart
        else:
            # Remove the category if the checkbox is unchecked
            if category in self.category_profit:
                del self.category_profit[category]  # Remove the category and its profit
                self.update_plot() # Update chart

    def get_price(self, stock, quantity):
        # setting up dictionary of Stocks and format the date
        self.data_reader = StockDataReader()
        data = self.data_reader.make_data()
        purchaseDateTuple = self.data_reader.string_date_into_tuple(self.purchase_date.toString('dd-MM-yyyy'))
        sellDateTuple = self.data_reader.string_date_into_tuple(self.sell_date.toString('dd-MM-yyyy'))
        self.stock_buy_price = data[stock][purchaseDateTuple]
        self.stock_sell_price = data[stock][sellDateTuple]
        total =  self.stock_sell_price * quantity - self.stock_buy_price * quantity
        return total

    def update_plot(self):
        categories = list(self.category_profit.keys())
        profits = list(self.category_profit.values())

        # Call the plot_bar_chart method in the Canvas class
        self.canvas.plot_bar_chart(categories, profits, bg_colour='black')

class LineGraphWindow(QMainWindow):
    def __init__(self, stock_name_parameter, purchase_date_parameter, sell_date_parameter):
        super().__init__()
        self.setWindowTitle("Line Graph for Stock Growth")
        self.setGeometry(100, 100, 600, 400)

        # Setting up dictionary of Stocks
        self.data_getter = StockDataReader()
        self.data = self.data_getter.make_data()

        # Assign value
        dates = []
        prices = []

        # Create a QWidget for the central widget
        widget = QWidget()
        self.setCentralWidget(widget)

        # Set up the layout
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.canvas = MatplotlibCanvas(self)
        layout.addWidget(self.canvas)

        # Filter the stock data between the given date range
        price_per_unit = {date: price for date, price in self.data[stock_name_parameter].items() if purchase_date_parameter <= date <= sell_date_parameter}

        for date, price in price_per_unit.items():
            dates.append(date)
            prices.append(price)

        # Plot the data
        self.canvas.plot_line_graph(stock_name_parameter, dates, prices)


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
        self.data_reader = StockDataReader()
        self.data = self.data_reader.make_data()

        # TODO: initialize the layout - 6 rows to start
        # Initialize the layout
        layout = QVBoxLayout(self)

        # Assign variable
        self.purchase_total_price = 0
        self.sell_total_price = 0
        self.total_profit = 0
        self.stock_buy_price = 0
        self.stock_sell_price = 0
        self.purchase_active = False
        self.sell_active = False

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
        # Check if current stock exists, if not, handle it gracefully
        if self.stock_name in self.data:
            self.sellDefaultDate = list(self.data[self.stock_name].keys())[0]
            self.purchaseDefaultDate = list(self.data[self.stock_name].keys())[1]
            self.sellDate = QDate(self.sellDefaultDate[0],self.sellDefaultDate[1],self.sellDefaultDate[2]) # Tuple convert to datetime obj
            self.purchaseDate = QDate(self.purchaseDefaultDate[0], self.purchaseDefaultDate[1],self.purchaseDefaultDate[2])  # Tuple convert to datetime obj
            print(f'{self.sellDate}, {self.purchaseDate}')
        else:
            print("Current stock not found in the dataset. Available stocks:", self.data.keys())
            self.sellDate = QDate.currentDate()  # Default to the current date
            self.purchaseDate = QDate.currentDate()

        # TODO: create QLabel for Quantity selection
        # Quantity selection label
        self.quantity_label = QLabel("Quantity:")
        layout.addWidget(self.quantity_label)

        # TODO: create QSpinBox to select Stock quantity purchased
        #Quantity select SpinBox
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setMaximum(10000)
        layout.addWidget(self.quantity_spinbox)

        #  status of data browse
        self.purchase_date_status = QLabel()
        layout.addWidget(self.purchase_date_status)

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

        # status of data browse
        self.sell_date_status = QLabel()
        layout.addWidget(self.sell_date_status)

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

        # A button to confirm your selection
        self.confirm_button = QPushButton("Calculate")
        layout.addWidget(self.confirm_button)

        # Initialize the UI
        self.updateCalendarUi()

        # TODO: connecting signals to slots so that a change in one control updates the UI
        self.confirm_button.clicked.connect(self.updateUi)
        self.purchase_calendar.clicked.connect(self.updateCalendarUi)
        self.sell_calendar.clicked.connect(self.updateCalendarUi)

        # TODO: set the window title
        self.setLayout(layout)
        self.setWindowTitle('Stock Trade Profit Calculator')
        self.show()

    def updateCalendarUi(self):
        # TODO: get selected dates from calendars
        self.selected_purchase_date = self.purchase_calendar.selectedDate()
        self.selected_sell_date = self.sell_calendar.selectedDate()

        # validation for sale date cannot earlier than purchase date
        if self.selected_sell_date <= self.selected_purchase_date:  # if error occur
            self.error_msg = "The sell date cannot earlier than purchase date"
            self.show_error_message()
            self.purchase_calendar.setSelectedDate(self.purchaseDate) # to recover the calendar
            self.sell_calendar.setSelectedDate(self.sellDate)

        else:
            self.get_price()
            self.purchaseDate = self.selected_purchase_date
            self.sellDate = self.selected_sell_date

            # render new label for purchase date, sell date and both calendar
            self.purchase_date.setText(f"{self.purchaseDate.toString('dd-MM-yyyy')}")
            self.sell_date.setText(f"{self.sellDate.toString('dd-MM-yyyy')}")
            self.purchase_calendar.setSelectedDate(self.purchaseDate)
            self.sell_calendar.setSelectedDate(self.sellDate)


    def updateUi(self): # TODO: update the UI
        '''
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        # Setting up data class
        self.tuple_convertor = StockDataReader()

        try:
            if self.quantity_spinbox.value() <= 0: # Validation for quantity
                self.error_msg = "Stock quantity must greater than 0"
                self.show_error_message()

            elif self.purchase_active and self.sell_active: # Both data found
                self.get_price()

                # TODO: perform necessary calculations to calculate totals
                self.purchase_total_price = self.stock_buy_price  * self.quantity_spinbox.value() # purchase total price
                self.sell_total_price = self.stock_sell_price * self.quantity_spinbox.value() # sell total price
                self.total_profit = self.sell_total_price - self.purchase_total_price #total profit

                # TODO: update the label displaying totals
                self.stock_purchase_total.setText(f"Purchase Total: $ {self.purchase_total_price:.2f}") #render label of purchase total
                self.stock_sell_total.setText(f"Sell Total :${self.sell_total_price:.2f}")  # render label of sell total
                self.stock_profit_total.setText(f"Profit :${self.total_profit:.2f}") # render label of total profit

                purchaseDateTuple = self.tuple_convertor.string_date_into_tuple(self.purchaseDate.toString('dd-MM-yyyy'))
                sellDateTuple = self.tuple_convertor.string_date_into_tuple(self.sellDate.toString('dd-MM-yyyy'))
                self.show_line_graph(purchaseDateTuple, sellDateTuple)
                self.show_graph()

            else:
                self.error_msg = "Please select a date that contain data"
                self.show_error_message()
                self.purchase_calendar.setSelectedDate(self.purchaseDate)  # to recover the calendar
                self.sell_calendar.setSelectedDate(self.sellDate)

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

    def show_graph(self):
        # Create and show the graph window
        self.quantity = self.quantity_spinbox.value()
        self.graph_window = GraphWindow(self.stock_name, self.purchaseDate, self.sellDate, self.quantity)
        self.graph_window.show()

    def show_line_graph(self, purchase_date, sell_date):
        # Create and show the line graph
        self.line_graph_window = LineGraphWindow(self.stock_name, purchase_date, sell_date)
        self.line_graph_window.show()

    def get_price(self):
        # setting up dictionary of Stocks and format the date
        self.data_reader = StockDataReader()
        data = self.data_reader.make_data()
        self.stock_name = self.stock_combobox.currentText()
        purchaseDateTuple = self.data_reader.string_date_into_tuple(self.selected_purchase_date.toString('dd-MM-yyyy'))
        sellDateTuple = self.data_reader.string_date_into_tuple(self.selected_sell_date.toString('dd-MM-yyyy'))

        # Retrieve the stock price for the purchase date
        if self.stock_name in data and purchaseDateTuple in data[self.stock_name]:
            self.stock_buy_price = data[self.stock_name][purchaseDateTuple]
            self.purchase_date_status.setText("Data found")
            self.purchase_date_status.setStyleSheet("QLabel { color : green; }")
            self.purchase_active = True
        else:
            self.stock_buy_price = 0
            self.purchase_active = False
            self.purchase_date_status.setText("No data found")
            self.purchase_date_status.setStyleSheet("QLabel { color : red; }")

        # Retrieve the stock price for the sell date
        if self.stock_name in data and sellDateTuple in data[self.stock_name]:
            self.stock_sell_price = data[self.stock_name][sellDateTuple]
            self.sell_date_status.setText("Data found")
            self.sell_date_status.setStyleSheet("QLabel { color : green; }")
            self.sell_active = True
        else:
            self.stock_sell_price = 0
            self.sell_active = False
            self.sell_date_status.setText("No data found")
            self.sell_date_status.setStyleSheet("QLabel { color : red; }")

class StockDataReader():
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
    stock_calculator.show()
    sys.exit(app.exec())
# This is complete
if __name__ == '__main__':
        main()
