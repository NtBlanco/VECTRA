import streamlit as st
import re

from PIL import Image

from catalogo_normas import CATALOGO_NORMAS

from utils_normativa import (
    construir_url_creg,
    obtener_pdf_desde_html,
    guardar_norma_catalogo
)

from lector_pdf import (
    leer_pdfs,
    leer_pdf_especifico
)

from ia_engine import preguntar_ia

st.markdown("""
<style>

/* Fondo */
.stApp{
    background-color:#F2F2EE;
}

/* Tipografía */
html, body, [class*="css"]{
    font-family:"Segoe UI", sans-serif;
}

/* Caja de texto */
.stTextInput input{
    border-radius:12px;
    border:1px solid #A7B89A;
    padding:10px;
}

/* Botón */
.stButton button{

    background-color:#CDAA63;

    color:white;

    border:none;

    border-radius:12px;

    font-weight:600;

    font-size:18px;

    width:260px;

    height:55px;

    white-space:nowrap;
}

/* Hover */
.stButton button:hover{

    background-color:#b9964e;

    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# INTERFAZ VECTRA
# =====================================

logo = Image.open(
    "assets/vectra_logo.png"
)

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.image(
        logo,
        width=550
    )

st.markdown(
    "<div style='height:3px;'></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='height:50px;'></div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#1E3E34;
        font-size:26px;
        margin-top:-100px;
        margin-bottom:20px;
    ">
        Inteligencia regulatoria para el sistema energético colombiano
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <hr style="
    border:1px solid #CDAA63;
    width:30%;
    margin:auto;
    margin-top:10px;
    margin-bottom:20px;
    ">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        position:relative;
        left:15px;
    ">
        <h2 style="
            color:#1E3E34;
            font-size:48px;
            font-weight:700;
            margin-top:0px;
            margin-bottom:5px;
        ">
            ¿Qué deseas consultar?
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# VARIABLES BASE
# =====================================

consulta = st.text_input(
    "",
    placeholder="Ej. ¿Qué es un AGPE según la CREG 174 de 2021?"
)

col1, col2, col3 = st.columns([1,1,1])

with col2:

    buscar = st.button(
        "⚡ Analizar regulación"
    )

consulta_lower = consulta.lower()

pdf_objetivo = None

norma_detectada = False

# =====================================
# BÚSQUEDA PRINCIPAL
# =====================================

if buscar:

    encontrados = []

    pdfs_relacionados = []

    # =====================================
    # DETECCIÓN DINÁMICA DE NORMAS
    # =====================================

    for clave, norma in CATALOGO_NORMAS.items():

        numero, anio = clave.split("-")

        if (
            numero in consulta_lower
            and
            anio in consulta_lower
        ):

            pdf_objetivo = norma["archivo"]

            norma_detectada = True

            for relacionada in norma.get(
                "relacionadas",
                []
            ):

                if relacionada in CATALOGO_NORMAS:

                    pdf_relacionado = (
                        CATALOGO_NORMAS[relacionada]["archivo"]
                    )

                    pdfs_relacionados.append(
                        pdf_relacionado
                    )

           # descargar_pdf_si_no_existe(

           #     norma["archivo"],

           #     norma["url"]
           # )

    # =====================================
    # DETECCIÓN DINÁMICA CREG
    # =====================================

    #"if not norma_detectada:

    #    match_creg = re.search(

    #        r'creg\s*(\d+).*?(\d{4})',

    #        consulta_lower
    #    )

    #    if match_creg:
    #        numero = match_creg.group(1)
    #        anio = match_creg.group(2)
    #        numero_pdf = numero.zfill(4)
    #        nombre_pdf = (
    #            f"Creg{numero_pdf}-{anio}.pdf"
    #        )
            
    #        url_pdf = obtener_pdf_desde_html(
    #            numero,
    #            anio
    #        )
            
    #    if not url_pdf:
    #        url_pdf = construir_url_creg(
    #            numero,
    #            anio
    #        )
            
    #    pdf_objetivo = nombre_pdf
    #    descarga_ok = descargar_pdf_si_no_existe(
    #        nombre_pdf,
    #        url_pdf
    #    )
        
    #    if descarga_ok:
    #        guardar_norma_catalogo(
    #            clave=f"{numero_pdf}-{anio}",
    #            nombre=(
    #                f"Resolución CREG {numero} de {anio}"
    #            ),

    #            archivo=nombre_pdf,

    #            url=url_pdf
    #        )

        #    st.success(
        #        f"📥 Norma oficial encontrada dinámicamente: CREG {numero} de {anio}"
        #    )

        #else:
        #    st.error(
        #        "❌ No fue posible descargar la norma oficial."
        #        )


    # =====================================
    # LECTURA DOCUMENTAL
    # =====================================

# =====================================
# LECTURA DOCUMENTAL
# =====================================

    if pdf_objetivo:

        resultados = leer_pdf_especifico(
            pdf_objetivo
        )

        for pdf_relacionado in pdfs_relacionados:

            resultados.extend(

                leer_pdf_especifico(
                    pdf_relacionado
                )
            )

    else:

        resultados = []

        st.warning(
            "⚠️ No se encontró la norma solicitada en el catálogo."
        )

    # =====================================
    # DETECCIÓN DE ARTÍCULO
    # =====================================

    match = re.search(

        r'art[íi]?culo\s*(\d+)',

        consulta_lower
    )

    # =====================================
    # BÚSQUEDA POR ARTÍCULO
    # =====================================

    if match:

        numero_articulo = match.group(1)

        for doc in resultados:

            for chunk in doc["chunks"]:

                # =====================================
                # COMPATIBILIDAD CHUNKS
                # =====================================

                if isinstance(chunk, dict):

                    texto_chunk = chunk["texto"]

                    pagina_chunk = chunk["pagina"]

                else:

                    texto_chunk = chunk

                    pagina_chunk = "No identificada"

                chunk_lower = texto_chunk.lower()

                score = 0

                # =====================================
                # COINCIDENCIA DE ARTÍCULO
                # =====================================

                patron_articulo = re.search(
                    
                    rf'art[ií]?culo\s*{numero_articulo}',
                    
                    chunk_lower,
                    
                    re.IGNORECASE
                )
                if patron_articulo:
                    
                    score += 100

                # =====================================
                # PRIORIDAD NORMATIVA
                # =====================================

                if "174" in consulta_lower:

                    score += 5

                if "174" in doc["archivo"]:

                    score += 20

                if "2021" in doc["archivo"]:

                    score += 10

                # =====================================
                # GUARDAR RESULTADO
                # =====================================

                if score > 0:

                    encontrados.append({

                        "archivo": doc["archivo"],

                        "texto": texto_chunk,

                        "categoria": doc["categoria"],

                        "score": score,

                        "pagina": pagina_chunk
                    })

    # =====================================
    # BÚSQUEDA GENERAL POR CONTEXTO
    # =====================================

    else:

        palabras = consulta_lower.split()

        for doc in resultados:

            for chunk in doc["chunks"]:

                # =====================================
                # COMPATIBILIDAD CHUNKS
                # =====================================

                if isinstance(chunk, dict):

                    texto_chunk = chunk["texto"]

                    pagina_chunk = chunk["pagina"]

                else:

                    texto_chunk = chunk

                    pagina_chunk = "No identificada"

                chunk_lower = texto_chunk.lower()

                score = 0

                # =====================================
                # COINCIDENCIAS POR PALABRAS
                # =====================================

                for palabra in palabras:

                    if palabra in chunk_lower:

                        score += 5

                # =====================================
                # ACTORES REGULATORIOS
                # =====================================

                for actor in doc["actores"]:

                    if actor.lower() in consulta_lower:

                        score += 15

                # =====================================
                # PRIORIDAD NORMATIVA
                # =====================================

                if "174" in doc["archivo"]:

                    score += 20

                if "2021" in doc["archivo"]:

                    score += 10

                # =====================================
                # GUARDAR RESULTADOS
                # =====================================

                if score > 0:

                    encontrados.append({

                        "archivo": doc["archivo"],

                        "texto": texto_chunk,

                        "categoria": doc["categoria"],

                        "score": score,

                        "pagina": pagina_chunk
                    })

    # =====================================
    # ORDENAR RESULTADOS
    # =====================================

    encontrados = sorted(

        encontrados,

        key=lambda x: x.get("score", 0),

        reverse=True
    )

    # =====================================
    # VALIDAR RESULTADOS
    # =====================================

    if len(encontrados) > 0:

        doc = encontrados[0]

        texto = doc["texto"]

        cantidad = len(encontrados)
        

        fragmento = texto

        st.markdown("---")

        st.markdown(
            "## 🤖 Análisis Inteligente de VECTRA"
        )

        with st.spinner(
            "🧠 VECTRA está analizando la regulación energética..."
        ):

            tipo_consulta = "general"

            if (
                "artículo" in consulta_lower
                or
                "articulo" in consulta_lower
            ):

                tipo_consulta = "articulo"

            elif (
                "obligación" in consulta_lower
                or
                "obligaciones" in consulta_lower
            ):

                tipo_consulta = "obligaciones"

            elif (
                "qué es" in consulta_lower
                or
                "definición" in consulta_lower
            ):

                tipo_consulta = "definicion"

            elif (
                "cómo" in consulta_lower
                or
                "procedimiento" in consulta_lower
            ):

                tipo_consulta = "procedimiento"

            elif "qué regula" in consulta_lower:

                tipo_consulta = "objeto"

            respuesta = preguntar_ia(

                consulta,

                fragmento,

                tipo_consulta
            )

        st.markdown(respuesta)

    else:

        st.warning(
            "⚠️ No se encontraron coincidencias regulatorias relevantes."
        )

  