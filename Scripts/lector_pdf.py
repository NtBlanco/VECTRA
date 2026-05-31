import os

from functools import lru_cache
from PyPDF2 import PdfReader

CARPETA_PDFS = "CREG/PDF"


# =====================================
# LECTURA GENERAL DE PDFs
# =====================================

@lru_cache(maxsize=1)
def leer_pdfs():

    documentos = []

    print("🚀 Iniciando lectura de PDFs...")

    for archivo in os.listdir(CARPETA_PDFS):

        if not archivo.endswith(".pdf"):
            continue

        ruta = os.path.join(
            CARPETA_PDFS,
            archivo
        )

        try:

            print(f"📖 Leyendo PDF: {archivo}")

            reader = PdfReader(ruta)

            texto = ""

            for pagina in reader.pages:

                contenido = pagina.extract_text()

                if contenido:

                    texto += contenido

            print(
                f"📄 {archivo} -> {len(texto)} caracteres"
            )

            chunks = [{

                "texto": texto,

                "pagina": "PDF completo"
            }]

            actores = []

            actores_base = [
                "ASIC",
                "LAC",
                "OR",
                "AGPE",
                "GD",
                "Comercializador"
            ]

            for actor in actores_base:

                if actor.lower() in texto.lower():

                    actores.append(actor)

            documentos.append({

                "archivo": archivo,

                "texto": texto,

                "chunks": chunks,

                "categoria": "CREG",

                "actores": actores,

                "pagina": len(reader.pages)
            })

            print(
                f"✅ PDF leído correctamente: {archivo}"
            )

        except Exception as e:

            print(
                f"❌ Error leyendo {archivo}: {e}"
            )

    print("🏁 Lectura finalizada")

    return documentos


# =====================================
# LECTURA DE PDF ESPECÍFICO
# =====================================

def leer_pdf_especifico(nombre_pdf):

    documentos = []

    ruta = os.path.join(
        CARPETA_PDFS,
        nombre_pdf
    )

    if not os.path.exists(ruta):

        print(
            f"❌ No existe el PDF: {nombre_pdf}"
        )

        return documentos

    try:

        print(
            f"📖 Leyendo PDF específico: {nombre_pdf}"
        )

        reader = PdfReader(ruta)

        texto = ""

        for pagina in reader.pages:

            contenido = pagina.extract_text()

            if contenido:

                texto += contenido

        print("=" * 50)
        print(f"PDF: {nombre_pdf}")
        print(
            f"CARACTERES EXTRAIDOS: {len(texto)}"
        )
        print("=" * 50)

        chunks = [{

            "texto": texto,

            "pagina": "PDF completo"
        }]

        actores = []

        actores_base = [
            "ASIC",
            "LAC",
            "OR",
            "AGPE",
            "GD",
            "Comercializador"
        ]

        for actor in actores_base:

            if actor.lower() in texto.lower():

                actores.append(actor)

        documentos.append({

            "archivo": nombre_pdf,

            "texto": texto,

            "chunks": chunks,

            "categoria": "CREG",

            "actores": actores,

            "pagina": len(reader.pages)
        })

        print(
            f"✅ PDF procesado: {nombre_pdf}"
        )

    except Exception as e:

        print(
            f"❌ Error leyendo PDF: {e}"
        )

    return documentos