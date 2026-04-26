# Capítulo 20. Bibliografía y referencias

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 20.1. Documentación de OMIE

OMIE es la fuente principal de datos de precio utilizada en el proyecto. La aplicación descarga ficheros públicos `MARGINALPDBC`, que contienen precios marginales del mercado diario. Estos datos permiten construir la variable objetivo `marginal_es`.

Referencias recomendadas:

- OMIE. Página oficial del operador del mercado ibérico de energía.
- OMIE. Ficheros de resultados del mercado diario.
- OMIE. Documentación y formatos de ficheros públicos.

En el proyecto se usa el endpoint público de descarga:

```text
https://www.omie.es/es/file-download
```

Y ficheros con patrón:

```text
marginalpdbc_YYYYMMDD.1
```

Estas referencias deben citarse para justificar el origen oficial de la serie de precios.

### 20.2. Documentación de ESIOS/REE

ESIOS, gestionado por Red Eléctrica, se utiliza como fuente opcional de variables externas. En concreto, se emplean indicadores de previsión eólica, solar fotovoltaica y solar térmica.

Indicadores usados:

```text
541 -> previsión eólica
542 -> previsión solar fotovoltaica
543 -> previsión solar térmica
```

Referencias recomendadas:

- Red Eléctrica. Sistema de Información del Operador del Sistema, ESIOS.
- Documentación API ESIOS.
- Listado oficial de indicadores ESIOS.

Estas referencias son necesarias para explicar la procedencia de las variables renovables y el motivo por el que se requiere un token de acceso.

### 20.3. Documentación de scikit-learn

scikit-learn es la biblioteca principal utilizada para los modelos de aprendizaje automático. El proyecto utiliza `RidgeCV`, `MLPRegressor`, `HistGradientBoostingRegressor`, pipelines, escaladores y métricas.

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
- Documentación de modelos lineales.
- Documentación de redes neuronales supervisadas.
- Documentación de ensemble methods y gradient boosting.
- Documentación de métricas de regresión.

Estas referencias permiten justificar técnicamente los modelos y métricas empleados.

### 20.4. Bibliografía sobre predicción de precios eléctricos

La predicción de precios eléctricos es un campo amplio que combina economía energética, series temporales y aprendizaje automático. La literatura suele estudiar modelos estadísticos, redes neuronales, métodos de ensemble, modelos híbridos y variables exógenas.

Temás bibliograficos recomendados:

- Electricity price forecasting.
- Short-term electricity price forecasting.
- Day-ahead market price forecasting.
- Machine learning for electricity markets.
- Forecasting in renewable-intensive power systems.

En la memoria final conviene incluir articulos académicos que revisen el estado del arte y comparen modelos. También es útil citar trabajos sobre mercados con alta penetración renovable, ya que el mercado eléctrico español está cada vez más influido por eólica y solar.

### 20.5. Bibliografía sobre series temporales

El proyecto se basa en tratar el precio eléctrico como una serie temporal. Por ello, debe apoyarse en bibliografía sobre retardos, autocorrelación, estacionalidad, validación temporal y backtesting.

Conceptos relevantes:

- series temporales
- estacionariedad
- autocorrelación
- estacionalidad diaria, semanal y anual
- validación temporal
- ventanas deslizantes
- backtesting

Referencias recomendadas:

- libros introductorios de series temporales
- documentación sobre modelos ARIMA y SARIMA
- textos sobre forecasting aplicado
- recursos sobre evaluación temporal sin fuga de información

Estas referencias permiten fundamentar decisiones como usar retardos, medias móviles y separación temporal entre entrenamiento y validación.

### 20.6. Bibliografía sobre aprendizaje automático

El proyecto utiliza aprendizaje supervisado de regresión. La bibliografía debe cubrir conceptos generales como entrenamiento, validación, sobreajuste, regularización, métricas, modelos lineales, redes neuronales y modelos de árboles.

Conceptos relevantes:

- aprendizaje supervisado
- regresión
- regularización
- sobreajuste
- escalado de variables
- redes neuronales multicapa
- gradient boosting
- métricas MAE, RMSE y R2

Referencias recomendadas:

- libros generales de machine learning
- documentación de scikit-learn
- recursos académicos sobre modelos de regresión
- textos sobre interpretabilidad y evaluación de modelos

La bibliografía final debería combinar referencias oficiales de herramientas, fuentes de datos y articulos académicos sobre predicción de precios eléctricos. Esta combinación permite justificar tanto el origen de los datos como las decisiones metodológicas y técnicas.
