# -*- coding: utf-8 -*-
"""
La Joaquina | Eventos gastronómicos
Sistema de Gestión y Orquestación Logística - Unidad 6 (Implementación de SBC)

La interfaz muestra únicamente resultados operativos. El motor semántico
(TTL, TIPOS, heredar, motor_inferencia y base_de_reglas) se ejecuta de forma
transparente en segundo plano cada vez que el organizador modifica un dato.
"""

import re
import math
import html as html_lib

import streamlit as st
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="SBC La Joaquina - Asesor Gastronómico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# HOJA DE ESTILOS (ALTA GASTRONOMÍA: NEGRO, CARBÓN Y DORADO)
# ==============================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

html, body, p, label, input, button, textarea, li, td, th {
    font-family: 'Montserrat', sans-serif;
}

/* Protección de los íconos nativos de Streamlit (evita el texto _arrow_right) */
[data-testid="stIconMaterial"], .material-icons, span[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
}

.stApp {
    background-color: #0b0b0b;
    color: #e8e4da;
}
[data-testid="stHeader"] {
    background-color: rgba(11, 11, 11, 0.85);
}
section[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #2a2a2a;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #cfcac0 !important;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
}

h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f5f5f0 !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
}

/* Controles de formulario */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="base-input"], input, textarea {
    background-color: #1a1a1a !important;
    color: #f5f5f0 !important;
    border-color: #333333 !important;
}
ul[role="listbox"], div[data-baseweb="popover"] li {
    background-color: #1a1a1a !important;
    color: #f5f5f0 !important;
}

/* Botones */
.stButton > button {
    background-color: #141414 !important;
    color: #f5f5f0 !important;
    border: 1px solid #c5a059 !important;
    border-radius: 3px !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: normal !important;
    min-height: 2.6rem;
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    background-color: #c5a059 !important;
    color: #0b0b0b !important;
}
.stButton > button p {
    font-weight: 500;
}

/* Desplegables de la barra lateral */
[data-testid="stExpander"] details {
    background-color: #141414;
    border: 1px solid #2a2a2a !important;
    border-radius: 4px;
}
[data-testid="stExpander"] summary p {
    font-weight: 500;
    color: #f5f5f0;
    letter-spacing: 0.03em;
}
[data-testid="stExpander"] summary:hover p {
    color: #c5a059;
}

/* Pestañas */
button[data-baseweb="tab"] p {
    font-size: 0.82rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a8a29e;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #c5a059 !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #c5a059 !important;
}

/* Marca en la barra lateral */
.marca-sidebar {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.7rem;
    color: #f5f5f0;
    border-bottom: 1px solid #c5a059;
    padding-bottom: 6px;
    margin-bottom: 4px;
}
.marca-sidebar-sub {
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c5a059;
    margin-bottom: 18px;
}
.rotulo-seccion {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c5a059;
    margin: 16px 0 6px 0;
}

