from intern.helpers.datenManagement import WahlManager
from intern.helpers import person

data = WahlManager()

print("""
     --- Kandidaturen eingeben ---

Hier können Kandidaturen eingetragen werden. 
Zum Beenden einfach Enter drücken, ohne etwas einzugeben.
""")

while True:
    eingabe = input("Matrikelnummer des Kandidaten: ").strip()
    if not eingabe:
        print("Beendet.")
        break

    try:
        mtknr = int(eingabe)
        kandidat = data.get_person(mtknr)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        continue

    if kandidat.get("kandidatur") == "x":
        print("⚠️  Diese Person kandidiert bereits.")
        continue

    print(f"🔹 Name: {kandidat.get('Vorname')} {kandidat.get('Nachname')}")
    print(f"🔹 Mat.Nr.: {kandidat.mtknr}")
    print(f"🔹 Studiengang: {kandidat.get('Fach1_1')}")

    # Unterstützer 1
    try:
        unter1_nr = int(input("Matrikelnummer des 1. Unterstützers: ").strip())
        unter1 = data.get_person(unter1_nr)
        if unter1 == kandidat:
            print("Man kann sich nicht selbst unterstützen...")
            continue
        if unter1.has("unterstützer"):
            bereits = data.get_person(int(unter1.get("unterstützer")))
            print(f"⚠️  Unterstützt bereits: {bereits.get('Vorname')} {bereits.get('Nachname')}")
            continue
        print("Erster Unterstützer:", unter1.get("Vorname"), unter1.get("Nachname"))
    except Exception as e:
        print(f"❌ Fehler mit Unterstützer 1: {e}")
        raise e
        continue

    # Unterstützer 2
    try:
        unter2_nr = int(input("Matrikelnummer des 2. Unterstützers: ").strip())
        unter2 = data.get_person(unter2_nr)
        if unter2 == kandidat:
            print("Man kann sich nicht selbst unterstützen...")
            continue
        if unter2 == unter1:
            print("Es müssen zwei verschiedene Unterstützer sein...")
            continue
        if unter2.has("unterstützer"):
            bereits = data.get_person(int(unter2.get("unterstützer")))
            print(f"⚠️  Unterstützt bereits: {bereits.get('Vorname')} {bereits.get('Nachname')}")
            continue
        print("Zweiter Unterstützer:", unter2.get("Vorname"), unter2.get("Nachname"))

    except Exception as e:
        print(f"❌ Fehler mit Unterstützer 2: {e}")
        continue

    try:
        kandidat.setze_kreuz("kandidatur")
        unter1.set("unterstützer", kandidat.mtknr)
        unter2.set("unterstützer", kandidat.mtknr)
        print("✅ Kandidatur erfolgreich eingetragen und gespeichert.")
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
