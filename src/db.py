import sqlite3
import os

DB_PATH = "database/food_waste.db"

def get_connection():
    """
    Creates and returns a SQLite database connection.
    Ensures database folder exists before connecting.
    """
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH)
