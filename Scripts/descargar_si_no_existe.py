import os
import requests

CARPETA_PDFS = "CREG/PDF"

os.makedirs(
    CARPETA_PDFS,
    exist_ok=True
)

def descargar_pdf_si_no_existe(

    nombre_archivo,

    url
):

    ruta = os.path.join(

        CARPETA_PDFS,

        nombre_archivo
    )

    # =====================================
    # YA EXISTE
    # =====================================

    if os.path.exists(ruta):

        print(
            f"✅ Ya existe: {nombre_archivo}"
        )

        return True

    try:

        print(
            f"⬇️ Descargando: {nombre_archivo}"
        )

        response = requests.get(
            url,
            timeout=20
        )

        # =====================================
        # VALIDAR RESPUESTA
        # =====================================

        if response.status_code != 200:

            print(
                f"❌ No encontrada: {url}"
            )

            return False

        if (
            "application/pdf"
            not in
            response.headers.get(
                "Content-Type",
                ""
            )
        ):

            print(
                "❌ La respuesta no es PDF"
            )

            return False

        # =====================================
        # GUARDAR PDF
        # =====================================

        with open(ruta, "wb") as f:

            f.write(response.content)

        print(
            f"✅ Descarga completada: {nombre_archivo}"
        )

        return True

    except Exception as e:

        print(
            f"❌ Error descargando PDF: {e}"
        )

        return False