from bank import Bank

# Define a class called BankCLI to create a command-line interface for banking operations.
class BankCLI:
    def __init__(self):
        # Initialize the BankCLI with an instance of the Bank class.
        self._bank = Bank()
        # Define a dictionary to map user input choices to corresponding Bank methods.
        self._choices = {
            "1": self._bank._open_account,
            "2": self._bank._show_summary,
            "3": self._bank._select_account,
            "4": self._bank._add_transaction,
            "5": self._bank._list_transactions,
            "6": self._bank._calculate_interest_and_fees,
            "7": self._bank._save,
            "8": self._bank._load,
            "9": self._bank._quit,
        }

    # Method to display the menu of available banking operations.
    def _display_menu(self):
        selected = self._bank.get_selected_account()

        if selected is not None:
            selected = f"{selected.get_type()}#{str(selected.get_id()).zfill(9)},\tbalance: ${selected.get_balance():.2f}"

        print("--------------------------------")
        print(
f"""Currently selected account: {selected}
Enter command
1: open account
2: summary
3: select account
4: add transaction
5: list transactions
6: interest and fees
7: save
8: load
9: quit""")

    # Method to run the BankCLI, allowing users to input commands and perform operations.
    def run(self):
        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)

            action()

if __name__ == "__main__":
    # Create an instance of the BankCLI class and run the CLI application.
    account_manager = BankCLI()
    account_manager.run()
