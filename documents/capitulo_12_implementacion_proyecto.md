# Capítulo 12. Implementación del proyecto

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 12.1. Estructura de directorios

La implementación sigue una estructura clara:

```text
src/omie_price_nn/
documents/
data/
models/
```

El código fuente vive en `src/omie_price_nn/`. La documentación del TFG se almacena en `documents/`. Los datos descargados y procesados se guardan en `data/`. Los modelos y gráficas se guardan en `models/`.

Esta separación evita mezclar código, datos, documentación y artefactos.

El directorio `src/` contiene el paquete instalable. El directorio `documents/` contiene la memoria del TFG y los resúmenes del desarrollo. Los directorios `data/` y `models/` se consideran artefactos locales generados durante la ejecución, por lo que están excluidos del repositorio.

### 12.2. Módulo de descarga y parseo de OMIE

El módulo `data.py` implementa la descarga de ficheros `MARGINALPDBC`. Genera nombres diarios como `marginalpdbc_YYYYMMDD.1`, solicita el fichero a OMIE y lo guarda en `data/raw/`.

El parser descarta cabeceras y comentarios, separa campos por punto y coma y convierte precios a valores numericos. Después crea un `timestamp` a partir de fecha y periodo. Si un día tiene más de 25 periodos, se interpreta como cuarto-horario; en caso contrario, horario.

El resultado final se guarda en `data/processed/omie_prices.csv`.

La función de carga recorre el rango de fechas indicado y acumula los días válidos. Si un día falla, se registra el problema y se continúa con el resto. Esta estrategia permite usar rangos largos aunque existan ausencias puntuales.

### 12.3. Módulo de integración con ESIOS

El módulo `esios.py` descarga indicadores de previsión renovable desde ESIOS:

```text
541 eólica
542 solar fotovoltaica
543 solar térmica
```

Convierte fechas a hora de Madrid, agrupa valores por `timestamp` y genera variables derivadas. Después une los datos con OMIE usando `merge_asof`, dirección hacia atrás y tolerancia de una hora.

Esta implementación permite enriquecer el dataset sin hacer obligatorio el uso de ESIOS.

Los datos ESIOS se cachean por rango temporal. Esto reduce llamadas a la API y acelera ejecuciones repetidas. La unión con OMIE se realiza después de ordenar ambas tablas por `timestamp`, evitando desalineaciones temporales.

### 12.4. Módulo de generación de variables

El módulo `features.py` crea las variables del modelo. Incluye variables cíclicas, retardos, medias móviles, desviaciones, mínimos, máximos, diferencias y ratios.

También detecta automáticamente si existen columnas ESIOS y las incorpora a la lista de variables. Esto permite que el mismo código funcione con datasets básicos y enriquecidos.

La función principal para entrenamiento es `make_supervised_dataset`, que devuelve `X` e `y`. Para inferencia se usa `make_next_prediction_features`, que construye la fila del siguiente periodo.

La función `get_feature_columns` detecta columnas externas disponibles. Gracias a ello, el mismo pipeline funciona con OMIE solo o con OMIE enriquecido con ESIOS. Las filas incompletas se eliminan antes de entrenar para que los modelos reciban una matriz numérica completa.

### 12.5. Módulo de entrenamiento

El módulo `train.py` define los modelos candidatos, realiza la división temporal, entrena, evalúa y guarda resultados.

Los modelos son:

```text
RidgeCV
MLPRegressor
HistGradientBoostingRegressor
```

La función `train_model` calcula MAE, RMSE, R2 y baseline. Después guarda un diccionario con:

```text
model
feature_columns
metrics
```

El modelo se serializa en `models/omie_model.joblib` y la gráfica en `models/validation_plot.png`.

El entrenamiento exige un mínimo de filas útiles después de generar variables. Esto evita entrenar con histórico insuficiente, especialmente porque existen retardos largos. El módulo también guarda métricas y columnas de entrada junto con el modelo, facilitando la inferencia posterior.

### 12.6. Módulo de inferencia

El módulo `predict.py` carga el modelo guardado y predice el siguiente periodo. Utiliza las columnas esperadas por el modelo para evitar inconsistencias entre entrenamiento e inferencia.

El sistema calcula el siguiente `timestamp` usando la diferencia temporal más frecuente en los datos recientes. Asi puede funcionar con datos horarios o cuarto-horarios.

Si no hay histórico suficiente para calcular retardos y ventanas, la inferencia falla con un mensaje claro.

Durante la inferencia se usa la lista de `feature_columns` guardada en el modelo. Esta decisión evita inconsistencias entre entrenamiento y predicción. Si el modelo fue entrenado con ESIOS, la inferencia debe disponer de esas columnas o no podrá construir la entrada correcta.

### 12.7. Interfaz gráfica con Tkinter

El módulo `gui.py` implementa la GUI. Usa Tkinter, `ttk`, hilos y una cola de eventos para mantener la interfaz viva durante procesos largos.

La aplicación evita bloquear la ventana ejecutando tareas en un hilo secundario. Los mensajes se envian a la interfaz mediante una cola, y el metodo `_poll_events` actualiza logs, estados y resultados.

Esta implementación mejora la experiencia del usuario y permite ver el avance de entrenamientos largos.

La GUI define rutas comúnes para datos, features, modelo y gráfica. Los botones llaman a métodos que ejecutan cada fase en segundo plaño. También se validan fechas, modelo y token ESIOS antes de iniciar tareas largas.

### 12.8. Serialización del modelo entrenado

La serialización se realiza con joblib. El fichero `models/omie_model.joblib` no contiene solo el estimador entrenado, sino también las columnas usadas y las métricas.

Guardar `feature_columns` es importante porque la inferencia debe construir exactamente las mismas entradas que el entrenamiento. Esto es especialmente relevante cuando se entrena con ESIOS, ya que el modelo espera columnas externas adicionales.

El fichero serializado incluye también métricas. Esto permite saber posteriormente qué modelo fue seleccionado, cuántas variables se usaron y cómo se comportó en validación. El artefacto no es solo un estimador, sino un resumen mínimo del experimento.

### 12.9. Generación de gráficas de validación

Durante el entrenamiento se genera `models/validation_plot.png`. La gráfica compara:

- valores reales
- predicción del modelo
- baseline `lag 24`

Se muestran los primeros 240 periodos del tramo de validación. Esto permite inspeccionar visualmente si el modelo sigue la forma general de la serie, si suaviza picos o si se separa del precio real.

La gráfica complementa las métricas numéricas y facilita la explicación del resultado en la memoria del TFG.

La gráfica se genera con matplotlib en modo no interactivo, por lo que puede crearse desde consola sin abrir ventanas adicionales. En conjunto, la implementación convierte la metodología descrita en capítulos anteriores en una aplicación ejecutable, reproducible y extensible.
