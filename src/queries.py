from src.db import get_connection
from datetime import datetime

# =========================================================
# AUTHENTICATION
# =========================================================

def create_user(username, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, username, role, linked_id
        FROM users
        WHERE username = ? AND password = ?
    """, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


# =========================================================
# RECEIVER CRUD (USER ↔ RECEIVER LINKED)
# =========================================================

def create_receiver(user_id, name, city, contact):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO receivers (name, city, contact)
        VALUES (?, ?, ?)
    """, (name, city, contact))

    receiver_id = cursor.lastrowid

    cursor.execute("""
        UPDATE users
        SET linked_id = ?
        WHERE user_id = ?
    """, (receiver_id, user_id))

    conn.commit()
    conn.close()


def update_receiver(receiver_id, name, city, contact):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE receivers
        SET name = ?, city = ?, contact = ?
        WHERE receiver_id = ?
    """, (name, city, contact, receiver_id))
    conn.commit()
    conn.close()


def get_receiver_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.receiver_id, r.name, r.city, r.contact
        FROM receivers r
        JOIN users u ON u.linked_id = r.receiver_id
        WHERE u.user_id = ?
    """, (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data


# =========================================================
# PROVIDER / FOOD LISTINGS (CRUD)
# =========================================================

def create_food_listing(
    food_name, quantity, expiry_date,
    provider_id, provider_type,
    location, food_type, meal_type
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO food_listings
        (food_name, quantity, expiry_date, provider_id,
         provider_type, location, food_type, meal_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        food_name, quantity, expiry_date,
        provider_id, provider_type,
        location, food_type, meal_type
    ))
    conn.commit()
    conn.close()


# =========================================================
# FOOD DISCOVERY
# =========================================================

def get_food_by_city(city):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT food_id, food_name, quantity, expiry_date,
               provider_id, location, food_type, meal_type
        FROM food_listings
        WHERE quantity > 0
          AND LOWER(location) = LOWER(?)
        ORDER BY expiry_date
    """, (city,))
    data = cursor.fetchall()
    conn.close()
    return data


def get_available_food():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT food_id, food_name, quantity, location,
               food_type, meal_type, expiry_date
        FROM food_listings
        WHERE quantity > 0
        ORDER BY expiry_date
    """)
    data = cursor.fetchall()
    conn.close()
    return data


# =========================================================
# CLAIMS (FULL DATA IMPACT)
# =========================================================

def create_claim(food_id, receiver_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO claims (food_id, receiver_id, status, timestamp)
        VALUES (?, ?, 'Completed', ?)
    """, (food_id, receiver_id, datetime.now()))

    cursor.execute("""
        UPDATE food_listings
        SET quantity = quantity - 1
        WHERE food_id = ? AND quantity > 0
    """, (food_id,))

    conn.commit()
    conn.close()


# =========================================================
# HOME PAGE ANALYTICS
# =========================================================

def total_food_available():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM food_listings")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def most_common_food_types():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT food_type, COUNT(*)
        FROM food_listings
        GROUP BY food_type
        ORDER BY COUNT(*) DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def claim_status_percentage():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims)
        FROM claims
        GROUP BY status
    """)
    data = cursor.fetchall()
    conn.close()
    return data


# =========================================================
# EDA / RANKINGS / TRENDS
# =========================================================

def top_receivers_by_claims(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.name, COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY r.receiver_id
        ORDER BY total_claims DESC
        LIMIT ?
    """, (limit,))
    data = cursor.fetchall()
    conn.close()
    return data


def top_providers_by_donation(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT provider_id, SUM(quantity) AS total_donated
        FROM food_listings
        GROUP BY provider_id
        ORDER BY total_donated DESC
        LIMIT ?
    """, (limit,))
    data = cursor.fetchall()
    conn.close()
    return data


def food_by_city():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT location, SUM(quantity)
        FROM food_listings
        GROUP BY location
        ORDER BY SUM(quantity) DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def claims_over_time():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(timestamp) AS date, COUNT(*) AS total_claims
        FROM claims
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """)
    data = cursor.fetchall()
    conn.close()
    return data
