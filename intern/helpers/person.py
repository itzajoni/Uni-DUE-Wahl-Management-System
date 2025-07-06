import pandas as pd
from pathlib import Path


class Person:
    def __init__(self, mtknr: int, path: Path):
        self.mtknr = mtknr
        self.path = path
        self.sheet_name = "Kandidaten"

        if not self.path.exists():
            raise FileNotFoundError(f"{self.path} existiert nicht")

    def __eq__(self, other):
        return self.mtknr == other.mtknr

    def __load(self):
        try:
            df = pd.read_excel(self.path, sheet_name=self.sheet_name)
            idx = df[df["Mtknr"] == self.mtknr].index
            if idx.empty:
                raise ValueError(f"Person mit Matrikelnummer {self.mtknr} nicht gefunden")
            return df, idx[0]
        except Exception as e:
            raise RuntimeError(f"Fehler beim Lesen der Excel-Datei: {e}")

    def __save(self, df):
        try:
            with pd.ExcelWriter(self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name=self.sheet_name, index=False)
        except PermissionError:
            raise PermissionError("Datei ist gesperrt. Bitte Excel schließen.")
        except Exception as e:
            raise RuntimeError(f"Fehler beim Speichern: {e}")

    def get(self, feld: str):
        df, idx = self.__load()
        return df.at[idx, feld] if feld in df.columns else None

    def set(self, feld: str, wert = "x"):
        df, idx = self.__load()
        if feld not in df.columns:
            raise KeyError(f"Feld '{feld}' existiert nicht in der Datei.")
        df.at[idx, feld] = wert
        self.__save(df)

    def setze_kreuz(self, feld: str):
        self.set(feld, "x")

    def setze_stimmen(self, anzahl: int):
        self.set("stimmen", anzahl)

    def get_daten(self):
        df, idx = self.__load()
        return df.loc[idx].to_dict()

    def has(self, feld:str):
        return self.get(feld) == "x"
