from src.models import Port, Route, ShipType, Ship, CargoType, Customer
from src.models import Order, OrderLine, Voyage, VoyageManifest


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


def test_order_creation():
    order = Order(
        customer_id=1,
        destination_port_id=2,
        order_date="753-03-15",
        status="pending",
    )
    assert order.customer_id == 1
    assert order.status == "pending"


def test_order_line_creation():
    line = OrderLine(
        order_id=1,
        cargo_type_id=3,
        quantity=50,
    )
    assert line.order_id == 1
    assert line.cargo_type_id == 3
    assert line.quantity == 50


def test_voyage_creation():
    voyage = Voyage(
        ship_id=1,
        route_id=3,
        departure_date="753-04-01",
        status="underway",
    )
    assert voyage.ship_id == 1
    assert voyage.route_id == 3
    assert voyage.arrival_date is None
    assert voyage.status == "underway"


def test_voyage_manifest_creation():
    manifest = VoyageManifest(
        voyage_id=1,
        order_line_id=7,
    )
    assert manifest.voyage_id == 1
    assert manifest.order_line_id == 7
