import json
from pathlib import Path
from src.models import Port, Route, ShipType, Ship, CargoType, Customer
from src.models import Order, OrderLine, Voyage, VoyageManifest


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


def load_orders(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "orders.jsonl"

    customers = {c.name: c.id for c in session.query(Customer).all()}
    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                Order(
                    customer_id=customers[row["customer"]],
                    destination_port_id=ports[row["destination_port"]],
                    order_date=row["order_date"],
                    status=row["status"],
                )
            )

    session.commit()


def load_order_lines(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "order_lines.jsonl"

    orders = session.query(Order).all()
    order_ids = {i + 1: o.id for i, o in enumerate(orders)}
    cargo_types = {ct.name: ct.id for ct in session.query(CargoType).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                OrderLine(
                    order_id=order_ids[row["order_index"]],
                    cargo_type_id=cargo_types[row["cargo_type"]],
                    quantity=row["quantity"],
                )
            )

    session.commit()


def load_voyages(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "voyages.jsonl"

    ships = {s.name: s.id for s in session.query(Ship).all()}
    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            origin_id = ports[row["origin"]]
            destination_id = ports[row["destination"]]
            route = (
                session.query(Route)
                .filter_by(
                    origin_port_id=origin_id,
                    destination_port_id=destination_id,
                )
                .first()
            )
            session.add(
                Voyage(
                    ship_id=ships[row["ship"]],
                    route_id=route.id,
                    departure_date=row["departure_date"],
                    arrival_date=row["arrival_date"],
                    status=row["status"],
                )
            )

    session.commit()


def load_voyage_manifest(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "voyage_manifest.jsonl"

    voyages = session.query(Voyage).all()
    voyage_ids = {i + 1: v.id for i, v in enumerate(voyages)}
    order_lines = session.query(OrderLine).all()
    order_line_ids = {i + 1: ol.id for i, ol in enumerate(order_lines)}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                VoyageManifest(
                    voyage_id=voyage_ids[row["voyage_index"]],
                    order_line_id=order_line_ids[row["order_line_index"]],
                )
            )

    session.commit()
