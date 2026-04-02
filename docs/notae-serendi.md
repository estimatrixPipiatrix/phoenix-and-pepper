Phoenix et Piper — Notae Serendi
Quid aedificavimus et cur
Generator datorum fictorum

Basim datorum habemus (Postgres in continente), schema habemus (modela SQLAlchemy), sed tabulae vacuae sunt. Mundus noster portus, naves, merces, clientes continet—sed nemo adhuc exstat. Generator datorum fictorum mundum nostrum implet.

Duas res separavimus: ipsa data (in fasciculis JSONL) et rationem inserendi (in seed.py). Cur? Quia data legere et mutare volumus sine codice Pythonico tangendo, atque ratio inserendi eadem manet etiam cum data crescunt.

Fasciculi JSONL

JSONL significat “JSON Lines”—quisque versus est obiectum JSON integrum:

{"name": "Ostia", "latitude": 41.76, "longitude": 12.29, "size": 5, "base_fee": 50}
{"name": "Puteoli", "latitude": 40.82, "longitude": 14.12, "size": 5, "base_fee": 55}

Cur JSONL et non CSV? Quia JSONL campos nominatos habet—non pendemus ab ordine columnarum. Praeterea valores nullos exprimere potest (null in JSON, quod fit None in Python), quod CSV minus commode efficit.

Cur JSONL et non JSON simplex? Quia JSONL versus singillatim legi potest; non opus est totum fasciculum simul in memoriam recipere. Pro datis nostris parvis hoc fortasse parum refert, sed tamen mos bonus est.

Fasciculi nostri in directorio data/ habitant:

data/
├── ports.jsonl
├── routes.jsonl
├── ship_types.jsonl
├── ships.jsonl
├── cargo_types.jsonl
├── customers.jsonl
├── orders.jsonl
├── order_lines.jsonl
├── voyages.jsonl
└── voyage_manifest.jsonl

Ordo inserendi (catena clavium alienarum)

Claves alienae ordinem inserendi regunt. Non possumus navem creare antequam portus domesticus et genus navis exstent. Catena haec est:

ports — nullae dependentiae
routes — pendent a ports (origo et destinatio)
ship_types — nullae dependentiae
ships — pendent a ship_types et ports
cargo_types — nullae dependentiae
customers — pendent a ports
orders — pendent a customers et ports
order_lines — pendent a orders et cargo_types
voyages — pendent a ships et routes
voyage_manifest — pendet a voyages et order_lines

Si ordinem violamus, Postgres recusat—clavem alienam ad rem nondum exstantem referentem non admittit. Hoc bonum est: dator integritatem servat.

Fasciculus seed.py

Omnis ratio inserendi in src/seed.py continetur. Quisque fasciculus JSONL suam functionem habet: load_ports, load_routes, load_ship_types, et cetera.

Functiones in tres species dividuntur:

Species prima: insertio directa

Ubi campi JSONL directe campis modelorum respondent, dictionarium in constructorem expandimus:

