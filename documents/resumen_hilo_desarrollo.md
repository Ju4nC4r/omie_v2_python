# Resumen estructurado actualizado del hilo de desarrollo

## 1. Objetivo inicial del proyecto

El proyecto comenzo como una aplicacion sencilla para entrenar una red neuronal capaz de inferir el precio del mercado electrico espanol a partir de datos publicos de OMIE.

La idea inicial era intencionadamente pequena: aprender de calendario, ciclos horarios/semanales y precios retardados. Durante el hilo, el alcance se amplio progresivamente hasta convertirse en una aplicacion completa para:

- descargar datos OMIE
- preparar un dataset supervisado
- entrenar varios modelos
- comparar metricas
- realizar inferencia
- ejecutar el flujo desde una interfaz grafica
- incorporar opcionalmente prevision eolica y solar desde ESIOS
- documentar el proyecto como base de un Trabajo Fin de Grado
- guardar los avances con Git

El proyecto se ha orientado tanto a la parte practica de machine learning como a la redaccion academica del TFG.

## 2. Estructura general del proyecto

Se creo un paquete Python llamado:

```text
omie_price_nn
```

La estructura principal del proyecto quedo organizada asi:

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── documents/
├── models/
├── src/omie_price_nn/
│   ├── __init__.py
│   ├── data.py
│   ├── esios.py
│   ├── features.py
│   ├── gui.py
│   ├── predict.py
│   └── train.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

El directorio `documents/` se creo para alojar la documentacion del TFG y los resumenes del desarrollo.

## 3. Entorno Python

Se preparo un entorno virtual local:

```text
.venv/
```

Comandos principales de preparacion:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Dependencias principales:

- `pandas`
- `numpy`
- `requests`
- `scikit-learn`
- `joblib`
- `matplotlib`

El proyecto exige Python `>=3.10`.

## 4. Comandos disponibles

En `pyproject.toml` se definieron tres comandos principales:

```text
omie-price-gui
omie-price-train
omie-price-predict
```

Significado:

- `omie-price-gui`: abre la interfaz grafica.
- `omie-price-train`: descarga/prepara datos y entrena modelos.
- `omie-price-predict`: carga el modelo entrenado y predice el siguiente periodo.

Ejemplo de entrenamiento:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Ejemplo con ESIOS:

```bash
export ESIOS_TOKEN="tu_token_esios"
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios
```

## 5. Descarga y parseo de datos OMIE

Se implemento el modulo:

```text
src/omie_price_nn/data.py
```

Funciones principales:

- descarga de ficheros diarios OMIE
- parseo de ficheros `MARGINALPDBC`
- generacion de `timestamp`
- cache local en `data/raw/`
- generacion de `data/processed/omie_prices.csv`
- gestion de fallos por dia en rangos largos

Fuente OMIE usada:

```text
https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_YYYYMMDD.1
```

Campo objetivo del modelo:

```text
marginal_es
```

El parser se preparo para:

- datos horarios de 24 periodos
- datos cuarto-horarios de 96 periodos

La deteccion se realiza por el numero maximo de periodos del dia.

## 6. Integracion opcional con ESIOS

Se implemento el modulo:

```text
src/omie_price_nn/esios.py
```

La integracion ESIOS permite incorporar prevision renovable:

```text
541 -> wind_forecast_mwh
542 -> solar_pv_forecast_mwh
543 -> solar_thermal_forecast_mwh
```

Variables derivadas:

```text
solar_forecast_mwh
renewable_forecast_mwh
wind_solar_ratio
```

Caracteristicas de la integracion:

- requiere token ESIOS
- puede usarse con `--include-esios`
- tambien acepta la variable de entorno `ESIOS_TOKEN`
- cachea datos en `data/processed/esios_generation_YYYYMMDD_YYYYMMDD.csv`
- une OMIE y ESIOS por `timestamp`
- usa union temporal hacia atras con tolerancia de una hora
- rellena huecos pequenos con `ffill` y `bfill`

Si se activa ESIOS sin token, el programa falla de forma temprana con un mensaje claro.

## 7. Ingenieria de variables

Se implemento el modulo:

```text
src/omie_price_nn/features.py
```

Variables base generadas:

- `period`
- `time_of_day_sin`
- `time_of_day_cos`
- `hour_sin`
- `hour_cos`
- `dow_sin`
- `dow_cos`
- `month_sin`
- `month_cos`
- `is_weekend`
- retardos del precio
- medias moviles
- desviaciones moviles
- minimos y maximos recientes
- diferencias temporales
- ratios temporales

Retardos usados:

```text
1, 2, 3, 4, 5, 6, 12, 23, 24, 25, 48, 72, 168, 336
```

