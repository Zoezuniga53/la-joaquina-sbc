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
    clase_tarjeta = f"tarjeta-resumen tarjeta-{estado}" if estado else "tarjeta-resumen"
    clase_valor = f"tarjeta-valor {estado}".strip()
    return (
        f'<div class="{clase_tarjeta}"><div class="tarjeta-titulo">{titulo}</div>'
        f'<div class="{clase_valor}">{valor}</div>'
        f'<div class="tarjeta-detalle">{detalle}</div></div>'
    )


def render_hero():
    render_html(f"""
<div class="hero-banner" style="background-image: linear-gradient(135deg, rgba(6, 10, 20, 0.85) 0%, rgba(13, 22, 42, 0.82) 70%, rgba(127, 29, 29, 0.45) 100%), url('{IMG_HERO}');">
<p class="hero-eyebrow">Bienvenido a La Joaquina</p>
<h1 class="hero-titulo">La Joaquina | Eventos gastronómicos</h1>
<p class="hero-subtitulo">Sistema de Gestión y Orquestación Logística</p>
</div>
""")
