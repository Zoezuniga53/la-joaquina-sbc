"""Estado de sesión de Streamlit y callbacks de la interfaz."""

import streamlit as st
from backend.catalogos import SALON_PROPIO, SALONES_EXTERNOS, TIPO_EXTERNO, TIPO_PROPIO, tipo_de_salon
from backend.grafo import construir_grafo_inicial, crear_evento, reasignar_salon


def init_key(clave, valor):
    if clave not in st.session_state:
        st.session_state[clave] = valor



def iniciar_estado():
    """Crea (una sola vez por sesión) el grafo y las claves de estado; devuelve el grafo."""
    if "g" not in st.session_state:
        st.session_state.g = construir_grafo_inicial()
    init_key("eventos_ids", ["MI-Casamiento_256", "MI-Coffee_Ministerio"])
    init_key("evento_activo", "MI-Casamiento_256")
    init_key("modo_alta", False)
    return st.session_state.g


def cb_restaurar():
    for clave in list(st.session_state.keys()):
        del st.session_state[clave]


def cb_abrir_alta():
    st.session_state.modo_alta = True


def cb_cancelar_alta():
    st.session_state.modo_alta = False


def cb_confirmar_alta():
    nombre = (st.session_state.get("alta_cliente") or "").strip() or "Nuevo Cliente"
    modalidad = st.session_state.get("alta_modalidad", "Cena Formal")
    if st.session_state.get("alta_tipo_salon", TIPO_EXTERNO) == TIPO_PROPIO:
        salon_id = SALON_PROPIO
    else:
        salon_id = st.session_state.get("alta_salon_ext", SALONES_EXTERNOS[0])
    nuevo_id = crear_evento(st.session_state.g, nombre, modalidad, salon_id, st.session_state.eventos_ids)
    st.session_state.eventos_ids.append(nuevo_id)
    st.session_state.evento_activo = nuevo_id
    st.session_state.modo_alta = False


def cb_reasignar_salon(evento_id, salon_id):
    st.session_state[f"{evento_id}__salon"] = salon_id
    st.session_state[f"{evento_id}__tipo_salon"] = tipo_de_salon(salon_id)
    st.session_state[f"{evento_id}__salon_ext"] = salon_id if salon_id in SALONES_EXTERNOS else None
    st.session_state[f"{evento_id}__electrico"] = "Normal"
    reasignar_salon(st.session_state.g, evento_id, salon_id)
