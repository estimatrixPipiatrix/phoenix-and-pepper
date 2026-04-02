import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, Port, CargoType, Customer, Order, OrderLine
from src.seed import (
    load_ports,
    load_cargo_types,
    load_customers,
    load_orders,
    load_order_lines,
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
    {
        "name": "Panormus",
        "latitude": 38.12,
        "longitude": 13.36,
        "size": 2,
        "base_fee": 25,
    },
]

CARGO_TYPES = [
    {
        "name": "Phoenix Ash",
        "cargo_class": "phoenix",
        "unit_price_denarii": 500,
        "unit_weight_kg": 0.5,
        "special_handling": "Fireproof container",
    },
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
    {
        "name": "Decimus Obscurus",
        "customer_type": "magus",
        "home_port": "Panormus",
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
        "customer": "Decimus Obscurus",
        "destination_port": "Puteoli",
        "order_date": "200-03-20",
        "status": "delivered",
    },
    {
        "customer": "Decimus Obscurus",
        "destination_port": "Ostia",
        "order_date": "200-04-01",
        "status": "pending",
    },
]

ORDER_LINES = [
    {"order_index": 1, "cargo_type": "Black Pepper", "quantity": 200},
    {"order_index": 1, "cargo_type": "Phoenix Ash", "quantity": 5},
    {"order_index": 2, "cargo_type": "Phoenix Ash", "quantity": 3},
    {"order_index": 3, "cargo_type": "Phoenix Ash", "quantity": 4},
]


class TestLoadOrders:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))
        load_customers(self.session, make_test_file(CUSTOMERS))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_orders(self.session, make_test_file(ORDERS))
        assert self.session.query(Order).count() == 3

    def test_status_valid(self):
        valid = {"pending", "in_transit", "delivered", "cancelled"}
        load_orders(self.session, make_test_file(ORDERS))
        for o in self.session.query(Order).all():
            assert o.status in valid

    def test_customer_foreign_key_resolves(self):
        load_orders(self.session, make_test_file(ORDERS))
        for o in self.session.query(Order).all():
            customer = (
                self.session.query(Customer)
                .filter_by(id=o.customer_id)
                .first()
            )
            assert customer is not None

    def test_destination_foreign_key_resolves(self):
        load_orders(self.session, make_test_file(ORDERS))
        for o in self.session.query(Order).all():
            port = (
                self.session.query(Port)
                .filter_by(id=o.destination_port_id)
                .first()
            )
            assert port is not None


class TestLoadOrderLines:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        load_customers(self.session, make_test_file(CUSTOMERS))
        load_orders(self.session, make_test_file(ORDERS))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_order_lines(self.session, make_test_file(ORDER_LINES))
        assert self.session.query(OrderLine).count() == 4

    def test_quantity_positive(self):
        load_order_lines(self.session, make_test_file(ORDER_LINES))
        for ol in self.session.query(OrderLine).all():
            assert ol.quantity > 0

    def test_order_foreign_key_resolves(self):
        load_order_lines(self.session, make_test_file(ORDER_LINES))
        for ol in self.session.query(OrderLine).all():
            order = self.session.query(Order).filter_by(id=ol.order_id).first()
            assert order is not None

    def test_magus_orders_only_phoenix(self):
        load_order_lines(self.session, make_test_file(ORDER_LINES))
        magus = (
            self.session.query(Customer)
            .filter_by(customer_type="magus")
            .first()
        )
        magus_orders = (
            self.session.query(Order).filter_by(customer_id=magus.id).all()
        )
        magus_order_ids = {o.id for o in magus_orders}
        magus_lines = (
            self.session.query(OrderLine)
            .filter(OrderLine.order_id.in_(magus_order_ids))
            .all()
        )
        for line in magus_lines:
            cargo = (
                self.session.query(CargoType)
                .filter_by(id=line.cargo_type_id)
                .first()
            )
            assert cargo.cargo_class == "phoenix"
