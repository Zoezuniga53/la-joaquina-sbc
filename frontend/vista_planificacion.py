"""Pestaña 2: planificación de insumos, proveedores y personal."""

import math
import streamlit as st
from rdflib.namespace import RDFS
from backend.catalogos import ESTADOS_ENTREGA, PROVEEDORES, TXT_CONSERVACION, TXT_PAGO, TXT_RETIRO
from backend.grafo import nombre_proveedor
from backend.motor import heredar, proveedor_activo
from backend.ontologia import cat
from frontend.componentes import esc, render_html, tabla_html


def render_planificacion(g, ctx, an):
    """Dibuja la pestaña de planificación (solo presentación)."""
    cliente = ctx.cliente
    adultos = ctx.adultos
    ninos = ctx.ninos
    ninera = ctx.ninera
    transporte = ctx.transporte
    dj = ctx.dj
    bajas = ctx.bajas
    jefa_ausente = ctx.jefa_ausente
    comensales = ctx.comensales
    compras = an.compras
    proveedor_bebidas = an.proveedor_bebidas
    fallas_suministro = an.fallas_suministro
    mozos_requeridos = an.mozos_requeridos
    st.markdown(f"### Planificación de compras — {esc(cliente)}")
    st.caption(f"Cantidades calculadas para {adultos} adultos y {ninos} niños. Las condiciones de conservación, pago y retiro provienen de la categoría de cada insumo.")

    if fallas_suministro:
        items_falla = "".join(f"<li>{esc(f)}</li>" for f in fallas_suministro)
        render_html(f"""
<div class="panel panel-bloqueado">
<div class="etiqueta">Alerta de Abastecimiento</div>
<p>Se detectaron fallas sin cobertura en la cadena de suministro que impiden confirmar el evento:</p>
<ul>{items_falla}</ul>
</div>""")

    filas = []
    for ins_id, nombre, base, extra, unidad in compras:
        ins = cat[ins_id]
        decimales = 0 if unidad == "bolsas" else 1
        conservacion = heredar(ins, "conservacion", g)
        pago = heredar(ins, "momento_pago", g) or heredar(ins, "momento_compra", g)
        retiro = heredar(ins, "momento_retiro", g)
        es_bebida = heredar(ins, "rubro", g) is not None and str(heredar(ins, "rubro", g)) == "Bebida"

        titular = g.value(ins, cat.provisto_por)
        if titular is None and es_bebida:
            titular = proveedor_bebidas

        if titular is None:
            estado = '<span class="txt-alerta">Sin proveedor asignado</span>' \
                if g.value(ins, cat.estado_compra) == cat.SinProveedor else '<span class="txt-alerta">Sin proveedor</span>'
            final = '<span class="txt-alerta">Asignar proveedor con urgencia</span>'
        else:
            est_tit = str(g.value(titular, cat.estado_entrega))
            estado = f'<span class="{"txt-ok" if est_tit == "OK" else "txt-alerta"}">{ESTADOS_ENTREGA.get(est_tit, est_tit)}</span>'
            activo = proveedor_activo(titular, g)
            if activo is None:
                final = '<span class="txt-alerta">Sin respaldo disponible en la red</span>'
            elif activo == titular:
                final = nombre_proveedor(activo, g)
            else:
                final = f'<span class="txt-aviso">{nombre_proveedor(activo, g)} — suplente activado</span>'

        filas.append([
            nombre,
            f"{base:.{decimales}f} {unidad}",
            f"{extra:.{decimales}f} {unidad}" if extra else "—",
            f"<strong>{base + extra:.{decimales}f} {unidad}</strong>",
            TXT_CONSERVACION.get(str(conservacion), "Bebida (cámara de servicio)" if es_bebida else "—"),
            TXT_PAGO.get(str(pago), "Contra entrega"),
            TXT_RETIRO.get(str(retiro), "Entrega previa en depósito"),
            nombre_proveedor(titular, g) if titular is not None else "—",
            estado,
            final,
        ])
    tabla_html(["Insumo", "Cantidad base", "Refuerzo extra", "Total a comprar", "Conservación",
                "Momento de pago", "Momento de retiro", "Proveedor titular", "Estado", "Proveedor activo final"], filas)

    # ---------- Red de proveedores ----------
    st.markdown("### Red de proveedores")
    filas_prov = []
    for pid, etiqueta in PROVEEDORES.items():
        p = cat[pid]
        est = str(g.value(p, cat.estado_entrega))
        if g.value(p, cat.estado_alerta) == cat.Reemplazado:
            situacion = '<span class="txt-alerta">Reemplazado por su suplente</span>'
        elif g.value(p, cat.activo_como) == cat.ProveedorActivo:
            situacion = '<span class="txt-aviso">Activado como suplente</span>'
        elif est != "OK":
            situacion = '<span class="txt-alerta">Con falla y sin suplente registrado</span>'
        else:
            situacion = '<span class="txt-ok">Operativo</span>'
        filas_prov.append([
            etiqueta,
            ESTADOS_ENTREGA.get(est, est),
            situacion,
            "Estricta" if heredar(p, "exige_cadena_frio", g) else "Estándar",
            str(heredar(p, "confirmacion_final", g)).replace("_", " ").replace("Dias", "días").replace("Antes Por Telefono", "antes por teléfono"),
        ])
    tabla_html(["Proveedor", "Estado de entrega", "Situación", "Cadena de frío", "Confirmación final"], filas_prov)

    # ---------- Brigada de personal ----------
    st.markdown("### Distribución de la brigada")
    tarea_exp = str(heredar(cat["MI-Mozo_Exp_1"], "tareas", g)).replace("_", " ")
    tarea_nov = str(heredar(cat["MI-Mozo_Nov_1"], "tareas", g)).replace("_", " ")
    funcion_jefe = str(g.value(cat["MI-Cocinero_Jefe"], cat.funcion))
    brigada = []
    if jefa_ausente:
        brigada.append(["Encargado General (reemplazo)", "1", funcion_jefe, '<span class="txt-aviso">Asume por baja imprevista de la Jefa de Cocina</span>'])
        brigada.append(["Ayudantes de cocina", str(max(2, math.ceil(comensales / 100))), "Tareas operativas de cocina", "Contratación de urgencia"])
    else:
        brigada.append(["Jefa de Cocina", "1", funcion_jefe, "Titular disponible"])
    titulares = max(mozos_requeridos - bajas, 0)
    obs_tit = "Plantel completo" if bajas == 0 else (f"Sectores reorganizados por {bajas} baja(s)" if bajas <= 2 else f"{bajas} bajas cubiertas por personal de urgencia")
    brigada.append(["Mozos experimentados", str(titulares), tarea_exp, f"Bandejeo principal y escaleras. {obs_tit}"])
    if bajas > 2:
        cubre = g.value(cat["MI-Apoyo_Urgencia_1"], cat.cubre_baja_de)
        brigada.append(["Mozos novatos de urgencia", str(bajas), tarea_nov,
                        f"Solo bebida, pan, hielo y servilletas. Sin bandejeo caliente ni escaleras. Cubren bajas de {str(g.value(cubre, RDFS.label)).lower()}s"])
    if ninera:
        brigada.append(["Niñeras", str(max(1, math.ceil(ninos / 15))), "Cuidado de niños", f"{ninos} niños registrados"])
    if dj:
        brigada.append(["DJ", "1", "Ambientación y música", "Servicio contratado"])
    if transporte:
        brigada.append(["Coordinador de transporte", "1", "Traslado de invitados", "Servicio contratado"])
    tabla_html(["Rol", "Cantidad", "Tarea asignada", "Observaciones"], brigada)
