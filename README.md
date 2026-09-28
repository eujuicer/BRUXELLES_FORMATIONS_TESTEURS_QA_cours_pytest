# Cours pytest — Plugins installés

Ce projet utilise plusieurs plugins pytest en plus du framework de base. Ce README recense ce qui est installé, ce qui est activé automatiquement, et comment déclencher manuellement chaque fonctionnalité.

## Installation

```
pip install -r requirements.txt
```

## Configuration automatique (`pytest.ini`)

À la racine du projet, `pytest.ini` définit des options appliquées à **chaque** `pytest`, sans rien taper en plus :

```ini
[pytest]
addopts = --cov=. --cov-report=term-missing --cov-report=html --html=report.html --self-contained-html
```

Concrètement, un simple :
```
pytest
```
génère automatiquement :
- le résumé de couverture dans le terminal (avec les lignes manquantes)
- `htmlcov/index.html` (rapport de couverture détaillé)
- `report.html` (rapport des résultats de tests)

Ces deux fichiers HTML sont générés localement et ignorés par git (voir `.gitignore`).

---

## Plugins installés

### Activés automatiquement (rien à taper)

| Plugin | Rôle |
|---|---|
| **pytest-sugar** | Remplace l'affichage par défaut : barre de progression, résultats colorés compacts, échecs affichés immédiatement. S'active dès qu'il est installé, aucune option requise. |
| **pytest-cov** | Mesure la couverture de code. Activé ici via `--cov=...` dans `pytest.ini`. |
| **pytest-html** | Génère le rapport HTML des résultats de tests. Activé ici via `--html=...` dans `pytest.ini`. |
| **pytest-randomly** | Mélange l'ordre d'exécution des tests à **chaque run**, pour détecter les tests mal isolés (qui dépendraient d'un ordre ou d'un état partagé). Affiche une seed en haut du run. |
| **pytest-describe** | Permet d'écrire des tests façon BDD avec des fonctions `describe_...`. Pas d'option à activer, c'est une syntaxe de découverte de tests. |

### À activer manuellement via une option

| Plugin | Commande | Effet |
|---|---|---|
| **pytest-rich** | `pytest --rich` | Reporter terminal alternatif basé sur `rich` (tables, panels). Nécessite un vrai terminal (TTY) — ne fonctionne pas si la sortie est redirigée. |
| **pytest-clarity** | `pytest --force-color` | Diffs colorés et lisibles côte-à-côte quand une assertion sur un dict/liste/objet complexe échoue, au lieu du diff brut de pytest. |
| **pytest-xdist** | `pytest -n auto` | Exécute les tests en parallèle sur plusieurs cœurs CPU. `auto` détecte le nombre de cœurs disponibles ; on peut aussi forcer un nombre : `pytest -n 4`. Utile surtout sur une grosse suite ou des tests lents. |
| **pytest-repeat** | `pytest --count=10 test_orders.py::test_create_order_nominal` | Relance le(s) test(s) ciblé(s) N fois de suite. Utile pour traquer un test flaky (qui échoue parfois de façon aléatoire). |
| **pytest-cov** (mode détaillé) | `pytest --cov=. --cov-report=term-missing` | Déjà actif par défaut via `pytest.ini`, mais utile de savoir le taper explicitement si besoin d'un rapport ponctuel différent (ex. `--cov=booking` pour ne couvrir qu'un seul module). |

### Disponible dans le code des tests (pas une option CLI)

| Plugin | Usage |
|---|---|
| **pytest-mock** | Ajoute la fixture `mocker` à n'importe quel test : `def test_x(mocker): mock_fn = mocker.patch("module.fonction")`. Équivalent à `unittest.mock.patch`, mais avec nettoyage automatique du patch en fin de test (pas besoin de context manager ni de `.stop()`). |

---

## Commandes utiles au quotidien

```bash
# Run standard (couverture + rapports HTML générés automatiquement)
pytest

# Cibler un fichier
pytest test_orders.py

# Cibler un test précis
pytest test_orders.py::test_create_order_nominal

# Mode verbeux
pytest -v

# Filtrer par nom de test (expression sur le nom, pas un chemin de fichier)
pytest -k "order"

# Rendu terminal Rich (nécessite un vrai terminal)
pytest --rich

# Diffs colorés sur assertions complexes
pytest --force-color

# Paralléliser l'exécution
pytest -n auto

# Rejouer un test plusieurs fois (test flaky)
pytest --count=20 test_orders.py::test_create_order_nominal

# Désactiver temporairement le mélange aléatoire de pytest-randomly
# (retrouver l'ordre des fichiers)
pytest -p no:randomly

# Rejouer exactement le même ordre aléatoire qu'un run précédent
# (la seed est affichée en haut de chaque run : "Using --randomly-seed=12345")
pytest -p randomly --randomly-seed=12345
```

## Rapports générés

| Fichier | Contenu |
|---|---|
| `htmlcov/index.html` | Couverture de code ligne par ligne, par fichier (vert = couvert, rouge = non couvert) |
| `report.html` | Résultats des tests (passés/échoués), autonome (`--self-contained-html`), donc partageable tel quel sans dépendance externe |

Ces fichiers sont régénérés à chaque `pytest` et ne sont pas versionnés (voir `.gitignore`).
