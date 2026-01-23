from src.db import get_connection

print("Testing database connection...")

conn = get_connection()
print("Database connection successful")

conn.close()
