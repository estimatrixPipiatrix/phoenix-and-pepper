import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, ShipType, Ship
from src.seed import load_ports, load_ship_types, load_ships


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
    {
        "name": "Actuaria",
        "description": "Fast courier",
        "cargo_capacity_tons": 40,
        "base_speed_knots": 7.0,
        "operating_speed_knots": 5.5,
        "operating_cost_daily": 120,
        "can_carry_phoenix": True,
    },
]

SHIPS = [
    {
        "name": "Ignis Maris",
        "ship_type": "Actuaria",
        "home_port": "Ostia",
        "condition": 4,
        "status": "in_port",
    },
    {
        "name": "Fortuna Lenta",
        "ship_type": "Corbita",
        "home_port": "Puteoli",
        "condition": 5,
        "status": "in_port",
    },
]


class TestLoadShipTypes:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_ship_types(self.session, make_test_file(SHIP_TYPES))
        assert self.session.query(ShipType).count() == 2

    def test_attributes(self):
        load_ship_types(self.session, make_test_file(SHIP_TYPES))
        corbita = (
            self.session.query(ShipType).filter_by(name="Corbita").first()
        )
        assert corbita.cargo_capacity_tons == 150
        assert corbita.can_carry_phoenix is False

    def test_only_one_carries_phoenix(self):
        load_ship_types(self.session, make_test_file(SHIP_TYPES))
        phoenix_capable = (
            self.session.query(ShipType)
            .filter_by(can_carry_phoenix=True)
            .all()
        )
        assert len(phoenix_capable) == 1
        assert phoenix_capable[0].name == "Actuaria"

    def test_speed_ordering(self):
        load_ship_types(self.session, make_test_file(SHIP_TYPES))
        types = self.session.query(ShipType).all()
        for st in types:
            assert st.operating_speed_knots <= st.base_speed_knots


class TestLoadShips:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        load_ports(self.session, make_test_file(PORTS))
        load_ship_types(self.session, make_test_file(SHIP_TYPES))

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_ships(self.session, make_test_file(SHIPS))
        assert self.session.query(Ship).count() == 2

    def test_foreign_keys_resolve(self):
        load_ships(self.session, make_test_file(SHIPS))
        ship = self.session.query(Ship).filter_by(name="Ignis Maris").first()
        ship_type = (
            self.session.query(ShipType)
            .filter_by(id=ship.ship_type_id)
            .first()
        )
        assert ship_type.name == "Actuaria"

    def test_condition_in_range(self):
        load_ships(self.session, make_test_file(SHIPS))
        for ship in self.session.query(Ship).all():
            assert 1 <= ship.condition <= 5

    def test_valid_status(self):
        valid = {"in_port", "at_sea", "under_repair"}
        load_ships(self.session, make_test_file(SHIPS))
        for ship in self.session.query(Ship).all():
            assert ship.status in valid