/* Tarjetas de resumen ejecutivo */
.tarjeta-resumen {
    background-color: #141414;
    border: 1px solid #c5a059;
    border-radius: 4px;
    padding: 18px;
    min-height: 115px;
    white-space: normal;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.tarjeta-titulo {
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #a8a29e;
    margin-bottom: 8px;
    white-space: normal;
}
.tarjeta-valor {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.45rem;
    font-weight: 600;
    color: #f5f5f0;
    line-height: 1.25;
    white-space: normal;
}
.tarjeta-valor.ok { color: #a9d1ae; }
.tarjeta-valor.alerta { color: #e09a9a; }
.tarjeta-detalle {
    font-size: 0.78rem;
    color: #9c968c;
    margin-top: 6px;
}

/* Paneles de dictamen */
.panel {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    padding: 22px 26px;
    margin: 14px 0;
}
.panel p, .panel li { color: #e0dbd0; line-height: 1.6; }
.panel-confirmable { border: 1px solid #c5a059; border-left: 5px solid #7fae86; }
.panel-bloqueado   { border: 1px solid #5a2e2e; border-left: 5px solid #b85c5c; }
.panel-incompleto  { border: 1px solid #c5a059; border-left: 5px solid #c5a059; }
.panel-neutro      { border-left: 3px solid #c5a059; }
.etiqueta {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c5a059;
    margin-bottom: 6px;
}
.titular-dictamen {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: #f5f5f0;
    margin: 0 0 8px 0;
}
.destacado { color: #c5a059; font-weight: 600; }

/* Tarjetas fotográficas */
.foto-card {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    overflow: hidden;
    height: 100%;
}
.foto-card .foto {
    height: 180px;
    background-color: #1d1d1d;
    background-size: cover;
    background-position: center;
    border-bottom: 1px solid #c5a059;
}
.foto-card .cuerpo { padding: 18px 20px; }
.foto-card .cuerpo h4 { margin: 0 0 8px 0; font-size: 1.35rem; }
.foto-card .cuerpo p { margin: 3px 0; font-size: 0.86rem; color: #cfcac0; }

/* Tablas operativas */
.tabla-contenedor { overflow-x: auto; margin: 10px 0 24px 0; }
table.tabla-lj {
    width: 100%;
    border-collapse: collapse;
    background-color: #141414;
    border: 1px solid #2a2a2a;
    font-size: 0.82rem;
}
table.tabla-lj th {
    background-color: #1a1a1a;
    color: #c5a059;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.7rem;
    font-weight: 600;
    text-align: left;
    padding: 12px 12px;
    border-bottom: 1px solid #c5a059;
}
table.tabla-lj td {
    color: #e0dbd0;
    padding: 10px 12px;
    border-bottom: 1px solid #232323;
    vertical-align: top;
}
table.tabla-lj tr:hover td { background-color: #181818; }
.txt-ok { color: #a9d1ae; }
.txt-alerta { color: #e09a9a; }
.txt-aviso { color: #d9bf85; }
hr { border-color: #2a2a2a !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# ESPACIO DE NOMBRES, BLOQUE TTL COMPLETO Y DICCIONARIO DE TIPOS
# ==============================================================================
cat = Namespace("http://lajoaquina.com/ontologia#")

TTL = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix cat: <http://lajoaquina.com/ontologia#> .

# ---------- 1. CLASES ----------
cat:MC-Evento a owl:Class .
cat:MC-Cena_formal a owl:Class ; rdfs:subClassOf cat:MC-Evento .
cat:MC-Coffee_Break a owl:Class ; rdfs:subClassOf cat:MC-Evento .
cat:MC-Fecha a owl:Class .
cat:MC-Salon a owl:Class .
cat:MC-Salon_propio a owl:Class ; rdfs:subClassOf cat:MC-Salon .
cat:MC-Salon_externo a owl:Class ; rdfs:subClassOf cat:MC-Salon .
cat:MC-Insumo a owl:Class .
cat:MC-Insumo_Frio a owl:Class ; rdfs:subClassOf cat:MC-Insumo .
cat:MC-Insumo_Almacenable a owl:Class ; rdfs:subClassOf cat:MC-Insumo .
cat:MC-Bebida a owl:Class ; rdfs:subClassOf cat:MC-Insumo .
cat:MC-Cerveza a owl:Class ; rdfs:subClassOf cat:MC-Bebida .
cat:MC-Gaseosa a owl:Class ; rdfs:subClassOf cat:MC-Bebida .
cat:MC-Proveedor a owl:Class .
cat:MC-Proveedor_Nivel_1 a owl:Class ; rdfs:subClassOf cat:MC-Proveedor .
cat:MC-Proveedor_Nivel_2 a owl:Class ; rdfs:subClassOf cat:MC-Proveedor .
cat:MC-Proveedor_Nivel_3 a owl:Class ; rdfs:subClassOf cat:MC-Proveedor .
cat:MC-Personal a owl:Class .
cat:MC-Personal_Cocina a owl:Class ; rdfs:subClassOf cat:MC-Personal .
cat:MC-Personal_Salon a owl:Class ; rdfs:subClassOf cat:MC-Personal .
cat:MC-Mozo_Experimentado a owl:Class ; rdfs:subClassOf cat:MC-Personal_Salon .
cat:MC-Mozo_Novato a owl:Class ; rdfs:subClassOf cat:MC-Personal_Salon .
cat:MC-Personal_Apoyo a owl:Class ; rdfs:subClassOf cat:MC-Personal .

cat:MC-Cena_formal owl:disjointWith cat:MC-Coffee_Break .
cat:MC-Salon_propio owl:disjointWith cat:MC-Salon_externo .
cat:MC-Insumo_Frio owl:disjointWith cat:MC-Insumo_Almacenable .
cat:MC-Mozo_Experimentado owl:disjointWith cat:MC-Mozo_Novato .

# Todo evento debe tener al menos un lugar asignado (restricción OWL)
cat:MC-Evento rdfs:subClassOf [ a owl:Restriction ; owl:onProperty cat:lugar_asignado ;
    owl:minCardinality "1"^^xsd:nonNegativeInteger ] .

# ---------- 2. PROPIEDADES DE OBJETO ----------
cat:fecha_evento a owl:ObjectProperty, owl:FunctionalProperty ; rdfs:domain cat:MC-Evento ; rdfs:range cat:MC-Fecha .
cat:lugar_asignado a owl:ObjectProperty, owl:FunctionalProperty ; rdfs:domain cat:MC-Evento ; rdfs:range cat:MC-Salon .
cat:salon_respaldo_de a owl:ObjectProperty, owl:TransitiveProperty ; rdfs:domain cat:MC-Salon_externo ; rdfs:range cat:MC-Salon_externo .
cat:tiene_salon_respaldo a owl:ObjectProperty ; owl:inverseOf cat:salon_respaldo_de .
cat:provisto_por a owl:ObjectProperty, owl:FunctionalProperty ; rdfs:domain cat:MC-Insumo ; rdfs:range cat:MC-Proveedor .
cat:plan_suplente_de a owl:ObjectProperty, owl:TransitiveProperty ; rdfs:domain cat:MC-Proveedor ; rdfs:range cat:MC-Proveedor .
cat:tiene_suplente a owl:ObjectProperty ; owl:inverseOf cat:plan_suplente_de .
cat:cubre_baja_de a owl:ObjectProperty ; rdfs:domain cat:MC-Personal ; rdfs:range cat:MC-Personal .
cat:asignado_a a owl:ObjectProperty ; rdfs:domain cat:MC-Personal ; rdfs:range cat:MC-Evento .

# ---------- 3. EVENTOS Y FECHA ----------
cat:MI-Fecha_Sabado a cat:MC-Fecha ; cat:dia 17 ; cat:mes "Octubre" ; cat:año 2026 ; cat:ambiente "Frio" .

cat:MI-Casamiento_256 a cat:MC-Cena_formal ;
    cat:cliente "Familia Flores" ; cat:cant_adultos 200 ; cat:cant_niños 30 ;
    cat:presupuesto "cerrado" ; cat:plato_principal "Asado" ; cat:menu_infantil "Hamburguesas" ;
    cat:mesa_dulce true ; cat:servicio_niñera true ; cat:transporte true ;
    cat:ambientacion_y_DJ true ; cat:hielo false ;
    cat:fecha_evento cat:MI-Fecha_Sabado ; cat:lugar_asignado cat:MI-Salon_Labarta .

cat:MI-Coffee_Ministerio a cat:MC-Coffee_Break ;
    cat:cliente "Min. de Salud" ; cat:cant_adultos 80 ; cat:insumo_panaderia "Medialunas" .

# ---------- 4. SALONES ----------
cat:MI-Salon_Soc_Española a cat:MC-Salon_propio ;
    cat:nombre_lugar "Salon 1 Sociedad Española" ; cat:capacidad_max 250 ;
    cat:estado_baños "Aprobado" ; cat:requiere_inspeccion false ;
    cat:cocina_equipada true ; cat:habilitaciones "Vigentes" .

cat:MI-Salon_Labarta a cat:MC-Salon_externo ;
    cat:nombre_lugar "Labarta" ; cat:capacidad_max 400 ; cat:estado_baños "Aprobado" ;
    cat:tipo_espacio "Cerrado" ; cat:tiene_cocina true ; cat:suministro_gas "Red" ; cat:llevar "Solo_Insumos" ;
    cat:permiso_bomberos "Vigente" ; cat:habilitacion_municipal "Aprobada" ; cat:permiso_policial "Aprobado" .
cat:MI-Salon_Borus a cat:MC-Salon_externo ;
    cat:nombre_lugar "Borus" ; cat:capacidad_max 80 ; cat:estado_baños "Aprobado" ;
    cat:tipo_espacio "Cerrado" ; cat:tiene_cocina false ; cat:suministro_gas "Sin_Gas" ; cat:llevar "Insumos_Garrafa" ;
    cat:permiso_bomberos "Vigente" ; cat:habilitacion_municipal "Aprobada" ; cat:permiso_policial "Aprobado" ;
    cat:salon_respaldo_de cat:MI-Salon_Labarta .
cat:MI-Salon_Fed_Gaucha a cat:MC-Salon_externo ;
    cat:nombre_lugar "Fed_Gaucha" ; cat:capacidad_max 600 ; cat:estado_baños "Aprobado" ;
    cat:tipo_espacio "Abierto_Con_Carpa" ; cat:tiene_cocina true ; cat:suministro_gas "Red" ; cat:llevar "Solo_Insumos" ;
    cat:permiso_bomberos "Vigente" ; cat:habilitacion_municipal "Aprobada" ; cat:permiso_policial "Aprobado" ;
    cat:salon_respaldo_de cat:MI-Salon_Borus .
cat:MI-Salon_Uta a cat:MC-Salon_externo ;
    cat:nombre_lugar "Uta" ; cat:capacidad_max 400 ; cat:estado_baños "Aprobado" ;
    cat:tipo_espacio "Cerrado" ; cat:tiene_cocina true ; cat:suministro_gas "Red" ; cat:llevar "Solo_Insumos" ;
    cat:permiso_bomberos "Vigente" ; cat:habilitacion_municipal "Aprobada" ; cat:permiso_policial "Aprobado" ;
    cat:salon_respaldo_de cat:MI-Salon_Fed_Gaucha .
cat:MI-Salon_Biofal a cat:MC-Salon_externo ;
    cat:nombre_lugar "Biofal" ; cat:capacidad_max 200 ; cat:estado_baños "Aprobado" ;
    cat:tipo_espacio "Cerrado" ; cat:tiene_cocina true ; cat:suministro_gas "Red" ; cat:llevar "Solo_Insumos" ;
    cat:permiso_bomberos "Vigente" ; cat:habilitacion_municipal "Aprobada" ; cat:permiso_policial "Aprobado" ;
    cat:salon_respaldo_de cat:MI-Salon_Uta .

# ---------- 5. PROVEEDORES ----------
cat:MI-Proveedor_A a cat:MC-Proveedor_Nivel_1 ; cat:razon_social "Proveedor A" ; cat:ubicacion "Jujuy" ;
    cat:tipo "Mayorista" ; cat:rol "Plan_A" ; cat:estado_entrega "OK" .
cat:MI-Proveedor_B a cat:MC-Proveedor_Nivel_1 ; cat:razon_social "Proveedor B" ; cat:ubicacion "Salta" ;
    cat:tipo "Mayorista" ; cat:rol "Plan_B" ; cat:estado_entrega "OK" ; cat:plan_suplente_de cat:MI-Proveedor_A .
cat:MI-Proveedor_C a cat:MC-Proveedor_Nivel_1 ; cat:razon_social "Proveedor C" ; cat:ubicacion "Buenos Aires" ;
    cat:tipo "Mayorista" ; cat:rol "Plan_C" ; cat:estado_entrega "OK" ; cat:plan_suplente_de cat:MI-Proveedor_B .
cat:MI-Proveedor_D a cat:MC-Proveedor_Nivel_2 ; cat:razon_social "Proveedor D" ; cat:ubicacion "Jujuy" ;
    cat:tipo "Mayorista" ; cat:rol "Plan_A" ; cat:estado_entrega "OK" .
cat:MI-Proveedor_E a cat:MC-Proveedor_Nivel_2 ; cat:razon_social "Proveedor E" ; cat:ubicacion "Jujuy" ;
    cat:tipo "Mayorista" ; cat:rol "Plan_B" ; cat:estado_entrega "OK" ; cat:plan_suplente_de cat:MI-Proveedor_D .
cat:MI-Proveedor_F a cat:MC-Proveedor_Nivel_3 ; cat:razon_social "Proveedor F" ; cat:ubicacion "Jujuy" ;
    cat:tipo "Mayorista" ; cat:rol "Plan_A" ; cat:estado_entrega "OK" .

# ---------- 6. INSUMOS ----------
cat:MI-Carne_Vacuna a cat:MC-Insumo_Frio ; cat:nombre_insumo "Cortes Asado y Embutidos" ; cat:subtipo "Carne_Asado" ;
    cat:cant_base_calculada 150.0 ; cat:insumos_extra 0.0 ; cat:cant_total 150.0 ; cat:unidad "kg" ; cat:provisto_por cat:MI-Proveedor_A .
cat:MI-Lomo a cat:MC-Insumo_Frio ; cat:nombre_insumo "Lomo" ; cat:subtipo "Lomo" ;
    cat:cant_base_por_persona 0.480 ; cat:insumos_extra 0.0 ; cat:unidad "kg" ; cat:provisto_por cat:MI-Proveedor_A .
cat:MI-Mariscos a cat:MC-Insumo_Frio ; cat:nombre_insumo "Mariscos" ; cat:subtipo "Marisco" ;
    cat:cant_base_por_persona 0.500 ; cat:insumos_extra 0.0 ; cat:unidad "kg" ; cat:provisto_por cat:MI-Proveedor_A .
cat:MI-Pollo a cat:MC-Insumo_Frio ; cat:nombre_insumo "Pollo" ; cat:subtipo "Pollo" ;
    cat:cant_base_por_persona 0.400 ; cat:insumos_extra 0.0 ; cat:unidad "kg" ; cat:provisto_por cat:MI-Proveedor_A .
cat:MI-Lacteos a cat:MC-Insumo_Frio ; cat:nombre_insumo "Lácteos" ; cat:subtipo "Lacteo" ;
    cat:cant_base_por_persona 0.300 ; cat:insumos_extra 0.0 ; cat:unidad "kg" ; cat:provisto_por cat:MI-Proveedor_A .

cat:MI-Bolsa_Papa a cat:MC-Insumo_Almacenable ; cat:nombre_insumo "Papa Blanca" ; cat:subtipo "Verdura" ;
    cat:cant_base_calculada 8.0 ; cat:insumos_extra 2.0 ; cat:cant_total 10.0 ; cat:unidad "bolsas" ; cat:provisto_por cat:MI-Proveedor_D .
cat:MI-Tomate a cat:MC-Insumo_Almacenable ; cat:nombre_insumo "Tomate" ; cat:subtipo "Verdura" ; cat:provisto_por cat:MI-Proveedor_D .
cat:MI-Cebolla a cat:MC-Insumo_Almacenable ; cat:nombre_insumo "Cebolla" ; cat:subtipo "Verdura" ; cat:provisto_por cat:MI-Proveedor_D .
cat:MI-Perejil a cat:MC-Insumo_Almacenable ; cat:nombre_insumo "Perejil" ; cat:subtipo "Verdura" ; cat:provisto_por cat:MI-Proveedor_D .
cat:MI-Harina a cat:MC-Insumo_Almacenable ; cat:nombre_insumo "Harina" ; cat:subtipo "Panaderia" .

# ---------- 7. BEBIDAS ----------
cat:MI-Cerveza a cat:MC-Cerveza ; cat:nombre_insumo "Cerveza" ; cat:regimen_compra "Mayorista" ;
    cat:cant_base_calculada 200.0 ; cat:insumos_extra 80.0 ; cat:cant_total 280.0 ; cat:unidad "L" ; cat:provisto_por cat:MI-Proveedor_D .
cat:MI-Hielo a cat:MC-Bebida ; cat:nombre_insumo "Hielo" ; cat:subtipo "Hielo" ; cat:regimen_compra "Mayorista" ; cat:provisto_por cat:MI-Proveedor_D .
cat:MI-Cerveza_Heineken a cat:MC-Cerveza ; cat:nombre_marca "Heineken" ; cat:pais_origen "Paises Bajos" ; cat:estilo "Pale Lager" .
cat:MI-Cerveza_Quilmes a cat:MC-Cerveza ; cat:nombre_marca "Quilmes" ; cat:pais_origen "Argentina" ; cat:estilo "Pilsner" .
cat:MI-Cerveza_Stella_Artois a cat:MC-Cerveza ; cat:nombre_marca "Stella Artois" ; cat:pais_origen "Bélgica" ; cat:estilo "Pilsner" .
cat:MI-Cerveza_Corona a cat:MC-Cerveza ; cat:nombre_marca "Corona" ; cat:pais_origen "México" ; cat:estilo "Pale Lager" .
cat:MI-Cerveza_Patagonia_Amber_Lager a cat:MC-Cerveza ; cat:nombre_marca "Patagonia Amber Lager" ; cat:pais_origen "Argentina" ; cat:estilo "Amber Lager" .
cat:MI-Gaseosa_CocaCola a cat:MC-Gaseosa ; cat:nombre_marca "Coca Cola" ; cat:pais_origen "Estados Unidos" ; cat:sabor "Cola" ; cat:contiene_gas true .
cat:MI-Gaseosa_Pepsi a cat:MC-Gaseosa ; cat:nombre_marca "Pepsi" ; cat:pais_origen "Estados Unidos" ; cat:sabor "Cola" ; cat:contiene_gas true .
cat:MI-Gaseosa_Aquarius a cat:MC-Gaseosa ; cat:nombre_marca "Aquarius" ; cat:pais_origen "Japón" ; cat:sabor "Frutal" ; cat:contiene_gas false .
cat:MI-Gaseosa_Benedictino a cat:MC-Gaseosa ; cat:nombre_marca "Benedictino" ; cat:pais_origen "Chile" ; cat:sabor "Sin sabor" ;
    rdfs:comment "Contiene gas: segun variedad" .

# ---------- 8. PERSONAL (ejemplos) ----------
cat:MI-Cocinero_Jefe a cat:MC-Personal_Cocina ; rdfs:label "Jefe de cocina" ; cat:funcion "Jefatura de cocina" ; cat:asignado_a cat:MI-Casamiento_256 .
cat:MI-Mozo_Exp_1 a cat:MC-Mozo_Experimentado ; rdfs:label "Mozo experimentado 1" ; cat:asignado_a cat:MI-Casamiento_256 .
cat:MI-Mozo_Nov_1 a cat:MC-Mozo_Novato ; rdfs:label "Mozo novato 1" ; cat:asignado_a cat:MI-Casamiento_256 .
cat:MI-Ninera_1 a cat:MC-Personal_Apoyo ; rdfs:label "Niñera 1" ; cat:funcion "Niñera" ; cat:asignado_a cat:MI-Casamiento_256 .
cat:MI-DJ_1 a cat:MC-Personal_Apoyo ; rdfs:label "DJ 1" ; cat:funcion "DJ" ; cat:asignado_a cat:MI-Casamiento_256 .
cat:MI-Apoyo_Urgencia_1 a cat:MC-Personal_Apoyo ; rdfs:label "Mozo de urgencia 1" ; cat:funcion "Cobertura de baja" ;
    cat:cubre_baja_de cat:MI-Mozo_Exp_1 .

# ---------- 9. VALORES POR DEFECTO DE LAS CLASES (herencia de marcos) ----------
cat:MC-Cena_formal cat:modalidad "Cena" ; cat:degustacion "30_Dias_Antes" .
cat:MC-Coffee_Break cat:modalidad "Coffee" ; cat:control_insumos "Obligatorio" ; cat:hora_llegada "2hs_antes" .
cat:MC-Salon_propio cat:sede "Propia" .
cat:MC-Salon_externo cat:sede "Externa" ; cat:inspeccion_tecnica "Obligatoria" ; cat:plazo_reubicacion_horas 48 .
cat:MC-Insumo_Frio cat:conservacion "Frio_critico" ; cat:momento_pago "7_Dias_Antes" ; cat:momento_retiro "Mismo_Dia_Evento" .
cat:MC-Insumo_Almacenable cat:conservacion "Almacenable" ; cat:momento_compra "A_definir" .
cat:MC-Bebida cat:rubro "Bebida" ; cat:validado_por "Bartender" .
cat:MC-Cerveza cat:subtipo "Alcohol" .
cat:MC-Gaseosa cat:subtipo "Gaseosa" .
cat:MC-Proveedor cat:confirmacion_final "7_Dias_Antes_Por_Telefono" .
cat:MC-Proveedor_Nivel_1 cat:prioridad_contacto "Nivel_1" ; cat:rubro "Carnes_Pescado_Marisco_Lacteos" ;
    cat:orden_reserva "Inmediato" ; cat:exige_cadena_frio "Estricto" .
cat:MC-Proveedor_Nivel_2 cat:prioridad_contacto "Nivel_2" ; cat:rubro "Verduras_Bebida_Hielo" ; cat:orden_reserva "Estandar" .
cat:MC-Proveedor_Nivel_3 cat:prioridad_contacto "Nivel_3" ; cat:rubro "Carpas_Sonido_Transporte" ; cat:orden_reserva "Segun_Salon" .
cat:MC-Personal_Salon cat:ratio_comensales_por_mozo 25 .
cat:MC-Mozo_Experimentado cat:tareas "Platos_calientes" .
cat:MC-Mozo_Novato cat:tareas "Reposicion_basica" .
"""

TIPOS = {
    XSD.string: "cliente modalidad presupuesto degustacion plato_principal menu_infantil insumo_panaderia control_insumos hora_llegada mes ambiente nombre_lugar sede estado_baños inspeccion_tecnica tipo_espacio suministro_gas llevar permiso_bomberos habilitacion_municipal permiso_policial habilitaciones nombre_insumo subtipo conservacion momento_pago momento_retiro momento_compra unidad regimen_compra rubro validado_por nombre_marca pais_origen estilo sabor razon_social ubicacion tipo rol estado_entrega confirmacion_final prioridad_contacto orden_reserva exige_cadena_frio funcion tareas",
    XSD.integer: "cant_adultos cant_niños dia año capacidad_max plazo_reubicacion_horas ratio_comensales_por_mozo mozos_requeridos",
    XSD.decimal: "cant_base_calculada cant_base_por_persona insumos_extra cant_total",
    XSD.boolean: "mesa_dulce servicio_niñera transporte ambientacion_y_DJ hielo tiene_cocina cocina_equipada requiere_inspeccion contiene_gas",
}

PROPIEDADES_INFERIDAS = [
    "capacidad_salon",
    "estado_habilitacion",
    "estado_evento",
    "estado_compra",
    "activo_como",
    "estado_alerta",
    "mozos_requeridos",
]

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

# ==============================================================================
# FUNCIONES DEL SISTEMA BASADO EN CONOCIMIENTO (TERCER MODELO)
# ==============================================================================
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


def heredar(ind, prop, grafo=None):
    """Valor propio de la instancia o, si no lo tiene, el de su clase o superclase."""
    g_ref = grafo if grafo is not None else st.session_state.g
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
    st.session_state.bitacora_inferencia = bitacora
    return bitacora


def proveedor_activo(p, grafo=None):
    """Recorre la cadena plan_suplente_de hasta hallar un proveedor con entrega OK."""
    g_ref = grafo if grafo is not None else st.session_state.g
    while str(g_ref.value(p, cat.estado_entrega)) != "OK":
        p = g_ref.value(predicate=cat.plan_suplente_de, object=p)
        if p is None:
            return None
    return p


def salon_alternativo(evento, grafo=None):
    """Reubicación de emergencia (48 hs) recorriendo la cadena salon_respaldo_de."""
    g_ref = grafo if grafo is not None else st.session_state.g
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


# ==============================================================================
# CATÁLOGOS DE PRESENTACIÓN (SIN JERGA TÉCNICA)
# ==============================================================================
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

TXT_CONSERVACION = {"Frio_critico": "Frío crítico", "Almacenable": "Almacenable"}
TXT_PAGO = {"7_Dias_Antes": "7 días antes", "A_definir": "A definir con el proveedor"}
TXT_RETIRO = {"Mismo_Dia_Evento": "Mismo día del evento"}
TXT_LLEVAR = {
    "Solo_Insumos": "Solo insumos gastronómicos",
    "Insumos_Garrafa": "Insumos, garrafas y hornos móviles",
    "Completo": "Equipamiento de cocina completo, garrafas e insumos",
}

IMG_HERO = "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=1600&q=80"
IMG_ASADO = "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80"
IMG_PANADERIA = "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80"
IMG_BEBIDAS = "https://images.unsplash.com/photo-1470337458703-46ad1756a187?auto=format&fit=crop&w=900&q=80"
IMG_SALON = "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=900&q=80"


# ==============================================================================
# UTILIDADES DE INTERFAZ Y DE ESCRITURA EN EL GRAFO
# ==============================================================================
def esc(texto):
    return html_lib.escape(str(texto))


def render_html(fragmento):
    """Compacta el HTML en una sola línea para que Markdown no lo trate como código."""
    st.markdown(" ".join(l.strip() for l in fragmento.splitlines() if l.strip()), unsafe_allow_html=True)


def tabla_html(columnas, filas):
    cab = "".join(f"<th>{c}</th>" for c in columnas)
    cuerpo = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in fila) + "</tr>" for fila in filas)
    render_html(f'<div class="tabla-contenedor"><table class="tabla-lj"><thead><tr>{cab}</tr></thead><tbody>{cuerpo}</tbody></table></div>')


def tarjeta(titulo, valor, detalle="", estado=""):
    return (
        f'<div class="tarjeta-resumen"><div class="tarjeta-titulo">{titulo}</div>'
        f'<div class="tarjeta-valor {estado}">{valor}</div>'
        f'<div class="tarjeta-detalle">{detalle}</div></div>'
    )


def set_txt(grafo, s, p, valor):
    # Literal simple (sin datatype explícito) para que coincida con los literales del TTL
    # y con los patrones de las reglas SPARQL (ej. cat:estado_baños "Aprobado").
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


def init_key(clave, valor):
    if clave not in st.session_state:
        st.session_state[clave] = valor


# ==============================================================================
# ESTADO PERSISTENTE
# ==============================================================================
if "g" not in st.session_state:
    st.session_state.g = construir_grafo_inicial()
init_key("eventos_ids", ["MI-Casamiento_256", "MI-Coffee_Ministerio"])
init_key("evento_activo", "MI-Casamiento_256")
init_key("modo_alta", False)

g = st.session_state.g


# ==============================================================================
# CALLBACKS (se ejecutan antes de redibujar la página)
# ==============================================================================
def cb_restaurar():
    for clave in list(st.session_state.keys()):
        del st.session_state[clave]


def cb_abrir_alta():
    st.session_state.modo_alta = True


def cb_cancelar_alta():
    st.session_state.modo_alta = False


def cb_confirmar_alta():
    grafo = st.session_state.g
    nombre = (st.session_state.get("alta_cliente") or "").strip() or "Nuevo Cliente"
    modalidad = st.session_state.get("alta_modalidad", "Cena Formal")
    salon_id = st.session_state.get("alta_salon", "MI-Salon_Labarta")

    slug = re.sub(r"[^A-Za-z0-9]+", "_", nombre).strip("_") or "Cliente"
    nuevo_id, i = f"MI-Evento_{slug}", 2
    while nuevo_id in st.session_state.eventos_ids:
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

    st.session_state.eventos_ids.append(nuevo_id)
    st.session_state.evento_activo = nuevo_id
    st.session_state.modo_alta = False
    limpiar_inferencias(grafo)
    motor_inferencia(grafo, base_de_reglas)


def cb_reasignar_salon(evento_id, salon_id):
    st.session_state[f"{evento_id}__salon"] = salon_id
    st.session_state[f"{evento_id}__electrico"] = "Normal"
    st.session_state.g.set((cat[evento_id], cat.lugar_asignado, cat[salon_id]))


# ==============================================================================
# BARRA LATERAL: GESTIÓN DE EVENTOS
# ==============================================================================
with st.sidebar:
    render_html('<div class="marca-sidebar">La Joaquina</div><div class="marca-sidebar-sub">Panel del Organizador</div>')

    st.button("CREAR NUEVO EVENTO", width="stretch", on_click=cb_abrir_alta)
    st.button("RESTAURAR VALORES INICIALES", width="stretch", on_click=cb_restaurar)

    if st.session_state.modo_alta:
        render_html('<div class="rotulo-seccion">Alta de nuevo evento</div>')
        st.text_input("Nombre del Cliente", value="Familia López", key="alta_cliente")
        st.selectbox("Modalidad", ["Cena Formal", "Coffee Break"], key="alta_modalidad")
        st.selectbox(
            "Salón inicial",
            [k for k in SALONES if k != SIN_SALON],
            format_func=lambda k: SALONES[k],
            key="alta_salon",
        )
        st.button("CONFIRMAR ALTA DEL EVENTO", width="stretch", on_click=cb_confirmar_alta)
        st.button("CANCELAR", width="stretch", on_click=cb_cancelar_alta)

    render_html('<div class="rotulo-seccion">Evento activo</div>')

    def etiqueta_evento(eid):
        u = cat[eid]
        modalidad = "Coffee Break" if (u, RDF.type, cat["MC-Coffee_Break"]) in g else "Cena Formal"
        return f"{g.value(u, cat.cliente)} — {modalidad}"

    if st.session_state.evento_activo not in st.session_state.eventos_ids:
        st.session_state.evento_activo = st.session_state.eventos_ids[0]
    E = st.selectbox(
        "Evento Activo",
        st.session_state.eventos_ids,
        format_func=etiqueta_evento,
        key="evento_activo",
        label_visibility="collapsed",
    )
    ev_uri = cat[E]
    k = lambda nombre: f"{E}__{nombre}"

    # ---------- Inicialización de controles a partir del grafo ----------
    fecha_uri = g.value(ev_uri, cat.fecha_evento)
    salon_uri_g = g.value(ev_uri, cat.lugar_asignado)
    mes_g = str(g.value(fecha_uri, cat.mes)) if fecha_uri else "Octubre"

    init_key(k("cliente"), str(g.value(ev_uri, cat.cliente) or ""))
    init_key(k("modalidad"), "Coffee Break" if (ev_uri, RDF.type, cat["MC-Coffee_Break"]) in g else "Cena Formal")
    init_key(k("dia"), int(g.value(fecha_uri, cat.dia) or 17) if fecha_uri else 17)
    init_key(k("mes"), mes_g if mes_g in MESES else "Octubre")
    init_key(k("anio"), int(g.value(fecha_uri, cat["año"]) or 2026) if fecha_uri else 2026)
    init_key(k("clima"), "Calor" if fecha_uri is not None and str(g.value(fecha_uri, cat.ambiente)) == "Calor" else "Frío")
    init_key(k("salon"), fv(salon_uri_g) if salon_uri_g is not None and fv(salon_uri_g) in SALONES else SIN_SALON)
    init_key(k("electrico"), "Normal")
    init_key(k("adultos"), int(g.value(ev_uri, cat.cant_adultos) or 100))
    init_key(k("ninos"), int(g.value(ev_uri, cat["cant_niños"]) or 0))
    init_key(k("presupuesto"), "Abierto" if str(g.value(ev_uri, cat.presupuesto)).lower() == "abierto" else "Cerrado")
    plato_g = str(g.value(ev_uri, cat.plato_principal) or "Asado")
    init_key(k("plato"), plato_g if plato_g in PLATOS else "Asado")
    infantil_g = str(g.value(ev_uri, cat.menu_infantil) or "Hamburguesas")
    init_key(k("infantil"), infantil_g if infantil_g in ["Hamburguesas", "Milanesas", "Nuggets"] else "Hamburguesas")
    pan_g = str(g.value(ev_uri, cat.insumo_panaderia) or "Medialunas")
    init_key(k("panaderia"), pan_g if pan_g in ["Medialunas", "Pastelitos", "Buñuelos"] else "Medialunas")
    init_key(k("mesa_dulce"), "Sí" if bool(g.value(ev_uri, cat.mesa_dulce)) else "No")
    init_key(k("cerveza"), "Quilmes")
    init_key(k("gaseosa"), "Coca Cola")
    init_key(k("ninera"), bool(g.value(ev_uri, cat["servicio_niñera"])))
    init_key(k("transporte"), bool(g.value(ev_uri, cat.transporte)))
    init_key(k("dj"), bool(g.value(ev_uri, cat.ambientacion_y_DJ)))
    init_key(k("bajas"), 0)
    init_key(k("jefa"), "Disponible")
    init_key("extra_papa", float(g.value(cat["MI-Bolsa_Papa"], cat.insumos_extra) or 0.0))
    init_key("extra_cerveza", float(g.value(cat["MI-Cerveza"], cat.insumos_extra) or 0.0))
    for pid in PROVEEDORES:
        estado_g = str(g.value(cat[pid], cat.estado_entrega) or "OK")
        init_key(f"prov__{pid}", estado_g if estado_g in ESTADOS_ENTREGA else "OK")

    # ---------- 1. Datos del Evento y Fecha ----------
    with st.expander("1. Datos del Evento y Fecha", expanded=True):
        st.text_input("Cliente", key=k("cliente"))
        st.selectbox("Modalidad", ["Cena Formal", "Coffee Break"], key=k("modalidad"))
        c1, c2 = st.columns([1, 2])
        with c1:
            st.number_input("Día", min_value=1, max_value=31, step=1, key=k("dia"))
        with c2:
            st.selectbox("Mes", MESES, key=k("mes"))
        c3, c4 = st.columns(2)
        with c3:
            st.number_input("Año", min_value=2025, max_value=2030, step=1, key=k("anio"))
        with c4:
            st.selectbox("Clima previsto", ["Frío", "Calor"], key=k("clima"))

    # ---------- 2. Salón ----------
    with st.expander("2. Salón", expanded=False):
        st.selectbox(
            "Salón asignado",
            list(SALONES.keys()),
            format_func=lambda s: SALONES[s] if s == SIN_SALON
            else f"{SALONES[s]} ({g.value(cat[s], cat.capacidad_max)} personas)",
            key=k("salon"),
        )
        salon_id = st.session_state[k("salon")]
        if salon_id != SIN_SALON:
            s_uri = cat[salon_id]
            es_externo = (s_uri, RDF.type, cat["MC-Salon_externo"]) in g
            sk = lambda nombre: f"salon__{salon_id}__{nombre}"
            init_key(sk("banos"), str(g.value(s_uri, cat["estado_baños"]) or "Aprobado"))
            st.selectbox("Estado de Baños", ["Aprobado", "No aprobado"], key=sk("banos"))
            if es_externo:
                init_key(sk("bomberos"), str(g.value(s_uri, cat.permiso_bomberos) or "Vigente"))
                init_key(sk("municipal"), str(g.value(s_uri, cat.habilitacion_municipal) or "Aprobada"))
                init_key(sk("policial"), str(g.value(s_uri, cat.permiso_policial) or "Aprobado"))
                st.selectbox("Permiso de Bomberos", ["Vigente", "Vencido"], key=sk("bomberos"))
                st.selectbox("Habilitación Municipal", ["Aprobada", "Pendiente"], key=sk("municipal"))
                st.selectbox("Permiso Policial", list(ESTADOS_POLICIAL.keys()),
                             format_func=lambda x: ESTADOS_POLICIAL[x], key=sk("policial"))
            else:
                init_key(sk("habilitaciones"), str(g.value(s_uri, cat.habilitaciones) or "Vigentes"))
                st.selectbox("Habilitaciones de la sede propia", ["Vigentes", "Vencidas"], key=sk("habilitaciones"))
            st.selectbox("Suministro Eléctrico", ["Normal", "Cortocircuito a 48 hs"], key=k("electrico"))

    # ---------- 3. Invitados ----------
    with st.expander("3. Invitados", expanded=False):
        st.number_input("Cantidad de Adultos", min_value=1, max_value=700, step=5, key=k("adultos"))
        st.number_input("Cantidad de Niños", min_value=0, max_value=200, step=1, key=k("ninos"))
        st.selectbox("Presupuesto", ["Cerrado", "Abierto"], key=k("presupuesto"))

    # ---------- 4. Menú y Bebidas ----------
    with st.expander("4. Menú y Bebidas", expanded=False):
        if st.session_state[k("modalidad")] == "Cena Formal":
            st.selectbox("Plato Principal", list(PLATOS.keys()), key=k("plato"))
            st.selectbox("Menú Infantil", ["Hamburguesas", "Milanesas", "Nuggets"], key=k("infantil"))
            st.selectbox("Mesa Dulce", ["Sí", "No"], key=k("mesa_dulce"))
        else:
            st.selectbox("Panadería", ["Medialunas", "Pastelitos", "Buñuelos"], key=k("panaderia"))
        st.selectbox("Marca de Cerveza", list(CERVEZAS.keys()), key=k("cerveza"))
        st.selectbox("Marca de Gaseosa", list(GASEOSAS.keys()), key=k("gaseosa"))
        st.number_input("Refuerzo extra de papa (bolsas)", min_value=0.0, max_value=50.0, step=1.0, key="extra_papa")
        st.number_input("Refuerzo extra de cerveza (litros)", min_value=0.0, max_value=500.0, step=10.0, key="extra_cerveza")

    # ---------- 5. Proveedores ----------
    with st.expander("5. Proveedores", expanded=False):
        for pid, etiqueta in PROVEEDORES.items():
            st.selectbox(etiqueta, list(ESTADOS_ENTREGA.keys()),
                         format_func=lambda x: ESTADOS_ENTREGA[x], key=f"prov__{pid}")

    # ---------- 6. Personal y Servicios ----------
    with st.expander("6. Personal y Servicios", expanded=False):
        st.checkbox("Servicio de Niñera", key=k("ninera"))
        st.checkbox("Transporte de Invitados", key=k("transporte"))
        st.checkbox("Ambientación y DJ", key=k("dj"))
        st.number_input("Bajas de mozos titulares a 48 hs", min_value=0, max_value=10, step=1, key=k("bajas"))
        st.selectbox("Estado de la Jefa de Cocina", ["Disponible", "Baja imprevista"], key=k("jefa"))

# ==============================================================================
# LECTURA DE CONTROLES
# ==============================================================================
ss = st.session_state
cliente = ss[k("cliente")].strip() or "Cliente sin nombre"
modalidad = ss[k("modalidad")]
es_cena = modalidad == "Cena Formal"
dia, mes, anio = int(ss[k("dia")]), ss[k("mes")], int(ss[k("anio")])
clima = ss[k("clima")]
ambiente = "Calor" if clima == "Calor" else "Frio"
salon_id = ss[k("salon")]
salon_uri = cat[salon_id] if salon_id != SIN_SALON else None
cortocircuito = salon_uri is not None and ss[k("electrico")] == "Cortocircuito a 48 hs"
adultos, ninos = int(ss[k("adultos")]), int(ss[k("ninos")])
presupuesto = ss[k("presupuesto")]
plato = ss[k("plato")]
infantil = ss[k("infantil")]
panaderia = ss[k("panaderia")]
mesa_dulce = es_cena and ss[k("mesa_dulce")] == "Sí"
marca_cerveza, marca_gaseosa = ss[k("cerveza")], ss[k("gaseosa")]
extra_papa, extra_cerveza = float(ss["extra_papa"]), float(ss["extra_cerveza"])
ninera, transporte, dj = ss[k("ninera")], ss[k("transporte")], ss[k("dj")]
bajas = int(ss[k("bajas")])
jefa_ausente = ss[k("jefa")] == "Baja imprevista"
hielo = ambiente == "Calor"
comensales = adultos + ninos

# ==============================================================================
# ACTUALIZACIÓN DEL GRAFO Y EJECUCIÓN DEL MOTOR (SEGUNDO PLANO)
# ==============================================================================
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
    sk = lambda nombre: f"salon__{salon_id}__{nombre}"
    set_txt(g, salon_uri, cat["estado_baños"], ss[sk("banos")])
    if (salon_uri, RDF.type, cat["MC-Salon_externo"]) in g:
        set_txt(g, salon_uri, cat.permiso_bomberos, ss[sk("bomberos")])
        set_txt(g, salon_uri, cat.habilitacion_municipal, ss[sk("municipal")])
        set_txt(g, salon_uri, cat.permiso_policial, ss[sk("policial")])
    else:
        set_txt(g, salon_uri, cat.habilitaciones, ss[sk("habilitaciones")])
else:
    g.remove((ev_uri, cat.lugar_asignado, None))

for pid in PROVEEDORES:
    set_txt(g, cat[pid], cat.estado_entrega, ss[f"prov__{pid}"])

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
motor_inferencia(g, base_de_reglas)

# ---------- Conclusiones deducidas ----------
estados_evento = set(fv(o) for o in g.objects(ev_uri, cat.estado_evento))
capacidad_estado = g.value(ev_uri, cat.capacidad_salon)
mozos_requeridos = int(g.value(ev_uri, cat.mozos_requeridos) or 0)
salon_externo = salon_uri is not None and (salon_uri, RDF.type, cat["MC-Salon_externo"]) in g
salon_habilitado = salon_uri is not None and g.value(salon_uri, cat.estado_habilitacion) == cat.Habilitado
capacidad_salon = int(g.value(salon_uri, cat.capacidad_max) or 0) if salon_uri is not None else 0
nombre_salon = SALONES[salon_id]


def motivos_legales(s_uri):
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


# ==============================================================================
# HERO BANNER
# ==============================================================================
render_html(f"""
<div style="background: linear-gradient(rgba(8, 8, 8, 0.65), rgba(8, 8, 8, 0.88)), url('{IMG_HERO}'); background-size: cover; background-position: center; padding: 75px 30px; text-align: center; border-bottom: 1px solid #c5a059; margin-bottom: 28px; border-radius: 4px;">
<p style="color: #c5a059; font-family: 'Montserrat', sans-serif; font-size: 0.85rem; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 10px;">Bienvenido a La Joaquina</p>
<h1 style="color: #ffffff; font-family: 'Cormorant Garamond', serif; font-size: 3.4rem; font-weight: 600; margin: 0;">La Joaquina | Eventos gastronómicos</h1>
<p style="color: #d4d4d4; font-family: 'Montserrat', sans-serif; font-size: 0.95rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 12px;">Sistema de Gestión y Orquestación Logística</p>
</div>
""")

tab_eval, tab_plan = st.tabs([
    "Evaluación y Viabilidad del Evento",
    "Planificación de Insumos, Proveedores y Personal",
])

# ==============================================================================
# PESTAÑA 1: EVALUACIÓN Y VIABILIDAD DEL EVENTO
# ==============================================================================
with tab_eval:
    st.markdown(f"### {esc(cliente)} — {modalidad}")
    st.caption(f"{dia} de {mes} de {anio}  |  Clima previsto: {clima}  |  Presupuesto: {presupuesto}  |  Sede: {nombre_salon}")

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
    ratio_mozo = heredar(cat["MI-Mozo_Exp_1"], "ratio_comensales_por_mozo", g)
    t_moz = tarjeta("Mozos Requeridos", f"{mozos_requeridos} mozos", f"Un mozo cada {ratio_mozo} invitados")

    for col, t in zip(st.columns(4), [t_cap, t_moz, t_est, t_hab]):
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
    elif "Confirmable" in estados_evento and not cortocircuito:
        render_html(f"""
<div class="panel panel-confirmable">
<div class="etiqueta">Dictamen del Sistema</div>
<div class="titular-dictamen">Evento confirmable</div>
<p>El evento de <strong>{esc(cliente)}</strong> en <strong>{nombre_salon}</strong> cumple con la capacidad requerida
({comensales} invitados sobre {capacidad_salon} plazas) y el salón tiene sus habilitaciones, permisos y baños en regla.
Puede confirmarse con el cliente.</p>
</div>""")
    else:
        motivos = []
        if capacidad_estado == cat.Insuficiente:
            motivos.append(f"Capacidad insuficiente: {comensales} invitados para {capacidad_salon} plazas disponibles en {nombre_salon}.")
        legales = motivos_legales(salon_uri)
        if legales:
            motivos.append("Riesgo de clausura legal o sanitaria: " + ", ".join(legales) + ".")
        if cortocircuito:
            motivos.append(f"Cortocircuito informado en {nombre_salon} a 48 horas del evento: la cocina y las cámaras de frío no pueden operar.")
        if not motivos:
            motivos.append("Las condiciones del salón aún no fueron verificadas por completo.")
        items = "".join(f"<li>{m}</li>" for m in motivos)
        render_html(f"""
<div class="panel panel-bloqueado">
<div class="etiqueta">Dictamen del Sistema</div>
<div class="titular-dictamen">Bloqueado por riesgo operativo o legal</div>
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
        tarea_exp = str(heredar(cat["MI-Mozo_Exp_1"], "tareas", g)).replace("_", " ")
        tarea_nov = str(heredar(cat["MI-Mozo_Nov_1"], "tareas", g)).replace("_", " ")
        if bajas == 0:
            txt_mozos = f"Plantel titular completo: {mozos_requeridos} mozos experimentados asignados a {tarea_exp.lower()}."
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
        cuerpo_menu = (f"<p>Plato principal: {plato}</p><p>Menú infantil: {infantil}</p>"
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

# ==============================================================================
# PESTAÑA 2: PLANIFICACIÓN DE INSUMOS, PROVEEDORES Y PERSONAL
# ==============================================================================
with tab_plan:
    st.markdown(f"### Planificación de compras — {esc(cliente)}")
    st.caption(f"Cantidades calculadas para {adultos} adultos y {ninos} niños. Las condiciones de conservación, pago y retiro provienen de la categoría de cada insumo.")

    proveedor_bebidas = g.value(cat["MI-Cerveza"], cat.provisto_por)  # Canal mayorista de bebidas
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
