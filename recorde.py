import json
import os


ARQUIVO_RECORDE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "recorde.json"
)


def carregar_recorde():
    try:
        with open(ARQUIVO_RECORDE, "r", encoding="utf-8") as arquivo:
            return int(json.load(arquivo).get("recorde", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def salvar_recorde(valor):
    try:
        with open(ARQUIVO_RECORDE, "w", encoding="utf-8") as arquivo:
            json.dump({"recorde": valor}, arquivo)
    except OSError:
        pass
