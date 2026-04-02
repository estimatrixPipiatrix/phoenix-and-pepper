Phoenix et Piper — Notae Continentis
Quid aedificavimus et cur
Continentes (Podman)

Podman instituimus ut servitia (velut PostgreSQL) in continentibus curramus, non in ipsa machina. Continens est quasi capsula clausa: systema operandi, programmata, configurationes — omnia intra se continet, quae a machina nostra separantur.

Docker quoque consideravimus. Docker Desktop licentiam solutam requirit in societatibus maioribus; Docker Engine (in Linux) gratis est. Podman omnino gratis et apertus est, et fere eadem mandata accipit ac Docker. Pro proposito nostro, utrumque sufficit — Podman elegimus.

Mandata praecipua:

sudo apt install podman           — Podman instituit
uv tool install podman-compose    — instrumentum compositionis instituit
podman ps                         — continentes currentes ostendit
podman-compose up -d              — continentes in occulto excitat
podman-compose down               — continentes sistit
Imagines et continentes

Distinctio magni momenti: imago est exemplar praeparatum (quasi forma), continens est instantia currens illius imaginis.

Cum podman-compose up primum currimus:

Podman imaginem localiter quaerit
Si non invenitur, eam ex Docker Hub deducit (semel tantum)
Continentem ex imagine creat et excitat

Secunda vice, imago iam adest — continens statim surgit.

PostgreSQL in continente

Servitorem PostgreSQL non in machina nostra instituimus. Potius imaginem officialem docker.io/library/postgres:16 adhibemus, quae PostgreSQL iam institutum atque configuratum continet.

Fasciculus docker-compose.yml

Hic fasciculus definit quae continentes excitanda sint et quomodo configurentur:

version: "3.9"

services:
  db:
    image: docker.io/library/postgres:16
    container_name: phoenix_db
    environment:
      POSTGRES_DB: phoenix_and_pepper
      POSTGRES_USER: phoenix
      POSTGRES_PASSWORD: pepper
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:

Quid singulae partes significent:

version — versio formae compositionis
services — index continentium. Nunc unum tantum habemus: db
image — quae imago ex Docker Hub deducatur
container_name — nomen humanum continentis (aliter Podman nomen fortuitum dat)
environment — variabiles ambitus quas imago Postgres legit cum primum excitatur: nomen datorum, nomen usoris, tessera
ports: "5432:5432" — portam 5432 continentis ad portam 5432 machinae nostrae coniungit. Sic SQLAlchemy (in machina nostra currens) basim datorum (in continente currentem) attingere potest
volumes: pgdata:/var/lib/postgresql/data — data datorum in volumine nominato servat, ut persistant etiam continente sistente. Sine hoc, omnia data cum continente perirent
volumes: pgdata: (infra) — volumen nominatum declarat cum optionibus praedefinitis. Clavis sine valore in YAML significat “hoc exsistit, optiones praedefinitas adhibeantur”
Connexio ad basim datorum

Cum continens currit, per psql intra continentem conecti possumus:

podman exec -it phoenix_db psql -U phoenix -d phoenix_and_pepper

Hoc significat: “intra continentem phoenix_db, psql aperi cum usore ‘phoenix’ et basi datorum ‘phoenix_and_pepper’.”

Mandata utilia intra psql:

\dt    — tabulas enumerat (nullae adhuc sunt)
\q     — exit
Structura proiecti (nunc)
phoenix-and-pepper/
├── .github/workflows/ci.yml
├── docs/
│   ├── notae-apparandi.md        — notae Phase 0a (pipeline, uv, ruff)
│   └── notae-continentis.md      — notae Phase 0b (hae notae)
├── src/
├── tests/
├── .pre-commit-config.yaml
├── docker-compose.yml             — NOVUM: definitio continentium
├── pyproject.toml
├── uv.lock
└── main.py
Mandata cotidiana
# Continentem excitare
podman-compose up -d

# Statum inspicere
podman ps

# Ad basim datorum conectere
podman exec -it phoenix_db psql -U phoenix -d phoenix_and_pepper

# Continentem sistere
podman-compose down
Quid proximum

SQLAlchemy — schema datorum per classes Pythonicas definiemus: naves, merces, itinera, clientes, ordines. Deinde generatores datorum artificialium scribentur, et probationes unitatis omnia confirmabunt.
