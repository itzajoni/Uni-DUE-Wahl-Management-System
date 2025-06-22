from pathlib import Path

from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert  # nur unter Windows/Mac
from intern.helpers.json_helper import json_read
import os
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent


def load_template(name: str):
    path = SCRIPT_DIR / ("../templates/" + name + ".docx")
    if not os.path.exists(path):
        print(f"Template {name} not found")
        exit(1)

    file = DocxTemplate(path)
    return file


def save_result(name: str, file: DocxTemplate, placeholder=None):
    if placeholder is None:
        placeholder = {}
    template_data = {
        "current_date": datetime.today().strftime('%d.%m.%Y'),
    }
    # fsr_logo einbinden, falls da
    for datei in Path("../FSR Logo").iterdir():
        if datei.suffix.lower() in {".png", ".jpg", ".jpeg"} and datei.is_file():
            template_data["fachschaft_logo"] = InlineImage(file, str(datei), width=Mm(40))

    template_data.update(json_read("rahmenbedingungen"))
    template_data.update(placeholder)
    file.render(template_data)

    fsr_data = json_read("rahmenbedingungen")
    path = f"../Wahldokumente/{name} FSR {fsr_data.get("fachschaft_nummer")} {fsr_data.get("fachschaft_name")}"
    file.save(path + ".docx")
    print(f"✅ \"{name}\" als Docx (Word) gespeichert.")

    if os.name == "nt" or os.name == "mac":
        print("Konvertiere zu PDF...")
        convert(path + ".docx", path + ".pdf")
        print(f"✅ \"{name}\" als PDF gespeichert.")
    else:
        print("⚠️ PDF-Konvertierung nicht möglich: nutze LibreOffice (Linux)")

        # Optional: LibreOffice verwenden
        # os.system(f'libreoffice --headless --convert-to pdf "{output_docx}" --outdir .')
