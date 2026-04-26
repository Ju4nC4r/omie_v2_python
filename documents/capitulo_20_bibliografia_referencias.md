# Capitulo 20. Bibliografia y referencias

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 20.1. Documentacion de OMIE

OMIE es la fuente principal de datos de precio utilizada en el proyecto. La aplicacion descarga ficheros publicos `MARGINALPDBC`, que contienen precios marginales del mercado diario. Estos datos permiten construir la variable objetivo `marginal_es`.

Referencias recomendadas:

- OMIE. Pagina oficial del operador del mercado iberico de energia.
- OMIE. Ficheros de resultados del mercado diario.
- OMIE. Documentacion y formatos de ficheros publicos.

En el proyecto se usa el endpoint publico de descarga:

```text
https://www.omie.es/es/file-download
```

Y ficheros con patron:

```text
marginalpdbc_YYYYMMDD.1
```

Estas referencias deben citarse para justificar el origen oficial de la serie de precios.

### 20.2. Documentacion de ESIOS/REE

ESIOS, gestionado por Red Electrica, se utiliza como fuente opcional de variables externas. En concreto, se emplean indicadores de prevision eolica, solar fotovoltaica y solar termica.

Indicadores usados:

```text
541 -> prevision eolica
542 -> prevision solar fotovoltaica
543 -> prevision solar termica
```

Referencias recomendadas:

- Red Electrica. Sistema de Informacion del Operador del Sistema, ESIOS.
- Documentacion API ESIOS.
- Listado oficial de indicadores ESIOS.

Estas referencias son necesarias para explicar la procedencia de las variables renovables y el motivo por el que se requiere un token de acceso.

### 20.3. Documentacion de scikit-learn

scikit-learn es la biblioteca principal utilizada para los modelos de aprendizaje automatico. El proyecto utiliza `RidgeCV`, `MLPRegressor`, `HistGradientBoostingRegressor`, pipelines, escaladores y metricas.

Componentes usados:

- `RidgeCV`
- `MLPRegressor`
- `HistGradientBoostingRegressor`
- `RobustScaler`
- `StandardScaler`
- `TransformedTargetRegressor`
- `mean_absolute_error`
- `root_mean_squared_error`
- `r2_score`

Referencias recomendadas:

- scikit-learn. User Guide.
- scikit-learn. API Reference.
- Documentacion de modelos lineales.
- Documentacion de redes neuronales supervisadas.
- Documentacion de ensemble methods y gradient boosting.
- Documentacion de metricas de regresion.

Estas referencias permiten justificar tecnicamente los modelos y metricas empleados.

### 20.4. Bibliografia sobre prediccion de precios electricos

La prediccion de precios electricos es un campo amplio que combina economia energetica, series temporales y aprendizaje automatico. La literatura suele estudiar modelos estadisticos, redes neuronales, metodos de ensemble, modelos hibridos y variables exogenas.

Temas bibliograficos recomendados:

- Electricity price forecasting.
- Short-term electricity price forecasting.
- Day-ahead market price forecasting.
- Machine learning for electricity markets.
- Forecasting in renewable-intensive power systems.

En la memoria final conviene incluir articulos academicos que revisen el estado del arte y comparen modelos. Tambien es util citar trabajos sobre mercados con alta penetracion renovable, ya que el mercado electrico espanol esta cada vez mas influido por eolica y solar.

### 20.5. Bibliografia sobre series temporales

El proyecto se basa en tratar el precio electrico como una serie temporal. Por ello, debe apoyarse en bibliografia sobre retardos, autocorrelacion, estacionalidad, validacion temporal y backtesting.

Conceptos relevantes:

- series temporales
- estacionariedad
- autocorrelacion
- estacionalidad diaria, semanal y anual
- validacion temporal
- ventanas deslizantes
- backtesting

Referencias recomendadas:

- libros introductorios de series temporales
- documentacion sobre modelos ARIMA y SARIMA
- textos sobre forecasting aplicado
- recursos sobre evaluacion temporal sin fuga de informacion

Estas referencias permiten fundamentar decisiones como usar retardos, medias moviles y separacion temporal entre entrenamiento y validacion.

### 20.6. Bibliografia sobre aprendizaje automatico

El proyecto utiliza aprendizaje supervisado de regresion. La bibliografia debe cubrir conceptos generales como entrenamiento, validacion, sobreajuste, regularizacion, metricas, modelos lineales, redes neuronales y modelos de arboles.

Conceptos relevantes:

- aprendizaje supervisado
- regresion
- regularizacion
- sobreajuste
- escalado de variables
- redes neuronales multicapa
- gradient boosting
- metricas MAE, RMSE y R2

Referencias recomendadas:

- libros generales de machine learning
- documentacion de scikit-learn
- recursos academicos sobre modelos de regresion
- textos sobre interpretabilidad y evaluacion de modelos

La bibliografia final deberia combinar referencias oficiales de herramientas, fuentes de datos y articulos academicos sobre prediccion de precios electricos. Esta combinacion permite justificar tanto el origen de los datos como las decisiones metodologicas y tecnicas.
