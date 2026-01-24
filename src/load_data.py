import pandas as pd
from src.db import get_connection

def load_providers():
    """
    Loads providers data from CSV into the providers table.
    """
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
            ) VALUES (?, ?, ?, ?, ?, ?)
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
    
    

def load_receivers():
    """
    Loads receivers data from CSV into the receivers table.
    """
    df = pd.read_csv("data/receivers_data.csv")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO receivers (
                receiver_id,
                name,
                type,
                city,
                contact
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            int(row["Receiver_ID"]),
            row["Name"],
            row["Type"],
            row["City"],
            row["Contact"]
        ))

    conn.commit()
    conn.close()


def load_food_listings():
    """
    Loads food listings data from CSV into the food_listings table.
    """
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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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


def load_claims():
    """
    Loads claims data from CSV into the claims table.
    """
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
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            int(row["Claim_ID"]),
            int(row["Food_ID"]),
            int(row["Receiver_ID"]),
            row["Status"],
            row["Timestamp"]
        ))

    conn.commit()
    conn.close()
