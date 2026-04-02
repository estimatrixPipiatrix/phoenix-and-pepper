import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import (
    Base,
    Route,
    Ship,
    OrderLine,
    Voyage,
    VoyageManifest,
)
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


def make_test_file(data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    for row in data:
        f.write(json.dumps(row) + "\n")
    f.close()
    return f.name


PORTS = [
    {
        "name": "Ostia",
        "latitude": 41.76,
        "longitude": 12.29,
        "size": 5,
        "base_fee": 50,
    },
    {
        "name": "Puteoli",
        "latitude": 40.82,
        "longitude": 14.12,
        "size": 5,
        "base_fee": 55,
    },
]

ROUTES = [
    {
        "origin": "Ostia",
        "destination": "Puteoli",
        "distance_km": 260,
        "base_sailing_days": 3,
        "danger_level": 1,
        "danger_type": "none",
    },
    {
        "origin": "Puteoli",
        "destination": "Ostia",
        "distance_km": 260,
        "base_sailing_days": 3,
        "danger_level": 1,
        "danger_type": "none",
    },
]

SHIP_TYPES = [
    {
        "name": "Corbita",
        "description": "Bulk hauler",
        "cargo_capacity_tons": 150,
        "base_speed_knots": 4.0,
        "operating_speed_knots": 3.0,
        "operating_cost_daily": 80,
        "can_carry_phoenix": False,
    },
]

SHIPS = [
    {
        "name": "Fortuna Lenta",
        "ship_type": "Corbita",
        "home_port": "Ostia",
        "condition": 5,
        "status": "in_port",
    },
]

CARGO_TYPES = [
    {
        "name": "Black Pepper",
        "cargo_class": "pepper",
        "unit_price_denarii": 30,
        "unit_weight_kg": 1.0,
        "special_handling": None,
    },
]

CUSTOMERS = [
    {
        "name": "Marcus Crassus Minor",
        "customer_type": "mercator",
        "home_port": "Ostia",
    },
]

ORDERS = [
    {
        "customer": "Marcus Crassus Minor",
        "destination_port": "Puteoli",
        "order_date": "200-03-15",
        "status": "delivered",
    },
    {
        "customer": "Marcus Crassus Minor",
        "destination_port": "Ostia",
        "order_date": "200-04-01",
        "status": "in_transit",
    },
]

ORDER_LINES = [
    {"order_index": 1, "cargo_type": "Black Pepper", "quantity": 200},
    {"order_index": 2, "cargo_type": "Black Pepper", "quantity": 150},
]

VOYAGES = [
    {
        "ship": "Fortuna Lenta",
        "origin": "Ostia",
        "destination": "Puteoli",
        "departure_date": "200-03-16",
        "arrival_date": "200-03-19",
        "status": "completed",
    },
    {
        "ship": "Fortuna Lenta",
        "origin": "Puteoli",
        "destination": "Ostia",
        "departure_date": "200-04-02",
        "arrival_date": None,
        "status": "in_transit",
    },
]

MANIFEST = [
    {"voyage_index": 1, "order_line_index": 1},
    {"voyage_index": 2, "order_line_index": 2},
]


class TestLoadVoyages:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))
        load_routes(self.session, make_test_file(ROUTES))
        load_ship_types(self.session, make_test_file(SHIP_TYPES))
        load_ships(self.session, make_test_file(SHIPS))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_voyages(self.session, make_test_file(VOYAGES))
        assert self.session.query(Voyage).count() == 2

    def test_ship_foreign_key_resolves(self):
        load_voyages(self.session, make_test_file(VOYAGES))
        for v in self.session.query(Voyage).all():
            ship = self.session.query(Ship).filter_by(id=v.ship_id).first()
            assert ship is not None

    def test_route_foreign_key_resolves(self):
        load_voyages(self.session, make_test_file(VOYAGES))
        for v in self.session.query(Voyage).all():
            route = self.session.query(Route).filter_by(id=v.route_id).first()
            assert route is not None

    def test_status_valid(self):
        valid = {"completed", "in_transit", "cancelled"}
        load_voyages(self.session, make_test_file(VOYAGES))
        for v in self.session.query(Voyage).all():
            assert v.status in valid

    def test_completed_has_arrival_date(self):
        load_voyages(self.session, make_test_file(VOYAGES))
        completed = (
            self.session.query(Voyage).filter_by(status="completed").all()
        )
        for v in completed:
            assert v.arrival_date is not None

    def test_in_transit_has_no_arrival_date(self):
        load_voyages(self.session, make_test_file(VOYAGES))
        in_transit = (
            self.session.query(Voyage).filter_by(status="in_transit").all()
        )
        for v in in_transit:
            assert v.arrival_date is None


class TestLoadVoyageManifest:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))
        load_routes(self.session, make_test_file(ROUTES))
        load_ship_types(self.session, make_test_file(SHIP_TYPES))
        load_ships(self.session, make_test_file(SHIPS))
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        load_customers(self.session, make_test_file(CUSTOMERS))
        load_orders(self.session, make_test_file(ORDERS))
        load_order_lines(self.session, make_test_file(ORDER_LINES))
        load_voyages(self.session, make_test_file(VOYAGES))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_voyage_manifest(self.session, make_test_file(MANIFEST))
        assert self.session.query(VoyageManifest).count() == 2

    def test_voyage_foreign_key_resolves(self):
        load_voyage_manifest(self.session, make_test_file(MANIFEST))
        for vm in self.session.query(VoyageManifest).all():
            voyage = (
                self.session.query(Voyage).filter_by(id=vm.voyage_id).first()
            )
            assert voyage is not None

    def test_order_line_foreign_key_resolves(self):
        load_voyage_manifest(self.session, make_test_file(MANIFEST))
        for vm in self.session.query(VoyageManifest).all():
            order_line = (
                self.session.query(OrderLine)
                .filter_by(id=vm.order_line_id)
                .first()
            )
            assert order_line is not None
