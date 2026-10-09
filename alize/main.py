"""Interpreteur Alize : traduit du Python francais (.az) puis l'execute.

Le traducteur utilise `tokenize` et ne remplace que les tokens de type NAME
presents dans le dictionnaire : les chaines et les commentaires sont intacts.
"""
import argparse
import importlib.util
import sys
import tokenize
from io import BytesIO
from pathlib import Path

from alize import __version__


def charger_remplacements(chemin=None):
    """Charge le dictionnaire de remplacements.

    Sans chemin : dictionnaire par defaut du package (marche depuis
    n'importe quel repertoire une fois installe).
    Avec un chemin : fichier Python definissant `remplacements` (dict).
    """
    if chemin is None:
        from alize.remplacements import remplacements
        return dict(remplacements)
    spec = importlib.util.spec_from_file_location("remplacements_perso", chemin)
    if spec is None or spec.loader is None:
        print("Erreur : impossible de charger " + str(chemin), file=sys.stderr)
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError:
        print("Erreur : fichier introuvable : " + str(chemin), file=sys.stderr)
        raise SystemExit(1)
    except Exception as e:
        print("Erreur chargement " + str(chemin) + " : " + str(e), file=sys.stderr)
        raise SystemExit(1)
    if not hasattr(module, "remplacements"):
        print("Erreur : le fichier doit definir une variable remplacements (dict)",
              file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(module.remplacements, dict):
        print("Erreur : 'remplacements' doit etre un dictionnaire", file=sys.stderr)
        raise SystemExit(1)
    return module.remplacements


def traduire(code, remplacements):
    """Traduit le code Alize en Python via tokenize (NAME uniquement)."""
    tokens = tokenize.tokenize(BytesIO(code.encode("utf-8")).readline)
    resultat = []
    for token in tokens:
        if token.type == tokenize.NAME:
            token = token._replace(
                string=remplacements.get(token.string, token.string)
            )
        resultat.append(token)
    return tokenize.untokenize(resultat).decode("utf-8")


def executer(fichier, remplacements):
    """Lit, traduit et execute un fichier .az.Code de sortie != 0 en erreur."""
    chemin = Path(fichier)
    if not chemin.is_file():
        print("Erreur : fichier introuvable : " + str(fichier), file=sys.stderr)
        raise SystemExit(1)
    try:
        code = chemin.read_text(encoding="utf-8")
    except OSError as e:
        print("Erreur lecture " + str(fichier) + " : " + str(e), file=sys.stderr)
        raise SystemExit(1)
    try:
        code_python = traduire(code, remplacements)
    except (tokenize.TokenError, IndentationError, SyntaxError) as e:
        print("Erreur de syntaxe dans " + str(fichier) + " : " + str(e),
              file=sys.stderr)
        raise SystemExit(1)
    try:
        bytecode = compile(code_python, str(fichier), "exec")
    except SyntaxError as e:
        print("Erreur de syntaxe dans " + str(fichier) + " : " + str(e),
              file=sys.stderr)
        raise SystemExit(1)
    exec(bytecode, {"__name__": "__main__"})


def construire_parseur():
    p = argparse.ArgumentParser(
        prog="alize",
        description="Alize : execute du Python en francais (.az)",
    )
    p.add_argument("fichier", nargs="?",
                   help="fichier .az a executer")
    p.add_argument("dictionnaire", nargs="?",
                   help="dictionnaire personnalise (script Python, EN DERNIER)")
    p.add_argument("--version", action="version", version="alize " + __version__)
    return p


def main(argv=None):
    args = construire_parseur().parse_args(argv)
    if not args.fichier:
        print("Utilisation : alize programme.az [dictionnaire.py]", file=sys.stderr)
        raise SystemExit(2)
    remplacements = charger_remplacements(args.dictionnaire)
    executer(args.fichier, remplacements)


if __name__ == "__main__":
    main()
