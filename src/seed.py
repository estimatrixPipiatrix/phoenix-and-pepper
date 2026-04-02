import json
from pathlib import Path
from src.models import Port


def load_ports(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ports.jsonl"

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(Port(**row))

    session.commit()
