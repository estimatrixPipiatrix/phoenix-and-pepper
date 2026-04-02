from src.models import Port, Route, ShipType, Ship, CargoType, Customer


def test_port_creations():
    port = Port(
        name="Ostia",
        latitude=41.76,
        longitude=12.29,
        size=5,
        base_fee=50,
    )
    assert port.name == "Ostia"
    assert port.size == 5
    assert port.base_fee == 50


def test_route_creation():
    route = Route(
        origin_port_id=1,
        destination_port_id=2,
        distance_km=220.0,
        base_sailing_days=2,
        danger_level=3,
        danger_type="mythological",
    )
    assert route.origin_port_id == 1
    assert route.destination_port_id == 2
    assert route.distance_km == 220.0
    assert route.danger_level == 3
    assert route.danger_type == "mythological"


def test_ship_type_creation():
    ship_type = ShipType(
        name="Actuaria",
        description="Fast vessel with oars and sails, suitable for dangerous cargo",
        cargo_capacity_tons=80,
        base_speed_knots=6.5,
        operating_cost_daily=120,
        can_carry_phoenix=True,
    )
    assert ship_type.name == "Actuaria"
    assert ship_type.cargo_capacity_tons == 80
    assert ship_type.can_carry_phoenix is True


def test_ship_creation():
    ship = Ship(
        name="Vesper",
        ship_type_id=1,
        home_port_id=1,
        condition=4,
        status="in_port",
    )
    assert ship.name == "Vesper"
    assert ship.condition == 4
    assert ship.status == "in_port"


def test_cargo_type_creation():
    cargo = CargoType(
        name="Basilisk Venom",
        cargo_class="phoenix",
        unit_price_denarii=500,
        unit_weight_kg=2.0,
        special_handling="Requires sealed lead container",
    )
    assert cargo.name == "Basilisk Venom"
    assert cargo.cargo_class == "phoenix"
    assert cargo.special_handling is not None


def test_cargo_type_no_special_handling():
    cargo = CargoType(
        name="Pepper",
        cargo_class="pepper",
        unit_price_denarii=15,
        unit_weight_kg=0.5,
    )
    assert cargo.name == "Pepper"
    assert cargo.special_handling is None


def test_customer_creation():
    customer = Customer(
        name="Marcus Aurelius Garum",
        customer_type="merchant",
        home_port_id=1,
    )
    assert customer.name == "Marcus Aurelius Garum"
    assert customer.customer_type == "merchant"
