import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("localhost"),
        port=os.getenv("5432"),
        dbname=os.getenv("airfare_index"),
        user=os.getenv("postgres"),
        password=os.getenv("SHUD@05yaaz27"),
    )