"""Base de reglas SPARQL CONSTRUCT (reglas de producción del SBC)."""




# ==============================================================================
# BASE DE REGLAS SPARQL CONSTRUCT (9 REGLAS DE PRODUCCIÓN)
# R1 y R2 usan OPTIONAL + COALESCE para evaluar eventos sin niños (Coffee Break).
# ==============================================================================
base_de_reglas = [
    {
        "id": "R1_CapacidadSuficiente",
        "prioridad": 10,
        "query": """
    CONSTRUCT { ?e cat:capacidad_salon cat:Suficiente . }
    WHERE { ?e cat:lugar_asignado ?s ; cat:cant_adultos ?a . OPTIONAL { ?e cat:cant_niños ?n }
            ?s cat:capacidad_max ?cap . FILTER (?cap >= ?a + COALESCE(?n, 0)) }""",
    },
    {
        "id": "R2_CapacidadInsuficiente",
        "prioridad": 10,
        "query": """
    CONSTRUCT { ?e cat:capacidad_salon cat:Insuficiente . }
    WHERE { ?e cat:lugar_asignado ?s ; cat:cant_adultos ?a . OPTIONAL { ?e cat:cant_niños ?n }
            ?s cat:capacidad_max ?cap . FILTER (?cap < ?a + COALESCE(?n, 0)) }""",
    },
    {
        "id": "R3_SalonExternoHabilitado",
        "prioridad": 10,
        "query": """
    CONSTRUCT { ?s cat:estado_habilitacion cat:Habilitado . }
    WHERE { ?s a cat:MC-Salon_externo ; cat:estado_baños "Aprobado" ; cat:permiso_bomberos "Vigente" ;
            cat:habilitacion_municipal "Aprobada" ; cat:permiso_policial "Aprobado" . }""",
    },
    {
        "id": "R4_SalonPropioHabilitado",
        "prioridad": 10,
        "query": """
    CONSTRUCT { ?s cat:estado_habilitacion cat:Habilitado . }
    WHERE { ?s a cat:MC-Salon_propio ; cat:estado_baños "Aprobado" ; cat:habilitaciones "Vigentes" . }""",
    },
    {
        "id": "R5_MozosRequeridos",
        "prioridad": 10,
        "query": """
    CONSTRUCT { ?e cat:mozos_requeridos ?m . }
    WHERE { ?e cat:cant_adultos ?a . OPTIONAL { ?e cat:cant_niños ?n }
            BIND(STRDT(STR(FLOOR((?a + COALESCE(?n, 0) + 24) / 25.0)), xsd:integer) AS ?m) }""",
    },
    {
        "id": "R6_EventoIncompleto",
        "prioridad": 10,
        "query": """
    CONSTRUCT { ?e cat:estado_evento cat:Incompleto . }
    WHERE { ?e rdf:type/rdfs:subClassOf* cat:MC-Evento . FILTER NOT EXISTS { ?e cat:lugar_asignado ?l } }""",
    },
    {
        "id": "R7_InsumoSinProveedor",
        "prioridad": 5,
        "query": """
    CONSTRUCT { ?i cat:estado_compra cat:SinProveedor . }
    WHERE { ?i cat:nombre_insumo ?n . FILTER NOT EXISTS { ?i cat:provisto_por ?p } }""",
    },
    {
        "id": "R8_ActivarProveedorSuplente",
        "prioridad": 15,
        "query": """
    CONSTRUCT { ?s cat:activo_como cat:ProveedorActivo . ?p cat:estado_alerta cat:Reemplazado . }
    WHERE { ?p cat:estado_entrega ?est . FILTER (?est != "OK") ?s cat:plan_suplente_de ?p . }""",
    },
    {
        "id": "R9_EventoConfirmable",
        "prioridad": 20,
        "query": """
    CONSTRUCT { ?e cat:estado_evento cat:Confirmable . }
    WHERE { ?e cat:capacidad_salon cat:Suficiente ; cat:lugar_asignado ?s .
            ?s cat:estado_habilitacion cat:Habilitado . }""",
    },
]
