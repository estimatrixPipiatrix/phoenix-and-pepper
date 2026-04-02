import json
from pathlib import Path
from src.models import Port, Route


def load_ports(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ports.jsonl"

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(Port(**row))

    session.commit()


def load_routes(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "routes.jsonl"

    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                Route(
                    origin_port_id=ports[row["origin"]],
                    destination_port_id=ports[row["destination"]],
                    distance_km=row["distance_km"],
                    base_sailing_days=row["base_sailing_days"],
                    danger_level=row["danger_level"],
                    danger_type=row["danger_type"],
                )
            )

    session.commit()
