import sys
import pickle
import decimal
import logging
from datetime import datetime

from decimal import Decimal, setcontext, BasicContext
from exceptions import *

from bank import Bank

# context with ROUND_HALF_UP
setcontext(BasicContext)
logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='error.log', encoding='utf-8', level=logging.DEBUG)

class BankCLI:
    """Driver class for a command-line REPL interface to the Bank application"""

    def __init__(self):
        self._bank = Bank()

        # establishes relationship to Accounts
        self._selected_account = None

        self._choices = {
            "1": self._open_account,
            "2": self._summary,
            "3": self._select,
            "4": self._add_transaction,
            "5": self._list_transactions,
            "6": self._monthly_triggers,
            "7": self._save,
            "8": self._load,
            "9": self._quit,
        }

    def _display_menu(self):
        print(f"""--------------------------------
Currently selected account: {self._selected_account}
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

    def run(self):
        """Display the menu and respond to choices."""

        while True:
            try:
                self._display_menu()
                choice = input(">")
                action = self._choices.get(choice)

                # expecting a digit 1-9
                if action:
                    action()
                else:
                    # not officially part of spec since we don't give invalid options
                    print("{0} is not a valid choice".format(choice))
            except AttributeError:      
                print("This command requires that you first select an account.")

    def _summary(self):
        # dependency on Account objects
        for x in self._bank.show_accounts():
            print(x)

    def _load(self):
        with open("bank.pickle", "rb") as f:
            self._bank = pickle.load(f)
        # clearing the selected account so it doesn't get out of sync with the new account objects loaded from the pickle file
        self._selected_account = None
        logging.debug("Loaded from bank.pickle")

    def _save(self):
        with open("bank.pickle", "wb") as f:
            pickle.dump(self._bank, f)
        logging.debug("Saved to bank.pickle")

    def _quit(self):
        sys.exit(0)

    def _add_transaction(self):
        if self._selected_account is None:
            raise AttributeError("This command requires that you first select an account.")
        
        # Latest Transaction Date Const
        all_transactions = self._selected_account.get_transactions()
        if (all_transactions):
            latest_date = max(all_transactions).get_date()

        while True:
            # Amound Exception
            while True:
                try:
                    amount = input("Amount?\n>")
                    amount = Decimal(amount)
                    break
                except decimal.InvalidOperation:
                    print("Please try again with a valid dollar amount.")

            # Date Exception
            while True:
                try:
                    date = input("Date? (YYYY-MM-DD)\n>")
                    date = datetime.strptime(date, "%Y-%m-%d").date()

                    if (all_transactions and date < latest_date):
                        raise TransactionSequenceError(latest_date)
                    break
                except ValueError:
                    print("Please try again with a valid date in the format YYYY-MM-DD.")
                except TransactionSequenceError as seq:
                    print(f"New transactions must be from {seq.latest_date} onward.")
            
            # Adding Exceptions
            try:
                self._selected_account.add_transaction(amount, date)
                break
            except OverdrawError as error:
                print(error.message)
            except TransactionLimitError as transaction:
                if (transaction.times_today >= 2):
                    print("This transaction could not be completed because this account already has 2 transactions in this day.")
                elif (transaction.times_this_month >= 5):
                    print("This transaction could not be completed because this account already has 5 transactions in this month.")
                break

    def _open_account(self):
        acct_type = input("Type of account? (checking/savings)\n>")
        self._bank.add_account(acct_type)

    def _select(self):
        # Note: in the PSet were no clarification about the output in this case
        num = input("Enter account number\n>")
        try:
            num = int(num)
        except:
            return

        self._selected_account = self._bank.get_account(num)

    def _monthly_triggers(self):
        try:
            self._selected_account.assess_interest_and_fees()
            logging.debug("Triggered interest and fees")
        except TransactionSequenceError as seq:
            month = seq.latest_date.strftime("%B")
            print(f"Cannot apply interest and fees again in the month of {month}.")

    def _list_transactions(self):
        if self._selected_account is None:
            raise AttributeError("This command requires that you first select an account.")

        for t in self._selected_account.get_transactions():
            print(t)


if __name__ == "__main__":
    try:
        BankCLI().run()
    except Exception as e:
        error_message = repr(e).replace('\n', '\\n')
        print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        logging.error(error_message)
        sys.exit(1)
