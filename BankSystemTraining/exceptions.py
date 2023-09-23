
class OverdrawError(Exception):
    """Custom exception for overdrawn accounts."""
    def __init__ (self, message):
        self.message = message

class TransactionSequenceError(Exception):
    """Custom exception for the transaction order."""
    def __init__ (self, latest_date):
        self.latest_date = latest_date

class TransactionLimitError(Exception):
    """Custom exception for the transaction limit by date."""
    def __init__(self, times_today, times_this_month):
        self.times_today = times_today
        self.times_this_month = times_this_month
