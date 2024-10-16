import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up a button to trigger the error message
        self.button = QPushButton("Trigger Error", self)
        self.button.clicked.connect(self.show_error_message)
        self.setCentralWidget(self.button)

    def show_error_message(self):
        # Pop up an error message
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText("An error occurred!")
        error_dialog.setInformativeText("Please check the input and try again.")
        error_dialog.setWindowTitle("Error")
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    sys.exit(app.exec())
