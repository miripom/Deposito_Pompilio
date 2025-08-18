def conta_righe(file):
    try:
        with open(file, "r" , encoding="utf-8") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return f"Errore: il file '{file}' non esiste."



