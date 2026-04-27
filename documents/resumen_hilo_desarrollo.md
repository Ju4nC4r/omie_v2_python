# Resumen estructurado actualizado del hilo de desarrollo

## 1. Objetivo inicial del proyecto

El proyecto comenzó como una aplicación sencilla para entrenar una red neuronal capaz de inferir el precio del mercado eléctrico español a partir de datos públicos de OMIE.

La idea inicial era intencionadamente pequeña: aprender de calendario, ciclos horarios/semanales y precios retardados. Durante el hilo, el alcance se amplio progresivamente hasta convertirse en una aplicación completa para:

- descargar datos OMIE
- preparar un dataset supervisado
- entrenar varios modelos
- comparar métricas
- realizar inferencia
- ejecutar el flujo desde una interfaz gráfica
- incorporar opcionalmente previsión eólica y solar desde ESIOS
- documentar el proyecto como base de un Trabajo Fin de Grado
- guardar los avances con Git

El proyecto se ha orientado tanto a la parte práctica de machine learning como a la redaccion académica del TFG.

## 2. Estructura general del proyecto

Se creo un paquete Python llamado:

```text
omie_price_nn
```

La estructura principal del proyecto quedó organizada así:

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

El directorio `documents/` se creo para alojar la documentación del TFG y los resúmenes del desarrollo.

## 3. Entorno Python

Se preparo un entorno virtual local:

```text
.venv/
```

Comandos principales de preparación:

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

- `omie-price-gui`: abre la interfaz gráfica.
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

Se implementó el módulo:

```text
src/omie_price_nn/data.py
```

Funciones principales:

- descarga de ficheros diarios OMIE
- parseo de ficheros `MARGINALPDBC`
- generación de `timestamp`
- cache local en `data/raw/`
- generación de `data/processed/omie_prices.csv`
- gestión de fallos por día en rangos largos

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

La deteccion se realiza por el número máximo de periodos del día.

## 6. Integración opcional con ESIOS

Se implementó el módulo:

```text
src/omie_price_nn/esios.py
```

La integración ESIOS permite incorporar previsión renovable:

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

Caracteristicas de la integración:

- requiere token ESIOS
- puede usarse con `--include-esios`
- también acepta la variable de entorno `ESIOS_TOKEN`
- cachea datos en `data/processed/esios_generation_YYYYMMDD_YYYYMMDD.csv`
- une OMIE y ESIOS por `timestamp`
- usa unión temporal hacia atrás con tolerancia de una hora
- rellena huecos pequeños con `ffill` y `bfill`

Si se activa ESIOS sin token, el programa falla de forma temprana con un mensaje claro.

## 7. Ingeniería de variables

Se implementó el módulo:

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
- medias móviles
- desviaciones móviles
- mínimos y máximos recientes
- diferencias temporales
- ratios temporales

Retardos usados:

```text
1, 2, 3, 4, 5, 6, 12, 23, 24, 25, 48, 72, 168, 336
```

Ventanas móviles:

```text
3, 6, 12, 24, 48, 168
```

La matriz sin ESIOS tiene 45 variables. Al activar ESIOS se añaden 6 variables externas y derivadas, subiendo a 51 variables.

Para evitar fuga de información, las medias y estadísticos móviles se calculan usando el precio desplazado un periodo.

## 8. Modelos de entrenamiento

Se implementó el entrenamiento en:

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

Es una regresión lineal regularizada. Es rápida, estable y adecuada como modelo base.

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

Es un modelo basado en árboles con boosting. En datos tabulares y con más histórico obtuvo muy buen rendimiento.

### 8.4. `auto`

No es un modelo, sino un modo de selección. Entrena:

```text
ridge
mlp
hist_gradient_boosting
```

Después selecciona el que obtiene menor `MAE` en validación temporal.

## 9. Interfaz gráfica

Se implementó la GUI en:

```text
src/omie_price_nn/gui.py
```

Comando:

```bash
omie-price-gui
```

La interfaz permite ejecutar fases del flujo:

- extracción de datos
- preparación de datos
- entrenamiento
- test
- inferencia

Elementos principales:

