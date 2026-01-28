import sqlite3
import os

# =========================================================
# DATABASE CONFIG
# =========================================================

DB_FOLDER = "database"
DB_PATH = os.path.join(DB_FOLDER, "food_waste.db")


# =========================================================
# CONNECTION
# =========================================================

def get_connection():
    """
    Creates and returns a SQLite database connection.
    Ensures database folder exists.
    Enables foreign key constraints.
    """
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# =========================================================
# TABLE CREATION
# =========================================================

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            linked_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_providers_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    Receiver profile created by logged-in users.
    One-to-one mapping with users table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receivers (
            receiver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            contact TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()


def create_food_listings_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_listings (
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            expiry_date TEXT NOT NULL,
            provider_id INTEGER,
            provider_type TEXT,
            location TEXT NOT NULL,
            food_type TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(provider_id) REFERENCES providers(provider_id)
        )
    """)

    conn.commit()
    conn.close()


def create_claims_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('Pending','Completed','Cancelled')) NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(food_id) REFERENCES food_listings(food_id),
            FOREIGN KEY(receiver_id) REFERENCES receivers(receiver_id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# DATABASE INITIALIZER
# =========================================================

def initialize_database():
    """
    Initializes all database tables.
    Safe to call multiple times (idempotent).
    """
    create_users_table()
    create_providers_table()
    create_receivers_table()
    create_food_listings_table()
    create_claims_table()
