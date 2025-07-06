import sys

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from intern.helpers.person import Person


class WahlManager:
    def __init__(self):
        self.path = Path("../Wahl-Daten.xlsx")
        self.tables = {
            "Allgemein": pd.DataFrame(columns=["Schlüssel", "Wert"]),
            "Wahltermine": pd.DataFrame(columns=["Tag", "Datum", "Startzeit", "Endzeit", "Raum"]),
            "Kandidaten": pd.DataFrame(columns=[
                "Semester", "Mtknr", "Nachname", "Vorname", "Wahlfb", "Abschluss1", "Fach1_1",
                "kandidatur", "unterstützer", "gewählt", "stimmen"]),
            "Wahlausschuss": pd.DataFrame(columns=["Name"])
        }
        if not self.path.exists():
            self.erstelle_excel()

    def findeLogo(self):
        for datei in Path("../FSR Logo").iterdir():
            if datei.suffix.lower() in {".png", ".jpg", ".jpeg"} and datei.is_file():
                return datei
        print("FSR Logo nicht gefunden", file=sys.stderr)
        return None

    def __findeWaehlerverzeichnis(self):
        for datei in Path("../Waehlerverzeichnis").iterdir():
            if datei.suffix.lower() in {".xlsx"} and datei.is_file():
                return datei
        raise Exception("Waehlerverzeichnis nicht gefunden")

    def erstelle_excel(self):
        # Waehlerverzeichnis laden
        waehler_df = pd.read_excel(self.__findeWaehlerverzeichnis())

        # Felder ergänzen, falls nicht vorhanden
        for spalte in ["kandidatur", "unterstützer", "gewählt", "stimmen"]:
            if spalte not in waehler_df.columns:
                waehler_df[spalte] = ""

        self.tables["Kandidaten"] = waehler_df

        # Standardwerte
        self.tables["Allgemein"] = pd.DataFrame([
            ["Fachschaft", ""],
            ["Fachschaftsnummer", ""],
            ["FSR Plätze", ""],
            ["E-Mail", "fsk@asta-due.org"],
            ["Briefkasten", ""],
            ["VV Datum", ""]
        ], columns=["Schlüssel", "Wert"])

        heute = datetime.today().date()
        startzeit, endzeit = "10:00", "16:00"
        raum = "TBA"
        self.tables["Wahltermine"] = pd.DataFrame([
            ["Tag 1", heute, startzeit, endzeit, raum],
            ["Tag 2", heute + timedelta(days=1), startzeit, endzeit, raum],
            ["Tag 3", heute + timedelta(days=2), startzeit, endzeit, raum]
        ], columns=["Tag", "Datum", "Startzeit", "Endzeit", "Raum"])

        # Speichern
        with pd.ExcelWriter(self.path, engine="openpyxl") as writer:
            for name, df in self.tables.items():
                df.to_excel(writer, sheet_name=name, index=False)

    def lade_excel(self):
        xls = pd.ExcelFile(self.path)
        for name in xls.sheet_names:
            self.tables[name] = pd.read_excel(xls, sheet_name=name)

    def save(self):
        with pd.ExcelWriter(self.path, engine="openpyxl") as writer:
            for name, df in self.tables.items():
                df.to_excel(writer, sheet_name=name, index=False)

    def get_statistik(self):
        kandidaten = self.tables["Kandidaten"]
        gesamt = len(kandidaten)
        kandidatenanzahl = kandidaten["kandidatur"] == "x"
        gewaehltanzahl = kandidaten["gewählt"] == "x"
        return {
            "gesamt": gesamt,
            "kandidaturen": kandidatenanzahl.sum(),
            "gewaehlt": gewaehltanzahl.sum()
        }

    def setze_wahlausschuss(self, namen: list[str]):
        self.tables["Wahlausschuss"] = pd.DataFrame(namen, columns=["Name"])

    def get_termine(self):
        return self.tables["Wahltermine"]

    def setze_termin(self, tag: str, datum: datetime.date, start: str, ende: str, raum: str):
        termine = self.tables["Wahltermine"]
        idx = termine[termine["Tag"] == tag].index
        if not idx.empty:
            termine.loc[idx[0]] = [tag, datum, start, ende, raum]
        else:
            termine.loc[len(termine)] = [tag, datum, start, ende, raum]

    def get_person(self, mtknr: int):
        return Person(mtknr, self.path)