Ventanas moviles:

```text
3, 6, 12, 24, 48, 168
```

La matriz sin ESIOS tiene 45 variables. Al activar ESIOS se anaden 6 variables externas y derivadas, subiendo a 51 variables.

Para evitar fuga de informacion, las medias y estadisticos moviles se calculan usando el precio desplazado un periodo.

## 8. Modelos de entrenamiento

Se implemento el entrenamiento en:

```text
src/omie_price_nn/train.py
```

Modelos disponibles:

```text
auto
ridge
mlp
hist_gradient_boosting
```

### 8.1. `ridge`

Usa:

```text
RidgeCV
```

Es una regresion lineal regularizada. Es rapida, estable y adecuada como modelo base.

### 8.2. `mlp`

Usa:

```text
MLPRegressor
```

Es una red neuronal feed-forward sencilla. Representa la idea inicial del proyecto, pero no siempre es el modelo con mejor resultado.

### 8.3. `hist_gradient_boosting`

Usa:

```text
HistGradientBoostingRegressor
```

Es un modelo basado en arboles con boosting. En datos tabulares y con mas historico obtuvo muy buen rendimiento.

### 8.4. `auto`

No es un modelo, sino un modo de seleccion. Entrena:

```text
ridge
mlp
hist_gradient_boosting
```

Despues selecciona el que obtiene menor `MAE` en validacion temporal.

## 9. Interfaz grafica

Se implemento la GUI en:

```text
src/omie_price_nn/gui.py
```

Comando:

```bash
omie-price-gui
```

La interfaz permite ejecutar fases del flujo:

- extraccion de datos
- preparacion de datos
- entrenamiento
- test
- inferencia

Elementos principales:

- fecha inicial
- fecha final
- selector de modelo
- checkbox ESIOS
- campo Token ESIOS
- logs de ejecucion
- barra de progreso

Se corrigio el problema de que el entrenamiento pareciera quedarse bloqueado mostrando progreso y mensajes por candidato.

## 10. Inferencia

Se implemento la inferencia en:

```text
src/omie_price_nn/predict.py
```

Comando:

```bash
omie-price-predict
```

El sistema:

- carga `models/omie_model.joblib`
- lee los datos procesados
- calcula el siguiente `timestamp`
- genera las variables esperadas por el modelo
- predice el siguiente periodo

Tambien se silenció un aviso de CPU de joblib configurando `LOKY_MAX_CPU_COUNT=1` en la fase de prediccion.

## 11. Metricas usadas

Metricas explicadas y utilizadas:

```text
MAE
RMSE
R2
Baseline lag 24 MAE
```

Significado:

- `MAE`: error absoluto medio en `EUR/MWh`. Mas bajo es mejor.
- `RMSE`: raiz del error cuadratico medio. Penaliza mas errores grandes.
- `R2`: proporcion de variacion explicada. Mas cercano a 1 es mejor.
- `Baseline lag 24 MAE`: error usando el precio de 24 periodos antes.

El baseline sirve para comprobar si el modelo aporta valor frente a una regla sencilla.

## 12. Resultados obtenidos

### 12.1. Entrenamiento enero-marzo 2025

Comando:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Resultado:

```text
Mejor modelo: ridge
MAE: 10.02 EUR/MWh
RMSE: 15.70 EUR/MWh
R2: 0.871
Baseline lag 24 MAE: 20.97 EUR/MWh
```

Comparacion:

```text
ridge: MAE 10.02
mlp: MAE 13.70
hist_gradient_boosting: MAE 10.23
```

### 12.2. Entrenamiento con casi todo 2025

Comando:

```bash
omie-price-train --start 2025-01-01 --end 2025-12-31 --model auto
```

OMIE no devolvio datos para:

```text
2025-10-30
2025-11-27
```

Resultado:

```text
Mejor modelo: hist_gradient_boosting
MAE: 3.17 EUR/MWh
RMSE: 4.59 EUR/MWh
R2: 0.973
Baseline lag 24 MAE: 24.91 EUR/MWh
```

Comparacion:

```text
ridge: MAE 4.10
mlp: MAE 3.98
hist_gradient_boosting: MAE 3.17
```

## 13. Inferencia comparada con valor real OMIE

Tras entrenar con datos de 2025, se genero una prediccion:

```text
Prediccion para 2026-01-01 00:00:00: 94.20 EUR/MWh
```

Se comparo con el valor real extraido de OMIE:

```text
Valor real OMIE: 112.01 EUR/MWh
```

Error:

```text
Error: -17.81 EUR/MWh
Error absoluto: 17.81 EUR/MWh
Error relativo: 15.90%
```

Conclusion:

