class DataBase:
    def __init__ (self):
        self._selected = None
        self._accounts = []

    def set_selected_account (self, id):
        if id is None:
            self._selected = None
            return
        self._selected = self._accounts[int(id)-1]

    def get_selected_account (self):
        selected = self._selected
        if selected is None:
            return None

        # Selected Account Information
        return selected

    def all_accounts (self):
        return self._accounts

    def new_account (self, acc_type):
        id = len(self._accounts) + 1

        if (acc_type == 'checking'):
            new_acc = Checking_Account(id)
        elif (acc_type == 'savings'):
            new_acc = Savings_Account(id)
        else: 
            return
        
        self._accounts.append(new_acc)

class Transactions:
    def __init__(self):
        self._transactions = []

    def add_transaction(self, data, amount):
        self._transactions.append({"data": data, "amount": amount})

    def get_transactions(self):
        return self._transactions

class Account:
    def __init__ (self, id, acc_type):
        self._id = id
        self._balance = 0
        self._type = acc_type
        self.transactions = Transactions()

    def get_balance (self):
        return self._balance
    
    def set_balance (self, amount):
        self._balance += amount
    
    def get_id (self):
        return self._id
    
    def get_type(self):
        return self._type

class Checking_Account (Account):
    def __init__ (self, id):
        super().__init__(id, "Checking") 

class Savings_Account (Account):
    def __init__ (self, id):
        super().__init__(id, "Savings")
        
