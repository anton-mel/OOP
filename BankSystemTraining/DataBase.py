class DataBase:
    # initialize DataBase
    def __init__ (self):
        self._selected = None
        self._accounts = []

    # Method to set the selected account by its ID.
    def set_selected_account (self, id):
        if id is None:
            self._selected = None
            return
        self._selected = self._accounts[int(id)-1]

    # Method to get the currently selected account.
    def get_selected_account (self):
        selected = self._selected
        if selected is None:
            return None
        return selected

    # Method to return all accounts in the database.
    def all_accounts (self):
        return self._accounts

    # Method to create a new account based on the account type ('checking' or 'savings').
    def new_account (self, acc_type):
        id = len(self._accounts) + 1

        # Depending on the account type, create a Checking_Account or Savings_Account object.
        if (acc_type == 'checking'):
            new_acc = Checking_Account(id)
        elif (acc_type == 'savings'):
            new_acc = Savings_Account(id)
        else: 
            return
        
        # Append the newly created account to the list of accounts.
        self._accounts.append(new_acc)

# Define a class called Transactions to manage transaction records.
class Transactions:
    def __init__(self):
        # Initialize an empty list to store transaction data.
        self._transactions = []

    # Method to add a new transaction with data and amount.
    def add_transaction(self, data, amount):
        self._transactions.append({"data": data, "amount": amount})

    # Method to get all transactions.
    def get_transactions(self):
        return self._transactions

# Define a base class called Account to represent bank accounts.
class Account:
    def __init__ (self, id, acc_type):
        # Initialize the account ID, balance, account type, and a Transactions object.
        self._id = id
        self._balance = 0
        self._type = acc_type
        self.transactions = Transactions()

    # Method to get the current balance of the account.
    def get_balance (self):
        return self._balance
    
    # Method to set the balance of the account.
    def set_balance (self, amount):
        self._balance += amount
    
    # Method to get the account ID.
    def get_id (self):
        return self._id
    
    # Method to get the account type.
    def get_type(self):
        return self._type

# Define a subclass Checking_Account that inherits from the Account class.
class Checking_Account (Account):
    def __init__ (self, *args, **kwargs):
        # Initialize a Checking_Account by calling the parent class's constructor with the account type 'Checking'.
        super().__init__(*args, "Checking") 

# Define a subclass Savings_Account that inherits from the Account class.
class Savings_Account (Account):
    def __init__ (self, *args, **kwargs):
        # Initialize a Savings_Account by calling the parent class's constructor with the account type 'Savings'.
        super().__init__(*args, "Savings")
