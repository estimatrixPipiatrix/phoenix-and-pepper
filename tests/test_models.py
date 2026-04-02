from src.models import Port, Route


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
