from PyQt6.QtWidgets import *
from gui import *
import csv



class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        """Initializes the GUI and connects button actions
        :return: None
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.create_file()

        self.ui.add_btn.clicked.connect(self.add_expense)
        self.ui.summary_btn.clicked.connect(self.show_summary)
        self.ui.clear_btn.clicked.connect(self.clear_fields)

    def create_file(self) -> None: #ai recommended this section to make my code clearer
        """Ensures the CSV file exists with a header row
        :return: None
        """
        try:
            with open("expenses.csv", "r"):
                pass
        except FileNotFoundError:
            with open("expenses.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Expense Name", "Amount", "Category"])

    def valid_name(self, name: str) -> bool: #ai help me make my first validation and that helped me with the rest
        """Checks that the expense name is not empty
        :param name: The expense name input
        :return: True if valid, False otherwise
        """
        return name.strip() != ""

    def valid_amount(self, amount_text: str):
        """Validates that the amount is numeric and positive
        :param amount_text: The amount input as text
        :return: Tuple (is_valid, value or message)
        """
        try:
            amount = float(amount_text)
        except ValueError:
            return False, "Amount must be a number."

        if amount <= 0:
            return False, "Amount must be positive."

        return True, amount

    def add_expense(self) -> None:
        """Validates input and saves a new expense
        :return: None
        """
        name = self.ui.expense_input.text()
        amount_text = self.ui.amount_input.text()
        category = self.ui.category_box.currentText()

        if not self.valid_name(name):
            self.show_message("Expense name cannot be empty.", "red")
            return

        result = self.valid_amount(amount_text)

        if result[0] == False:
            self.show_message(result[1], "red")
            return

        amount = result[1]

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name.strip(), f"{amount:.2f}", category])

        self.show_message("Expense added successfully.", "green")
        self.clear_inputs_only() #i used google to find how to change my message color

    def show_summary(self) -> None:
        """Calculates and displays total and category expenses
        :return: None
        """
        totals = {
            "Food": 0.0,
            "Gas": 0.0,
            "Shopping": 0.0,
            "Bills": 0.0,
            "Debt": 0.0,
            "Others": 0.0,
        }

        total = 0.0

        try:
            with open("expenses.csv", "r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)

                for row in reader:
                    try:
                        amount = float(row[1])
                        category = row[2]

                        total += amount
                        if category in totals:
                            totals[category] += amount
                    except:
                        continue
        except FileNotFoundError:
            self.create_file()

        message = (
            f"Total: ${total:.2f} | "
            f"Food: ${totals['Food']:.2f} | "
            f"Gas: ${totals['Gas']:.2f} | "
            f"Shopping: ${totals['Shopping']:.2f} | "
            f"Bills: ${totals['Bills']:.2f} | "
            f"Debt: ${totals['Debt']:.2f} | "
            f"Others: ${totals['Others']:.2f}"
        )

        self.show_message(message, "white")

    def clear_inputs_only(self) -> None:
        """Clears input fields without clearing the message label
        :return: None
        """
        self.ui.expense_input.clear()
        self.ui.amount_input.clear()
        self.ui.category_box.setCurrentIndex(0)

    def clear_fields(self) -> None:
        """Clears input fields and the message label
        :return: None
        """
        self.clear_inputs_only()
        self.ui.message_label.clear()

    def show_message(self, text: str, color: str) -> None:
        """Displays a message in the UI with a given color
        :param text: Message to display
        :param color: Color of the message text
        :return: None
        """
        self.ui.message_label.setStyleSheet(f"color: {color};")
        self.ui.message_label.setText(text)