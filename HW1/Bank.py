import sys
import pickle
from DataBase import DataBase

class Bank:
    def __init__(self):
        self._db = DataBase()

    def _open_account (self):
        acc_type = input("Type of account? (checking/savings)\n>")
        self._db.new_account(acc_type)

    def _show_summary (self):
        accounts = self._db.all_accounts()
        for acc in accounts:
            print(f"{acc.get_type()}#{str(acc.get_id()).zfill(9)},\tbalance: ${acc.get_balance():.2f}")

    def _select_account (self):
        if len(self._db.all_accounts()) == 0:
            return

        id = input("Enter account number\n>")
        self._db.set_selected_account(id)

    def _add_transaction (self):
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

    def _list_transactions (self):
        selected = self._db.get_selected_account()

        if selected is None:
            print("Extra check: No account selected.")
            return

        transaction_list = selected.transactions.get_transactions()

        #  Buble Sort
        for i in range(len(transaction_list) - 1):
            for j in range(0, len(transaction_list) - i - 1):
                date1 = transaction_list[j][1]
                date2 = transaction_list[j + 1][1]

                if date1 > date2:
                    transaction_list[j], transaction_list[j + 1] = transaction_list[j + 1], transaction_list[j]

        # Print Sorted List
        for transaction in transaction_list:
            print(f"{transaction[1]}, ${transaction[0]:.2f}")

    def _calculate_interest_and_fees (self):
        selected = self._db.get_selected_account()

        if selected is None:
            print("Extra check: No account selected.")
            return

        transaction_list = selected.transactions.get_transactions()
        fee = 0; int = 0

        if (selected.get_type() == "Savings"):
            int = .41
        elif (selected.get_type() == "Checking"):
            int = .08
            fee = -5.44

        upd_balance = selected.get_balance() * (int / 100)
        new_balance = selected.get_balance() * (1 + int / 100)

        transaction_list.append((upd_balance, "-".join(transaction_list[-1][1].split("-")[:2] + ["30"])))
        if (new_balance < 100):
            upd_balance += fee
        transaction_list.append((fee, "-".join(transaction_list[-1][1].split("-")[:2] + ["30"])))
        selected.set_balance(upd_balance)

    def _save (self):
        with open("SavedAccount.txt", 'wb') as file:
            pickle.dump(self._db, file)

    def _load (self):
        try:
            with open("SavedAccount.txt", 'rb') as file:
                self._db = pickle.load(file)
                self._db.set_selected_account(None)
        except FileNotFoundError:
            return

    def _quit (self):
        sys.exit(0)

    def get_selected_account (self): 
        return self._db.get_selected_account()
