from PyQt6.QtCore import QDate


class MyClass:
    def get_first_stock_date(self):
        if self.stock_name in self.data:
            # The keys are tuples, so no need to parse them
            # Sort the tuples directly
            date_keys = sorted(self.data[self.stock_name].keys())

            # Get the first (earliest) date tuple
            first_date = date_keys[0]

            # Unpack the tuple (year, month, day) and convert it to QDate
            self.sellDefaultDate = QDate(first_date[0], first_date[1], first_date[2])

            print(f'{self.sellDefaultDate.toString("yyyy-MM-dd")}')
        else:
            print("Current stock not found in the dataset. Available stocks:", self.data.keys())
            self.sellDefaultDate = QDate.currentDate()  # Default to the current date


# Example usage
my_instance = MyClass()
my_instance.data = {
    'Amazon': {
        (2024, 5, 1): {},
        (2022, 1, 15): {},
        (2023, 7, 10): {}
    }
}
my_instance.stock_name = 'Amazon'
my_instance.get_first_stock_date()
