from src.models import Port


def test_port_creations():
    port = Port(name="Ostia", latitude=41.76, longitude=12.29, size=5, base_fee=50)
    assert port.name == "Ostia"
    assert port.size == 5
    assert port.base_fee == 50
