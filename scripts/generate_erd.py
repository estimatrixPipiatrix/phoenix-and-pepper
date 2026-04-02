from graphviz import Digraph
from sqlalchemy import create_engine
from src.models import Base


engine = create_engine(
    "postgresql://phoenix:pepper@localhost:5432/phoenix_and_pepper",
)
Base.metadata.reflect(bind=engine)

dot = Digraph(
    "Phoenix et Piper",
    format="png",
    graph_attr={
        "rankdir": "TB",
        "fontname": "Helvetica",
        "bgcolor": "black",
    },
    node_attr={
        "shape": "record",
        "fontname": "Helvetica",
        "fontsize": "10",
        "fontcolor": "green",
        "color": "green",
        "style": "filled",
        "fillcolor": "black",
    },
    edge_attr={
        "fontname": "Helvetica",
        "fontsize": "8",
        "fontcolor": "green",
        "color": "green",
    },
)

for table in Base.metadata.sorted_tables:
    columns = "\\l".join(col.name for col in table.columns)
    label = f"{{{table.name}|{columns}\\l}}"
    dot.node(table.name, label)

    for fk in table.foreign_keys:
        target_table = fk.column.table.name
        dot.edge(table.name, target_table, label=fk.parent.name)

dot.render("docs/erd", cleanup=True, view=True)
