"""Tests execution : dicos, erreurs, CLI, espaces, syntaxe, --version."""
import subprocess
import sys

import pytest

from alize import __version__
from alize.main import charger_remplacements, executer, main
from alize.remplacements import remplacements as dico_defaut


def test_dictionnaire_defaut_charge_apres_installation():
    dico = charger_remplacements(None)
    assert isinstance(dico, dict)
    assert dico["si"] == "if"
    assert dico["afficher"] == "print"
    assert len(dico) >= 100


def test_dictionnaire_personnalise(tmp_path):
    perso = tmp_path / "mes_remplacements.py"
    perso.write_text('remplacements = {"dire": "print"}\n', encoding="utf-8")
    dico = charger_remplacements(str(perso))
    assert dico == {"dire": "print"}


def test_dictionnaire_personnalise_invalide(tmp_path):
    mauvais = tmp_path / "mauvais.py"
    mauvais.write_text("x = 1\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        charger_remplacements(str(mauvais))
    assert exc.value.code != 0


def test_execution_fichier_az(tmp_path, capsys):
    prog = tmp_path / "bonjour.az"
    prog.write_text('afficher("bonjour")\n', encoding="utf-8")
    executer(str(prog), charger_remplacements(None))
    assert capsys.readouterr().out.strip() == "bonjour"


def test_fichier_inexistant():
    with pytest.raises(SystemExit) as exc:
        executer("/tmp/n_existe_pas_az.az", dico_defaut)
    assert exc.value.code != 0


def test_erreur_syntaxe(tmp_path):
    prog = tmp_path / "cassé.az"
    prog.write_text("si :\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        executer(str(prog), dico_defaut)
    assert exc.value.code != 0


def test_cli_version():
    r = subprocess.run([sys.executable, "-m", "alize.main", "--version"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert __version__ in r.stdout


def test_chemin_avec_espaces(tmp_path, capsys):
    dossier = tmp_path / "mon dossier"
    dossier.mkdir()
    prog = dossier / "mon prog.az"
    prog.write_text('afficher("espaces ok")\n', encoding="utf-8")
    main([str(prog)])
    assert capsys.readouterr().out.strip() == "espaces ok"
