import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, Port, Customer
from src.seed import load_ports, load_customers


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
        "name": "Panormus",
        "latitude": 38.12,
        "longitude": 13.36,
        "size": 2,
        "base_fee": 25,
    },
]

CUSTOMERS = [
    {
        "name": "Marcus Crassus Minor",
        "customer_type": "mercator",
        "home_port": "Ostia",
    },
    {
        "name": "Templum Apollinis",
        "customer_type": "templum",
        "home_port": "Ostia",
    },
    {
        "name": "Aulus Vitellius",
        "customer_type": "praefectus",
        "home_port": "Ostia",
    },
    {
        "name": "Decimus Obscurus",
        "customer_type": "magus",
        "home_port": "Panormus",
    },
]


class TestLoadCustomers:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_customers(self.session, make_test_file(CUSTOMERS))
        assert self.session.query(Customer).count() == 4

    def test_customer_type_valid(self):
        valid = {"mercator", "templum", "praefectus", "magus"}
        load_customers(self.session, make_test_file(CUSTOMERS))
        for c in self.session.query(Customer).all():
            assert c.customer_type in valid

    def test_foreign_key_resolves(self):
        load_customers(self.session, make_test_file(CUSTOMERS))
        for c in self.session.query(Customer).all():
            port = (
                self.session.query(Port).filter_by(id=c.home_port_id).first()
            )
            assert port is not None

    def test_magus_in_panormus(self):
        load_customers(self.session, make_test_file(CUSTOMERS))
        magus = (
            self.session.query(Customer)
            .filter_by(customer_type="magus")
            .first()
        )
        port = (
            self.session.query(Port).filter_by(id=magus.home_port_id).first()
        )
        assert port.name == "Panormus"
