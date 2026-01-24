from src.db import (
    create_providers_table,
    create_receivers_table,
    create_food_listings_table,
    create_claims_table
)
from src.load_data import (
    load_providers,
    load_receivers,
    load_food_listings,
    load_claims
)

print("Creating database tables...")
create_providers_table()
create_receivers_table()
create_food_listings_table()
create_claims_table()

print("Loading providers data...")
load_providers()

print("Loading receivers data...")
load_receivers()

print("Loading food listings data...")
load_food_listings()

print("Loading claims data...")
load_claims()

print("All data loaded successfully")
