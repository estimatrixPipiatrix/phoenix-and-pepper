# Phoenix et Piper — Notae Continentis

## Quid aedificavimus et cur

### Continentes (Podman)

Podman instituimus ut servitia (velut PostgreSQL) in continentibus curramus, non in machina ipsa. Continens est quasi capsula clausa: systema operandi, programmata, configurationem — omnia intra se continet, a machina nostra separata.

Docker quoque consideravimus. Docker Desktop licentiam solutam requirit pro societatibus maioribus; Docker Engine (in Linux) gratis est. Podman omnino gratis et apertus est, et fere eadem mandata accipit ac Docker. Pro proposito nostro, utrumque sufficit — Podman elegimus.

Mandata praecipua:

    sudo apt install podman           — Podman instituit
    uv tool install podman-compose    — instrumentum compositionis instituit
    podman ps                         — continentes currentes ostendit
    podman-compose up -d              — continentes in fundo excitat
    podman-compose down               — continentes sistit

### Imagines et continentes

Distinctio magni momenti: **imago** est exemplar praeparatum (quasi forma), **continens** est instantia currens illius imaginis.

Cum `podman-compose up` primum currimus:

1. Podman imaginem localiter quaerit
2. Non inventa, eam ex Docker Hub deducit (semel tantum)
3. Continentem ex imagine creat et excitat

Secunda vice, imago iam adest — continens statim surgit.

### PostgreSQL in continente

Servitorem PostgreSQL non in machina nostra instituimus. Potius imaginem officialem `docker.io/library/postgres:16` adhibemus, quae PostgreSQL iam institutum et configuratum continet.

### Fasciculus docker-compose.yml

Hic fasciculus definit quae continentes excitanda sint et quomodo configurentur:

```yaml
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
```

Quid singulae partes significent:

- **version** — versio formae compositionis (formulae)
- **services** — index continentium. Nunc unum tantum habemus: `db`
- **image** — quae imago ex Docker Hub deducatur
- **container\_name** — nomen humanum continentis (aliter Podman nomen fortuitum dat)
- **environment** — variabiles ambitus quas imago Postgres legit cum primum excitatur: nomen datorum, nomen usoris, tessera
- **ports: "5432:5432"** — portam 5432 continentis ad portam 5432 machinae nostrae ligat. Sic SQLAlchemy (in machina nostra currens) datorum (in continente currens) attingere potest
- **volumes: pgdata:/var/lib/postgresql/data** — data datorum in volumine nominato servat, ut persistant etiam cum continens sistitur. Sine hoc, omnia data cum continente perirent
- **volumes: pgdata:** (infra) — volumen nominatum declarat cum optionibus praedefinitis. Clavis sine valore in YAML significat "hoc exsistit, optiones praedefinitas adhibe"

### Connexio ad datorum

Cum continens currit, per `psql` intra continentem conecti possumus:

    podman exec -it phoenix_db psql -U phoenix -d phoenix_and_pepper

Hoc significat: "intra continentem phoenix_db, psql aperi cum usore 'phoenix' et datore 'phoenix_and_pepper'."

Mandata utilia intra psql:

    \dt    — tabulas enumerat (nullae adhuc sunt)
    \q     — exit

### Structura proiecti (nunc)

```
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
```

### Mandata cotidiana

```bash
# Continentem excitare
podman-compose up -d

# Statum inspicere
podman ps

# Ad datorum conectere
podman exec -it phoenix_db psql -U phoenix -d phoenix_and_pepper

# Continentem sistere
podman-compose down
```

### Quid proximum

SQLAlchemy — schema datorum per classes Pythonicas definiemus: naves, merces, itinera, clientes, ordines. Deinde generatores datorum syntheticorum scribentur, et probationes unitatis omnia confirmabunt.
