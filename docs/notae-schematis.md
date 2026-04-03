Phoenix et Piper — Notae Schematis

Quid aedificavimus et cur
Schema et modela

Schema est structura datorum in Postgres — tabulae, columnae, typi, vincula. Modelum est classis Pythonica (in SQLAlchemy scripta) quae schema definit. Modela scribimus; SQLAlchemy schema creat.

Hoc instrumentum ORM nominatur — Object-Relational Mapper. Inter duos mundos versatur: Python obiecta habet, Postgres tabulas habet; ORM inter eos interpretatur.

Omnia modela nostra ex una classe Base haereditant:

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

SQLAlchemy per Base omnes tabulas cognoscit atque creare potest.

Claves primariae et alienae

Clavis primaria (primary key) quemque ordinem in tabula unice designat. Quisque portus, quaeque navis, quisque ordo suum id habet — numerum quem dator ipse assignat.

Clavis aliena (foreign key) tabulam ad aliam tabulam coniungit. Iter duos portus habet: origin_port_id et destination_port_id. Hi numeri ad ordines in tabula ports referunt. Si portum 99 referas qui non exsistit, Postgres recusat — integritatem datorum ipse custodit.

origin_port_id: Mapped[int] = mapped_column(ForeignKey("ports.id"))

Catena "ports.id" nomen tabulae et columnae indicat.

Columnae nullabiles

Non omnis columna semper valorem habet. special_handling in mercibus Pepper-classis vacua est, quia piper nullam curam propriam requirit. Hoc per nullable=True significamus:

special_handling: Mapped[str | None] = mapped_column(String(200), nullable=True)

Mapped[str | None] Pythoni dicit: “valor fortasse None erit.” nullable=True Postgres dicit: “columna vacua esse licet.”

Entia nostra
Portus (ports)

Locus ubi naves applicant. Nomen, situs (latitudo et longitudo), magnitudo, vectigal fundamentale.

name — unicum (duo portus Ostia nominari non possunt)
size — 1 ad 5 (a vico piscatorio ad emporium magnum)
base_fee — vectigal applicandi, in denariis
Iter (routes)

Connexio inter duos portus, directionalis — Ostia→Puteoli et Puteoli→Ostia sunt ordines separati, quia venti et fluctus directionem praeferunt.

origin_port_id, destination_port_id — claves alienae ad ports
distance_km — longitudo itineris
base_sailing_days — tempus navigandi sub condicionibus ordinariis
danger_level — 1 ad 5 (a tranquillo ad periculosissimum)
danger_type — “natural”, “mythological”, “divine”, “piracy”, vel “none”
Genus navis (ship_types)

Categoriae navium Romanarum:

Corbita — navis oneraria communissima, ampla et lenta, ad merces Pepper-classis
Actuaria — navis velox cum remis et velis, ad merces Phoenix-classis
Ponto — navis magna asymmetrica, duos malos habens

Attributa: cargo_capacity_tons, base_speed_knots, operating_cost_daily, et can_carry_phoenix — non omnis navis merces mythologicas ferre debet!

Navis (ships)

Navis singularis cum nomine, typo (ship_type_id), portu domestico (home_port_id), condicione (1–5), et statu (“in_port”, “at_sea”, “under_repair”).

Duas claves alienas habet — ad ship_types et ad ports. Ita rete relationum paulatim crescit.

Genus mercis (cargo_types)

Merces quas Phoenix et Piper transportat. Duae classes:

Phoenix-classis — rarae, periculosae, mythologicae (cinis phoenicis, venenum basilisci, lapides magnetici). Pretia alta, periculum altum, cura propria.
Pepper-classis — merces communes (piper, garum, silphium, purpura Tyria). Moles magna, margines tenues.

special_handling nullabilis est — merces Pepper-classis hoc campo non egent.

Clientes (customers)

Qui merces emunt: mercatores, templa, praefecti provinciarum, magi. Nomen, typum (customer_type), et portum domesticum habent.

name non est unicum — duo mercatores idem nomen habere possunt. Roma magna erat.

Ordines (orders)

Cliens merces alicubi destinandas iubet. Ordo diem, statum (“pending”, “in_transit”, “delivered”, “cancelled”), clientem (customer_id), et portum destinationis habet.

Ordo ipse non dicit quid iussum sit — hoc lineae ordinis efficiunt.

Lineae ordinum (order_lines)

Singula res in ordine: “L amphorae gari” vel “III vasa veneni basilisci.” Quaeque linea ad ordinem (order_id) et genus mercis (cargo_type_id) refertur, cum quantitate.

Hoc exemplar classicum est: tabula capitis (orders) cum tabula singularum rerum (order_lines).

Navigationes (voyages)

Navis iter faciens. Navigatio navem (ship_id) et iter (route_id) coniungit, cum die profectionis et die adventus.

arrival_date nullabilis est — si navis adhuc navigat, nondum advenit.

Manifestum navigationis (voyage_manifest)

Tabula ligandi — navigationes ad lineas ordinum conectit. Si navis L amphoras gari et III vasa veneni fert, duae lineae in manifesto sunt, eadem voyage_id habentes sed diversas order_line_id.

Haec tabula interrogationibus fundamentalibus respondet: quid in hac nave est? quanta pecunia haec navigatio fert? quid accidit si navis mergitur?

Probationes (tests)

Quodque ens probatione simplici confirmamus — obiectum Pythonicum creamus et attributa inspicimus:

def test_port_creation():
    port = Port(name="Ostia", latitude=41.76, longitude=12.29, size=5, base_fee=50)
    assert port.name == "Ostia"
    assert port.base_fee == 50

Hae probationes basim datorum nondum attingunt — tantum confirmant classes Pythonicas recte definitas esse. Probationes profundiores (cum ipsa basi datorum) postea scribentur.

XI probationes habemus, omnes virides. uv run pytest eas currit.

Migrationes

Schema non oportet ab initio perfectum esse. Migrationes (per instrumentum Alembic) schema mutare sinunt — columnam addere, typum mutare, tabulam restruere. Quaeque migratio se ipsam invertere potest.

Modela Pythonica mutamus; Alembic differentiam deprehendit et scriptum migrationis generat. Sic schema una cum proposito crescit.

Instrumenta
uv add sqlalchemy — dependentiam ordinariam addit (proiectum ipsum eget)
uv add psycopg2-binary — adaptor Pythonicus pro PostgreSQL
uv add --dev jupyter — ad commentarios (blogos) scribendos
uv run pytest — probationes currit
Quid proximum

SQLAlchemy ad Postgres conectere et tabulas re vera creare. Deinde generatorem datorum artificialium scribere — mundum nostrum portibus, navibus, clientibus, ordinibus implere. Denique Metabase instituetur, et interrogationes ut “quae navis maxime lucrosa est?” responderi poterunt.

Structura proiecti (nunc)
phoenix-and-pepper/
├── .github/workflows/ci.yml
├── docs/
│   ├── notae-apparandi.md         — notae Phase 0a (pipeline, uv, ruff)
│   ├── notae-continentis.md       — notae Phase 0b (continentes, Postgres)
│   └── notae-schematis.md         — notae Phase 0c (hae notae)
├── src/
│   ├── __init__.py
│   └── models.py                  — omnia modela SQLAlchemy
├── tests/
│   └── test_models.py             — XI probationes entium
├── .pre-commit-config.yaml
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── main.py
