"""Barra lateral: alta de eventos y controles de entrada."""

import streamlit as st
from rdflib.namespace import RDF
from backend.catalogos import CERVEZAS, ESTADOS_ENTREGA, ESTADOS_POLICIAL, GASEOSAS, MESES, PLATOS, PROVEEDORES, SALONES, SALONES_EXTERNOS, SALON_PROPIO, SIN_SALON, TIPO_EXTERNO, TIPO_PROPIO, max_dias_mes
from backend.fechas import FECHA_MAXIMA, a_fecha, ajustar_a_reservable, primer_dia_reservable
from backend.motor import fv
from backend.ontologia import cat
from frontend.componentes import render_html
from frontend.estado import cb_abrir_alta, cb_cancelar_alta, cb_confirmar_alta, cb_restaurar, init_key


def render_sidebar(g):
    """Dibuja la barra lateral y devuelve el id del evento activo."""
    with st.sidebar:
        render_html('<div class="marca-sidebar">La Joaquina</div><div class="marca-sidebar-sub">Panel del Organizador</div>')

        st.button("CREAR NUEVO EVENTO", width="stretch", on_click=cb_abrir_alta)
        st.button("RESTAURAR VALORES INICIALES", width="stretch", on_click=cb_restaurar)

        if st.session_state.modo_alta:
            render_html('<div class="rotulo-seccion">Alta de nuevo evento</div>')
            st.text_input("Nombre del Cliente", value="Familia López", key="alta_cliente")
            st.selectbox("Modalidad", ["Cena Formal", "Coffee Break"], key="alta_modalidad")
            st.selectbox("Tipo de salón", [TIPO_PROPIO, TIPO_EXTERNO], index=1, key="alta_tipo_salon")
            if st.session_state["alta_tipo_salon"] == TIPO_PROPIO:
                render_html(f'<div class="etiqueta-salon">{SALONES[SALON_PROPIO]}</div>')
            else:
                st.selectbox("Salón externo", SALONES_EXTERNOS, format_func=lambda s: SALONES[s], key="alta_salon_ext")
            st.button("CONFIRMAR ALTA DEL EVENTO", width="stretch", on_click=cb_confirmar_alta)
            st.button("CANCELAR", width="stretch", on_click=cb_cancelar_alta)

        render_html('<div class="rotulo-seccion">Evento activo</div>')

        def etiqueta_evento(eid):
            u = cat[eid]
            modalidad = "Coffee Break" if (u, RDF.type, cat["MC-Coffee_Break"]) in g else "Cena Formal"
            return f"{g.value(u, cat.cliente)} — {modalidad}"

        if st.session_state.evento_activo not in st.session_state.eventos_ids:
            st.session_state.evento_activo = st.session_state.eventos_ids[0]
        E = st.selectbox(
            "Evento Activo",
            st.session_state.eventos_ids,
            format_func=etiqueta_evento,
            key="evento_activo",
            label_visibility="collapsed",
        )
        ev_uri = cat[E]
        k = lambda nombre: f"{E}__{nombre}"

        # ---------- Inicialización de controles a partir del grafo ----------
        fecha_uri = g.value(ev_uri, cat.fecha_evento)
        salon_uri_g = g.value(ev_uri, cat.lugar_asignado)
        mes_g = str(g.value(fecha_uri, cat.mes)) if fecha_uri else "Octubre"
        anio_g = int(g.value(fecha_uri, cat["año"]) or 2026) if fecha_uri else 2026
        max_dia_init = max_dias_mes(mes_g if mes_g in MESES else "Octubre", anio_g)
        dia_g = min(int(g.value(fecha_uri, cat.dia) or 17) if fecha_uri else 17, max_dia_init)

        init_key(k("cliente"), str(g.value(ev_uri, cat.cliente) or ""))
        init_key(k("modalidad"), "Coffee Break" if (ev_uri, RDF.type, cat["MC-Coffee_Break"]) in g else "Cena Formal")
        if k("fecha") not in st.session_state:
            fecha_guardada = a_fecha(dia_g, mes_g if mes_g in MESES else "Octubre", anio_g)
            st.session_state[k("fecha")] = ajustar_a_reservable(fecha_guardada)
        init_key(k("clima"), "Calor" if fecha_uri is not None and str(g.value(fecha_uri, cat.ambiente)) == "Calor" else "Frío")
        salon_ini = fv(salon_uri_g) if salon_uri_g is not None and fv(salon_uri_g) in SALONES else SIN_SALON
        init_key(k("tipo_salon"), TIPO_PROPIO if salon_ini == SALON_PROPIO else TIPO_EXTERNO)
        init_key(k("salon_ext"), salon_ini if salon_ini in SALONES_EXTERNOS else None)
        init_key(k("electrico"), "Normal")
        init_key(k("adultos"), int(g.value(ev_uri, cat.cant_adultos) or 100))
        init_key(k("ninos"), int(g.value(ev_uri, cat["cant_niños"]) or 0))
        init_key(k("presupuesto"), "Abierto" if str(g.value(ev_uri, cat.presupuesto)).lower() == "abierto" else "Cerrado")
        plato_g = str(g.value(ev_uri, cat.plato_principal) or "Asado")
        init_key(k("plato"), plato_g if plato_g in PLATOS else "Asado")
        infantil_g = str(g.value(ev_uri, cat.menu_infantil) or "Hamburguesas")
        init_key(k("infantil"), infantil_g if infantil_g in ["Hamburguesas", "Milanesas", "Nuggets"] else "Hamburguesas")
        pan_g = str(g.value(ev_uri, cat.insumo_panaderia) or "Medialunas")
        init_key(k("panaderia"), pan_g if pan_g in ["Medialunas", "Pastelitos", "Buñuelos"] else "Medialunas")
        init_key(k("mesa_dulce"), "Sí" if bool(g.value(ev_uri, cat.mesa_dulce)) else "No")
        init_key(k("cerveza"), "Quilmes")
        init_key(k("gaseosa"), "Coca Cola")
        init_key(k("ninera"), bool(g.value(ev_uri, cat["servicio_niñera"])))
        init_key(k("transporte"), bool(g.value(ev_uri, cat.transporte)))
        init_key(k("dj"), bool(g.value(ev_uri, cat.ambientacion_y_DJ)))
        init_key(k("bajas"), 0)
        init_key(k("jefa"), "Disponible")
        init_key("extra_papa", float(g.value(cat["MI-Bolsa_Papa"], cat.insumos_extra) or 0.0))
        init_key("extra_cerveza", float(g.value(cat["MI-Cerveza"], cat.insumos_extra) or 0.0))
        for pid in PROVEEDORES:
            estado_g = str(g.value(cat[pid], cat.estado_entrega) or "OK")
            init_key(f"prov__{pid}", estado_g if estado_g in ESTADOS_ENTREGA else "OK")

        # ---------- 1. Datos del Evento y Fecha ----------
        with st.expander("1. Datos del Evento y Fecha", expanded=True):
            st.text_input("Cliente", key=k("cliente"))
            st.selectbox("Modalidad", ["Cena Formal", "Coffee Break"], key=k("modalidad"))
            minimo = primer_dia_reservable()
            if st.session_state[k("fecha")] < minimo:  # p. ej. si la sesión quedó abierta de un día para otro
                st.session_state[k("fecha")] = minimo
            st.date_input("Fecha del evento", min_value=minimo, max_value=FECHA_MAXIMA,
                          format="DD/MM/YYYY", key=k("fecha"))
            st.caption(f"Solo se admiten fechas desde el {minimo:%d/%m/%Y}.")
            st.selectbox("Clima previsto", ["Frío", "Calor"], key=k("clima"))

        # ---------- 2. Salón ----------
        with st.expander("2. Salón", expanded=False):
            st.selectbox("Tipo de salón", [TIPO_PROPIO, TIPO_EXTERNO], key=k("tipo_salon"))
            if st.session_state[k("tipo_salon")] == TIPO_PROPIO:
                salon_id = SALON_PROPIO
                render_html(f'<div class="etiqueta-salon">{SALONES[SALON_PROPIO]}</div>')
                st.caption(f"Capacidad: {g.value(cat[SALON_PROPIO], cat.capacidad_max)} personas")
            else:
                st.selectbox(
                    "Salón externo",
                    SALONES_EXTERNOS,
                    index=None,
                    placeholder="Elegí un salón externo",
                    format_func=lambda s: f"{SALONES[s]} ({g.value(cat[s], cat.capacidad_max)} personas)",
                    key=k("salon_ext"),
                )
                salon_id = st.session_state[k("salon_ext")] or SIN_SALON
            st.session_state[k("salon")] = salon_id
            if salon_id != SIN_SALON:
                s_uri = cat[salon_id]
                es_externo = (s_uri, RDF.type, cat["MC-Salon_externo"]) in g
                sk = lambda nombre: f"salon__{salon_id}__{nombre}"
                init_key(sk("banos"), str(g.value(s_uri, cat["estado_baños"]) or "Aprobado"))
                st.selectbox("Estado de Baños", ["Aprobado", "No aprobado"], key=sk("banos"))
                if es_externo:
                    init_key(sk("bomberos"), str(g.value(s_uri, cat.permiso_bomberos) or "Vigente"))
                    init_key(sk("municipal"), str(g.value(s_uri, cat.habilitacion_municipal) or "Aprobada"))
                    init_key(sk("policial"), str(g.value(s_uri, cat.permiso_policial) or "Aprobado"))
                    st.selectbox("Permiso de Bomberos", ["Vigente", "Vencido"], key=sk("bomberos"))
                    st.selectbox("Habilitación Municipal", ["Aprobada", "Pendiente"], key=sk("municipal"))
                    st.selectbox("Permiso Policial", list(ESTADOS_POLICIAL.keys()),
                                 format_func=lambda x: ESTADOS_POLICIAL[x], key=sk("policial"))
                else:
                    init_key(sk("habilitaciones"), str(g.value(s_uri, cat.habilitaciones) or "Vigentes"))
                    st.selectbox("Habilitaciones de la sede propia", ["Vigentes", "Vencidas"], key=sk("habilitaciones"))
                st.selectbox("Suministro Eléctrico", ["Normal", "Cortocircuito a 48 hs"], key=k("electrico"))

        # ---------- 3. Invitados ----------
        with st.expander("3. Invitados", expanded=False):
            st.number_input("Cantidad de Adultos", min_value=1, max_value=700, step=5, key=k("adultos"))
            st.number_input("Cantidad de Niños", min_value=0, max_value=200, step=1, key=k("ninos"))
            st.selectbox("Presupuesto", ["Cerrado", "Abierto"], key=k("presupuesto"))

        # ---------- 4. Menú y Bebidas ----------
        with st.expander("4. Menú y Bebidas", expanded=False):
            if st.session_state[k("modalidad")] == "Cena Formal":
                st.selectbox("Plato Principal", list(PLATOS.keys()), key=k("plato"))
                if st.session_state[k("ninos")] > 0:
                    st.selectbox("Menú Infantil", ["Hamburguesas", "Milanesas", "Nuggets"], key=k("infantil"))
                else:
                    st.caption("Menú infantil no aplica (cantidad de niños: 0).")
                st.selectbox("Mesa Dulce", ["Sí", "No"], key=k("mesa_dulce"))
            else:
                st.selectbox("Panadería", ["Medialunas", "Pastelitos", "Buñuelos"], key=k("panaderia"))
            st.selectbox("Marca de Cerveza", list(CERVEZAS.keys()), key=k("cerveza"))
            st.selectbox("Marca de Gaseosa", list(GASEOSAS.keys()), key=k("gaseosa"))
            st.number_input("Refuerzo extra de papa (bolsas)", min_value=0.0, max_value=50.0, step=1.0, key="extra_papa")
            st.number_input("Refuerzo extra de cerveza (litros)", min_value=0.0, max_value=500.0, step=10.0, key="extra_cerveza")

        # ---------- 5. Proveedores ----------
        with st.expander("5. Proveedores", expanded=False):
            for pid, etiqueta in PROVEEDORES.items():
                st.selectbox(etiqueta, list(ESTADOS_ENTREGA.keys()),
                             format_func=lambda x: ESTADOS_ENTREGA[x], key=f"prov__{pid}")

        # ---------- 6. Personal y Servicios ----------
        with st.expander("6. Personal y Servicios", expanded=False):
            if st.session_state[k("ninos")] > 0:
                st.checkbox("Servicio de Niñera", key=k("ninera"))
            else:
                st.caption("Servicio de niñera no aplica (cantidad de niños: 0).")
            st.checkbox("Transporte de Invitados", key=k("transporte"))
            st.checkbox("Ambientación y DJ", key=k("dj"))
            st.number_input("Bajas de mozos titulares a 48 hs", min_value=0, max_value=10, step=1, key=k("bajas"))
            st.selectbox("Estado de la Jefa de Cocina", ["Disponible", "Baja imprevista"], key=k("jefa"))
    return E
