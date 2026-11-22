"""Catálogos de dominio: salones, proveedores, menús, meses y textos de presentación."""

import calendar


SIN_SALON = "SIN_SALON"
SALONES = {
    SIN_SALON: "Pendiente de asignación",
    "MI-Salon_Labarta": "Salón Labarta",
    "MI-Salon_Soc_Española": "Sociedad Española",
    "MI-Salon_Borus": "Salón Borus",
    "MI-Salon_Fed_Gaucha": "Federación Gaucha",
    "MI-Salon_Uta": "Salón UTA",
    "MI-Salon_Biofal": "Salón Biofal",
}

PROVEEDORES = {
    "MI-Proveedor_A": "Proveedor A (Jujuy - Carnes)",
    "MI-Proveedor_B": "Proveedor B (Salta - Suplente Carnes)",
    "MI-Proveedor_C": "Proveedor C (Buenos Aires - Mariscos / Plan C)",
    "MI-Proveedor_D": "Proveedor D (Jujuy - Verduras y Bebidas)",
    "MI-Proveedor_E": "Proveedor E (Jujuy - Suplente Bebidas)",
    "MI-Proveedor_F": "Proveedor F (Jujuy - Carpas y Sonido)",
    "MI-Proveedor_G": "Proveedor G (Jujuy - Harina y Panificación)",
}
ESTADOS_ENTREGA = {"OK": "OK", "Falla_Frio": "Falla de frío", "Sin_Stock": "Sin stock"}
ESTADOS_POLICIAL = {"Aprobado": "Aprobado", "En_Tramite": "En trámite", "Rechazado": "Rechazado"}

PLATOS = {
    "Asado": ("MI-Carne_Vacuna", 0.500),
    "Lomo": ("MI-Lomo", None),
    "Mariscos": ("MI-Mariscos", None),
    "Pollo": ("MI-Pollo", None),
}
CERVEZAS = {
    "Quilmes": "MI-Cerveza_Quilmes",
    "Patagonia Amber Lager": "MI-Cerveza_Patagonia_Amber_Lager",
    "Heineken": "MI-Cerveza_Heineken",
    "Stella Artois": "MI-Cerveza_Stella_Artois",
    "Corona": "MI-Cerveza_Corona",
}
GASEOSAS = {
    "Coca Cola": "MI-Gaseosa_CocaCola",
    "Pepsi": "MI-Gaseosa_Pepsi",
    "Aquarius": "MI-Gaseosa_Aquarius",
    "Benedictino": "MI-Gaseosa_Benedictino",
}
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
         "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def max_dias_mes(mes_nombre, anio_num):
    """Devuelve la cantidad máxima de días válida para un mes y año dados."""
    mes_idx = MESES.index(mes_nombre) + 1 if mes_nombre in MESES else 1
    return calendar.monthrange(int(anio_num), mes_idx)[1]


TXT_CONSERVACION = {"Frio_critico": "Frío crítico", "Almacenable": "Almacenable"}
TXT_PAGO = {"7_Dias_Antes": "7 días antes", "A_definir": "A definir con el proveedor"}
TXT_RETIRO = {"Mismo_Dia_Evento": "Mismo día del evento"}
TXT_LLEVAR = {
    "Solo_Insumos": "Solo insumos gastronómicos",
    "Insumos_Garrafa": "Insumos, garrafas y hornos móviles",
    "Completo": "Equipamiento de cocina completo, garrafas e insumos",
}
