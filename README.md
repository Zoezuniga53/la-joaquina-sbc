# la-joaquina-sbc

Sistema basado en conocimiento (SBC) para la gestión logística de eventos gastronómicos de **La Joaquina**.
Interfaz en Streamlit; razonamiento con RDF/SPARQL (rdflib).

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```
app.py                      Punto de entrada: conecta frontend y backend
backend/                    Lógica. No importa Streamlit
  ontologia.py              Espacio de nombres, bloque Turtle, tipos de datos
  reglas.py                 Base de reglas SPARQL CONSTRUCT (R1-R9)
  motor.py                  Motor de inferencia, herencia de marcos, proveedor activo, salón alternativo
  catalogos.py              Salones, proveedores, menús, meses y textos de dominio
  grafo.py                  Escritura en el grafo, grafo inicial, alta y reasignación de eventos
  fechas.py                 Regla de fechas: solo se reserva desde el día siguiente a hoy
  modelos.py                ParametrosEvento (entrada) y Analisis (salida)
  servicios.py              analizar_evento(): actualiza el grafo, calcula insumos, corre el motor, evalúa suministros
frontend/                   Presentación (Streamlit)
  estilos.py                Hoja de estilos
  recursos.py               URLs de imágenes
  componentes.py            Banner, tarjetas y tablas HTML
  estado.py                 Estado de sesión y callbacks
  sidebar.py                Barra lateral (controles)
  controles.py              Lee los controles y arma ParametrosEvento
  vista_evaluacion.py       Pestaña "Evaluación y Viabilidad"
  vista_planificacion.py    Pestaña "Planificación de Insumos, Proveedores y Personal"
```

## Flujo de una ejecución

1. `frontend.estado.iniciar_estado()` crea el grafo una sola vez por sesión.
2. `frontend.sidebar.render_sidebar()` dibuja los controles y devuelve el evento activo.
3. `frontend.controles.leer_parametros()` los convierte en un `ParametrosEvento`.
4. `backend.servicios.analizar_evento()` actualiza el grafo, ejecuta el motor y devuelve un `Analisis`.
5. `frontend.vista_*` dibujan los resultados a partir de `ParametrosEvento` y `Analisis`.

## Reglas de la interfaz

- **Fechas:** el selector de fecha solo permite días posteriores a hoy (hasta 2030). Si un evento guardado tiene una fecha que ya pasó, se ajusta al primer día disponible y se avisa.
- **Niñera:** la opción solo aparece si el evento tiene al menos un niño. Con 0 niños no se ofrece ni se cuenta en la brigada.

## Regla de oro

`backend/` no importa `streamlit`. Si necesitás probar una regla o un cálculo, podés hacerlo desde un script de Python común.
