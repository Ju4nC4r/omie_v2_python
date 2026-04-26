# Resumen estructurado del hilo de desarrollo

## 1. Objetivo inicial

El proyecto comenzo como una aplicacion sencilla para entrenar una red neuronal capaz de inferir el precio del mercado electrico espanol a partir de datos publicos de OMIE.

Durante el desarrollo, el alcance se amplio progresivamente hasta convertirse en una herramienta completa para:

- descargar datos OMIE
- preparar un dataset supervisado
- entrenar varios modelos
- comparar metricas
- realizar inferencia
- usar una interfaz grafica
- incorporar opcionalmente datos eolicos y solares de ESIOS
- documentar el proyecto como base para un Trabajo Fin de Grado

## 2. Estructura general del proyecto

Se creo un paquete Python llamado:

```text
omie_price_nn
```

La estructura principal quedo organizada asi:

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
├── README.md
├── pyproject.toml
└── requirements.txt
```

## 3. Entorno Python

Se creo un entorno virtual en:

```text
.venv/
```

Comandos principales:

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

## 4. Descarga de datos OMIE

Se implemento el modulo:

```text
src/omie_price_nn/data.py
```

Funciones principales:

- descarga de ficheros diarios OMIE
- parseo de ficheros `MARGINALPDBC`
- generacion de timestamps
- cache local en `data/raw/`
- generacion de `data/processed/omie_prices.csv`

Fuente OMIE usada:

```text
https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_YYYYMMDD.1
```

Campo objetivo:

```text
marginal_es
```

El parser se preparo para:

- datos horarios de 24 periodos
- datos cuarto-horarios de 96 periodos

## 5. Preparacion de variables

Se implemento el modulo:

```text
src/omie_price_nn/features.py
```

Variables generadas:

- variables ciclicas de hora
- variables ciclicas de dia de la semana
- variables ciclicas de mes
- indicador de fin de semana
- retardos del precio
- medias moviles
- desviaciones moviles
- minimos y maximos recientes
- diferencias temporales
- ratios temporales

Retardos principales:

```text
1, 2, 3, 4, 5, 6, 12, 23, 24, 25, 48, 72, 168, 336
```

La matriz inicial de entrenamiento tenia 45 variables. Al activar ESIOS sube a 51 variables.

## 6. Modelos de entrenamiento

Inicialmente se planteo una red neuronal sencilla, pero se mejoro el sistema para comparar varios modelos.

Se implemento en:

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

### 6.1. `ridge`

Usa:

```text
RidgeCV
```

Es una regresion lineal regularizada.

### 6.2. `mlp`

Usa:

```text
MLPRegressor
```

Es una red neuronal feed-forward sencilla.

### 6.3. `hist_gradient_boosting`

Usa:

```text
HistGradientBoostingRegressor
```

Es un modelo de arboles con boosting.

### 6.4. `auto`

Entrena los tres modelos y selecciona el de menor `MAE` en validacion temporal.

## 7. Metricas

Se explicaron y usaron estas metricas:

```text
MAE
RMSE
R2
Baseline lag 24 MAE
```

### 7.1. MAE

Error absoluto medio en `EUR/MWh`. Mas bajo es mejor.

### 7.2. RMSE

Raiz del error cuadratico medio. Penaliza mas los errores grandes.

### 7.3. R2

Proporcion de variacion explicada por el modelo. Cuanto mas cerca de 1, mejor.

### 7.4. Baseline lag 24

Prediccion simple que usa el precio de 24 periodos antes.

Ejemplo:

```text
prediccion = precio de ayer a la misma hora
```

Sirve como referencia para comprobar si el modelo realmente aporta valor.

## 8. Resultados obtenidos

### 8.1. Entrenamiento enero-marzo 2025

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

### 8.2. Entrenamiento con casi todo 2025

Comando:

```bash
omie-price-train --start 2025-01-01 --end 2025-12-31 --model auto
```

OMIE devolvio 404 para dos dias:

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

## 9. Inferencia y comparacion con valor real

Tras entrenar con 2025, se genero una prediccion:

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

El modelo infraestimo el precio del primer periodo de 2026. Se identifico que este tipo de error puede estar relacionado con festivos, cambios de regimen, falta de variables externas y particularidades de un dia como Año Nuevo.

## 10. Interfaz grafica

Se creo una interfaz grafica en:

```text
src/omie_price_nn/gui.py
```

Comando:

```bash
omie-price-gui
```

La GUI permite ejecutar:

- extraccion de datos
- preparacion
- entrenamiento y test
- inferencia
- apertura de grafica de validacion

Tambien permite elegir modelo:

- `auto`
- `ridge`
- `mlp`
- `hist_gradient_boosting`

Se corrigio un problema en el que el entrenamiento parecia quedarse bloqueado. Se anadio:

- barra de progreso
- logs por candidato
- ejecucion en segundo plano
- backend `Agg` para Matplotlib

## 11. Integracion con ESIOS

Se creo el modulo:

```text
src/omie_price_nn/esios.py
```

Permite incorporar prevision eolica y solar como variables externas.

Indicadores usados:

```text
541 -> wind_forecast_mwh
542 -> solar_pv_forecast_mwh
543 -> solar_thermal_forecast_mwh
```

Columnas derivadas:

```text
solar_forecast_mwh
renewable_forecast_mwh
wind_solar_ratio
```

Uso por consola:

```bash
export ESIOS_TOKEN="tu_token_esios"
omie-price-train --start 2025-01-01 --end 2025-12-31 --model auto --include-esios
```

Tambien se anadio a la GUI:

- checkbox `ESIOS`
- campo `Token ESIOS`

Si se activa ESIOS sin token, el programa falla antes de modificar datos.

## 12. Documentacion creada

Se creo el directorio:

```text
documents/
```

Documentos creados:

```text
documents/indice_tfg_prediccion_mercado_electrico.md
documents/capitulo_01_resumen.md
documents/resumen_hilo_desarrollo.md
```

### 12.1. Indice del TFG

Incluye estructura completa del Trabajo Fin de Grado y enlaces a capitulos desarrollados.

Actualmente enlaza a:

```text
capitulo_01_resumen.md
```

### 12.2. Capitulo 1

Se desarrollo el capitulo:

```text
Capitulo 1. Resumen
```

Contenido:

- contexto del mercado electrico
- objetivo principal
- metodologia
- resultados esperados
- aplicacion practica
- contribuciones
- alcance y limites
- sintesis

Tiene aproximadamente 4.350 palabras.

## 13. README

Se amplio el `README.md` con:

- emojis
- tabla de contenidos
- instalacion
- uso GUI
- uso CLI
- modelos disponibles
- integracion ESIOS
- metricas
- estructura del proyecto
- GitHub con SSH
- problemas frecuentes
- referencias

## 14. Git y commits principales

Se inicializo el repositorio Git local.

Commits relevantes:

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
```

