"""Componentes HTML reutilizables de la interfaz."""

import html as html_lib
import streamlit as st
from frontend.recursos import IMG_HERO


def esc(texto):
    return html_lib.escape(str(texto))


def render_html(fragmento):
    """Compacta el HTML en una sola línea para que Markdown no lo trate como código."""
    st.markdown(" ".join(l.strip() for l in fragmento.splitlines() if l.strip()), unsafe_allow_html=True)


def tabla_html(columnas, filas):
    cab = "".join(f"<th>{c}</th>" for c in columnas)
    cuerpo = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in fila) + "</tr>" for fila in filas)
    render_html(f'<div class="tabla-contenedor"><table class="tabla-lj"><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></div>')


def tarjeta(titulo, valor, detalle="", estado=""):
    return (
        f'<div class="tarjeta-resumen"><div class="tarjeta-titulo">{titulo}</div>'
        f'<div class="tarjeta-valor {estado}">{valor}</div>'
        f'<div class="tarjeta-detalle">{detalle}</div></div>'
    )



def render_hero():
    render_html(f"""
<div style="background: linear-gradient(rgba(8, 8, 8, 0.65), rgba(8, 8, 8, 0.90)), url('{IMG_HERO}'); background-size: cover; background-position: center; padding: 72px 30px; text-align: center; border-bottom: 1px solid #c5a059; margin-bottom: 26px; border-radius: 4px;">
<p style="color: #c5a059; font-family: 'Montserrat', sans-serif; font-size: 0.85rem; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 10px;">Bienvenido a La Joaquina</p>
<h1 style="color: #ffffff; font-family: 'Cormorant Garamond', serif; font-size: 3.4rem; font-weight: 600; margin: 0;">La Joaquina | Eventos gastronómicos</h1>
<p style="color: #d4d4d4; font-family: 'Montserrat', sans-serif; font-size: 0.95rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 12px;">Sistema de Gestión y Orquestación Logística</p>
</div>
""")
