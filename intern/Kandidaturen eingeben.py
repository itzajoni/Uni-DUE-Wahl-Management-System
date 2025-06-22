from helpers.waehlerverzeichnis import *

print("""
     --- Kandidaturen eingeben ---
     
Hier können Kandidaturen eingetragen werden. Zum Beenden leeren Eintrag eingeben.    
    """)

while True:
    kand = int(input("Matrikelnummer des Kandidaten: ").strip())
    kand = suche_nach_mtk(kand)
    if kand is None:
        print("Matrikelnummer ist nicht im Wählerverzeichnis")
        continue
    if kand.kandidatur == "x":
        print("Kandidiert bereits")
        continue
    print(f"Name: {kand.Vorname} {kand.Nachname},\n Mat.Nr.: {kand.Mtknr} \n Studiengang: {kand.Fach1_1}")
    unter_1 = int(input("Matrikelnummer des 1. Unterstützer: ").strip())
    unter_1 = suche_nach_mtk(unter_1)
    if unter_1 is None:
        print("Matrikelnummer ist nicht im Wählerverzeichnis")
        continue
    if not (unter_1.unterstuetzer is None or unter_1.unterstuetzer == ""):
        other = suche_nach_mtk(unter_1.unterstuetzer)
        print(f"Unterstützt bereits {other.Vorname} {other.Nachname}")
        continue
    print(f"{unter_1.Vorname} {unter_1.Nachname} als Unterstützer eingetragen.")
    unter_2 = int(input("Matrikelnummer des 2. Unterstützer: ").strip())
    unter_2 = suche_nach_mtk(unter_2)
    if unter_2 is None:
        print("Matrikelnummer ist nicht im Wählerverzeichnis")
        continue
    if not (unter_2.unterstuetzer is None or unter_2.unterstuetzer == ""):
        other = suche_nach_mtk(unter_2.unterstuetzer)
        print(f"Unterstützt bereits {other.Vorname} {other.Nachname}")
        continue
    print(f"{unter_2.Vorname} {unter_2.Nachname} als Unterstützer eingetragen.")
    setze_kreuz(kand, "kandidatur")
    setze_wert(unter_1, "unterstuetzer", kand.Mtknr)
    setze_wert(unter_2, "unterstuetzer", kand.Mtknr)

    print("In Excel gespeichert")



