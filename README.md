# ⚡ OMIE v2 Python - Prediccion del precio electrico espanol

Proyecto en Python para **descargar datos publicos de OMIE**, preparar una serie temporal supervisada y entrenar modelos capaces de estimar el precio del mercado diario electrico espanol.

Incluye:

- 🖥️ Interfaz grafica con fases visibles del flujo.
- 🧠 Seleccion de modelo: `auto`, `ridge`, `mlp` o `hist_gradient_boosting`.
- 📊 Validacion temporal con metricas `MAE`, `RMSE` y `R2`.
- 🔮 Inferencia del siguiente periodo disponible.
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
- [Variables del modelo](#-variables-del-modelo)
- [Metricas](#-metricas)
- [Artefactos generados](#-artefactos-generados)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [GitHub con SSH](#-github-con-ssh)
- [Problemas frecuentes](#-problemas-frecuentes)
- [Ideas de mejora](#-ideas-de-mejora)

## 🚀 Resumen

El proyecto trabaja con el precio marginal espanol publicado por OMIE:

- **Fuente:** ficheros publicos `MARGINALPDBC`.
- **Objetivo:** `marginal_es`, precio marginal espanol en `EUR/MWh`.
- **Frecuencia:** horaria y preparada para periodos de 15 minutos cuando OMIE los publique en el fichero.
- **Modelos:** `RidgeCV`, `MLPRegressor`, `HistGradientBoostingRegressor`.
- **Modo recomendado:** `auto`, que prueba los tres modelos y guarda el que obtiene menor `MAE`.
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
  ↓
Feature engineering
  ↓
lags + calendario + medias moviles + volatilidad
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

Desde la carpeta del proyecto:

```bash
cd /Users/juancarlos/temporal/kk
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

### `ridge`

`RidgeCV` es una regresion lineal regularizada. Es rapida, estable y suele funcionar bien cuando las variables historicas explican una parte importante del precio.

### `mlp`

`MLPRegressor` es una red neuronal sencilla con capas densas. Puede aprender relaciones no lineales, aunque necesita suficientes datos y puede tardar mas en entrenar.

### `hist_gradient_boosting`

`HistGradientBoostingRegressor` es un modelo de arboles con boosting. Suele capturar no linealidades y cambios de regimen mejor que una regresion lineal simple.

### `auto`

Entrena los tres candidatos, compara el `MAE` en validacion temporal y guarda el mejor.

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

## 🧪 Variables del modelo

Los modelos no usan todavia variables externas. Aprenden a partir de informacion historica del propio precio:

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
