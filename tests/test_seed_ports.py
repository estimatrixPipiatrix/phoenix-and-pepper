import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, Port
from src.seed import load_ports


def make_test_ports_file(ports_data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    for row in ports_data:
        f.write(json.dumps(row) + "\n")
    f.close()
    return f.name


class TestLoadPorts:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        path = make_test_ports_file(
            [
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
        )
        load_ports(self.session, path)
        assert self.session.query(Port).count() == 2

    def test_port_attributes(self):
        path = make_test_ports_file(
            [
                {
                    "name": "Ostia",
                    "latitude": 41.76,
                    "longitude": 12.29,
                    "size": 5,
                    "base_fee": 50,
                },
            ]
        )
        load_ports(self.session, path)
        port = self.session.query(Port).first()
        assert port.name == "Ostia"
        assert port.latitude == 41.76
        assert port.size == 5
        assert port.base_fee == 50

    def test_names_are_unique(self):
        path = make_test_ports_file(
            [
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
        )
        load_ports(self.session, path)
        names = [p.name for p in self.session.query(Port).all()]
        assert len(names) == len(set(names))

    def test_sizes_in_valid_range(self):
        path = make_test_ports_file(
            [
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
        )
        load_ports(self.session, path)
        for port in self.session.query(Port).all():
            assert 1 <= port.size <= 5

    def test_base_fees_positive(self):
        path = make_test_ports_file(
            [
                {
                    "name": "Ostia",
                    "latitude": 41.76,
                    "longitude": 12.29,
                    "size": 5,
                    "base_fee": 50,
                },
            ]
        )
        load_ports(self.session, path)
        for port in self.session.query(Port).all():
            assert port.base_fee > 0

    def test_coordinates_in_mediterranean(self):
        path = make_test_ports_file(
            [
                {
                    "name": "Ostia",
                    "latitude": 41.76,
                    "longitude": 12.29,
                    "size": 5,
                    "base_fee": 50,
                },
                {
                    "name": "Syracusae",
                    "latitude": 37.07,
                    "longitude": 15.29,
                    "size": 4,
                    "base_fee": 40,
                },
            ]
        )
        load_ports(self.session, path)
        for port in self.session.query(Port).all():
            assert 35.0 <= port.latitude <= 45.0
            assert 10.0 <= port.longitude <= 20.0
