from docx import Document
import pandas as pd

from intern.helpers.waehlerverzeichnis import kandidaten

kandidaten_list = kandidaten()
if kandidaten_list.empty:
    print("⚠️ Keine Kandidaturen gefunden.")
    exit(1)

# Template öffnen
doc = Document("templates/Kandidaturen.docx")

# Erste Tabelle im Dokument annehmen
table = doc.tables[0]

for _, row in kandidaten_list.iterrows():
    cells = table.add_row().cells
    cells[0].text = f"{row.get('Nachname', '')}, {row.get('Vorname', '')}"
    cells[1].text = str(row.get("Mtknr", ""))
    cells[2].text = str(row.get("Wahlfb", ""))  # Studiengang

doc.save("../Wahldokumente/Bekanntgabe der Kandidaturen.docx")
print(f"✅ Kandidatenliste gespeichert in Wahldokumente")
