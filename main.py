"""
main.py
---------
Initializes database tables and loads initial CSV data.
Run this file ONLY ONCE during project setup.
"""

from src.db import initialize_database
from src.load_data import load_all_data


def main():
    print("🚀 Initializing database...")
    initialize_database()

    print("📥 Loading initial dataset...")
    load_all_data()

    print("✅ Database setup and data loading completed successfully!")


if __name__ == "__main__":
    main()
