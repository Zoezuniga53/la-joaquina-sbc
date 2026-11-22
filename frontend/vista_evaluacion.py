"""Pestaña 1: evaluación y viabilidad del evento."""

import streamlit as st
from backend.catalogos import CERVEZAS, ESTADOS_ENTREGA, GASEOSAS, SALONES, TXT_LLEVAR
from backend.motor import fv, heredar, salon_alternativo
from backend.ontologia import cat
from backend.servicios import motivos_legales
from frontend.componentes import esc, render_html, tabla_html, tarjeta
from frontend.estado import cb_reasignar_salon
from frontend.recursos import IMG_ASADO, IMG_BEBIDAS, IMG_PANADERIA, IMG_SALON


def render_evaluacion(g, ctx, an):
    """Dibuja la pestaña de evaluación (solo presentación)."""
    E = ctx.E
    ev_uri = ctx.ev_uri
    cliente = ctx.cliente
    modalidad = ctx.modalidad
    es_cena = ctx.es_cena
    anio = ctx.anio
    mes = ctx.mes
    dia = ctx.dia
    clima = ctx.clima
    salon_uri = ctx.salon_uri
    cortocircuito = ctx.cortocircuito
    adultos = ctx.adultos
    ninos = ctx.ninos
    presupuesto = ctx.presupuesto
    plato = ctx.plato
    infantil = ctx.infantil
    panaderia = ctx.panaderia
    mesa_dulce = ctx.mesa_dulce
    marca_cerveza = ctx.marca_cerveza
    marca_gaseosa = ctx.marca_gaseosa
    ninera = ctx.ninera
    transporte = ctx.transporte
    dj = ctx.dj
    bajas = ctx.bajas
    jefa_ausente = ctx.jefa_ausente
    hielo = ctx.hielo
    comensales = ctx.comensales
    fallas_suministro = an.fallas_suministro
    suplentes_activados = an.suplentes_activados
    estados_evento = an.estados_evento
    capacidad_estado = an.capacidad_estado
    mozos_requeridos = an.mozos_requeridos
    salon_habilitado = an.salon_habilitado
    capacidad_salon = an.capacidad_salon
    nombre_salon = an.nombre_salon
    st.markdown(f"### {esc(cliente)} — {modalidad}")
    render_html(f"""
<div class="barra-meta">
<span class="badge-meta badge-oro">{dia} de {mes} de {anio}</span>
<span class="badge-meta">Clima: {esc(clima)}</span>
<span class="badge-meta">Presupuesto: {esc(presupuesto)}</span>
<span class="badge-meta">Sede: {esc(nombre_salon)}</span>
<span class="badge-meta">Invitados: {comensales} ({adultos} ad. / {ninos} niñ.)</span>
</div>
""")

    # ---------- Tarjetas de resumen ejecutivo ----------
    if salon_uri is None:
        t_cap = tarjeta("Comensales vs. Capacidad del Salón", f"{comensales} invitados", "Salón pendiente de asignación")
        t_est = tarjeta("Estado de Capacidad", "Sin evaluar", "Requiere un salón asignado", "alerta")
        t_hab = tarjeta("Estado de Habilitación Legal", "Sin evaluar", "Requiere un salón asignado", "alerta")
    else:
        cap_ok = capacidad_estado == cat.Suficiente
        t_cap = tarjeta("Comensales vs. Capacidad del Salón", f"{comensales} de {capacidad_salon}",
                        f"{adultos} adultos y {ninos} niños en {nombre_salon}")
        t_est = tarjeta("Estado de Capacidad", "Capacidad Suficiente" if cap_ok else "Capacidad Insuficiente",
                        f"{capacidad_salon - comensales} plazas libres" if cap_ok
                        else f"Exceso de {comensales - capacidad_salon} invitados",
                        "ok" if cap_ok else "alerta")
        t_hab = tarjeta("Estado de Habilitación Legal", "Habilitado" if salon_habilitado else "No habilitado",
                        "Permisos y baños en regla" if salon_habilitado else "Revisar permisos del salón",
                        "ok" if salon_habilitado else "alerta")

    if fallas_suministro:
        t_sum = tarjeta("Estado de Suministros", "Falla crítica", f"{len(fallas_suministro)} insumo(s) sin respaldo", "alerta")
    elif suplentes_activados:
        t_sum = tarjeta("Estado de Suministros", "Suplente activo", f"{len(suplentes_activados)} reemplazo(s) en curso", "aviso")
    else:
        t_sum = tarjeta("Estado de Suministros", "Abastecido", "Proveedores operativos", "ok")

    for col, t in zip(st.columns(4), [t_cap, t_est, t_hab, t_sum]):
        with col:
            render_html(t)

    # ---------- Dictamen del Sistema ----------
    if salon_uri is None or "Incompleto" in estados_evento:
        render_html(f"""
<div class="panel panel-incompleto">
<div class="etiqueta">Dictamen del Sistema</div>
<div class="titular-dictamen">Evento incompleto</div>
<p>El evento de <strong>{esc(cliente)}</strong> todavía no tiene un salón asignado. Sin sede no es posible
verificar la capacidad, las habilitaciones ni la logística de traslado. Asigne un salón desde la sección
<strong>2. Salón</strong> del panel lateral.</p>
</div>""")
    elif "Confirmable" in estados_evento and not cortocircuito and not fallas_suministro:
        aviso_supl = ""
        if suplentes_activados:
            aviso_supl = "<p><strong>Aviso de contingencia:</strong> " + " ".join(esc(x) for x in suplentes_activados) + "</p>"
        render_html(f"""
<div class="panel panel-confirmable">
<div class="etiqueta">Dictamen del Sistema</div>
<div class="titular-dictamen">Evento confirmable</div>
<p>El evento de <strong>{esc(cliente)}</strong> en <strong>{nombre_salon}</strong> cumple con la capacidad requerida
({comensales} invitados sobre {capacidad_salon} plazas), el salón tiene sus habilitaciones, permisos y baños en regla,
y los insumos cuentan con provisión asegurada. Puede confirmarse con el cliente.</p>
{aviso_supl}
</div>""")
    else:
        motivos = []
        if capacidad_estado == cat.Insuficiente:
            motivos.append(f"Capacidad insuficiente: {comensales} invitados para {capacidad_salon} plazas disponibles en {nombre_salon}.")
        legales = motivos_legales(g, salon_uri)
        if legales:
            motivos.append("Riesgo de clausura legal o sanitaria: " + ", ".join(legales) + ".")
        if cortocircuito:
            motivos.append(f"Cortocircuito informado en {nombre_salon} a 48 horas del evento: la cocina y las cámaras de frío no pueden operar.")
        for f in fallas_suministro:
            motivos.append(f"Falla de abastecimiento: {f}")
        if not motivos:
            motivos.append("Las condiciones del salón o de suministro aún no fueron verificadas por completo.")
        items = "".join(f"<li>{esc(m)}</li>" for m in motivos)
        render_html(f"""
<div class="panel panel-bloqueado">
<div class="etiqueta">Dictamen del Sistema</div>
<div class="titular-dictamen">Bloqueado por riesgo operativo, legal o de suministro</div>
<p>El evento de <strong>{esc(cliente)}</strong> no puede confirmarse por los siguientes motivos:</p>
<ul>{items}</ul>
</div>""")

    col_log, col_per = st.columns(2)

    # ---------- Logística de traslado (herencia de marcos) ----------
    with col_log:
        if salon_uri is not None:
            sede = str(heredar(salon_uri, "sede", g) or "-")
            tiene_cocina = bool(heredar(salon_uri, "tiene_cocina", g) or heredar(salon_uri, "cocina_equipada", g))
            gas = str(heredar(salon_uri, "suministro_gas", g) or ("Red" if tiene_cocina else "Sin gas"))
            llevar = str(heredar(salon_uri, "llevar", g) or ("Solo_Insumos" if tiene_cocina else "Completo"))
            tipo_espacio = str(heredar(salon_uri, "tipo_espacio", g) or "Cerrado")
            inspeccion = heredar(salon_uri, "inspeccion_tecnica", g)
            plazo = heredar(salon_uri, "plazo_reubicacion_horas", g)
            if es_cena:
                protocolo = "Degustación con el cliente 30 días antes del evento." if str(heredar(ev_uri, "degustacion", g)) == "30_Dias_Antes" else "Sin degustación previa."
            else:
                protocolo = "Control de insumos obligatorio y llegada del equipo 2 horas antes del servicio."
            carpa = ""
            if "Carpa" in tipo_espacio:
                est_f = ESTADOS_ENTREGA[str(g.value(cat["MI-Proveedor_F"], cat.estado_entrega))]
                carpa = f"<p><strong>Espacio abierto:</strong> requiere contratar carpa estructural y sonido con Proveedor F (Jujuy). Estado del proveedor: {est_f}.</p>"
            render_html(f"""
<div class="panel panel-neutro">
<div class="etiqueta">Logística de traslado</div>
<p><strong>Sede:</strong> {sede}{' — inspección técnica ' + str(inspeccion).lower() if inspeccion else ''}{f' — plazo de reubicación {plazo} hs' if plazo else ''}</p>
<p><strong>Cocina en el salón:</strong> {'Sí' if tiene_cocina else 'No'}  |  <strong>Gas:</strong> {gas.replace('_', ' ')}  |  <strong>Espacio:</strong> {tipo_espacio.replace('_', ' ').lower()}</p>
<p><strong>Carga del camión:</strong> <span class="destacado">{TXT_LLEVAR.get(llevar, llevar.replace('_', ' '))}</span></p>
{carpa}
<p><strong>Protocolo de servicio:</strong> {protocolo}</p>
</div>""")
        else:
            render_html('<div class="panel panel-neutro"><div class="etiqueta">Logística de traslado</div><p>Se definirá al asignar un salón.</p></div>')

    # ---------- Redistribución del personal ----------
    with col_per:
        ratio_mozo = heredar(cat["MI-Mozo_Exp_1"], "ratio_comensales_por_mozo", g)
        tarea_exp = str(heredar(cat["MI-Mozo_Exp_1"], "tareas", g)).replace("_", " ")
        tarea_nov = str(heredar(cat["MI-Mozo_Nov_1"], "tareas", g)).replace("_", " ")
        if bajas == 0:
            txt_mozos = f"Plantel titular completo: {mozos_requeridos} mozos experimentados asignados a {tarea_exp.lower()} (1 cada {ratio_mozo} invitados)."
        elif bajas <= 2:
            txt_mozos = (f"{bajas} baja(s) sobre {mozos_requeridos} mozos. Se reorganizan los sectores del salón "
                         f"con el plantel titular, sin incorporar personal externo.")
        else:
            txt_mozos = (f"{bajas} bajas: se activa el protocolo de crisis e ingresan {bajas} mozos de urgencia. "
                         f"Los mozos experimentados quedan a cargo de <strong>{tarea_exp.lower()}</strong> (bandejeo principal y escaleras). "
                         f"Los mozos novatos se limitan a <strong>{tarea_nov.lower()}</strong>: bebida, pan, hielo y servilletas, "
                         f"sin bandejeo caliente ni uso de escaleras.")
        if jefa_ausente:
            txt_cocina = ("Baja imprevista de la Jefa de Cocina: el <strong>Encargado General</strong> asume la jefatura de cocina "
                          "y se contratan ayudantes para las tareas operativas.")
        else:
            txt_cocina = "La Jefa de Cocina está disponible y al frente de la brigada."
        render_html(f"""
<div class="panel panel-neutro">
<div class="etiqueta">Personal de salón y cocina</div>
<p><strong>Mozos:</strong> {txt_mozos}</p>
<p><strong>Cocina:</strong> {txt_cocina}</p>
</div>""")

    # ---------- Reubicación por cortocircuito o falta de capacidad ----------
    if salon_uri is not None and (cortocircuito or capacidad_estado == cat.Insuficiente):
        elegido, pasos, _ = salon_alternativo(ev_uri, g)
        filas = []
        for p in pasos:
            resultado = '<span class="txt-ok">Apto</span>' if p["apto"] else \
                f'<span class="txt-alerta">Descartado: {", ".join(p["motivos"])}</span>'
            filas.append([SALONES.get(p["id"], p["id"]), f'{p["capacidad"]} personas',
                          "Sí" if p["cocina"] else "No", p["banos"], resultado])
        motivo_reubic = "cortocircuito en el salón" if cortocircuito else "falta de capacidad"
        if elegido is not None:
            elegido_id = fv(elegido)
            paso = pasos[-1]
            nota_carpa = " Al ser un espacio abierto, se contrata carpa estructural con Proveedor F (Jujuy)." if paso["requiere_carpa"] else ""
            render_html(f"""
<div class="panel panel-confirmable">
<div class="etiqueta">Reubicación recomendada por {motivo_reubic}</div>
<p>El sistema recorrió la red de salones de respaldo y recomienda trasladar el evento a
<strong>{SALONES[elegido_id]}</strong> ({paso['capacidad']} plazas, con cocina y baños aprobados).{nota_carpa}</p>
</div>""")
            tabla_html(["Salón evaluado", "Capacidad", "Cocina", "Baños", "Resultado"], filas)
            st.button(f"REASIGNAR EL EVENTO A {SALONES[elegido_id].upper()}",
                      on_click=cb_reasignar_salon, args=(E, elegido_id))
        else:
            render_html(f"""
<div class="panel panel-bloqueado">
<div class="etiqueta">Reubicación por {motivo_reubic}</div>
<p>No hay salones de respaldo disponibles después de {nombre_salon} que cumplan capacidad, cocina y baños aprobados.
Seleccione manualmente otro salón en la sección 2 del panel lateral.</p>
</div>""")
            if filas:
                tabla_html(["Salón evaluado", "Capacidad", "Cocina", "Baños", "Resultado"], filas)

    # ---------- Tarjetas fotográficas ----------
    st.markdown("<br>", unsafe_allow_html=True)
    if es_cena:
        foto_menu = IMG_ASADO
        linea_infantil = f"<p>Menú infantil: {infantil}</p>" if ninos > 0 else "<p>Menú infantil: Sin niños</p>"
        cuerpo_menu = (f"<p>Plato principal: {plato}</p>{linea_infantil}"
                       f"<p>Mesa dulce: {'Incluida' if mesa_dulce else 'No incluida'}</p>")
    else:
        foto_menu = IMG_PANADERIA
        cuerpo_menu = f"<p>Panadería: {panaderia}</p><p>Servicio de café para {comensales} personas</p>"
    cerveza_uri = cat[CERVEZAS[marca_cerveza]]
    gaseosa_uri = cat[GASEOSAS[marca_gaseosa]]
    servicios = [n for n, v in [("Niñera", ninera), ("Transporte", transporte), ("Ambientación y DJ", dj)] if v]
    tarjetas_foto = [
        (foto_menu, "Menú", cuerpo_menu),
        (IMG_BEBIDAS, "Bebidas",
         f"<p>Cerveza: {marca_cerveza} ({g.value(cerveza_uri, cat.estilo)}, {g.value(cerveza_uri, cat.pais_origen)})</p>"
         f"<p>Gaseosa: {marca_gaseosa} (sabor {str(g.value(gaseosa_uri, cat.sabor)).lower()})</p>"
         f"<p>Hielo: {'Incluido por clima cálido' if hielo else 'No requerido'}</p>"
         f"<p>Validación: {heredar(cerveza_uri, 'validado_por', g)}</p>"),
        (IMG_SALON, "Salón y Servicios",
         f"<p>Sede: {nombre_salon}</p><p>Fecha: {dia} de {mes} de {anio}</p>"
         f"<p>Servicios: {', '.join(servicios) if servicios else 'Sin servicios adicionales'}</p>"),
    ]
    for col, (img, titulo, cuerpo) in zip(st.columns(3), tarjetas_foto):
        with col:
            render_html(f'<div class="foto-card"><div class="foto" style="background-image: url(\'{img}\');"></div>'
                        f'<div class="cuerpo"><h4>{titulo}</h4>{cuerpo}</div></div>')
