# Capitulo 12. Implementacion del proyecto

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 12.1. Estructura de directorios

La implementacion sigue una estructura clara:

```text
src/omie_price_nn/
documents/
data/
models/
```

El codigo fuente vive en `src/omie_price_nn/`. La documentacion del TFG se almacena en `documents/`. Los datos descargados y procesados se guardan en `data/`. Los modelos y graficas se guardan en `models/`.

Esta separacion evita mezclar codigo, datos, documentacion y artefactos.

El directorio `src/` contiene el paquete instalable. El directorio `documents/` contiene la memoria del TFG y los resumenes del desarrollo. Los directorios `data/` y `models/` se consideran artefactos locales generados durante la ejecucion, por lo que estan excluidos del repositorio.

### 12.2. Modulo de descarga y parseo de OMIE

El modulo `data.py` implementa la descarga de ficheros `MARGINALPDBC`. Genera nombres diarios como `marginalpdbc_YYYYMMDD.1`, solicita el fichero a OMIE y lo guarda en `data/raw/`.

El parser descarta cabeceras y comentarios, separa campos por punto y coma y convierte precios a valores numericos. Despues crea un `timestamp` a partir de fecha y periodo. Si un dia tiene mas de 25 periodos, se interpreta como cuarto-horario; en caso contrario, horario.

El resultado final se guarda en `data/processed/omie_prices.csv`.

La funcion de carga recorre el rango de fechas indicado y acumula los dias validos. Si un dia falla, se registra el problema y se continua con el resto. Esta estrategia permite usar rangos largos aunque existan ausencias puntuales.

### 12.3. Modulo de integracion con ESIOS

El modulo `esios.py` descarga indicadores de prevision renovable desde ESIOS:

```text
541 eolica
542 solar fotovoltaica
543 solar termica
```

Convierte fechas a hora de Madrid, agrupa valores por `timestamp` y genera variables derivadas. Despues une los datos con OMIE usando `merge_asof`, direccion hacia atras y tolerancia de una hora.

Esta implementacion permite enriquecer el dataset sin hacer obligatorio el uso de ESIOS.

Los datos ESIOS se cachean por rango temporal. Esto reduce llamadas a la API y acelera ejecuciones repetidas. La union con OMIE se realiza despues de ordenar ambas tablas por `timestamp`, evitando desalineaciones temporales.

### 12.4. Modulo de generacion de variables

El modulo `features.py` crea las variables del modelo. Incluye variables ciclicas, retardos, medias moviles, desviaciones, minimos, maximos, diferencias y ratios.

Tambien detecta automaticamente si existen columnas ESIOS y las incorpora a la lista de variables. Esto permite que el mismo codigo funcione con datasets basicos y enriquecidos.

La funcion principal para entrenamiento es `make_supervised_dataset`, que devuelve `X` e `y`. Para inferencia se usa `make_next_prediction_features`, que construye la fila del siguiente periodo.

La funcion `get_feature_columns` detecta columnas externas disponibles. Gracias a ello, el mismo pipeline funciona con OMIE solo o con OMIE enriquecido con ESIOS. Las filas incompletas se eliminan antes de entrenar para que los modelos reciban una matriz numerica completa.

### 12.5. Modulo de entrenamiento

El modulo `train.py` define los modelos candidatos, realiza la division temporal, entrena, evalua y guarda resultados.

Los modelos son:

```text
RidgeCV
MLPRegressor
HistGradientBoostingRegressor
```

La funcion `train_model` calcula MAE, RMSE, R2 y baseline. Despues guarda un diccionario con:

```text
model
feature_columns
metrics
```

El modelo se serializa en `models/omie_model.joblib` y la grafica en `models/validation_plot.png`.

El entrenamiento exige un minimo de filas utiles despues de generar variables. Esto evita entrenar con historico insuficiente, especialmente porque existen retardos largos. El modulo tambien guarda metricas y columnas de entrada junto con el modelo, facilitando la inferencia posterior.

### 12.6. Modulo de inferencia

El modulo `predict.py` carga el modelo guardado y predice el siguiente periodo. Utiliza las columnas esperadas por el modelo para evitar inconsistencias entre entrenamiento e inferencia.

El sistema calcula el siguiente `timestamp` usando la diferencia temporal mas frecuente en los datos recientes. Asi puede funcionar con datos horarios o cuarto-horarios.

Si no hay historico suficiente para calcular retardos y ventanas, la inferencia falla con un mensaje claro.

Durante la inferencia se usa la lista de `feature_columns` guardada en el modelo. Esta decision evita inconsistencias entre entrenamiento y prediccion. Si el modelo fue entrenado con ESIOS, la inferencia debe disponer de esas columnas o no podra construir la entrada correcta.

### 12.7. Interfaz grafica con Tkinter

El modulo `gui.py` implementa la GUI. Usa Tkinter, `ttk`, hilos y una cola de eventos para mantener la interfaz viva durante procesos largos.

La aplicacion evita bloquear la ventana ejecutando tareas en un hilo secundario. Los mensajes se envian a la interfaz mediante una cola, y el metodo `_poll_events` actualiza logs, estados y resultados.

Esta implementacion mejora la experiencia del usuario y permite ver el avance de entrenamientos largos.

La GUI define rutas comunes para datos, features, modelo y grafica. Los botones llaman a metodos que ejecutan cada fase en segundo plano. Tambien se validan fechas, modelo y token ESIOS antes de iniciar tareas largas.

### 12.8. Serializacion del modelo entrenado

La serializacion se realiza con joblib. El fichero `models/omie_model.joblib` no contiene solo el estimador entrenado, sino tambien las columnas usadas y las metricas.

Guardar `feature_columns` es importante porque la inferencia debe construir exactamente las mismas entradas que el entrenamiento. Esto es especialmente relevante cuando se entrena con ESIOS, ya que el modelo espera columnas externas adicionales.

El fichero serializado incluye tambien metricas. Esto permite saber posteriormente que modelo fue seleccionado, cuantas variables se usaron y como se comporto en validacion. El artefacto no es solo un estimador, sino un resumen minimo del experimento.

### 12.9. Generacion de graficas de validacion

Durante el entrenamiento se genera `models/validation_plot.png`. La grafica compara:

- valores reales
- prediccion del modelo
- baseline `lag 24`

Se muestran los primeros 240 periodos del tramo de validacion. Esto permite inspeccionar visualmente si el modelo sigue la forma general de la serie, si suaviza picos o si se separa del precio real.

La grafica complementa las metricas numericas y facilita la explicacion del resultado en la memoria del TFG.

La grafica se genera con matplotlib en modo no interactivo, por lo que puede crearse desde consola sin abrir ventanas adicionales. En conjunto, la implementacion convierte la metodologia descrita en capitulos anteriores en una aplicacion ejecutable, reproducible y extensible.
