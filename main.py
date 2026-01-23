import sqlite3 as sq
import pandas as pd

print("Database creation")

connection = sq.connect("database/food_waste.db")

print("Database created")

connection.close()