- fecha inicial
- fecha final
- selector de modelo
- checkbox ESIOS
- campo Token ESIOS
- logs de ejecución
- barra de progreso

Se corrigió el problema de que el entrenamiento pareciera quedarse bloqueado mostrando progreso y mensajes por candidato.

## 10. Inferencia

Se implementó la inferencia en:

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

También se silenció un aviso de CPU de joblib configurando `LOKY_MAX_CPU_COUNT=1` en la fase de predicción.

## 11. Métricas usadas

Métricas explicadas y utilizadas:

```text
MAE
RMSE
R2
Baseline lag 24 MAE
```

Significado:

- `MAE`: error absoluto medio en `EUR/MWh`. Más bajo es mejor.
- `RMSE`: raíz del error cuadrático medio. Penaliza más errores grandes.
- `R2`: proporción de variación explicada. Más cercano a 1 es mejor.
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

Comparación:

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

Comparación:

```text
ridge: MAE 4.10
mlp: MAE 3.98
hist_gradient_boosting: MAE 3.17
```

## 13. Inferencia comparada con valor real OMIE

Tras entrenar con datos de 2025, se generó una predicción:

```text
Predicción para 2026-01-01 00:00:00: 94.20 EUR/MWh
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

- día festivo de Año Nuevo
- falta de variable explícita de festivos
- cambios de régimen
- falta de demanda prevista
- falta de meteorología
- falta de gas y CO2
- limitaciones del uso de retardos por número de periodos

## 14. README

El README se amplio varias veces. Actualmente documenta:

- objetivo del proyecto
- instalación con `.venv`
- comandos principales
- uso de la GUI
- modelos disponibles
- modo `auto`
- uso de ESIOS
- variables del modelo
- métricas
- artefactos generados
- solucion de problemas
- configuración de SSH para GitHub
- futuras mejoras

También se pidio que el README usara emojis y fuera más completo.

## 15. Repositorio Git y GitHub

Se inicializó y usó Git durante el desarrollo. Se realizaron commits para los principales hitos.

Repositorio remoto configurado:

```text
git@github.com:Ju4nC4r/omie_v2_python.git
```

También se documento la URL:

```text
https://github.com/Ju4nC4r/omie_v2_python.git
```

Los intentos de subida a GitHub fallaron por autenticación SSH:

```text
git@github.com: Permission denied (publickey).
```

Se explico como configurar una SSH key en macOS para GitHub.

## 16. Documentación creada

Se creo el directorio:

```text
documents/
```

Dentro se generó el índice del Documento y capítulos desarrollados en ficheros Markdown separados.

El índice actual es:

```text
documents/DOCUMENT-Predicion-MercadoElectrico-Indice.md
```

El fichero de índice fue renombrado desde un nombre anterior para quedar como:

```text
DOCUMENT-Predicion-MercadoElectrico-Indice.md
```

También se corrigió el índice para que los apartados de segundo nivel coincidieran con los capítulos ya desarrollados. En concreto, se añadieron al capítulo 1:

```text
1.6. Contribuciones del trabajo
1.7. Alcance y límites del resumen
1.8. Síntesis del capitulo
```

## 17. Capítulos del TFG desarrollados

Actualmente están desarrollados y enlazados en el índice:

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

### 17.1. Capítulo 1. Resumen

Presenta el contexto, objetivo, metodología, resultados esperados, aplicación práctica, contribuciones, alcance y síntesis.

### 17.2. Capítulo 2. Introducción

Desarrolla la motivacion, importancia de predecir el precio eléctrico, problema, alcance y estructura del documento.

### 17.3. Capítulo 3. Objetivos

Define el objetivo general, objetivos específicos, requisitos funcionales, requisitos no funcionales y limitaciones iniciales.

### 17.4. Capítulo 4. Marco teórico

Explica el funcionamiento del mercado eléctrico español, OMIE, ESIOS, factores de precio, renovables, series temporales y aprendizaje supervisado.

### 17.5. Capítulo 5. Estado del arte

Revisa modelos estadísticos clásicos, machine learning aplicado a energía, redes neuronales, modelos de boosting, comparación de enfoques y retos de la literatura.

### 17.6. Capítulo 6. Fuentes de datos

Documenta OMIE, ficheros `MARGINALPDBC`, ESIOS, previsión eólica, solar fotovoltaica, solar térmica, frecuencia temporal, calidad de datos y cache local.

### 17.7. Capítulo 7. Preparación de datos

Explica descarga OMIE, ESIOS opcional, limpieza, normalización, unión por `timestamp`, gestión de ausentes, dataset supervisado y validación temporal.

### 17.8. Capítulo 8. Ingeniería de variables

Detalla variables de calendario, codificación cíclica, retardos, medias móviles, desviaciones, mínimos, máximos, diferencias, ratios y variables renovables.

### 17.9. Capítulo 13. Aplicación práctica desarrollada

Describe la aplicación real, GUI, comandos, flujo de trabajo, selección de modelos, modo `auto`, OMIE, ESIOS, inferencia y comparación con valor real.

### 17.10. Capítulo 14. Información concreta del proyecto implementado

Recoge la ficha técnica del proyecto: nombre, Python, `.venv`, paquete, repositorio, comandos, modelo guardado y gráfica generada.

### 17.11. Capítulo 15. Resultados experimentales

Documenta los resultados de enero-marzo 2025, casi todo 2025, comparación de modelos, modo `auto`, baseline e inferencia frente a OMIE.

## 18. Capítulos pendientes del Documento

En el índice siguen pendientes:

```text
9. Modelos de predicción
10. Metodología de evaluación
11. Diseño de la aplicación práctica
12. Implementación del proyecto
16. Discusión
17. Conclusiones
18. Líneas futuras
19. Planificación del proyecto
20. Bibliografía y referencias
21. Anexos
```

Los capítulos 13, 14 y 15 se desarrollaron antes que 9-12 porque el usuario lo solicito explícitamente.

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

El entrenamiento, especialmente con `mlp` o `auto`, podía parecer parado. Se mejoró la GUI para mostrar progreso y logs.

### 20.4. Resolución horaria y cuarto-horaria

Se detecto que algunos datos pueden contener 24 periodos y otros 96 periodos.

Esto afecta a la interpretación de retardos como `lag 24`, que en horario equivale a un día, pero en cuarto-horario equivale a seis horas.

### 20.5. Inferencia con error puntual

La predicción para `2026-01-01 00:00` infraestimo el valor real. Se identifico la necesidad de incorporar festivos, demanda, meteorología y otras variables externas.

## 21. Proximos pasos sugeridos

Pasos técnicos:

- configurar correctamente la SSH key de GitHub y subir el repositorio
- desarrollar capítulos 9, 10, 11 y 12 para completar la parte metodológica/técnica
- desarrollar capítulos 16, 17 y 18 para discusión, conclusiones y líneas futuras
- añadir festivos nacionales y autonómicos como variables
- incorporar demanda prevista
- incorporar meteorología
- mejorar retardos para que dependan de duración real y no solo de número de periodos
- automatizar comparación entre predicción y valor real cuando OMIE publique el dato
- crear backtesting mensual
- estudiar importancia de variables

Pasos documentales:

- revisar estilo global de todos los capítulos
- unificar terminologia
- completar bibliografía
- añadir figuras, tablas y díagramás
- preparar anexos con comandos, estructura del proyecto y capturas de la GUI

## 22. Estado actual resumido

El proyecto ya cuenta con:

- aplicación Python funcional
- entorno virtual preparado
- descarga OMIE
- integración opcional ESIOS
- tres modelos de entrenamiento y modo `auto`
- interfaz gráfica
- comandos de consola
- inferencia
- README completo
- repositorio Git con commits
- documentación TFG en `documents/`
- capítulos 1, 2, 3, 4, 5, 6, 7, 8, 13, 14 y 15 desarrollados
- índice actualizado con enlaces a los capítulos desarrollados

El siguiente bloque natural de trabajo sería desarrollar los capítulos 9, 10, 11 y 12 para cerrar el hueco entre la ingeniería de variables y la aplicación práctica.
