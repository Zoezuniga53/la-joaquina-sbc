"""Hoja de estilos (azul noche profundo, rojo carmesí y sombras con relieve) y su inyección en la página."""

import streamlit as st


ESTILOS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');

html, body, p, label, input, button, textarea, li, td, th {
    font-family: 'Montserrat', sans-serif;
}

/* Protección de los íconos nativos de Streamlit (evita el texto _arrow_right) */
[data-testid="stIconMaterial"], .material-icons, span[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
}

/* Fondo principal y atmósfera azul noche profundo con destellos carmesí */
.stApp {
    background: radial-gradient(circle at 85% 15%, rgba(220, 38, 38, 0.16) 0%, rgba(10, 17, 32, 0.95) 45%, #060a14 100%) !important;
    color: #e2e8f0;
}
[data-testid="stHeader"] {
    background-color: rgba(6, 10, 20, 0.85);
    backdrop-filter: blur(8px);
}
[data-testid="stMainBlockContainer"], .block-container {
    padding-top: 3.2rem !important;
    padding-bottom: 3rem !important;
}

/* Barra lateral azul medianoche con borde carmesí y sombra profunda */
section[data-testid="stSidebar"] {
    background-color: #090f1d !important;
    border-right: 1px solid rgba(220, 38, 38, 0.25);
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.65);
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #cbd5e1 !important;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
}

h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f8fafc !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
}

/* Hero Banner superior */
.hero-banner {
    background-size: cover;
    background-position: center;
    padding: 68px 32px 58px 32px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-bottom: 2px solid #dc2626;
    margin: 8px 0 28px 0;
    border-radius: 6px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75);
    overflow: visible;
}
.hero-eyebrow {
    color: #f87171;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin: 0 0 12px 0;
}
.hero-titulo {
    color: #ffffff !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3.35rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    padding: 4px 0 !important;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.7);
}
.hero-subtitulo {
    color: #cbd5e1;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin: 14px 0 0 0;
}

/* Controles de formulario */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"],
input,
textarea {
    background-color: #0d1526 !important;
    color: #f8fafc !important;
    border-color: rgba(255, 255, 255, 0.14) !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: #dc2626 !important;
    box-shadow: 0 0 0 1px rgba(220, 38, 38, 0.45) !important;
}
ul[role="listbox"], div[data-baseweb="popover"] li {
    background-color: #0d1526 !important;
    color: #f8fafc !important;
}
ul[role="listbox"] li:hover, div[data-baseweb="popover"] li:hover {
    background-color: rgba(220, 38, 38, 0.18) !important;
}

/* Botones con acento rojo carmesí y brillo en hover */
.stButton > button {
    background-color: #0d1526 !important;
    color: #f8fafc !important;
    border: 1px solid #dc2626 !important;
    border-radius: 4px !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: normal !important;
    min-height: 2.6rem;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
    transition: all 0.22s ease-in-out;
}
.stButton > button:hover {
    background-color: #ef4444 !important;
    border-color: #ef4444 !important;
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(220, 38, 38, 0.4) !important;
    transform: translateY(-1px);
}
.stButton > button p {
    font-weight: 600;
}

/* Desplegables de la barra lateral */
[data-testid="stExpander"] details {
    background-color: #0d1526;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 6px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}
[data-testid="stExpander"] summary p {
    font-weight: 500;
    color: #f1f5f9;
    letter-spacing: 0.03em;
}
[data-testid="stExpander"] summary:hover p {
    color: #f87171;
}

/* Pestañas */
button[data-baseweb="tab"] p {
    font-size: 0.84rem !important;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    transition: color 0.2s ease;
}
button[data-baseweb="tab"]:hover p {
    color: #f8fafc !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #ef4444 !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #dc2626 !important;
    box-shadow: 0 0 12px rgba(220, 38, 38, 0.55);
}

/* Marca en la barra lateral */
.marca-sidebar {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #f8fafc;
    border-bottom: 2px solid #dc2626;
    padding-bottom: 6px;
    margin-bottom: 6px;
}
.marca-sidebar-sub {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #f87171;
    margin-bottom: 18px;
}
.rotulo-seccion {
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #f87171;
    margin: 18px 0 8px 0;
}

/* Barra de metadatos / badges */
.barra-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 8px 0 22px 0;
}
.badge-meta {
    background-color: #0d1526;
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: 999px;
    letter-spacing: 0.03em;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
}
.badge-oro {
    background-color: rgba(220, 38, 38, 0.14);
    border-color: rgba(220, 38, 38, 0.55);
    color: #f87171;
    font-weight: 600;
}

