# Alize V5 — Python in French

[Version francaise](FR_README.md)

Alize is a French version of Python: you write code with French keywords and
built-in names (`.az` files), Alize translates it to Python with `tokenize`
and runs it. Strings and comments are never modified.

## Requirements

- Python 3.9+ for development (tested on 3.13), no runtime dependency.
- Homebrew (macOS) only needed for the Homebrew install method.

Install Python if needed:

```bash
# macOS
brew install python@3.13
# Ubuntu/Debian
sudo apt install python3 python3-venv
```

## Install from source

```bash
git clone https://github.com/celtmen-cpu/alize
cd alize
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run a .az file

```bash
alize fichier.az
python3 -m alize.main fichier.az
```

Example `bonjour.az`:

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

## Custom dictionary

A custom dictionary is a Python file defining a `remplacements` dict. Its
script goes LAST on the command line:

```bash
alize fichier.az mes_remplacements.py
```

```python
# mes_remplacements.py
remplacements = {
    "dire": "print",
}
```

## Show the version

```bash
alize --version
```

## Run the tests

```bash
python -m pytest -v
```

12 tests cover: translation, strings/comments preservation, default and
custom dictionaries, invalid dictionary, `.az` execution, missing files,
syntax errors, `--version`, paths with spaces.

## Install via Homebrew (once published)

> Not available yet: the `alize/homebrew-alize` tap and the `v5.0.0`
> release are not published, so the commands below will fail until then.

```bash
brew tap alize/alize
brew install alize
alize fichier.az
```

## Contribute

1. Fork and clone the repo.
2. Create a venv and install with `.[dev]`.
3. Add words to `alize/remplacements.py` (keep `sans-accent` variants).
4. Add a test in `tests/`, run `python -m pytest -v`.
5. Open a pull request — no direct push to `main`, no secrets in code.

## Publish a new version

1. Bump `__version__` in `alize/__init__.py` and `version` in
   `pyproject.toml` (keep both in sync).
2. Run tests + build: `python -m pytest -v && python -m build`.
3. Commit, tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z`.
4. Create the GitHub release from the tag.
5. Compute `shasum -a 256` of the release tarball and fill `url`/`sha256`
   in `Formula/alize.rb`.
6. Publish the tap `alize/homebrew-alize` and test
   `brew install --build-from-source Formula/alize.rb`.

## Project layout

```
alize/
  alize/
    __init__.py       # __version__
    main.py           # CLI (argparse), tokenize translator, exec
    remplacements.py  # French -> Python dictionary (133 entries)
  tests/
    test_traduction.py
    test_execution.py
  Formula/
    alize.rb          # Homebrew formula (placeholders until release)
  README.md           # this file (English)
  FR_README.md        # documentation en francais
  pyproject.toml      # packaging, `alize` command, pytest config
  .gitignore
  LICENSE             # MIT
```

## License

MIT — see `LICENSE`.
