import time
from db.mongo import DB
from transactions.trc20_deposite import get_transactions



def load_transactions():
    """
    get transactions and insert them to db
    repeat interval: 30(s)
    """
    last_ts = DB.last_transaction_timestamp()
    current_ts = round(time.time()*10**3)
    transactions = get_transactions(last_ts, current_ts)
    DB.insert_transactions(transactions)

load_transactions()