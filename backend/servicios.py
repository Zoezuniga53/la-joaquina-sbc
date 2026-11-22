"""Servicios del evento: actualización del grafo, cálculo de insumos y evaluación de suministros."""

import math
from rdflib.namespace import RDF, RDFS
from backend.catalogos import ESTADOS_ENTREGA, GASEOSAS, PLATOS, PROVEEDORES, SALONES
from backend.grafo import set_bool, set_dec, set_int, set_txt
from backend.modelos import Analisis
from backend.motor import fv, heredar, limpiar_inferencias, motor_inferencia, proveedor_activo
from backend.ontologia import cat
from backend.reglas import base_de_reglas


def analizar_evento(g, E, ctx):
    """Aplica los parámetros al grafo, calcula insumos, ejecuta el motor y evalúa suministros.

    No toca la interfaz: recibe un ParametrosEvento y devuelve un Analisis.
    """
    E = ctx.E
    ev_uri = ctx.ev_uri
    cliente = ctx.cliente
    es_cena = ctx.es_cena
    anio = ctx.anio
    mes = ctx.mes
    dia = ctx.dia
    ambiente = ctx.ambiente
    salon_id = ctx.salon_id
    salon_uri = ctx.salon_uri
    adultos = ctx.adultos
    ninos = ctx.ninos
    presupuesto = ctx.presupuesto
    plato = ctx.plato
    infantil = ctx.infantil
    panaderia = ctx.panaderia
    mesa_dulce = ctx.mesa_dulce
    marca_cerveza = ctx.marca_cerveza
    marca_gaseosa = ctx.marca_gaseosa
    extra_papa = ctx.extra_papa
    extra_cerveza = ctx.extra_cerveza
    ninera = ctx.ninera
    transporte = ctx.transporte
    dj = ctx.dj
    hielo = ctx.hielo
    comensales = ctx.comensales
    fecha_uri = g.value(ev_uri, cat.fecha_evento)

    g.remove((ev_uri, RDF.type, cat["MC-Cena_formal"]))
    g.remove((ev_uri, RDF.type, cat["MC-Coffee_Break"]))
    g.add((ev_uri, RDF.type, cat["MC-Cena_formal"] if es_cena else cat["MC-Coffee_Break"]))

    set_txt(g, ev_uri, cat.cliente, cliente)
    set_txt(g, ev_uri, RDFS.label, cliente)
    set_int(g, ev_uri, cat.cant_adultos, adultos)
    set_int(g, ev_uri, cat["cant_niños"], ninos)
    set_txt(g, ev_uri, cat.presupuesto, presupuesto.lower())
    set_txt(g, ev_uri, cat.plato_principal, plato)
    set_txt(g, ev_uri, cat.menu_infantil, infantil)
    set_txt(g, ev_uri, cat.insumo_panaderia, panaderia)
    set_bool(g, ev_uri, cat.mesa_dulce, mesa_dulce)
    set_bool(g, ev_uri, cat.hielo, hielo)
    set_bool(g, ev_uri, cat["servicio_niñera"], ninera)
    set_bool(g, ev_uri, cat.transporte, transporte)
    set_bool(g, ev_uri, cat.ambientacion_y_DJ, dj)

    if fecha_uri is None:
        fecha_uri = cat[f"MI-Fecha_{E[3:]}"]
        g.add((fecha_uri, RDF.type, cat["MC-Fecha"]))
    g.set((ev_uri, cat.fecha_evento, fecha_uri))
    set_int(g, fecha_uri, cat.dia, dia)
    set_txt(g, fecha_uri, cat.mes, mes)
    set_int(g, fecha_uri, cat["año"], anio)
    set_txt(g, fecha_uri, cat.ambiente, ambiente)

    if salon_uri is not None:
        g.set((ev_uri, cat.lugar_asignado, salon_uri))
        set_txt(g, salon_uri, cat["estado_baños"], ctx.salon_detalle["banos"])
        if (salon_uri, RDF.type, cat["MC-Salon_externo"]) in g:
            set_txt(g, salon_uri, cat.permiso_bomberos, ctx.salon_detalle["bomberos"])
            set_txt(g, salon_uri, cat.habilitacion_municipal, ctx.salon_detalle["municipal"])
            set_txt(g, salon_uri, cat.permiso_policial, ctx.salon_detalle["policial"])
        else:
            set_txt(g, salon_uri, cat.habilitaciones, ctx.salon_detalle["habilitaciones"])
    else:
        g.remove((ev_uri, cat.lugar_asignado, None))

    for pid in PROVEEDORES:
        set_txt(g, cat[pid], cat.estado_entrega, ctx.estados_proveedores[pid])

    # ---------- Cálculo de insumos del evento activo ----------
    plato_id, ratio_fijo = PLATOS[plato]
    ratio_plato = ratio_fijo if ratio_fijo is not None else float(g.value(cat[plato_id], cat.cant_base_por_persona))
    ratio_lacteos = float(g.value(cat["MI-Lacteos"], cat.cant_base_por_persona))

    compras = []  # (insumo_id, nombre visible, base, extra, unidad)
    if es_cena:
        compras.append((plato_id, f"{plato} (plato principal)", adultos * ratio_plato, 0.0, "kg"))
        if mesa_dulce:
            compras.append(("MI-Lacteos", "Lácteos (mesa dulce)", adultos * ratio_lacteos, 0.0, "kg"))
        compras.append(("MI-Bolsa_Papa", "Papa Blanca", float(math.ceil(adultos / 25)), extra_papa, "bolsas"))
        compras.append(("MI-Tomate", "Tomate", adultos * 0.10, 0.0, "kg"))
        compras.append(("MI-Cebolla", "Cebolla", adultos * 0.05, 0.0, "kg"))
        compras.append(("MI-Perejil", "Perejil", adultos * 0.01, 0.0, "kg"))
        compras.append(("MI-Harina", "Harina (panificación)", comensales * 0.08, 0.0, "kg"))
        compras.append(("MI-Cerveza", f"Cerveza {marca_cerveza}", adultos * 1.0, extra_cerveza, "L"))
    else:
        compras.append(("MI-Harina", f"Harina ({panaderia})", comensales * 0.15, 0.0, "kg"))
        compras.append(("MI-Lacteos", "Lácteos (servicio de café)", comensales * 0.15, 0.0, "kg"))
    compras.append((GASEOSAS[marca_gaseosa], f"Gaseosa {marca_gaseosa}", comensales * 0.6, 0.0, "L"))
    if hielo:
        compras.append(("MI-Hielo", "Hielo", comensales * 0.8, 0.0, "kg"))

    for ins_id, _, base, extra, _ in compras:
        if g.value(cat[ins_id], cat.nombre_insumo) is not None:
            set_dec(g, cat[ins_id], cat.cant_base_calculada, base)
            set_dec(g, cat[ins_id], cat.insumos_extra, extra)
            set_dec(g, cat[ins_id], cat.cant_total, base + extra)

    limpiar_inferencias(g)
    bitacora = motor_inferencia(g, base_de_reglas)

    # ---------- Evaluación de suministros y proveedores ----------
    proveedor_bebidas = g.value(cat["MI-Cerveza"], cat.provisto_por)
    fallas_suministro = []
    suplentes_activados = []

    for ins_id, nombre_ins, _, _, _ in compras:
        ins = cat[ins_id]
        es_bebida = str(heredar(ins, "rubro", g) or "") == "Bebida"
        titular = g.value(ins, cat.provisto_por) or (proveedor_bebidas if es_bebida else None)
        if titular is None:
            fallas_suministro.append(f"Insumo '{nombre_ins}' sin proveedor asignado.")
            continue
        est_tit = str(g.value(titular, cat.estado_entrega) or "OK")
        activo = proveedor_activo(titular, g)
        if est_tit != "OK":
            motivo_est = ESTADOS_ENTREGA.get(est_tit, est_tit).lower()
            if activo is None:
                fallas_suministro.append(
                    f"{nombre_ins}: {g.value(titular, cat.razon_social)} reporta '{motivo_est}' y no hay suplente operativo disponible."
                )
            else:
                suplentes_activados.append(
                    f"{nombre_ins}: {g.value(titular, cat.razon_social)} ({motivo_est}) -> cubierto por {g.value(activo, cat.razon_social)}."
                )

    # Verificar explícitamente si todos los proveedores de carne (A, B, C) cayeron en cenas con carne
    if es_cena and plato_id in ("MI-Carne_Vacuna", "MI-Lomo", "MI-Pollo", "MI-Mariscos"):
        carnes_ids = ["MI-Proveedor_A", "MI-Proveedor_B", "MI-Proveedor_C"]
        carnes_ok = [pid for pid in carnes_ids if str(g.value(cat[pid], cat.estado_entrega) or "OK") == "OK"]
        if not carnes_ok:
            detalle_carnes = "Todos los proveedores de la cadena de carnes (A, B y C) presentan fallas sin suplente disponible."
            if detalle_carnes not in fallas_suministro:
                fallas_suministro.append(detalle_carnes)

    # ---------- Conclusiones deducidas ----------
    estados_evento = set(fv(o) for o in g.objects(ev_uri, cat.estado_evento))
    capacidad_estado = g.value(ev_uri, cat.capacidad_salon)
    mozos_requeridos = int(g.value(ev_uri, cat.mozos_requeridos) or 0)
    salon_externo = salon_uri is not None and (salon_uri, RDF.type, cat["MC-Salon_externo"]) in g
    salon_habilitado = salon_uri is not None and g.value(salon_uri, cat.estado_habilitacion) == cat.Habilitado
    capacidad_salon = int(g.value(salon_uri, cat.capacidad_max) or 0) if salon_uri is not None else 0
    nombre_salon = SALONES[salon_id]

    return Analisis(
        plato_id=plato_id,
        compras=compras,
        proveedor_bebidas=proveedor_bebidas,
        fallas_suministro=fallas_suministro,
        suplentes_activados=suplentes_activados,
        estados_evento=estados_evento,
        capacidad_estado=capacidad_estado,
        mozos_requeridos=mozos_requeridos,
        salon_externo=salon_externo,
        salon_habilitado=salon_habilitado,
        capacidad_salon=capacidad_salon,
        nombre_salon=nombre_salon,
        bitacora=bitacora,
    )


def motivos_legales(g, s_uri):
    """Lista explícita de los requisitos legales incumplidos según los hechos del grafo."""
    motivos = []
    if str(g.value(s_uri, cat["estado_baños"])) != "Aprobado":
        motivos.append("Baños no aprobados")
    if (s_uri, RDF.type, cat["MC-Salon_externo"]) in g:
        if str(g.value(s_uri, cat.permiso_bomberos)) != "Vigente":
            motivos.append("Permiso de Bomberos vencido")
        if str(g.value(s_uri, cat.habilitacion_municipal)) != "Aprobada":
            motivos.append("Habilitación Municipal pendiente")
        policial = str(g.value(s_uri, cat.permiso_policial))
        if policial == "En_Tramite":
            motivos.append("Permiso Policial en trámite")
        elif policial != "Aprobado":
            motivos.append("Permiso Policial rechazado")
    elif str(g.value(s_uri, cat.habilitaciones)) != "Vigentes":
        motivos.append("Habilitaciones de la sede propia vencidas")
    return motivos
