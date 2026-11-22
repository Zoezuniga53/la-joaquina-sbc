"""Contratos de datos entre la interfaz y la lógica."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParametrosEvento:
    """Valores elegidos por el organizador (los entrega la interfaz, los consume el backend)."""
    E: Any = None
    ev_uri: Any = None
    cliente: Any = None
    modalidad: Any = None
    es_cena: Any = None
    anio: Any = None
    mes: Any = None
    dia: Any = None
    clima: Any = None
    ambiente: Any = None
    salon_id: Any = None
    salon_uri: Any = None
    cortocircuito: Any = None
    adultos: Any = None
    ninos: Any = None
    presupuesto: Any = None
    plato: Any = None
    infantil: Any = None
    panaderia: Any = None
    mesa_dulce: Any = None
    marca_cerveza: Any = None
    marca_gaseosa: Any = None
    extra_papa: Any = None
    extra_cerveza: Any = None
    ninera: Any = None
    transporte: Any = None
    dj: Any = None
    bajas: Any = None
    jefa_ausente: Any = None
    hielo: Any = None
    comensales: Any = None
    salon_detalle: Any = None
    estados_proveedores: Any = None


@dataclass
class Analisis:
    """Resultado de aplicar los parámetros al grafo y ejecutar el motor de inferencia."""
    plato_id: Any = None
    compras: Any = None
    proveedor_bebidas: Any = None
    fallas_suministro: Any = None
    suplentes_activados: Any = None
    estados_evento: Any = None
    capacidad_estado: Any = None
    mozos_requeridos: Any = None
    salon_externo: Any = None
    salon_habilitado: Any = None
    capacidad_salon: Any = None
    nombre_salon: Any = None
    bitacora: Any = None
