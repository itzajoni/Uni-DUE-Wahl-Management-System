from helpers.json_helper import json_write
from datetime import datetime

def input_date(prompt):
    while True:
        val = input(f"{prompt} (TT.MM.JJJJ): ").strip()
        try:
            return datetime.strptime(val, "%d.%m.%Y").date()
        except ValueError:
            print("Ungültiges Datum. Bitte TT.MM.JJJJ eingeben.")

def input_time(prompt):
    while True:
        val = input(f"{prompt} (HH:MM): ").strip()
        try:
            return datetime.strptime(val, "%H:%M").time()
        except ValueError:
            print("Ungültige Uhrzeit. Bitte HH:MM eingeben.")

def setup_wahl():
    print("=== Wahlkonfiguration ===")
    daten = {
        "fachschaft_name": input("Name der Fachschaft: Fachschaft ").strip(),
        "fachschaft_nummer": input("Nummer der Fachschaft (z.B. 1a): ").strip(),
        "fachschaft_raum": input("Fachschafs-Büro: "),
        "fachschaft_tel_nr": input("Fachschafts-Telefon: "),
        "wahltag_start": str(input_date("Datum des ersten Wahltages")),
        "fsr_plaetze": int(input("Anzahl der Plätze im FSR: ").strip()),
        "raum": input("Raum der Wahl: ").strip(),
        "wahl_start": input_time("Startuhrzeit der Wahl").strftime("%H:%M"),
        "wahl_ende": input_time("Enduhrzeit der Wahl").strftime("%H:%M"),
        "wahlausschuss_mail": input("E-Mail des Wahlausschusses [fsk@asta-due.org]: ").strip() or "fsk@asta-due.org",
        "wahlausschuss_namen": [name.strip() for name in input("Namen der Wahlausschussmitglieder (kommagetrennt): ").split(",")],
        "briefkasten": input("Briefkasten für Kandidaturerklärungen: ").strip(),
        "fvv_uhrzeit": str(input_time("Uhrzeit der Fachschaftenvollversammlung")),
        "fvv_raum": input("Raum der Fachschaftenvollversammlung: ").strip(),
    }

    json_write("rahmenbedingungen", daten)
    print("\n✅ Wahlrahmenbedingungen gespeichert.")

if __name__ == "__main__":
    setup_wahl()
