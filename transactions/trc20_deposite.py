import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()

WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
LIMITE = 200    # number of transactions per page, default 20, max 200


def request_transactions(min_timestamp: int, max_timestamp: int) -> dict:
    """
    get only confirmed transactions to wallet address between min_timestamp and max_timestamp over TRC20
    """
    url = f"https://api.trongrid.io/v1/accounts/{WALLET_ADDRESS}/transactions/trc20?&contract_address=TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&only_to=true&only_confirmed=true&limit={LIMITE}&min_timestamp={min_timestamp}&max_timestamp={max_timestamp}"
    headers = {"accept": "application/json"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        res = res.json()
    else:
        res = {
            "data": list(),
            "success": False,
            "meta": {
                "at": round(time.time()*10**3),
                "page_size": 0
            }
        }
    return res


def get_page_size(response: dict) -> int:
    """
    returns response page size
    """
    if "meta" in response:
        return response["meta"].get("page_size", 0)
    return 0


def remove_duplicates(transactions: list) -> list:
    """
    remove duplicate transactions
    """
    seen_items = set()
    new_list = list()
    for obj in transactions:
        if obj["transaction_id"] not in seen_items:
            new_list.append(obj)
            seen_items.add(obj["transaction_id"])
    return new_list


def get_transactions(*args, **kwargs) -> list:
    """
    kwargs:
        wallet_address
        max_timestamp
        min_timestamp
    send few requests to gather all transactions 
    """
    transactions = list()
    res = request_transactions(*args, **kwargs)
    transactions.extend(res.get("data", list()))
    page_size = get_page_size(res)
    if page_size == LIMITE:
        last_timestamp = transactions[-1]["block_timestamp"]
        min_timestamp = kwargs.get("min_timestamp")
        while page_size == LIMITE:
            res = request_transactions(
                max_timestamp=last_timestamp,
                min_timestamp=min_timestamp
            )
            transactions.extend(res.get("data", list()))
            last_timestamp = transactions[-1]["block_timestamp"]
            page_size = get_page_size(res)
    transactions = remove_duplicates(transactions)
    return transactions
