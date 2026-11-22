"""Ontología de La Joaquina: espacio de nombres, bloque Turtle y tipos de datos."""

from rdflib import Namespace
from rdflib.namespace import XSD


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
cat:MI-Fecha_Sabado a cat:MC-Fecha ; cat:dia 17 ; cat:mes "Diciembre" ; cat:año 2026 ; cat:ambiente "Frio" .

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
cat:MI-Proveedor_G a cat:MC-Proveedor_Nivel_2 ; cat:razon_social "Proveedor G" ; cat:ubicacion "Jujuy" ;
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
cat:MI-Harina a cat:MC-Insumo_Almacenable ; cat:nombre_insumo "Harina" ; cat:subtipo "Panaderia" ; cat:provisto_por cat:MI-Proveedor_G .

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