El modelo infraestimo el precio del primer periodo de 2026. Se identificaron posibles causas:

- dia festivo de Ano Nuevo
- falta de variable explicita de festivos
- cambios de regimen
- falta de demanda prevista
- falta de meteorologia
- falta de gas y CO2
- limitaciones del uso de retardos por numero de periodos

## 14. README

El README se amplio varias veces. Actualmente documenta:

- objetivo del proyecto
- instalacion con `.venv`
- comandos principales
- uso de la GUI
- modelos disponibles
- modo `auto`
- uso de ESIOS
- variables del modelo
- metricas
- artefactos generados
- solucion de problemas
- configuracion de SSH para GitHub
- futuras mejoras

Tambien se pidio que el README usara emojis y fuera mas completo.

## 15. Repositorio Git y GitHub

Se inicializo y uso Git durante el desarrollo. Se realizaron commits para los principales hitos.

Repositorio remoto configurado:

```text
git@github.com:Ju4nC4r/omie_v2_python.git
```

Tambien se documento la URL:

```text
https://github.com/Ju4nC4r/omie_v2_python.git
```

Los intentos de subida a GitHub fallaron por autenticacion SSH:

```text
git@github.com: Permission denied (publickey).
```

Se explico como configurar una SSH key en macOS para GitHub.

## 16. Documentacion TFG creada

Se creo el directorio:

```text
documents/
```

Dentro se genero el indice del TFG y capitulos desarrollados en ficheros Markdown separados.

El indice actual es:

```text
documents/TFG-Predicion-MercadoElectrico-Indice.md
```

El fichero de indice fue renombrado desde un nombre anterior para quedar como:

```text
TFG-Predicion-MercadoElectrico-Indice.md
```

Tambien se corrigio el indice para que los apartados de segundo nivel coincidieran con los capitulos ya desarrollados. En concreto, se anadieron al capitulo 1:

```text
1.6. Contribuciones del trabajo
1.7. Alcance y limites del resumen
1.8. Sintesis del capitulo
```

## 17. Capitulos del TFG desarrollados

Actualmente estan desarrollados y enlazados en el indice:

```text
capitulo_01_resumen.md
capitulo_02_introduccion.md
capitulo_03_objetivos.md
capitulo_04_marco_teorico.md
capitulo_05_estado_del_arte.md
capitulo_06_fuentes_de_datos.md
capitulo_07_preparacion_de_datos.md
capitulo_08_ingenieria_de_variables.md
capitulo_13_aplicacion_practica_desarrollada.md
capitulo_14_informacion_concreta_proyecto.md
capitulo_15_resultados_experimentales.md
```

### 17.1. Capitulo 1. Resumen

Presenta el contexto, objetivo, metodologia, resultados esperados, aplicacion practica, contribuciones, alcance y sintesis.

### 17.2. Capitulo 2. Introduccion

Desarrolla la motivacion, importancia de predecir el precio electrico, problema, alcance y estructura del documento.

### 17.3. Capitulo 3. Objetivos

Define el objetivo general, objetivos especificos, requisitos funcionales, requisitos no funcionales y limitaciones iniciales.

### 17.4. Capitulo 4. Marco teorico

Explica el funcionamiento del mercado electrico espanol, OMIE, ESIOS, factores de precio, renovables, series temporales y aprendizaje supervisado.

### 17.5. Capitulo 5. Estado del arte

Revisa modelos estadisticos clasicos, machine learning aplicado a energia, redes neuronales, modelos de boosting, comparacion de enfoques y retos de la literatura.

### 17.6. Capitulo 6. Fuentes de datos

Documenta OMIE, ficheros `MARGINALPDBC`, ESIOS, prevision eolica, solar fotovoltaica, solar termica, frecuencia temporal, calidad de datos y cache local.

### 17.7. Capitulo 7. Preparacion de datos

Explica descarga OMIE, ESIOS opcional, limpieza, normalizacion, union por `timestamp`, gestion de ausentes, dataset supervisado y validacion temporal.

### 17.8. Capitulo 8. Ingenieria de variables

Detalla variables de calendario, codificacion ciclica, retardos, medias moviles, desviaciones, minimos, maximos, diferencias, ratios y variables renovables.

### 17.9. Capitulo 13. Aplicacion practica desarrollada

Describe la aplicacion real, GUI, comandos, flujo de trabajo, seleccion de modelos, modo `auto`, OMIE, ESIOS, inferencia y comparacion con valor real.

### 17.10. Capitulo 14. Informacion concreta del proyecto implementado

Recoge la ficha tecnica del proyecto: nombre, Python, `.venv`, paquete, repositorio, comandos, modelo guardado y grafica generada.

