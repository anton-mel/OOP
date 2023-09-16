import sys
import pickle
from dataBase import DataBase

# Define a class called Bank to manage banking operations.
class Bank:
    def __init__(self):
        # Initialize the Bank with a DataBase instance.
        self._db = DataBase()

    # Method to open a new bank account.
    def _open_account(self):
        acc_type = input("Type of account? (checking/savings)\n>")
        self._db.new_account(acc_type)

    # Method to show a summary of all accounts.
    def _show_summary(self):
        accounts = self._db.all_accounts()
        for acc in accounts:
            print(f"{acc.get_type()}#{str(acc.get_id()).zfill(9)},\tbalance: ${acc.get_balance():.2f}")

    # Method to select an account by entering its account number.
    def _select_account(self):
        if len(self._db.all_accounts()) == 0:
            return

        id = input("Enter account number\n>")
        self._db.set_selected_account(id)

    # Method to add a transaction to the selected account.
    def _add_transaction(self):
        amount = float(input("Amount?\n>"))
        data = input("Date? (YYYY-MM-DD)\n>")

        selected = self._db.get_selected_account()

        if selected is None:
            print("Extra check: No account selected.")
            return

        transaction_list = selected.transactions.get_transactions()

        if (selected.get_balance() + amount < 0):
            return

        if (selected.get_type() == "Savings"):
            times_today = 0
            times_month = 0

            for transaction in transaction_list:
                if transaction[1] == data:
                    times_today += 1
                if transaction[1].split("-")[:1] == data.split("-")[:1]:
                    times_month += 1

            if (times_today >= 2 or times_month > 5):
                return

        transaction_list.append((amount, data))
        selected.set_balance(amount)

    # Method to list transactions for the selected account, sorted by date.
    def _list_transactions(self):
        selected = self._db.get_selected_account()

        if selected is None:
            print("Extra check: No account selected.")
            return

        transaction_list = selected.transactions.get_transactions()

        # Bubble Sort to sort transactions by date.
        for i in range(len(transaction_list) - 1):
            for j in range(0, len(transaction_list) - i - 1):
                date1 = transaction_list[j][1]
                date2 = transaction_list[j + 1][1]

                if date1 > date2:
                    transaction_list[j], transaction_list[j + 1] = transaction_list[j + 1], transaction_list[j]

        # Print the sorted list of transactions.
        for transaction in transaction_list:
            # print(transaction[0]) round correctly!
            print(f"{transaction[1]}, ${transaction[0]:.2f}")

    # Method to calculate interest and fees for the selected account.
    def _calculate_interest_and_fees(self):
        selected = self._db.get_selected_account()
        lastdays = {
            "01": "31",
            "02": "28",
            "03": "31",
            "04": "30",
            "05": "31",
            "06": "30",
            "07": "31",
            "08": "31",
            "09": "30",
            "10": "31",
            "11": "30",
            "12": "31"
        }

        if selected is None:
            print("Extra check: No account selected.")
            return

        transaction_list = selected.transactions.get_transactions()
        fee = 0
        interest = 0

        if (selected.get_type() == "Savings"):
            interest = 0.41
        elif (selected.get_type() == "Checking"):
            interest = 0.08
            fee = -5.44

        upd_balance = selected.get_balance() * (interest / 100)
        new_balance = selected.get_balance() * (1 + interest / 100)

        lastday = lastdays.get(transaction_list[-1][1].split("-")[1])

        transaction_list.append((upd_balance, "-".join(transaction_list[-1][1].split("-")[:2] + [lastday])))
        if (new_balance < 100):
            upd_balance += fee
        transaction_list.append((fee, "-".join(transaction_list[-1][1].split("-")[:2] + [lastday])))
        selected.set_balance(upd_balance)

    # Method to save the current database to a file.
    def _save(self):
        with open("SavedAccount.txt", 'wb') as file:
            pickle.dump(self._db, file)

    # Method to load a saved database from a file.
    def _load(self):
        try:
            with open("SavedAccount.txt", 'rb') as file:
                self._db = pickle.load(file)
                self._db.set_selected_account(None)
        except FileNotFoundError:
            return

    # Method to quit the bank application.
    def _quit(self):
        sys.exit(0)

    # Method to get the selected account from the database.
    def get_selected_account(self):
        return self._db.get_selected_account()
