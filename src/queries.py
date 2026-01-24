from src.db import get_connection

def count_providers_and_receivers_by_city():
    """
    Returns the number of food providers and receivers in each city.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT city,
               COUNT(*) AS count,
               'Provider' AS role
        FROM providers
        GROUP BY city

        UNION ALL

        SELECT city,
               COUNT(*) AS count,
               'Receiver' AS role
        FROM receivers
        GROUP BY city
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results

def total_food_contribution_by_provider_type():
    """
    Returns total quantity of food contributed by each provider type.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT provider_type,
               SUM(quantity) AS total_quantity
        FROM food_listings
        GROUP BY provider_type
        ORDER BY total_quantity DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


def get_providers_contact_by_city(city):
    """
    Returns contact details of food providers in a specific city.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT name,
               address,
               contact
        FROM providers
        WHERE city = ?
    """

    cursor.execute(query, (city,))
    results = cursor.fetchall()

    conn.close()
    return results


def receivers_with_most_claims():
    """
    Returns receivers ordered by number of food claims made.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT r.name,
               r.city,
               COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN receivers r
            ON c.receiver_id = r.receiver_id
        GROUP BY r.receiver_id
        ORDER BY total_claims DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results

def total_food_available():
    """
    Returns the total quantity of food available from all providers.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT SUM(quantity) AS total_quantity
        FROM food_listings
    """

    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    return result[0]

def city_with_highest_food_listings():
    """
    Returns the city with the highest number of food listings.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT location,
               COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY location
        ORDER BY total_listings DESC
        LIMIT 1
    """

    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    return result


def most_common_food_types():
    """
    Returns food types ordered by how frequently they appear.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT food_type,
               COUNT(*) AS frequency
        FROM food_listings
        GROUP BY food_type
        ORDER BY frequency DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


def claims_per_food_item():
    """
    Returns number of claims made for each food item.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT f.food_name,
               COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f
            ON c.food_id = f.food_id
        GROUP BY f.food_id
        ORDER BY total_claims DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


def provider_with_most_successful_claims():
    """
    Returns the provider with the highest number of successful (completed) food claims.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT p.name,
               COUNT(c.claim_id) AS successful_claims
        FROM claims c
        JOIN food_listings f
            ON c.food_id = f.food_id
        JOIN providers p
            ON f.provider_id = p.provider_id
        WHERE c.status = 'Completed'
        GROUP BY p.provider_id
        ORDER BY successful_claims DESC
        LIMIT 1
    """

    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    return result


def claim_status_percentage():
    """
    Returns percentage distribution of claim statuses.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT status,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS percentage
        FROM claims
        GROUP BY status
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results

def average_food_quantity_per_receiver():
    """
    Returns the average quantity of food claimed per receiver.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT AVG(receiver_total) AS average_quantity
        FROM (
            SELECT c.receiver_id,
                   SUM(f.quantity) AS receiver_total
            FROM claims c
            JOIN food_listings f
                ON c.food_id = f.food_id
            GROUP BY c.receiver_id
        )
    """

    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    return result[0]


def most_claimed_meal_type():
    """
    Returns meal types ordered by number of claims.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT f.meal_type,
               COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f
            ON c.food_id = f.food_id
        GROUP BY f.meal_type
        ORDER BY total_claims DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results

def total_food_donated_by_provider():
    """
    Returns total quantity of food donated by each provider.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT p.name,
               SUM(f.quantity) AS total_quantity
        FROM food_listings f
        JOIN providers p
            ON f.provider_id = p.provider_id
        GROUP BY p.provider_id
        ORDER BY total_quantity DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results