## 15. GitHub

Repositorio remoto indicado:

```text
git@github.com:Ju4nC4r/omie_v2_python.git
```

Tambien se uso inicialmente:

```text
https://github.com/Ju4nC4r/omie_v2_python.git
```

Se intento subir a GitHub, pero fallo por autenticacion SSH:

```text
Permission denied (publickey)
```

Queda pendiente configurar correctamente la clave SSH en GitHub y ejecutar:

```bash
git push -u origin main
```

## 16. Problemas encontrados

### 16.1. Credenciales GitHub

No se pudo hacer push por falta de autenticacion SSH valida.

### 16.2. DNS / red en sandbox

Algunas descargas fallaron inicialmente por bloqueo de red del entorno. Se relanzaron con permisos cuando fue necesario.

### 16.3. Warning de joblib

Aparecio un warning sobre numero de cores fisicos. Se mitigio configurando:

```python
LOKY_MAX_CPU_COUNT=1
```

### 16.4. Entrenamiento aparentemente bloqueado

La GUI no mostraba progreso durante el entrenamiento. Se resolvio con:

- barra de progreso
- logs incrementales
- callback de progreso

### 16.5. OMIE con dias no disponibles

Durante el entrenamiento de 2025 faltaron:

```text
2025-10-30
2025-11-27
```

OMIE devolvio 404 para esos ficheros.

## 17. Proximos pasos sugeridos

1. Configurar SSH correctamente y subir el repositorio a GitHub.
2. Obtener token ESIOS y probar entrenamiento con `--include-esios`.
3. Comparar rendimiento con y sin variables renovables.
4. Anadir festivos nacionales y autonomicos.
5. Desarrollar el capitulo 2 del TFG.
6. Crear graficas y tablas para el capitulo de resultados.
7. Implementar backtesting mensual.
8. Ampliar inferencia para predecir el dia completo.

