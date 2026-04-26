# Prediccion del precio electrico espanol con OMIE

Proyecto para estimar el precio del mercado diario electrico espanol usando datos publicos de OMIE. Incluye una interfaz grafica para ejecutar el flujo completo y comandos de consola para automatizar cada fase.

El proyecto descarga precios, prepara una serie temporal supervisada, entrena varios modelos, compara metricas y genera una prediccion para el siguiente periodo disponible.

## Resumen

- Fuente: ficheros publicos `MARGINALPDBC` de OMIE.
- Objetivo: `marginal_es`, precio marginal espanol en EUR/MWh.
- Modelos candidatos: `RidgeCV`, `MLPRegressor` y `HistGradientBoostingRegressor`.
- Seleccion: puedes elegir un modelo concreto o usar `auto` para guardar el candidato con menor MAE.
- Interfaz: ventana con fases de extraccion, preparacion, entrenamiento, test e inferencia.
- Salida principal: `models/omie_model.joblib` y `models/validation_plot.png`.

## Arranque rapido

Crear entorno virtual e instalar el proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Abrir la interfaz grafica:

```bash
omie-price-gui
```

Tambien funciona con:

```bash
python -m omie_price_nn.gui
```

En la ventana puedes elegir el modelo y ejecutar las fases una a una o pulsar `Ejecutar todo`.

## Interfaz grafica

La interfaz esta pensada para ver claramente el ciclo del modelo:

1. `Extraccion`: descarga datos diarios de OMIE y los guarda en cache.
2. `Preparacion`: genera variables temporales y retardos para entrenamiento.
3. `Entrenamiento + test`: entrena el modelo seleccionado, valida y muestra metricas.
4. `Inferencia`: predice el siguiente periodo despues del ultimo dato disponible.
5. `Abrir grafica`: abre la comparacion entre valores reales, modelo y baseline.

El desplegable `Modelo` permite elegir:

- `auto`: entrena los tres candidatos y guarda el de menor MAE.
- `ridge`: entrena solo `RidgeCV`.
- `mlp`: entrena solo la red neuronal `MLPRegressor`.
- `hist_gradient_boosting`: entrena solo `HistGradientBoostingRegressor`.

Los logs de la ventana muestran el progreso, metricas, errores y artefactos generados.

## Uso por consola

Entrenar con un ano de datos:

```bash
omie-price-train --start 2024-01-01 --end 2024-12-31
```

Elegir un modelo concreto:

```bash
omie-price-train --start 2024-01-01 --end 2024-12-31 --model mlp
```

Equivalente con modulo Python:

```bash
python -m omie_price_nn.train --start 2024-01-01 --end 2024-12-31 --model auto
```

Predecir el siguiente periodo:

```bash
omie-price-predict
```

Equivalente:

```bash
python -m omie_price_nn.predict
```

## Datos OMIE

El proyecto usa el fichero diario `MARGINALPDBC`:

```text
https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_YYYYMMDD.1
```

Formato esperado:

```text
anio;mes;dia;periodo;marginal_pt;marginal_es;
```

El parser soporta datos horarios y tambien periodos recientes de 15 minutos cuando el fichero tiene mas de 25 periodos por dia.

## Flujo interno

Durante el entrenamiento:

1. Descarga los ficheros diarios de OMIE.
2. Guarda los originales en `data/raw/`.
3. Genera `data/processed/omie_prices.csv`.
4. Crea variables de calendario, retardos, medias moviles y cambios recientes.
5. Entrena el modelo elegido, o todos si la seleccion es `auto`.
6. Evalua con validacion temporal, sin mezclar futuro con pasado.
7. Guarda el modelo seleccionado en `models/omie_model.joblib`.
8. Guarda la grafica de validacion en `models/validation_plot.png`.

## Estructura

```text
.
├── data/
│   ├── raw/                 # ficheros originales descargados de OMIE
│   └── processed/           # CSV limpios y dataset preparado
├── models/                  # modelo entrenado y grafica de validacion
├── src/omie_price_nn/
│   ├── data.py              # descarga y parseo de OMIE
│   ├── features.py          # variables temporales y retardos
│   ├── train.py             # entrenamiento y seleccion del mejor candidato
│   ├── predict.py           # inferencia con el modelo entrenado
│   └── gui.py               # interfaz grafica
├── requirements.txt
└── pyproject.toml
```

## Artefactos generados

- `data/raw/`: ficheros OMIE originales cacheados.
- `data/processed/omie_prices.csv`: precios limpios.
- `data/processed/omie_features.csv`: dataset supervisado generado desde la GUI.
- `models/omie_model.joblib`: mejor modelo entrenado.
- `models/validation_plot.png`: grafica de validacion.

## Variables del modelo

Los modelos usan informacion historica derivada del propio precio:

- momento del dia
- dia de la semana
- mes
- indicador de fin de semana
- precios retardados de 1, 2, 3, 4, 5, 6, 12, 23, 24, 25, 48, 72, 168 y 336 periodos
- medias y desviaciones moviles de 3, 6, 12, 24, 48 y 168 periodos
- minimos y maximos moviles de 24 y 168 periodos
- diferencias frente al periodo anterior, el dia anterior y la semana anterior
- ratios frente al dia anterior y la semana anterior

## Metricas

El entrenamiento muestra:

```text
MAE: error absoluto medio en EUR/MWh. Mas bajo es mejor.
RMSE: penaliza mas los errores grandes. Mas bajo es mejor.
R2: proporcion de variacion explicada. Mas cercano a 1 es mejor.
Baseline lag 24 MAE: comparacion contra usar el precio de 24 periodos antes.
```

Ejemplo real con datos de `2025-01-01` a `2025-03-31`:

```text
Mejor modelo: ridge
MAE: 10.02 EUR/MWh
RMSE: 15.70 EUR/MWh
R2: 0.871
Baseline lag 24 MAE: 20.97 EUR/MWh
```

## Limitaciones

El modelo actual no usa factores externos. Para mejorar precision seria razonable anadir:

- demanda prevista
- produccion eolica y solar
- temperatura y meteorologia
- precio del gas
- derechos de CO2
- indisponibilidades de generacion
- interconexiones
- restricciones tecnicas e intradiario

Por eso las predicciones deben interpretarse como un ejercicio de aprendizaje y no como una senal fiable para decisiones economicas.

## Problemas frecuentes

### No se abre la interfaz grafica

Comprueba que estas dentro del entorno virtual y que instalaste el paquete:

```bash
source .venv/bin/activate
pip install -e .
omie-price-gui
```

### No descarga datos de OMIE

Comprueba que hay conexion a internet y que OMIE responde para la fecha elegida. Los datos se descargan desde `www.omie.es`.

### Hay pocos datos para entrenar

Usa un rango mayor. El proyecto crea retardos de hasta 336 periodos y exige al menos 700 filas utiles despues de construir variables, asi que funciona mejor con varios meses.

### Quiero repetir el entrenamiento desde cero

Puedes borrar los artefactos generados:

```bash
rm -f data/processed/omie_prices.csv data/processed/omie_features.csv
rm -f models/omie_model.joblib models/validation_plot.png
```

Los ficheros en `data/raw/` se pueden conservar como cache para no volver a descargarlos.

## Ideas de mejora

- Anadir datos de demanda y generacion de REE/ESIOS.
- Incluir variables meteorologicas por zona.
- Probar modelos especificos para series temporales.
- Separar validacion por meses completos.
- Guardar historico de experimentos con parametros y metricas.
- Crear un notebook de analisis exploratorio.
