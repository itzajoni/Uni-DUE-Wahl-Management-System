import pandas as pd
import sys
import os

_REQUIRED_COLUMNS = [
    "Semester", "Mtknr", "Nachname", "Vorname", "Wahlfb", "Abschluss1", "Fach1_1"
]

_ADDITIONAL_COLUMNS = ["kandidatur", "unterstuetzer", "gewählt", "stimmen", "mail"]

def _load_excel(path="../Wählerverzeichnis"):
    for file in os.walk(path): #datei finden
        if str(file).endswith(".xlsx"):
            path = file
            break
    else:
        print(f"Fehler: Datei {path} nicht gefunden.")
        sys.exit(1)

    df = pd.read_excel(path, dtype=str)

    # Prüfe Pflichtspalten
    for col in _REQUIRED_COLUMNS:
        if col not in df.columns:
            print(f"Fehler: Spalte '{col}' fehlt im Wählerverzeichnis.")
            sys.exit(1)

    # Zusätzliche Spalten anlegen, falls nicht vorhanden
    for col in _ADDITIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df, path

def suche_nach_mtk(mtk):
    df, _ = _load_excel()
    eintrag = df[df["Mtknr"] == str(mtk)]
    return eintrag if not eintrag.empty else None

def setze_kreuz(mtk, spalte):
    if hasattr(mtk, "Mtknr"): mtk = mtk.Mtknr #kann auch als objekt übergeben werden
    if spalte not in ["kandidatur", "unterstützer", "gewählt"]:
        raise ValueError("Ungültige Spalte")
    df, path = _load_excel()
    df.loc[df["Mtknr"] == str(mtk), spalte] = "x"
    df.to_excel(path, index=False)

def setze_wert(mtk, name, wert):
    if hasattr(mtk, "Mtknr"): mtk = mtk.Mtknr #kann auch als objekt übergeben werden
    df, path = _load_excel()
    df.loc[df["Mtknr"] == str(mtk), name] = str(wert)
    df.to_excel(path, index=False)

def zaehle_daten():
    df, _ = _load_excel()
    gesamt = len(df)
    gewaehlt = df["gewählt"].str.lower().eq("x").sum()
    kandidatur = df["kandidatur"].str.lower().eq("x").sum()
    return gesamt, gewaehlt, kandidatur

def kandidaten():
    df, _ = _load_excel()
    return df[df.get("kandidatur", "").astype(str).str.lower() == "x"]