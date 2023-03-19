import os
from dotenv import load_dotenv


load_dotenv()

broker_url = os.getenv('BROKER_ADDRESS')
result_backend = os.getenv('DB_ADDRESS')
mongodb_backend_settings = {
    'database': 'celery', 
    'taskmeta_collection': 'tasks'
}
result_serializer = "json"
accept_content = ["application/json"]
timezone = "UTC"
enable_utc = True
include = ['scheduler.tasks']