def load_ports(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ports.jsonl"

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(Port(**row))

    session.commit()

*Port(*row) dictionarium expandit—{"name": "Ostia"} fit Port(name="Ostia"). Hoc operatur quia claves dictionarii nominibus parametrorum exacte respondent.

load_ports, load_ship_types, et load_cargo_types hanc speciem sequuntur.

Species secunda: cum conversione nominum

Ubi JSONL nomina humana continet sed modelum claves numericas requirit, nomina in IDs convertimus:

def load_ships(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "ships.jsonl"

    ship_types = {st.name: st.id for st in session.query(ShipType).all()}
    ports = {p.name: p.id for p in session.query(Port).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                Ship(
                    name=row["name"],
                    ship_type_id=ship_types[row["ship_type"]],
                    home_port_id=ports[row["home_port"]],
                    condition=row["condition"],
                    status=row["status"],
                )
            )

    session.commit()

Dictionaria ship_types et ports nomina ad IDs convertunt. Ita in JSONL scribimus "Actuaria", et codex ID invenit.

Hoc significat: load_ports prius currere debet quam load_ships. Si portus nondum exstant, clavis inveniri non potest.

load_routes, load_ships, load_customers, load_orders hunc modum sequuntur.

Species tertia: cum indicibus

Ordines et lineae ordinum nomina naturalia non habent—ordo “Marcus Crassus Minor, die XV Martii” nimis longum est. Itaque indicibus utimur:

def load_order_lines(session, path=None):
    if path is None:
        path = Path(__file__).parent.parent / "data" / "order_lines.jsonl"

    orders = session.query(Order).all()
    order_ids = {i + 1: o.id for i, o in enumerate(orders)}
    cargo_types = {ct.name: ct.id for ct in session.query(CargoType).all()}

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            session.add(
                OrderLine(
                    order_id=order_ids[row["order_index"]],
                    cargo_type_id=cargo_types[row["cargo_type"]],
                    quantity=row["quantity"],
                )
            )

    session.commit()

enumerate(orders) paria (0, primus), (1, secundus)… gignit. i + 1 addimus quia indices in JSONL ab 1 incipiunt, sed enumerate a 0.

Hoc pendet ab ordine insertionis—ordines eodem ordine inseri debent quo in JSONL apparent.

load_order_lines, load_voyages, load_voyage_manifest hunc modum sequuntur.

Casus singularis: itinera in navigationibus

load_voyages iter non per nomen sed per par portuum quaerit:

route = (
    session.query(Route)
    .filter_by(origin_port_id=origin_id, destination_port_id=destination_id)
    .first()
)

Iter enim nomine caret; duobus portibus definitur.

Sessio SQLAlchemy

Tres operationes fundamentales:

session.add(obiectum) — additur sed nondum inseritur
session.commit() — omnia simul inseruntur
session.query(Classis) — data leguntur

session.add() obiecta colligit; commit() ea simul mittit. Hoc efficacius est et tutius: aut omnia aut nihil.

Dictionaria translationis

Exemplar:

ports = {p.name: p.id for p in session.query(Port).all()}

Exitus:

{"Ostia": 1, "Puteoli": 2, "Neapolis": 3, ...}

Data nostra

Mundus Phase 0 consulto parvus est—societas nascens, non imperium.

VIII portus
XVIII itinera
III genera navium
III naves
IX genera mercium
VIII clientes
XI ordines cum XIX lineis
IX navigationes cum XVI lineis manifesti

Decimus Obscurus

Magus noster exemplum singulare praebet:

Tantum merces Phoenix-classis emit
Quantitates parvas
Destinationes mutat
Ex Panormo operatur

Ceteri clientes merces mixtas, quantitates maiores, destinationes constantes habent.

Probationes

Probationes SQLite in memoria utuntur—non Postgres.

Processus:

Data ficta creantur
Basis in memoria constituitur
Functio vocatur
Exitus examinantur
Basis clauditur
Genera probationum
Numerus
Attributa
Claves alienae
Regulae negotii

Exempla:

Portus magnitudinem inter 1 et 5 habent
Velocitas operandi numquam velocitatem basalem excedit
Sola Actuaria merces Phoenix-classis ferre potest
Merces Phoenix-classis semper curam propriam habent
Merces Pepper-classis numquam curam propriam habent
Pretium minimum Phoenix-classis maximum Pepper-classis excedit
Navigationes completae diem adventus habent; aliae non habent
Decimus Obscurus tantum merces Phoenix-classis emit

Ultima probatio narrativa est — historiam magi nostri in codice figit.

Structura proiecti (nunc)

phoenix-and-pepper/
├── .github/workflows/ci.yml
├── data/
│   ├── ports.jsonl                — VIII portus Italici
│   ├── routes.jsonl               — XVIII itinera directionales
│   ├── ship_types.jsonl           — III genera navium
│   ├── ships.jsonl                — III naves nominatae
│   ├── cargo_types.jsonl          — IX genera mercium
│   ├── customers.jsonl            — VIII clientes (incluso mago)
│   ├── orders.jsonl               — XI ordines
│   ├── order_lines.jsonl          — XIX lineae ordinum
│   ├── voyages.jsonl              — IX navigationes
│   └── voyage_manifest.jsonl      — XVI lineae manifesti
├── docs/
│   ├── notae-apparandi.md         — notae Phase 0a
│   ├── notae-continentis.md       — notae Phase 0b
│   ├── notae-schematis.md         — notae Phase 0c
│   └── notae-serendi.md           — notae Phase 0d (hae notae)
├── src/
│   ├── __init__.py
│   ├── models.py                  — modela SQLAlchemy
│   └── seed.py                    — functiones inserendi
├── tests/
│   ├── test_models.py             — probationes modelorum
│   ├── test_seed_ports.py         — probationes portuum
│   ├── test_seed_routes.py        — probationes itinerum
│   ├── test_seed_ship_and_type.py — probationes navium et generum
│   ├── test_seed_cargo_types.py   — probationes mercium
│   ├── test_seed_customers.py     — probationes clientium
│   ├── test_seed_orders.py        — probationes ordinum et linearum
│   └── test_seed_voyages.py       — probationes navigationum et manifesti
├── .pre-commit-config.yaml
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── main.py

Quid proximum

SQLAlchemy ad Postgres conectere et seed.py contra basim datorum veram currere. Deinde Metabase instituere et interrogationes facere:

Quae navis maxime lucrosa est?
Quae merces maximum lucrum afferunt?
Quid Decimus Obscurus agit?
