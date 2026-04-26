# ⚡ OMIE v2 Python - Prediccion del precio electrico espanol

Proyecto en Python para **descargar datos publicos de OMIE**, preparar una serie temporal supervisada y entrenar modelos capaces de estimar el precio del mercado diario electrico espanol.

Incluye:

- 🖥️ Interfaz grafica con fases visibles del flujo.
- 🧠 Seleccion de modelo: `auto`, `ridge`, `mlp` o `hist_gradient_boosting`.
- 📊 Validacion temporal con metricas `MAE`, `RMSE` y `R2`.
- 🔮 Inferencia del siguiente periodo disponible.
- 🌬️☀️ Variables opcionales de prevision eolica y solar desde ESIOS/REE.
- 🧰 Comandos CLI para automatizar entrenamiento y prediccion.

> ⚠️ Este proyecto es educativo/experimental. No debe usarse como senal fiable para decisiones economicas o de trading energetico.

## 📚 Tabla de contenidos

- [Resumen](#-resumen)
- [Arquitectura del flujo](#-arquitectura-del-flujo)
- [Instalacion](#-instalacion)
- [Uso con interfaz grafica](#-uso-con-interfaz-grafica)
- [Uso por consola](#-uso-por-consola)
- [Modelos disponibles](#-modelos-disponibles)
- [Datos de OMIE](#-datos-de-omie)
- [Datos eolicos y solares de ESIOS](#-datos-eolicos-y-solares-de-esios)
- [Variables del modelo](#-variables-del-modelo)
- [Metricas](#-metricas)
- [Artefactos generados](#-artefactos-generados)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [GitHub con SSH](#-github-con-ssh)
- [Problemas frecuentes](#-problemas-frecuentes)
- [Ideas de mejora](#-ideas-de-mejora)
- [Referencias](#-referencias)

## 🚀 Resumen

El proyecto trabaja con el precio marginal espanol publicado por OMIE:

- **Fuente:** ficheros publicos `MARGINALPDBC`.
- **Objetivo:** `marginal_es`, precio marginal espanol en `EUR/MWh`.
- **Frecuencia:** horaria y preparada para periodos de 15 minutos cuando OMIE los publique en el fichero.
- **Modelos:** `RidgeCV`, `MLPRegressor`, `HistGradientBoostingRegressor`.
- **Modo recomendado:** `auto`, que prueba los tres modelos y guarda el que obtiene menor `MAE`.
- **Variables externas opcionales:** prevision eolica y solar desde ESIOS/REE.
- **Salida principal:** `models/omie_model.joblib`.
- **Grafica:** `models/validation_plot.png`.

## 🧭 Arquitectura del flujo

```text
OMIE
  ↓
Extraccion de datos
  ↓
data/raw/*.1
  ↓
Preparacion y limpieza
  ↓
data/processed/omie_prices.csv
  ↑
  │ opcional
  │
ESIOS/REE
  ↓
prevision eolica + solar
  ↓
Feature engineering
  ↓
lags + calendario + medias moviles + volatilidad + renovables opcionales
  ↓
Entrenamiento / test
  ↓
RidgeCV | MLPRegressor | HistGradientBoostingRegressor
  ↓
models/omie_model.joblib
  ↓
Inferencia siguiente periodo
```

## 🛠️ Instalacion

Extraer el repositorio de github

```bash
git clone [proyecto-github]
cd [dir-project]
```

Desde la carpeta del proyecto [dir-project]:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Comprobar que los comandos estan disponibles:

```bash
omie-price-train --help
omie-price-predict --help
```

## 🖥️ Uso con interfaz grafica

Abrir la aplicacion:

```bash
source .venv/bin/activate
omie-price-gui
```

Alternativa:

```bash
python -m omie_price_nn.gui
```

La ventana permite ejecutar las fases del modelo:

1. 📥 **Extraccion:** descarga datos diarios de OMIE.
2. 🧹 **Preparacion:** genera el dataset supervisado.
3. 🧠 **Entrenamiento + test:** entrena el modelo elegido y calcula metricas.
4. 🔮 **Inferencia:** predice el siguiente periodo.
5. 📈 **Abrir grafica:** abre la grafica de validacion.

Si marcas **ESIOS**, la extraccion tambien anade prevision eolica y solar. Para ello necesitas indicar un token en el campo **Token ESIOS** o exportar la variable `ESIOS_TOKEN`.

Flujo recomendado con ESIOS en la GUI:

1. Escribe fechas de inicio y fin.
2. Marca `ESIOS`.
3. Pega tu token en `Token ESIOS`.
4. Elige `auto` o un modelo concreto.
5. Pulsa `Ejecutar todo`.

### Selector de modelo

En el desplegable **Modelo** puedes elegir:

| Opcion | Que hace |
|---|---|
| `auto` | Entrena los tres modelos y guarda el que obtiene menor `MAE`. |
| `ridge` | Entrena solo `RidgeCV`. |
| `mlp` | Entrena solo la red neuronal `MLPRegressor`. |
| `hist_gradient_boosting` | Entrena solo `HistGradientBoostingRegressor`. |

## ⌨️ Uso por consola

Entrenar en modo automatico:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Entrenar solo la red neuronal:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model mlp
```

Entrenar solo Ridge:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model ridge
```

Entrenar solo Gradient Boosting:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model hist_gradient_boosting
```

Entrenar anadiendo prevision eolica/solar de ESIOS:

```bash
export ESIOS_TOKEN="tu_token_esios"
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios
```

Tambien puedes pasar el token directamente:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios --esios-token "tu_token_esios"
```

Predecir el siguiente periodo con el modelo guardado:

```bash
omie-price-predict
```

Tambien puedes usar los modulos directamente:

```bash
python -m omie_price_nn.train --start 2025-01-01 --end 2025-03-31 --model auto
python -m omie_price_nn.predict
```

## 🧠 Modelos disponibles

El proyecto permite elegir entre cuatro opciones de entrenamiento. Tres son modelos concretos y una (`auto`) es un modo de seleccion automatica.

| Opcion | Tipo | Cuándo usarla |
|---|---|---|
| `auto` | Selector automatico | Recomendado para empezar. Prueba todos y guarda el mejor por `MAE`. |
| `ridge` | Regresion lineal regularizada | Buena opcion rapida, estable e interpretable. |
| `mlp` | Red neuronal densa | Util para probar relaciones no lineales con una red sencilla. |
| `hist_gradient_boosting` | Arboles con boosting | Bueno para capturar no linealidades y cambios bruscos. |

### 🤖 `auto`

`auto` no es un modelo en si, sino un modo de entrenamiento. Ejecuta los tres candidatos (`ridge`, `mlp` y `hist_gradient_boosting`), calcula metricas sobre el tramo de validacion temporal y guarda el que obtiene menor `MAE`.

Es la opcion mas comoda cuando no sabes aun que modelo ira mejor para un rango de fechas concreto.

Ventajas:

- compara modelos con el mismo dataset
- evita elegir a mano antes de medir
- guarda automaticamente el mejor candidato
- muestra las metricas de todos los modelos entrenados

Inconvenientes:

- tarda mas porque entrena tres modelos
- el modelo elegido puede cambiar si cambias el rango de fechas
- no sustituye a una validacion mas profunda por meses, estaciones o anos

Ejemplo:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

### 📐 `ridge`

`ridge` usa `RidgeCV`, una regresion lineal con regularizacion L2. En palabras simples: intenta explicar el precio como una combinacion ponderada de las variables disponibles, pero evita que los pesos crezcan demasiado. Eso ayuda a reducir sobreajuste.

En este proyecto suele ser fuerte porque muchas variables ya resumen muy bien la historia reciente del precio: retardos, medias moviles, diferencias y ciclos de calendario.

Ventajas:

- muy rapido de entrenar
- estable con datasets medianos
- menos propenso a sobreajustar que una regresion lineal normal
- buena baseline seria para series temporales con muchas variables historicas

Inconvenientes:

- aprende relaciones principalmente lineales
- puede quedarse corto ante cambios de regimen o patrones muy no lineales
- depende mucho de que las variables creadas sean buenas

Ejemplo:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model ridge
```

### 🧠 `mlp`

`mlp` usa `MLPRegressor`, una red neuronal feed-forward sencilla. En este proyecto tiene capas densas y aprende a combinar las variables historicas para aproximar el precio.

Es el modelo mas cercano a la idea inicial de "red neuronal". Puede aprender relaciones no lineales, por ejemplo interacciones entre hora del dia, precio del dia anterior y volatilidad reciente.

Ventajas:

- puede capturar relaciones no lineales
- permite experimentar con arquitectura neuronal sencilla
- puede mejorar si se anaden mas datos y variables externas

Inconvenientes:

- tarda mas que `ridge`
- puede ser mas sensible a escalado, ruido y rango de fechas
- necesita suficientes datos para generalizar bien
- sus resultados pueden ser menos interpretables

Ejemplo:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model mlp
```

### 🌲 `hist_gradient_boosting`

`hist_gradient_boosting` usa `HistGradientBoostingRegressor`, un modelo basado en arboles de decision entrenados de forma secuencial. Cada arbol intenta corregir errores cometidos por los anteriores.

Es util cuando hay relaciones no lineales, umbrales o cambios bruscos. Por ejemplo, puede aprender comportamientos distintos para fines de semana, horas valle, horas punta o situaciones de alta volatilidad.

Ventajas:

- captura no linealidades sin necesitar mucho preprocesado
- suele funcionar bien con variables tabulares
- puede detectar interacciones entre variables
- es competitivo como modelo practico de machine learning clasico

Inconvenientes:

- menos interpretable que `ridge`
- puede sobreajustar si se aumenta demasiado la complejidad
- no extrapola tendencias lineales tan naturalmente como una regresion
- puede necesitar ajuste fino de hiperparametros

Ejemplo:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model hist_gradient_boosting
```

### 🧪 Comparacion recomendada

Para comparar modelos de forma justa, usa el mismo rango de fechas:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model ridge
omie-price-train --start 2025-01-01 --end 2025-03-31 --model mlp
omie-price-train --start 2025-01-01 --end 2025-03-31 --model hist_gradient_boosting
```

O deja que el proyecto lo haga automaticamente:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

En pruebas con datos reales de `2025-01-01` a `2025-03-31`, `ridge` fue el mejor de los tres por `MAE`, pero esto puede cambiar al usar otros anos, meses o datos externos.

## 📦 Datos de OMIE

El proyecto descarga ficheros `MARGINALPDBC` desde OMIE:

```text
https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_YYYYMMDD.1
```

Formato esperado:

```text
anio;mes;dia;periodo;marginal_pt;marginal_es;
```

Campos relevantes:

- `periodo`: periodo horario o cuarto-horario.
- `marginal_pt`: precio marginal Portugal.
- `marginal_es`: precio marginal Espana, usado como objetivo.

## 🌬️☀️ Datos eolicos y solares de ESIOS

ESIOS es la API de datos del sistema electrico de Red Electrica. El proyecto puede usar previsiones de eolica y solar como variables externas del modelo.

La motivacion es sencilla: el precio electrico no depende solo de su propia historia. Una alta prevision solar o eolica suele presionar precios a la baja, mientras que baja renovable puede coincidir con precios mas altos, especialmente si hay demanda elevada.

### Indicadores usados

El programa usa tres indicadores de prevision:

| Indicador | Columna generada | Descripcion |
|---|---|---|
| `541` | `wind_forecast_mwh` | Prevision de produccion eolica nacional peninsular. |
| `542` | `solar_pv_forecast_mwh` | Generacion prevista solar fotovoltaica. |
| `543` | `solar_thermal_forecast_mwh` | Generacion prevista solar termica. |

### Columnas derivadas

Ademas de las tres columnas originales, se crean variables agregadas:

- `solar_forecast_mwh`
- `renewable_forecast_mwh`
- `wind_solar_ratio`

Estas columnas se unen al dataset OMIE por `timestamp`. Si OMIE tiene periodos de 15 minutos y ESIOS viene horario, el programa usa la ultima prevision disponible dentro de una tolerancia de una hora.

### Configurar token

Necesitas un token de ESIOS. Puedes pasarlo de dos formas.

Opcion 1, variable de entorno:

```bash
export ESIOS_TOKEN="tu_token_esios"
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios
```

Opcion 2, argumento del comando:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios --esios-token "tu_token_esios"
```

Si activas `--include-esios` sin token, el programa falla antes de modificar los datos.

### Que cambia en el modelo

Sin ESIOS, el modelo aprende solo de calendario y precio historico. Con ESIOS, tambien ve cuanta eolica y solar se espera para cada periodo.

Esto puede ayudar a capturar situaciones como:

- muchas horas solares con precios bajos
- baja eolica con precios altos
- cambios rapidos de renovable disponible
- diferencias entre dias laborales, fines de semana y festivos con mucha renovable

Los datos ESIOS se cachean en `data/processed/esios_generation_YYYYMMDD_YYYYMMDD.csv`.

### Importante para inferencia

Si entrenas un modelo con ESIOS, el CSV usado en inferencia debe conservar esas columnas externas. El flujo normal lo hace automaticamente porque guarda el dataset enriquecido en:

```text
data/processed/omie_prices.csv
```

## 🧪 Variables del modelo

Los modelos siempre aprenden a partir de informacion historica del propio precio:

- 🕒 momento del dia
- 📅 dia de la semana
- 🗓️ mes
- 🛌 indicador de fin de semana
- ⏪ precios retardados de `1`, `2`, `3`, `4`, `5`, `6`, `12`, `23`, `24`, `25`, `48`, `72`, `168` y `336` periodos
- 📉 medias moviles de `3`, `6`, `12`, `24`, `48` y `168` periodos
- 📊 desviaciones moviles de `3`, `6`, `12`, `24`, `48` y `168` periodos
- 🔻 minimos y maximos moviles de `24` y `168` periodos
- 🔁 diferencias frente al periodo anterior, el dia anterior y la semana anterior
- ➗ ratios frente al dia anterior y la semana anterior

Si activas ESIOS, se anaden tambien:

- 🌬️ `wind_forecast_mwh`
- ☀️ `solar_pv_forecast_mwh`
- 🌞 `solar_thermal_forecast_mwh`
- ♻️ `renewable_forecast_mwh`
- ☀️ `solar_forecast_mwh`
- ⚖️ `wind_solar_ratio`

## 📏 Metricas

Durante el test se calculan:

| Metrica | Significado | Interpretacion |
|---|---|---|
| `MAE` | Error absoluto medio en `EUR/MWh`. | Mas bajo es mejor. |
| `RMSE` | Penaliza mas los errores grandes. | Mas bajo es mejor. |
| `R2` | Proporcion de variacion explicada. | Mas cercano a `1` es mejor. |
| `Baseline lag 24 MAE` | Error usando el precio de 24 periodos antes. | Sirve como comparacion simple. |

Ejemplo real con datos de `2025-01-01` a `2025-03-31`:

```text
Seleccion solicitada: auto
Mejor modelo: ridge
MAE: 10.02 EUR/MWh
RMSE: 15.70 EUR/MWh
R2: 0.871
Baseline lag 24 MAE: 20.97 EUR/MWh
```

## 📁 Artefactos generados

| Ruta | Contenido |
|---|---|
| `data/raw/` | Ficheros originales descargados de OMIE. |
| `data/processed/omie_prices.csv` | Dataset limpio de precios. |
| `data/processed/omie_features.csv` | Dataset supervisado generado desde la GUI. |
| `data/processed/esios_generation_*.csv` | Cache de prevision eolica/solar de ESIOS. |
| `models/omie_model.joblib` | Modelo entrenado y serializado. |
| `models/validation_plot.png` | Grafica de validacion. |

Los datos, modelos y caches estan excluidos de Git mediante `.gitignore`.

## 🗂️ Estructura del proyecto

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── src/omie_price_nn/
│   ├── __init__.py
│   ├── data.py
│   ├── features.py
│   ├── gui.py
│   ├── predict.py
│   └── train.py
├── .gitignore
├── README.md
├── pyproject.toml
└── requirements.txt
```

## 🔐 GitHub con SSH

Para subir el proyecto a GitHub usando SSH:

```bash
ssh-keygen -t ed25519 -C "tu_email_de_github@example.com"
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
pbcopy < ~/.ssh/id_ed25519.pub
```

Despues pega la clave publica en:

```text
GitHub → Settings → SSH and GPG keys → New SSH key
```

Probar conexion:

```bash
ssh -T git@github.com
```

Configurar remoto SSH:

```bash
git remote set-url origin git@github.com:Ju4nC4r/omie_v2_python.git
git push -u origin main
```

## 🧯 Problemas frecuentes

### 🖥️ No se abre la interfaz grafica

Activa el entorno e instala el paquete local:

```bash
source .venv/bin/activate
pip install -e .
omie-price-gui
```

### 🌐 No descarga datos de OMIE

Comprueba que hay conexion a internet y que OMIE responde para la fecha elegida.

### ⏳ El entrenamiento parece parado

La GUI muestra barra de progreso y logs por candidato. Si entrenas `mlp`, puede tardar mas que `ridge`.

### 📉 Hay pocos datos para entrenar

El proyecto usa retardos de hasta `336` periodos y exige al menos `700` filas utiles despues de construir variables. Usa varios meses de datos.

### 🧹 Repetir entrenamiento desde cero

Puedes borrar artefactos generados:

```bash
rm -f data/processed/omie_prices.csv data/processed/omie_features.csv
rm -f models/omie_model.joblib models/validation_plot.png
```

Conservar `data/raw/` evita descargar otra vez los ficheros ya cacheados.

## 🧭 Ideas de mejora

- 🌡️ Anadir meteorologia por zona.
- ⚡ Incorporar demanda y generacion de REE/ESIOS.
- ☀️ Separar variables de solar, eolica, hidraulica y nuclear.
- 🌍 Incluir gas, CO2 e interconexiones.
- 🧪 Guardar historico de experimentos y parametros.
- 📓 Crear notebooks de analisis exploratorio.
- 🧠 Probar modelos especificos de series temporales.

## 🔎 Referencias

- [Documentacion API ESIOS](https://api.esios.ree.es/doc/)
- [Listado de indicadores ESIOS](https://api.esios.ree.es/documents/658/download?locale=en)
- [OMIE](https://www.omie.es/)
