"""Lectura de los controles de la interfaz hacia ParametrosEvento."""

import streamlit as st
from backend.catalogos import PROVEEDORES, SIN_SALON, max_dias_mes
from backend.modelos import ParametrosEvento
from backend.ontologia import cat


def leer_parametros(E, g):
    """Lee los controles de la barra lateral y los devuelve como ParametrosEvento."""
    ss = st.session_state
    k = lambda nombre: f"{E}__{nombre}"
    ev_uri = cat[E]
    cliente = ss[k("cliente")].strip() or "Cliente sin nombre"
    modalidad = ss[k("modalidad")]
    es_cena = modalidad == "Cena Formal"
    anio = int(ss[k("anio")])
    mes = ss[k("mes")]
    dia = min(int(ss[k("dia")]), max_dias_mes(mes, anio))
    clima = ss[k("clima")]
    ambiente = "Calor" if clima == "Calor" else "Frio"
    salon_id = ss[k("salon")]
    salon_uri = cat[salon_id] if salon_id != SIN_SALON else None
    cortocircuito = salon_uri is not None and ss[k("electrico")] == "Cortocircuito a 48 hs"
    adultos, ninos = int(ss[k("adultos")]), int(ss[k("ninos")])
    presupuesto = ss[k("presupuesto")]
    plato = ss[k("plato")]
    infantil = ss[k("infantil")] if ninos > 0 else "No aplica"
    panaderia = ss[k("panaderia")]
    mesa_dulce = es_cena and ss[k("mesa_dulce")] == "Sí"
    marca_cerveza, marca_gaseosa = ss[k("cerveza")], ss[k("gaseosa")]
    extra_papa, extra_cerveza = float(ss["extra_papa"]), float(ss["extra_cerveza"])
    ninera, transporte, dj = ss[k("ninera")], ss[k("transporte")], ss[k("dj")]
    bajas = int(ss[k("bajas")])
    jefa_ausente = ss[k("jefa")] == "Baja imprevista"
    hielo = ambiente == "Calor"
    comensales = adultos + ninos
    salon_detalle = {}
    if salon_uri is not None:
        sk = lambda nombre: f"salon__{salon_id}__{nombre}"
        for campo in ("banos", "bomberos", "municipal", "policial", "habilitaciones"):
            if sk(campo) in ss:
                salon_detalle[campo] = ss[sk(campo)]
    estados_proveedores = {pid: ss[f"prov__{pid}"] for pid in PROVEEDORES}
    return ParametrosEvento(
        E=E,
        ev_uri=ev_uri,
        cliente=cliente,
        modalidad=modalidad,
        es_cena=es_cena,
        anio=anio,
        mes=mes,
        dia=dia,
        clima=clima,
        ambiente=ambiente,
        salon_id=salon_id,
        salon_uri=salon_uri,
        cortocircuito=cortocircuito,
        adultos=adultos,
        ninos=ninos,
        presupuesto=presupuesto,
        plato=plato,
        infantil=infantil,
        panaderia=panaderia,
        mesa_dulce=mesa_dulce,
        marca_cerveza=marca_cerveza,
        marca_gaseosa=marca_gaseosa,
        extra_papa=extra_papa,
        extra_cerveza=extra_cerveza,
        ninera=ninera,
        transporte=transporte,
        dj=dj,
        bajas=bajas,
        jefa_ausente=jefa_ausente,
        hielo=hielo,
        comensales=comensales,
        salon_detalle=salon_detalle,
        estados_proveedores=estados_proveedores,
    )
