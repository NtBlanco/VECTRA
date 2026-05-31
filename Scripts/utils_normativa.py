import requests
from bs4 import BeautifulSoup


# =====================================
# CONSTRUIR URL DIRECTA CREG
# =====================================

def construir_url_creg(numero, anio):

    numero = numero.zfill(4)

    return (

        "https://gestornormativo.creg.gov.co/"
        "gestor/entorno/docs/"
        f"resolucion_creg_{numero}_{anio}.pdf"
    )


# =====================================
# OBTENER PDF DESDE HTML OFICIAL
# =====================================

def obtener_pdf_desde_html(

    numero,

    anio
):

    numero = numero.zfill(4)

    url_html = (

        "https://gestornormativo.creg.gov.co/"
        "gestor/entorno/docs/"
        f"resolucion_creg_{numero}_{anio}.htm"
    )

    try:

        response = requests.get(
            url_html,
            timeout=20
        )

        if response.status_code != 200:

            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if href and ".pdf" in href.lower():

                if href.startswith("http"):

                    return href

                return (
                    "https://gestornormativo.creg.gov.co"
                    + href
                )

        return None

    except Exception as e:

        print(
            f"❌ Error obteniendo PDF: {e}"
        )

        return None


# =====================================
# GUARDAR NORMA EN CATÁLOGO
# =====================================

def guardar_norma_catalogo(

    clave,

    nombre,

    archivo,

    url
):

    with open(
        "Scripts/catalogo_normas.py",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(

            f'\nCATALOGO_NORMAS["{clave}"] = {{\n'
            f'    "nombre": "{nombre}",\n'
            f'    "archivo": "{archivo}",\n'
            f'    "url": "{url}",\n'
            f'    "relacionadas": []\n'
            f'}}\n'
        )