"""Motor de inferencia y funciones del sistema basado en conocimiento (sin dependencias de interfaz)."""

from rdflib import Graph
from rdflib.namespace import OWL, RDF, RDFS
from backend.ontologia import PROPIEDADES_INFERIDAS, TIPOS, TTL, cat


fv = lambda v: str(v).split("#")[-1] if "#" in str(v) else f'"{v}"'


def inicializar_grafo():
    """Crea el grafo RDF a partir del bloque TTL y declara los tipos de datos."""
    grafo = Graph()
    grafo.bind("cat", cat)
    grafo.parse(data=TTL, format="turtle")

    for tipo, props in TIPOS.items():
        for p in props.split():
            grafo.add((cat[p], RDF.type, OWL.DatatypeProperty))
            grafo.add((cat[p], RDFS.range, tipo))

    for p in ["capacidad_salon", "estado_habilitacion", "estado_evento", "estado_compra", "activo_como", "estado_alerta"]:
        grafo.add((cat[p], RDF.type, OWL.ObjectProperty))

    for p in ["nombre_insumo", "nombre_lugar", "razon_social", "nombre_marca", "cliente"]:
        for s, _, o in list(grafo.triples((None, cat[p], None))):
            grafo.add((s, RDFS.label, o))

    return grafo


def limpiar_inferencias(grafo):
    """Elimina las propiedades deducidas antes de re-ejecutar el motor de inferencia."""
    for p in PROPIEDADES_INFERIDAS:
        grafo.remove((None, cat[p], None))


def superclases(c, grafo):
    """Generador que asciende por la jerarquía rdfs:subClassOf."""
    while c is not None:
        yield c
        c = grafo.value(c, RDFS.subClassOf)


def heredar(ind, prop, grafo):
    """Valor propio de la instancia o, si no lo tiene, el de su clase o superclase."""
    g_ref = grafo
    v = g_ref.value(ind, cat[prop])
    if v is not None:
        return v
    for t in g_ref.objects(ind, RDF.type):
        for c in superclases(t, g_ref):
            v = g_ref.value(c, cat[prop])
            if v is not None:
                return v
    return None


def motor_inferencia(grafo, reglas):
    """Motor de producción con encadenamiento hacia adelante y resolución por prioridad."""
    it = 1
    bitacora = []
    while True:
        conflicto = []
        for r in reglas:  # 1. Reconocimiento
            nuevas = [t for t in grafo.query(r["query"]).graph if t not in grafo]
            if nuevas:
                conflicto.append({**r, "tripletas": nuevas})
        if not conflicto:  # Punto fijo
            bitacora.append(f"Iteración {it}: conjunto de conflicto vacío -> FIN")
            break
        ganadora = max(conflicto, key=lambda x: x["prioridad"])  # 2. Resolución de conflictos
        for t in ganadora["tripletas"]:  # 3. Acción
            grafo.add(t)
        bitacora.append(
            f"Iteración {it}: agenda={[c['id'] for c in conflicto]} -> dispara {ganadora['id']} "
            f"(prioridad {ganadora['prioridad']}) "
            + " ".join(f"+ {fv(t[0])} {fv(t[1])} {fv(t[2])}" for t in ganadora["tripletas"])
        )
        it += 1
    return bitacora


def proveedor_activo(p, grafo):
    """Recorre la cadena plan_suplente_de hasta hallar un proveedor con entrega OK."""
    g_ref = grafo
    visitados = set()
    while p is not None and p not in visitados:
        visitados.add(p)
        if str(g_ref.value(p, cat.estado_entrega)) == "OK":
            return p
        p = g_ref.value(predicate=cat.plan_suplente_de, object=p)
    return None


def salon_alternativo(evento, grafo):
    """Reubicación de emergencia (48 hs) recorriendo la cadena salon_respaldo_de."""
    g_ref = grafo
    comensales = int(g_ref.value(evento, cat.cant_adultos) or 0) + int(g_ref.value(evento, cat["cant_niños"]) or 0)
    actual = g_ref.value(evento, cat.lugar_asignado)
    pasos = []
    if actual is None:
        return None, pasos, comensales
    while True:
        actual = g_ref.value(predicate=cat.salon_respaldo_de, object=actual)
        if actual is None:
            return None, pasos, comensales
        cap = int(g_ref.value(actual, cat.capacidad_max) or 0)
        cocina = bool(heredar(actual, "tiene_cocina", g_ref) or heredar(actual, "cocina_equipada", g_ref))
        banos = str(g_ref.value(actual, cat["estado_baños"]) or "")
        tipo_esp = str(heredar(actual, "tipo_espacio", g_ref) or "Cerrado")
        motivos = []
        if cap < comensales:
            motivos.append(f"capacidad insuficiente ({cap} plazas para {comensales} invitados)")
        if not cocina:
            motivos.append("no posee cocina")
        if banos != "Aprobado":
            motivos.append("baños no aprobados")
        apto = not motivos
        pasos.append({
            "id": fv(actual),
            "capacidad": cap,
            "cocina": cocina,
            "banos": banos,
            "tipo_espacio": tipo_esp,
            "requiere_carpa": "Carpa" in tipo_esp,
            "apto": apto,
            "motivos": motivos,
        })
        if apto:
            return actual, pasos, comensales
