import Counter
import re

def conta_righe(file):
    try:
        with open(file, "r" , encoding="utf-8") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return f"Errore: il file '{file}' non esiste."


def conta_parole(file):
    try:
        with open(file, "r" , encoding="utf-8") as f:
            testo = f.read()
            parole = re.findall(r"\w+", testo.lower())
            return len(parole)
    except FileNotFoundError:
        return f"Errore: il file '{file}' non esiste."

