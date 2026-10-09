# Alize V5 — Python en francais

[English version](README.md)

Alize est une version francaise de Python : vous ecrivez du code avec des
mots-cles et fonctions en francais (fichiers `.az`), Alize le traduit en
Python avec `tokenize` et l'execute. Les chaines et les commentaires ne sont
jamais modifies.

## Pre-requis

- Python 3.9+ pour developper (teste en 3.13), aucune dependance a l'execution.
- Homebrew (macOS) uniquement pour la methode d'installation Homebrew.

Installer Python si besoin :

```bash
# macOS
brew install python@3.13
# Ubuntu/Debian
sudo apt install python3 python3-venv
```

## Installer depuis les sources

```bash
git clone https://github.com/celtmen-cpu/alize
cd alize
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Executer un fichier .az

```bash
alize fichier.az
python3 -m alize.main fichier.az
```

Exemple `bonjour.az` :

```python
fonction saluer(nom):
    retourner "Bonjour " + nom

pour i dans intervalle(3):
    si i == 1:
        afficher("un")
    sinonsi i == 2:
        afficher(saluer("Alize"))
    sinon:
        afficher(i)
```

## Dictionnaire personnalise

Un dictionnaire perso est un fichier Python qui definit un dict
`remplacements`. Son script se met A LA FIN de la commande :

```bash
alize fichier.az mes_remplacements.py
```

```python
# mes_remplacements.py
remplacements = {
    "dire": "print",
}
```

## Afficher la version

```bash
alize --version
```

## Lancer les tests

```bash
python -m pytest -v
```

12 tests couvrent : traduction, preservation chaines/commentaires, dicos par
defaut et perso, dico invalide, execution `.az`, fichiers manquants, erreurs
de syntaxe, `--version`, chemins avec espaces.

## Installer via Homebrew (une fois publie)

> Pas encore disponible : le tap `alize/homebrew-alize` et la release
> `v5.0.0` ne sont pas publies, les commandes ci-dessous echoueront jusque-la.

```bash
brew tap alize/alize
brew install alize
alize fichier.az
```

## Contribuer

1. Forkez et clonez le depot.
2. Creez un venv et installez avec `.[dev]`.
3. Ajoutez des mots dans `alize/remplacements.py` (gardez les variantes
   sans accent).
4. Ajoutez un test dans `tests/`, lancez `python -m pytest -v`.
5. Ouvrez une pull request — pas de push direct sur `main`, pas de secrets.

## Publier une nouvelle version

1. Montez `__version__` dans `alize/__init__.py` et `version` dans
   `pyproject.toml` (gardez les deux synchronises).
2. Tests + build : `python -m pytest -v && python -m build`.
3. Commit, tag et push : `git tag vX.Y.Z && git push origin vX.Y.Z`.
4. Creez la release GitHub depuis le tag.
5. Calculez `shasum -a 256` de l'archive et renseignez `url`/`sha256` dans
   `Formula/alize.rb`.
6. Publiez le tap `alize/homebrew-alize` et testez
   `brew install --build-from-source Formula/alize.rb`.

## Structure du projet

```
alize/
  alize/
    __init__.py       # __version__
    main.py           # CLI (argparse), traducteur tokenize, exec
    remplacements.py  # dictionnaire francais -> Python (133 entrees)
  tests/
    test_traduction.py
    test_execution.py
  Formula/
    alize.rb          # formule Homebrew (placeholders avant release)
  README.md           # documentation (anglais)
  FR_README.md        # ce fichier (francais)
  pyproject.toml      # packaging, commande `alize`, config pytest
  .gitignore
  LICENSE             # MIT
```

## Licence

MIT — voir `LICENSE`.
