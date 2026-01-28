import pandas as pd
from src.db import get_connection, initialize_database

# =========================================================
# LOAD PROVIDERS (CSV → providers)
# =========================================================

def load_providers():
    df = pd.read_csv("data/providers_data.csv")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO providers (
                provider_id,
                name,
                type,
                address,
                city,
                contact
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            int(row["Provider_ID"]),
            row["Name"],
            row["Type"],
            row["Address"],
            row["City"],
            row["Contact"]
        ))

    conn.commit()
    conn.close()


# =========================================================
# LOAD RECEIVERS (CSV → receivers)
# NOTE:
# - CSV receivers are demo / historical
# - Live users create their own receiver profiles
# =========================================================

def load_receivers():
    df = pd.read_csv("data/receivers_data.csv")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO receivers (
                receiver_id,
                name,
                city,
                contact
            )
            VALUES (?, ?, ?, ?)
        """, (
            int(row["Receiver_ID"]),
            row["Name"],
            row["City"],
            row["Contact"]
        ))

    conn.commit()
    conn.close()


# =========================================================
# LOAD FOOD LISTINGS
# =========================================================

def load_food_listings():
    df = pd.read_csv("data/food_listings_data.csv")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO food_listings (
                food_id,
                food_name,
                quantity,
                expiry_date,
                provider_id,
                provider_type,
                location,
                food_type,
                meal_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row["Food_ID"]),
            row["Food_Name"],
            int(row["Quantity"]),
            row["Expiry_Date"],
            int(row["Provider_ID"]),
            row["Provider_Type"],
            row["Location"],
            row["Food_Type"],
            row["Meal_Type"]
        ))

    conn.commit()
    conn.close()


# =========================================================
# LOAD CLAIMS
# =========================================================

def load_claims():
    df = pd.read_csv("data/claims_data.csv")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO claims (
                claim_id,
                food_id,
                receiver_id,
                status,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            int(row["Claim_ID"]),
            int(row["Food_ID"]),
            int(row["Receiver_ID"]),
            row["Status"],
            row["Timestamp"]
        ))

    conn.commit()
    conn.close()


# =========================================================
# MASTER LOADER (RUN ONCE)
# =========================================================

def load_all_data():
    """
    Initializes database and loads demo CSV data.
    Run ONLY ONCE during initial project setup.
    """
    initialize_database()
    load_providers()
    load_receivers()
    load_food_listings()
    load_claims()

    print("✅ Database initialized and demo data loaded successfully")


if __name__ == "__main__":
    load_all_data()
