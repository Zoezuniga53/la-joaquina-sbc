# -*- coding: utf-8 -*-
"""
La Joaquina | Eventos gastronómicos
Sistema de Gestión y Orquestación Logística - Unidad 6 (Implementación de SBC)

Punto de entrada. Conecta la interfaz (frontend/) con la lógica (backend/):
  1. frontend.estado        -> estado de sesión y grafo
  2. frontend.sidebar       -> controles
  3. frontend.controles     -> ParametrosEvento
  4. backend.servicios      -> actualiza el grafo, corre el motor, devuelve Analisis
  5. frontend.vista_*       -> dibuja los resultados
"""

import streamlit as st

from backend.servicios import analizar_evento
from frontend.componentes import render_hero
from frontend.controles import leer_parametros
from frontend.estado import iniciar_estado
from frontend.estilos import inyectar_estilos
from frontend.sidebar import render_sidebar
from frontend.vista_evaluacion import render_evaluacion
from frontend.vista_planificacion import render_planificacion

st.set_page_config(
    page_title="SBC La Joaquina - Asesor Gastronómico",
    layout="wide",
    initial_sidebar_state="expanded",
)

inyectar_estilos()
g = iniciar_estado()
E = render_sidebar(g)
ctx = leer_parametros(E, g)
an = analizar_evento(g, E, ctx)
st.session_state.bitacora_inferencia = an.bitacora

render_hero()
tab_eval, tab_plan = st.tabs([
    "Evaluación y Viabilidad del Evento",
    "Planificación de Insumos, Proveedores y Personal",
])
with tab_eval:
    render_evaluacion(g, ctx, an)
with tab_plan:
    render_planificacion(g, ctx, an)