### 17.11. Capitulo 15. Resultados experimentales

Documenta los resultados de enero-marzo 2025, casi todo 2025, comparacion de modelos, modo `auto`, baseline e inferencia frente a OMIE.

## 18. Capitulos pendientes del TFG

En el indice siguen pendientes:

```text
9. Modelos de prediccion
10. Metodologia de evaluacion
11. Diseno de la aplicacion practica
12. Implementacion del proyecto
16. Discusion
17. Conclusiones
18. Lineas futuras
19. Planificacion del proyecto
20. Bibliografia y referencias
21. Anexos
```

Los capitulos 13, 14 y 15 se desarrollaron antes que 9-12 porque el usuario lo solicito explicitamente.

## 19. Commits principales

Commits relevantes del hilo:

```text
bea9b74 Initial OMIE price forecasting app
b7e454c Show training progress in GUI
78a8937 Allow selecting training model
44c68e1 Expand README with visual guide
4b427a3 Document training models in detail
d3f6c88 Silence prediction CPU warning
0747216 Add optional ESIOS renewable forecasts
09a9f8c Expand ESIOS usage documentation
f729fc1 Add documentation directory
559175a Add TFG outline document
c06ea63 Draft TFG chapter 1 summary
b55effe Link TFG index to chapter files
1643c89 Add structured development thread summary
ff698a3 Draft TFG chapter 2 introduction
86898a1 Draft TFG chapter 3 objectives
50bda23 Rename TFG index document
1d5d185 Draft TFG chapter 4 theoretical framework
d186d3e Draft TFG chapter 5 state of the art
71efa11 Draft TFG chapter 6 data sources
7f00007 Align TFG index with developed chapters
f069611 Draft TFG chapter 7 data preparation
449201f Draft TFG chapter 8 feature engineering
91082bc Draft TFG chapter 13 practical application
a3950a9 Draft TFG chapters 14 and 15
```

## 20. Problemas encontrados

### 20.1. Autenticacion GitHub

Los intentos de `git push` fallaron por falta de clave SSH autorizada en GitHub.

Mensaje:

```text
Permission denied (publickey).
```

Se explico como generar/configurar una SSH key en macOS.

### 20.2. Red y descargas

Algunas descargas pueden fallar por red, DNS o disponibilidad del servidor.

En 2025, OMIE no devolvio ficheros para:

```text
2025-10-30
2025-11-27
```

### 20.3. Entrenamiento aparentemente bloqueado

El entrenamiento, especialmente con `mlp` o `auto`, podia parecer parado. Se mejoro la GUI para mostrar progreso y logs.

### 20.4. Resolucion horaria y cuarto-horaria

Se detecto que algunos datos pueden contener 24 periodos y otros 96 periodos.

Esto afecta a la interpretacion de retardos como `lag 24`, que en horario equivale a un dia, pero en cuarto-horario equivale a seis horas.

### 20.5. Inferencia con error puntual

La prediccion para `2026-01-01 00:00` infraestimo el valor real. Se identifico la necesidad de incorporar festivos, demanda, meteorologia y otras variables externas.

## 21. Proximos pasos sugeridos

Pasos tecnicos:

- configurar correctamente la SSH key de GitHub y subir el repositorio
- desarrollar capitulos 9, 10, 11 y 12 para completar la parte metodologica/tecnica
- desarrollar capitulos 16, 17 y 18 para discusion, conclusiones y lineas futuras
- anadir festivos nacionales y autonomicos como variables
- incorporar demanda prevista
- incorporar meteorologia
- mejorar retardos para que dependan de duracion real y no solo de numero de periodos
- automatizar comparacion entre prediccion y valor real cuando OMIE publique el dato
- crear backtesting mensual
- estudiar importancia de variables

Pasos documentales:

- revisar estilo global de todos los capitulos
- unificar terminologia
- completar bibliografia
- anadir figuras, tablas y diagramas
- preparar anexos con comandos, estructura del proyecto y capturas de la GUI

## 22. Estado actual resumido

El proyecto ya cuenta con:

- aplicacion Python funcional
- entorno virtual preparado
- descarga OMIE
- integracion opcional ESIOS
- tres modelos de entrenamiento y modo `auto`
- interfaz grafica
- comandos de consola
- inferencia
- README completo
- repositorio Git con commits
- documentacion TFG en `documents/`
- capitulos 1, 2, 3, 4, 5, 6, 7, 8, 13, 14 y 15 desarrollados
- indice actualizado con enlaces a los capitulos desarrollados

El siguiente bloque natural de trabajo seria desarrollar los capitulos 9, 10, 11 y 12 para cerrar el hueco entre la ingenieria de variables y la aplicacion practica.
