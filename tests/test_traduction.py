"""Tests du traducteur : fonction FR->Python, chaines, commentaires, multi-fonctions."""
from alize.main import traduire
from alize.remplacements import remplacements


def test_traduction_fonction_francaise():
    code = "fonction saluer(nom):\n    retourner nom\n"
    traduit = traduire(code, remplacements)
    assert "def saluer(nom):" in traduit
    assert "return nom" in traduit
    assert "fonction" not in traduit


def test_chaines_guillemets_preservees():
    code = 'afficher("si pour fonction")\n'
    traduit = traduire(code, remplacements)
    assert '"si pour fonction"' in traduit  # chaine intacte
    assert traduit.startswith("print(")  # seul l'appel est traduit


def test_commentaires_preserves():
    code = "# si pour fonction\nsi Vrai:\n    passer\n"
    traduit = traduire(code, remplacements)
    assert "# si pour fonction" in traduit  # commentaire intact
    assert "if True:" in traduit
    assert "pass" in traduit


def test_plusieurs_fonctions_meme_programme():
    code = (
        "fonction double(x):\n    retourner x * 2\n\n"
        "fonction triple(x):\n    retourner x * 3\n\n"
        "afficher(double(2))\n"
        "afficher(triple(2))\n"
    )
    traduit = traduire(code, remplacements)
    assert traduit.count("def ") == 2
    assert traduit.count("return ") == 2
    assert "print(double(2))" in traduit
    assert "print(triple(2))" in traduit
    # execution reelle du code traduit
    env = {}
    exec(compile(traduit, "test.az", "exec"), env)
    assert env["double"](2) == 4
    assert env["triple"](2) == 6
