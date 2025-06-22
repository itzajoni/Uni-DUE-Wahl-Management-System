from datetime import timedelta, datetime

from docx.shared import Mm
from docxtpl import InlineImage

from intern.helpers.json_helper import json_read
from intern.helpers.template_docx import load_template, save_result

file = load_template("Wahlbekanntmachung")
wahl_data = json_read("rahmenbedingungen")
wahltag_start = datetime.strptime(wahl_data.get("wahltag_start"), "%Y-%m-%d")
data = {
        # DATEN relativ zu wahltag_start
        "wahltag_start": (wahltag_start).strftime("%d.%m.%Y"),
        "end_date": (wahltag_start + timedelta(days=2)).strftime("%d.%m.%Y"),
        "begin_einsicht": (wahltag_start - timedelta(days=10)).strftime("%d.%m.%Y"),
        "end_einsicht": (wahltag_start - timedelta(days=5)).strftime("%d.%m.%Y"),
        "end_kandidatur": (wahltag_start - timedelta(days=7)).strftime("%d.%m.%Y"),
        "end_briefwahl": (wahltag_start - timedelta(days=1)).strftime("%d.%m.%Y"),
        "bekanntgabe": (wahltag_start - timedelta(days=3)).strftime("%d.%m.%Y"),
        "end_einspruch": (wahltag_start + timedelta(days=5)).strftime("%d.%m.%Y"),
        "wahltag_2": (wahltag_start + timedelta(days=1)).strftime("%d.%m.%Y"),
        "wahltag_3": (wahltag_start + timedelta(days=2)).strftime("%d.%m.%Y"),
        "wahlausschuss_namen": ", ".join(wahl_data.get("wahlausschuss_namen")),

        "template_link": "",      # z. B. "https://fsr.deinserver.de/kandidatur"
        #"qr_code": InlineImage(file, "path/to/generated_qr_code.png", width=Mm(30)),

        # Unterschriften als Tabelle mit einer Zeile, mehreren Spalten
        "unterschriften": [
            {"linie": "______________________", "name": name}
            for name in ["Max Mustermann", "Lisa Beispiel", "Ali Ahmed"]  # ← per setup laden
        ]
    }

save_result("Wahlbekanntmachung", file, data)

print("test")