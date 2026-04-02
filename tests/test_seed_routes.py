import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, Port, Route
from src.seed import load_ports, load_routes


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
        "name": "Messana",
        "latitude": 38.19,
        "longitude": 15.56,
        "size": 3,
        "base_fee": 35,
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
    {
        "origin": "Messana",
        "destination": "Ostia",
        "distance_km": 500,
        "base_sailing_days": 5,
        "danger_level": 4,
        "danger_type": "mythological",
    },
]


class TestLoadRoutes:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_routes(self.session, make_test_file(ROUTES))
        assert self.session.query(Route).count() == 3

    def test_foreign_keys_resolve(self):
        load_routes(self.session, make_test_file(ROUTES))
        route = self.session.query(Route).first()
        origin = (
            self.session.query(Port).filter_by(id=route.origin_port_id).first()
        )
        assert origin is not None

    def test_reverse_pairs_exist(self):
        load_routes(self.session, make_test_file(ROUTES))
        routes = self.session.query(Route).all()
        pairs = {(r.origin_port_id, r.destination_port_id) for r in routes}
        ostia = self.session.query(Port).filter_by(name="Ostia").first().id
        puteoli = self.session.query(Port).filter_by(name="Puteoli").first().id
        assert (ostia, puteoli) in pairs
        assert (puteoli, ostia) in pairs

    def test_danger_level_in_range(self):
        load_routes(self.session, make_test_file(ROUTES))
        for route in self.session.query(Route).all():
            assert 1 <= route.danger_level <= 5

    def test_danger_type_valid(self):
        valid_types = {"natural", "mythological", "divine", "piracy", "none"}
        load_routes(self.session, make_test_file(ROUTES))
        for route in self.session.query(Route).all():
            assert route.danger_type in valid_types

    def test_no_self_routes(self):
        load_routes(self.session, make_test_file(ROUTES))
        for route in self.session.query(Route).all():
            assert route.origin_port_id != route.destination_port_id
