import json
from pathlib import Path
from src.models import Port, Route, ShipType, Ship, CargoType, Customer


def load_ports(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ports.jsonl"

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(Port(**row))

    session.commit()


def load_routes(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "routes.jsonl"

    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                Route(
                    origin_port_id=ports[row["origin"]],
                    destination_port_id=ports[row["destination"]],
                    distance_km=row["distance_km"],
                    base_sailing_days=row["base_sailing_days"],
                    danger_level=row["danger_level"],
                    danger_type=row["danger_type"],
                )
            )

    session.commit()


def load_ship_types(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ship_types.jsonl"

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(ShipType(**row))

    session.commit()


def load_ships(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ships.jsonl"

    ship_types = {st.name: st.id for st in session.query(ShipType).all()}
    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                Ship(
                    name=row["name"],
                    ship_type_id=ship_types[row["ship_type"]],
                    home_port_id=ports[row["home_port"]],
                    condition=row["condition"],
                    status=row["status"],
                )
            )

    session.commit()


def load_cargo_types(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "cargo_types.jsonl"

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(CargoType(**row))

    session.commit()


def load_customers(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "customers.jsonl"

    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                Customer(
                    name=row["name"],
                    customer_type=row["customer_type"],
                    home_port_id=ports[row["home_port"]],
                )
            )

    session.commit()
