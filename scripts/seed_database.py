from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base
from src.seed import (
    load_ports,
    load_routes,
    load_ship_types,
    load_ships,
    load_cargo_types,
    load_customers,
    load_orders,
    load_order_lines,
    load_voyages,
    load_voyage_manifest,
)

DATABASE_URL = "postgresql://phoenix:pepper@localhost:5432/phoenix_and_pepper"

engine = create_engine(DATABASE_URL)

# Drop everything and start fresh
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session(engine)

# Foreign key order
load_ports(session)
load_routes(session)
load_ship_types(session)
load_ships(session)
load_cargo_types(session)
load_customers(session)
load_orders(session)
load_order_lines(session)
load_voyages(session)
load_voyage_manifest(session)

session.close()

print("Mundus creatus est.")
