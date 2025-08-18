from collections import Counter
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

def parole_frequenti(file):
    try:
        with open(file, "r" , encoding="utf-8") as f:
            testo = f.read()
            parole = re.findall(r"\w+", testo.lower())
            frequenze = Counter(parole).most_common(5)
            return [f"{parola}:{conteggio}" for parola, conteggio in frequenze]
    except FileNotFoundError:
        return f"Errore: il file '{file}' non esiste."

file = "18 Agosto\Esercizio 1\input.txt"
print("Numero di righe:", conta_righe(file))
print("Numero di parole totali:", conta_parole(file))
print("Top 5 parole:", parole_frequenti(file))