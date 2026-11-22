"""Regla de negocio de fechas: solo se aceptan reservas posteriores a la fecha actual."""

from datetime import date, timedelta

from backend.catalogos import MESES

FECHA_MAXIMA = date(2030, 12, 31)


def primer_dia_reservable(hoy=None):
    """Primer día en que se puede reservar: el día siguiente a hoy."""
    return (hoy or date.today()) + timedelta(days=1)


def ajustar_a_reservable(fecha, hoy=None):
    """Si la fecha ya pasó (o es hoy), devuelve el primer día reservable."""
    return max(fecha, primer_dia_reservable(hoy))


def a_fecha(dia, mes_nombre, anio):
    """Convierte día, nombre de mes y año en un objeto date."""
    return date(int(anio), MESES.index(mes_nombre) + 1, int(dia))
