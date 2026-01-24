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


def create_providers_table():
    """
    Creates the providers table in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            provider_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            address TEXT,
            city TEXT,
            contact TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_receivers_table():
    """
    Creates the receivers table in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receivers (
            receiver_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            city TEXT,
            contact TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_food_listings_table():
    """
    Creates the food_listings table in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_listings (
            food_id INTEGER PRIMARY KEY,
            food_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT,
            provider_id INTEGER,
            provider_type TEXT,
            location TEXT,
            food_type TEXT,
            meal_type TEXT
        )
    """)

    conn.commit()
    conn.close()

def create_claims_table():
    """
    Creates the claims table in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            claim_id INTEGER PRIMARY KEY,
            food_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
