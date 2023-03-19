import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

DB_ADDRESS = os.getenv('DB_ADDRESS')


class DB:
    """
    mongodb manager
    """
    client = MongoClient(DB_ADDRESS)
    db = client["telegram_game_bot"]

    @classmethod
    def initial_db(cls) -> None:
        col = cls.db["deposite_transactions"]
        col.create_index([('transaction_id', 1)], unique=True,
                         name="transaction_unq_idx")
        col = cls.db["deposite_announce"]
        col.create_index([('transaction_id', 1)], unique=True,
                         name="user_transaction_unq_idx")

    @classmethod
    def insert_transactions(cls, transactions: list) -> None:
        col = cls.db["deposite_transactions"]
        try:
            col.insert_many(transactions, ordered=False)
        except:
            pass

    @classmethod
    def last_transaction_timestamp(cls) -> int:
        col = cls.db["deposite_transactions"]
        query = [
            {
                '$sort': {
                    'block_timestamp': -1
                }
            }, {
                '$project': {
                    '_id': 0,
                    'block_timestamp': 1
                }
            }
        ]
        res = col.aggregate(query)
        return next(res, dict()).get('block_timestamp', 0)

    @classmethod
    def get_transaction(cls, transaction_id: str) -> dict:
        col = cls.db["deposite_transactions"]
        res = col.find_one({"transaction_id": transaction_id})
        if res:
            return res
        return dict()

    @classmethod
    def get_deposite_announce(cls, transaction_id: str) -> dict:
        col = cls.db["deposite_announce"]
        res = col.find_one({"transaction_id": transaction_id})
        if res:
            return res
        return dict() 
    
    @classmethod
    def make_deposite_announce(cls, user_id: str, transaction_id: str) -> dict:
        col = cls.db["deposite_announce"]
        try:
            col.insert_one({"user_id":user_id, "transaction_id": transaction_id, "is_accepted": False})
        except:
            pass


if __name__ == "__main__":
    DB.initial_db()