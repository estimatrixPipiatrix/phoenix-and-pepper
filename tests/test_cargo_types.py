import json
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, CargoType
from src.seed import load_cargo_types


def make_test_file(data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    for row in data:
        f.write(json.dumps(row) + "\n")
    f.close()
    return f.name


CARGO_TYPES = [
    {
        "name": "Phoenix Ash",
        "cargo_class": "phoenix",
        "unit_price_denarii": 500,
        "unit_weight_kg": 0.5,
        "special_handling": "Fireproof container",
    },
    {
        "name": "Basilisk Venom",
        "cargo_class": "phoenix",
        "unit_price_denarii": 800,
        "unit_weight_kg": 2.0,
        "special_handling": "Lead-sealed amphorae",
    },
    {
        "name": "Black Pepper",
        "cargo_class": "pepper",
        "unit_price_denarii": 30,
        "unit_weight_kg": 1.0,
        "special_handling": None,
    },
    {
        "name": "Garum",
        "cargo_class": "pepper",
        "unit_price_denarii": 15,
        "unit_weight_kg": 5.0,
        "special_handling": None,
    },
]


class TestLoadCargoTypes:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def teardown_method(self):
        self.session.close()

    def test_loads_correct_count(self):
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        assert self.session.query(CargoType).count() == 4

    def test_cargo_class_valid(self):
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        for ct in self.session.query(CargoType).all():
            assert ct.cargo_class in {"phoenix", "pepper"}

    def test_phoenix_has_special_handling(self):
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        phoenix = (
            self.session.query(CargoType)
            .filter_by(cargo_class="phoenix")
            .all()
        )
        for ct in phoenix:
            assert ct.special_handling is not None

    def test_pepper_has_no_special_handling(self):
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        pepper = (
            self.session.query(CargoType).filter_by(cargo_class="pepper").all()
        )
        for ct in pepper:
            assert ct.special_handling is None

    def test_prices_positive(self):
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        for ct in self.session.query(CargoType).all():
            assert ct.unit_price_denarii > 0

    def test_phoenix_more_expensive_than_pepper(self):
        load_cargo_types(self.session, make_test_file(CARGO_TYPES))
        phoenix_min = min(
            ct.unit_price_denarii
            for ct in self.session.query(CargoType)
            .filter_by(cargo_class="phoenix")
            .all()
        )
        pepper_max = max(
            ct.unit_price_denarii
            for ct in self.session.query(CargoType)
            .filter_by(cargo_class="pepper")
            .all()
        )
        assert phoenix_min > pepper_max