/* Tarjetas de resumen ejecutivo con relieve y profundidad */
.tarjeta-resumen {
    background-color: #0d1526;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 3px solid #dc2626;
    border-radius: 6px;
    padding: 20px 20px 18px 20px;
    min-height: 152px;
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.tarjeta-resumen:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.78), inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
.tarjeta-resumen.tarjeta-ok {
    border-left: 4px solid #22c55e;
}
.tarjeta-resumen.tarjeta-alerta {
    border-left: 4px solid #ef4444;
    background: linear-gradient(180deg, rgba(127, 29, 29, 0.22), rgba(127, 29, 29, 0.22)), #0d1526;
}
.tarjeta-resumen.tarjeta-aviso {
    border-left: 4px solid #f59e0b;
    background: linear-gradient(180deg, rgba(180, 83, 9, 0.16), rgba(180, 83, 9, 0.16)), #0d1526;
}
.tarjeta-titulo {
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #f8fafc;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 8px;
    margin-bottom: 12px;
    line-height: 1.35;
    white-space: normal;
}
.tarjeta-valor {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.62rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.25;
    white-space: normal;
}
.tarjeta-valor.ok {
    color: #22c55e;
    font-weight: 700;
    text-shadow: 0 0 14px rgba(34, 197, 94, 0.35);
}
.tarjeta-valor.alerta {
    color: #ff4d4d;
    font-weight: 700;
    text-shadow: 0 0 14px rgba(239, 68, 68, 0.45);
}
.tarjeta-valor.aviso {
    color: #fbbf24;
    font-weight: 700;
    text-shadow: 0 0 12px rgba(251, 191, 36, 0.3);
}
.tarjeta-detalle {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 8px;
    line-height: 1.45;
}

/* Paneles de dictamen y operación */
.panel {
    background-color: #0d1526;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 24px 28px;
    margin: 16px 0;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
.panel p, .panel li {
    color: #cbd5e1;
    line-height: 1.65;
}
.panel strong {
    color: #f8fafc;
}
.panel-confirmable {
    border: 1px solid rgba(34, 197, 94, 0.28);
    border-left: 4px solid #22c55e;
}
.panel-bloqueado {
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-left: 4px solid #ef4444;
    background: linear-gradient(180deg, rgba(127, 29, 29, 0.22), rgba(127, 29, 29, 0.22)), #0d1526;
}
.panel-incompleto {
    border: 1px solid rgba(220, 38, 38, 0.3);
    border-left: 4px solid #dc2626;
}
.panel-neutro {
    border-left: 3px solid #dc2626;
}
.etiqueta {
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #f87171;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 8px;
    margin-bottom: 12px;
}
.titular-dictamen {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 10px 0;
}
.panel-confirmable .titular-dictamen {
    color: #22c55e;
    font-weight: 700;
    text-shadow: 0 0 14px rgba(34, 197, 94, 0.35);
}
.panel-bloqueado .titular-dictamen {
    color: #ff4d4d;
    font-weight: 700;
    text-shadow: 0 0 14px rgba(239, 68, 68, 0.45);
}
.panel-incompleto .titular-dictamen {
    color: #f87171;
    font-weight: 700;
    text-shadow: 0 0 12px rgba(248, 113, 113, 0.35);
}
.destacado {
    color: #f87171;
    font-weight: 600;
}

/* Tarjetas fotográficas */
.foto-card {
    background-color: #0d1526;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    overflow: hidden;
    height: 100%;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
}
.foto-card:hover {
    transform: translateY(-3px);
    border-color: #dc2626;
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.78), 0 0 15px rgba(220, 38, 38, 0.28);
}
.foto-card .foto {
    height: 185px;
    background-color: #090f1d;
    background-size: cover;
    background-position: center;
    border-bottom: 2px solid #dc2626;
}
.foto-card .cuerpo {
    padding: 18px 20px;
}
.foto-card .cuerpo h4 {
    margin: 0 0 10px 0;
    font-size: 1.4rem;
    color: #f8fafc !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 6px;
}
.foto-card .cuerpo p {
    margin: 4px 0;
    font-size: 0.86rem;
    color: #cbd5e1;
}

/* Tablas operativas */
.tabla-contenedor {
    overflow-x: auto;
    margin: 12px 0 26px 0;
    border-radius: 6px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6);
}
table.tabla-lj {
    width: 100%;
    border-collapse: collapse;
    background-color: #0d1526;
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.82rem;
}
table.tabla-lj th {
    background-color: #090f1d;
    color: #f87171;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.74rem;
    font-weight: 700;
    text-align: left;
    padding: 13px 12px;
    border-bottom: 2px solid #dc2626;
}
table.tabla-lj td {
    color: #e2e8f0;
    padding: 11px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    vertical-align: top;
}
table.tabla-lj tr:hover td {
    background-color: #131e36;
}
.txt-ok {
    color: #22c55e;
    font-weight: 600;
    text-shadow: 0 0 10px rgba(34, 197, 94, 0.25);
}
.txt-alerta {
    color: #ff4d4d;
    font-weight: 600;
    text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}
.txt-aviso {
    color: #fbbf24;
    font-weight: 600;
}
hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

.etiqueta-salon {
    display: inline-block;
    background-color: #0d1526;
    border: 1px solid rgba(220, 38, 38, 0.55);
    border-left: 4px solid #dc2626;
    color: #f87171;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 8px 14px;
    margin: 4px 0 2px 0;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
</style>
"""


def inyectar_estilos():
    st.markdown(ESTILOS, unsafe_allow_html=True)
