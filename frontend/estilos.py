"""Hoja de estilos (negro, carbón y dorado) y su inyección en la página."""

import streamlit as st


ESTILOS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

html, body, p, label, input, button, textarea, li, td, th {
    font-family: 'Montserrat', sans-serif;
}

/* Protección de los íconos nativos de Streamlit (evita el texto _arrow_right) */
[data-testid="stIconMaterial"], .material-icons, span[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
}

.stApp {
    background: radial-gradient(circle at top, #15130f 0%, #0b0b0b 55%);
    color: #e8e4da;
}
[data-testid="stHeader"] {
    background-color: rgba(11, 11, 11, 0.85);
}
section[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #2a2a2a;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #cfcac0 !important;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
}

h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f5f5f0 !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
}

/* Controles de formulario */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="base-input"], input, textarea {
    background-color: #1a1a1a !important;
    color: #f5f5f0 !important;
    border-color: #333333 !important;
}
ul[role="listbox"], div[data-baseweb="popover"] li {
    background-color: #1a1a1a !important;
    color: #f5f5f0 !important;
}

/* Botones */
.stButton > button {
    background-color: #141414 !important;
    color: #f5f5f0 !important;
    border: 1px solid #c5a059 !important;
    border-radius: 3px !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: normal !important;
    min-height: 2.6rem;
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    background-color: #c5a059 !important;
    color: #0b0b0b !important;
}
.stButton > button p {
    font-weight: 500;
}

/* Desplegables de la barra lateral */
[data-testid="stExpander"] details {
    background-color: #141414;
    border: 1px solid #2a2a2a !important;
    border-radius: 4px;
}
[data-testid="stExpander"] summary p {
    font-weight: 500;
    color: #f5f5f0;
    letter-spacing: 0.03em;
}
[data-testid="stExpander"] summary:hover p {
    color: #c5a059;
}

/* Pestañas */
button[data-baseweb="tab"] p {
    font-size: 0.82rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a8a29e;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #c5a059 !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #c5a059 !important;
}

/* Marca en la barra lateral */
.marca-sidebar {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.7rem;
    color: #f5f5f0;
    border-bottom: 1px solid #c5a059;
    padding-bottom: 6px;
    margin-bottom: 4px;
}
.marca-sidebar-sub {
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c5a059;
    margin-bottom: 18px;
}
.rotulo-seccion {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c5a059;
    margin: 16px 0 6px 0;
}

/* Barra de metadatos / badges */
.barra-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 6px 0 18px 0;
}
.badge-meta {
    background-color: #151515;
    border: 1px solid #2e2e2e;
    color: #dcd6c8;
    font-size: 0.76rem;
    padding: 5px 11px;
    border-radius: 999px;
    letter-spacing: 0.03em;
}
.badge-oro {
    border-color: rgba(197, 160, 89, 0.55);
    color: #e5c481;
}

/* Tarjetas de resumen ejecutivo */
.tarjeta-resumen {
    background: linear-gradient(180deg, #171717 0%, #121212 100%);
    border: 1px solid #c5a059;
    border-radius: 4px;
    padding: 18px;
    min-height: 118px;
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
}
.tarjeta-titulo {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #a8a29e;
    margin-bottom: 8px;
    white-space: normal;
}
.tarjeta-valor {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.48rem;
    font-weight: 600;
    color: #f5f5f0;
    line-height: 1.25;
    white-space: normal;
}
.tarjeta-valor.ok { color: #a9d1ae; }
.tarjeta-valor.alerta { color: #e09a9a; }
.tarjeta-valor.aviso { color: #e5c481; }
.tarjeta-detalle {
    font-size: 0.78rem;
    color: #9c968c;
    margin-top: 6px;
}

/* Paneles de dictamen */
.panel {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    padding: 22px 26px;
    margin: 14px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.28);
}
.panel p, .panel li { color: #e0dbd0; line-height: 1.6; }
.panel-confirmable { border: 1px solid #c5a059; border-left: 5px solid #7fae86; }
.panel-bloqueado   { border: 1px solid #5a2e2e; border-left: 5px solid #b85c5c; }
.panel-incompleto  { border: 1px solid #c5a059; border-left: 5px solid #c5a059; }
.panel-neutro      { border-left: 3px solid #c5a059; }
.etiqueta {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c5a059;
    margin-bottom: 6px;
}
.titular-dictamen {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: #f5f5f0;
    margin: 0 0 8px 0;
}
.destacado { color: #c5a059; font-weight: 600; }

/* Tarjetas fotográficas */
.foto-card {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    overflow: hidden;
    height: 100%;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.foto-card:hover {
    transform: translateY(-2px);
    border-color: #c5a059;
}
.foto-card .foto {
    height: 185px;
    background-color: #1d1d1d;
    background-size: cover;
    background-position: center;
    border-bottom: 1px solid #c5a059;
}
.foto-card .cuerpo { padding: 18px 20px; }
.foto-card .cuerpo h4 { margin: 0 0 8px 0; font-size: 1.35rem; }
.foto-card .cuerpo p { margin: 3px 0; font-size: 0.86rem; color: #cfcac0; }

/* Tablas operativas */
.tabla-contenedor { overflow-x: auto; margin: 10px 0 24px 0; }
table.tabla-lj {
    width: 100%;
    border-collapse: collapse;
    background-color: #141414;
    border: 1px solid #2a2a2a;
    font-size: 0.82rem;
}
table.tabla-lj th {
    background-color: #1a1a1a;
    color: #c5a059;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.7rem;
    font-weight: 600;
    text-align: left;
    padding: 12px 12px;
    border-bottom: 1px solid #c5a059;
}
table.tabla-lj td {
    color: #e0dbd0;
    padding: 10px 12px;
    border-bottom: 1px solid #232323;
    vertical-align: top;
}
table.tabla-lj tr:hover td { background-color: #191919; }
.txt-ok { color: #a9d1ae; font-weight: 500; }
.txt-alerta { color: #e09a9a; font-weight: 500; }
.txt-aviso { color: #d9bf85; font-weight: 500; }
hr { border-color: #2a2a2a !important; }

.etiqueta-salon {
    display: inline-block;
    background-color: #141414;
    border: 1px solid #C5A059;
    border-left: 4px solid #C5A059;
    color: #C5A059;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 8px 14px;
    margin: 4px 0 2px 0;
    border-radius: 3px;
}
</style>
"""


def inyectar_estilos():
    st.markdown(ESTILOS, unsafe_allow_html=True)
