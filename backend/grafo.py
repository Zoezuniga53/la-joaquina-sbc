"""Escritura en el grafo RDF: utilidades, grafo inicial y altas/reasignaciones de eventos."""

import re
from rdflib import Literal
from rdflib.namespace import RDF, RDFS, XSD
from backend.catalogos import SIN_SALON
from backend.motor import inicializar_grafo, limpiar_inferencias, motor_inferencia
from backend.ontologia import cat
from backend.reglas import base_de_reglas


def set_txt(grafo, s, p, valor):
    grafo.set((s, p, Literal(str(valor))))


def set_int(grafo, s, p, valor):
    grafo.set((s, p, Literal(int(valor))))


def set_bool(grafo, s, p, valor):
    grafo.set((s, p, Literal(bool(valor))))


def set_dec(grafo, s, p, valor):
    grafo.set((s, p, Literal(f"{float(valor):.2f}", datatype=XSD.decimal)))



def nombre_proveedor(p_uri, grafo):
    if p_uri is None:
        return "Sin proveedor"
    return f"{grafo.value(p_uri, cat.razon_social)} ({grafo.value(p_uri, cat.ubicacion)})"



def construir_grafo_inicial():
    grafo = inicializar_grafo()
    ministerio = cat["MI-Coffee_Ministerio"]
    set_txt(grafo, ministerio, cat.cliente, "Ministerio de Salud")
    set_txt(grafo, ministerio, RDFS.label, "Ministerio de Salud")
    set_int(grafo, ministerio, cat["cant_niños"], 0)
    set_txt(grafo, ministerio, cat.presupuesto, "cerrado")
    fecha_min = cat["MI-Fecha_Ministerio"]
    grafo.add((fecha_min, RDF.type, cat["MC-Fecha"]))
    set_int(grafo, fecha_min, cat.dia, 5)
    set_txt(grafo, fecha_min, cat.mes, "Noviembre")
    set_int(grafo, fecha_min, cat["año"], 2026)
    set_txt(grafo, fecha_min, cat.ambiente, "Calor")
    grafo.set((ministerio, cat.fecha_evento, fecha_min))
    limpiar_inferencias(grafo)
    motor_inferencia(grafo, base_de_reglas)
    return grafo



def crear_evento(grafo, nombre, modalidad, salon_id, eventos_existentes):
    """Da de alta un evento nuevo en el grafo, re-ejecuta el motor y devuelve el id asignado."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", nombre).strip("_") or "Cliente"
    nuevo_id, i = f"MI-Evento_{slug}", 2
    while nuevo_id in eventos_existentes:
        nuevo_id, i = f"MI-Evento_{slug}_{i}", i + 1
    ev = cat[nuevo_id]
    fecha = cat[f"MI-Fecha_{nuevo_id[3:]}"]
    grafo.add((ev, RDF.type, cat["MC-Cena_formal"] if modalidad == "Cena Formal" else cat["MC-Coffee_Break"]))
    set_txt(grafo, ev, cat.cliente, nombre)
    set_txt(grafo, ev, RDFS.label, nombre)
    set_int(grafo, ev, cat.cant_adultos, 100)
    set_int(grafo, ev, cat["cant_niños"], 0)
    set_txt(grafo, ev, cat.presupuesto, "cerrado")
    set_txt(grafo, ev, cat.plato_principal, "Asado")
    set_txt(grafo, ev, cat.menu_infantil, "Hamburguesas")
    set_txt(grafo, ev, cat.insumo_panaderia, "Medialunas")
    set_bool(grafo, ev, cat.mesa_dulce, modalidad == "Cena Formal")
    set_bool(grafo, ev, cat["servicio_niñera"], False)
    set_bool(grafo, ev, cat.transporte, False)
    set_bool(grafo, ev, cat.ambientacion_y_DJ, False)
    set_bool(grafo, ev, cat.hielo, False)

    grafo.add((fecha, RDF.type, cat["MC-Fecha"]))
    set_int(grafo, fecha, cat.dia, 12)
    set_txt(grafo, fecha, cat.mes, "Diciembre")
    set_int(grafo, fecha, cat["año"], 2026)
    set_txt(grafo, fecha, cat.ambiente, "Frio")
    grafo.set((ev, cat.fecha_evento, fecha))
    if salon_id != SIN_SALON:
        grafo.set((ev, cat.lugar_asignado, cat[salon_id]))
    limpiar_inferencias(grafo)
    motor_inferencia(grafo, base_de_reglas)
    return nuevo_id


def reasignar_salon(grafo, evento_id, salon_id):
    """Asigna otro salón al evento (reubicación)."""
    grafo.set((cat[evento_id], cat.lugar_asignado, cat[salon_id]))
