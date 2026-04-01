Phoenix et Piper — Notae Apparandi
Quid paravimus et cur
Repositorium (GitHub)

Repositorium publicum apud GitHub creavimus, nomine phoenix-and-pepper. Publicum esse voluimus, quia hoc propositum opus demonstrativum est — homines codicem, historiam, progressionemque videre possint.

GitLab quoque consideravimus (consilium primum id nominabat), sed nihil in nostro proposito GitLab proprie requiritur. GitHub Actions pipeline CI/CD satis commode administrat, et GitHub communitatem latiorem habet cum pluribus exemplis unde discamus.

Administratio proiecti Pythonici (uv)

Proiectum per uv instituimus, quod versiones Pythonis, dependentias, atque ambitum virtualem administrat. Hic modus veterem substituit — ubi pip, venv, et requirements.txt manu tractabamus.

Mandata praecipua:

uv init — proiectum creat (pyproject.toml, lockfile, etc.)
uv add <package> — dependentiam addit
uv add --dev <package> — dependentiam ad development tantum addit
uv sync --dev — omnia ex lockfile instituit
uv run <command> — mandatum intra ambitum administratum currit

Fasciculus uv.lock magni momenti est — versiones exactas figit, ut quisquis repositorium clonat eundem ambitum recipiat.

Structura proiecti
phoenix-and-pepper/
├── .github/workflows/ci.yml   — pipeline definitio
├── docs/                      — notae et documenta
├── src/                       — codex noster hic continetur
├── tests/                     — probationes nostrae hic sunt
├── .pre-commit-config.yaml    — formatatio automatica ante commit
├── pyproject.toml             — metadata et dependentiae proiecti
├── uv.lock                    — versiones dependentiarum fixae
└── main.py                    — a uv init creatum (locus tenens)
Pipeline CI (GitHub Actions)

Fasciculus .github/workflows/ci.yml definit quid automatice fiat cum codicem impellimus. Pipeline nostra:

Machinam virtualem Ubuntu in nube GitHub excitat
uv instituit
Omnes dependentias nostras instituit
ruff currit (analysis statica et formatatio)
pytest currit

Si quis gradus deficit, pipeline rubet, et statim scimus aliquid errasse antequam ramum main attingat.

Pipeline etiam currit cum merge request facimus: id est, cum ramus proponitur ad coniungendum cum main, pipeline exitum coniunctionis probat antequam re vera coniungatur. Haec est quasi porta securitatis dum in ramis laboramus.

Analysis statica (ruff)

Ruff duas res praestat:

Linting (ruff check .): vitia codicis deprehendit — importationes inutiles, formas improbas, et cetera.
Formatatio (ruff format .): stilum constantem imponit, ne de tabulis contra spatia disputemus.

In pipeline, formatatio cum --check currit — queritur tantum, non corrigit. Localiter autem ruff format . currimus ut res re vera corrigantur.

Uncus pre-commit

pre-commit instituimus, ut ruff automatice currat quotiens git commit facimus. Si ruff aliquid mutat, commit sistitur; tum git add . iterum facimus et deinde committimus.

Hoc efficit ut ruff manu currere non opus sit, et pipeline numquam ob vitia formationis deficiat, quia ea antea deprehenduntur.

Mandata praecipua:

uv run pre-commit install — uncum activat (semel tantum opus est)
Uncus ipse automatice currit cum git commit
Probationes (pytest)

pytest simpliciter adhibemus — functiones nudas cum sententiis assert, nullis classibus necessariis:

def test_something():
    assert 1 + 1 == 2

pytest etiam probationes more unittest scriptas currere potest, ergo si illas ex consuetudine scribamus, nihil impedit quin operentur.

Mandata cotidiana
# Labor cotidianus
uv run ruff format .          # Codicem formare
uv run ruff check --fix .     # Vitia invenire et corrigere
uv run pytest                 # Probationes currere
git add .
git commit -m "nuntius"       # Uncus pre-commit automatice currit
git push                      # Pipeline in GitHub Actions currit

# Apparatio (semel tantum opus est)
uv sync --dev                 # Dependentias instituere
uv run pre-commit install     # Uncum activare
