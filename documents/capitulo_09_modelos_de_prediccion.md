# Capítulo 9. Modelos de predicción

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 9.1. Modelo baseline `lag 24`

El primer modelo de referencia utilizado en el proyecto es el baseline `lag 24`. Este baseline no es un modelo de aprendizaje automático entrenado, sino una regla sencilla que utiliza como predicción el precio observado 24 periodos antes. Su utilidad principal es proporcionar una referencia mínima contra la que comparar los modelos más avanzados.

En problemas de series temporales, un baseline es imprescindible. Sin una referencia simple, una métrica aislada puede parecer buena aunque el modelo no este aportando valor real. Por ejemplo, si el precio eléctrico presenta mucha persistencia temporal, una regla basada en el precio anterior podría obtener resultados razonables. El modelo de machine learning debe mejorar esa regla para justificar su complejidad.

El baseline `lag 24` se obtiene directamente de la matriz de variables, usando la columna `price_lag_24`. En datos horarios, esta variable representa aproximadamente el precio del mismo periodo del día anterior. Esto tiene sentido porque el mercado eléctrico muestra patrones diarios: las horas nocturnas, solares y punta tienden a repetirse parcialmente entre días consecutivos.

No obstante, existe una limitación importante. Cuando los datos son cuarto-horarios, 24 periodos equivalen a seis horas, no a un día completo. Por tanto, la interpretación de `lag 24` depende de la resolución temporal. En la versión actual se mantiene como baseline simple basado en periodos, pero una mejora futura sería definir un baseline basado en duración real, por ejemplo 24 horas.

En los experimentos realizados, el baseline fue claramente superado por los modelos entrenados. Esto confirma que las variables de calendario, retardos múltiples, ventanas móviles y modelos de aprendizaje automático aportan información adicional frente a una regla simple.

### 9.2. Regresión Ridge `RidgeCV`

El primer modelo entrenable incorporado es una regresión Ridge con selección de regularización mediante `RidgeCV`. Ridge es una extensión de la regresión lineal que penaliza coeficientes demasiado grandes. Esta penalización ayuda a reducir el sobreajuste y mejora la estabilidad cuando existen muchas variables correlacionadas.

En este proyecto, las variables de entrada incluyen numerosos retardos, medias móviles, desviaciones, diferencias y ratios. Muchas de estas variables están relacionadas entre si. Por ejemplo, `price_lag_24`, `price_roll_24_mean` y `price_diff_24` contienen información conectada con el comportamiento diario. En este contexto, una regresión lineal sin regularización podría producir coeficientes inestables. Ridge reduce ese riesgo.

La implementación utiliza un pipeline con `RobustScaler` y `TransformedTargetRegressor`. El escalado de variables mejora el comportamiento del modelo porque las entradas tienen magnitudes distintas. La transformación de la variable objetivo con `StandardScaler` ayuda a estabilizar el ajuste.

Los valores de alpha probados por `RidgeCV` son:

```text
0.1, 1.0, 10.0, 100.0
```

Ridge tiene varias ventajas. Es rápido, reproducible, relativamente interpretable y funciona bien con datasets de tamaño moderado. En el experimento de enero a marzo de 2025 fue el mejor modelo, con un MAE de `10.02 EUR/MWh`. Esto demuestra que un modelo lineal regularizado puede ser competitivo si las variables están bien construidas.

Su principal limitación es que modela relaciones lineales. Si el precio depende de interacciones complejas entre hora, renovables, volatilidad y nivel de precio, Ridge puede no capturarlas completamente. Aun así, es una excelente referencia entrenable.

### 9.3. Red neuronal `MLPRegressor`

La red neuronal del proyecto se implementa mediante `MLPRegressor`, un perceptrón multicapa de scikit-learn. Este modelo representa la idea inicial del proyecto: entrenar una red neuronal sencilla para inferir el precio del mercado eléctrico español.

La arquitectura utilizada tiene dos capas ocultas:

```text
64 neuronas
32 neuronas
```

La función de activación es `relu`, el optimizador es `adam` y se utiliza parada temprana. La parada temprana detiene el entrenamiento cuando el modelo deja de mejorar sobre una fracción de validación interna, lo que ayuda a reducir el sobreajuste. También se fija `random_state=42` para mejorar la reproducibilidad.

La red neuronal recibe variables tabulares, no secuencias completas. Es decir, no se alimenta con una ventana temporal en bruto, sino con variables ya construidas: calendario, ciclos, retardos, medias móviles, diferencias, ratios y, si procede, variables ESIOS. Esta decisión simplifica el modelo y permite integrarlo dentro del mismo pipeline que los demás algoritmos.

El MLP puede aprender relaciones no lineales. Por ejemplo, puede captar que una misma previsión solar tiene efectos distintos según la hora del día, o que un precio retardado alto tiene distinta interpretación según la volatilidad reciente. Esta flexibilidad es su principal ventaja.

Sin embargo, también presenta inconvenientes. Es más sensible a hiperparámetros, suele tardar más en entrenar y puede necesitar más datos para generalizar correctamente. En los experimentos realizados no siempre fue el mejor modelo: en enero-marzo de 2025 quedó por detrás de Ridge y boosting; con casi todo 2025 mejoró y obtuvo un MAE de `3.98 EUR/MWh`, aunque no supero a HistGradientBoosting.

### 9.4. Modelo `HistGradientBoostingRegressor`

El tercer modelo entrenable es `HistGradientBoostingRegressor`, un algoritmo basado en árboles de decisión y boosting. Este modelo construye árboles de forma secuencial, intentando corregir errores cometidos por los árboles anteriores. Es especialmente adecuado para datos tabulares con relaciones no lineales.

En el proyecto se configura con:

```text
loss = absolute_error
max_iter = 400
learning_rate = 0.04
max_leaf_nodes = 15
l2_regularization = 0.1
random_state = 42
```

La función de pérdida `absolute_error` está alineada con la métrica MAE, que es el criterio principal de selección del modo `auto`. El número de iteraciones y la tasa de aprendizaje buscan un equilibrio entre precisión y riesgo de sobreajuste. La regularización L2 ayuda a estabilizar el modelo.

Este modelo puede capturar umbrales e interacciones. Por ejemplo, puede aprender reglas no lineales relacionadas con horas solares, fines de semana, volatilidad alta o precios retardados extremos. Esta capacidad es valiosa en el mercado eléctrico, donde la relación entre variables y precio rara vez es puramente lineal.

En los experimentos con casi todo 2025, HistGradientBoosting fue el mejor candidato, con:

```text
MAE: 3.17 EUR/MWh
RMSE: 4.59 EUR/MWh
R2: 0.973
```

Su principal inconveniente es que resulta menos interpretable que Ridge. Aunque se pueden estudiar importancias de variables o dependencias parciales, la explicación directa es más difícil. Aun así, su rendimiento práctico justifica su inclusión.

### 9.5. Modo automático de selección de modelo

El modo `auto` no es un algoritmo predictivo, sino una estrategia de comparación. Cuando se selecciona, el sistema entrena los tres modelos candidatos: `ridge`, `mlp` e `hist_gradient_boosting`. Después evalúa cada uno sobre el mismo tramo de validación temporal y selecciona el que obtiene menor MAE.

Este enfoque evita elegir el modelo por intuición. El mercado eléctrico puede comportarse de forma distinta según el periodo de entrenamiento, la cantidad de datos y las variables disponibles. Por ello, el modelo ganador puede cambiar. De hecho, en enero-marzo de 2025 ganó Ridge, mientras que con casi todo 2025 ganó HistGradientBoosting.

El modo `auto` aporta comodidad y rigor. Comodidad porque el usuario ejecuta un solo entrenamiento. Rigor porque todos los candidatos se comparan con el mismo dataset y el mismo criterio. La aplicación guarda el mejor modelo en `models/omie_model.joblib`.

Su desventaja es el tiempo de ejecución. Entrenar tres modelos tarda más que entrenar uno. Por eso la GUI muestra logs de progreso por candidato, evitando que el usuario piense que el entrenamiento se ha quedado bloqueado.

### 9.6. Justificación de los modelos seleccionados

Los tres modelos seleccionados cubren enfoques complementarios. Ridge representa una aproximación lineal regularizada; MLP representa una red neuronal sencilla; HistGradientBoosting representa un modelo no lineal basado en árboles. Esta diversidad permite comparar familias distintas sin convertir el proyecto en un sistema excesivamente complejo.

La selección también responde al objetivo académico del Proyecto. No se busca solo obtener una métrica, sino entender cómo distintos enfoques se comportan ante el mismo problema. Ridge permite explicar la regularización; MLP introduce redes neuronales; boosting muestra la potencia de los modelos de árboles en datos tabulares.

Además, los tres modelos están disponibles en scikit-learn, lo que simplifica la implementación, instalación y reproducibilidad. Todos pueden entrenarse localmente sin depender de servicios externos ni GPUs.

### 9.7. Hiperparámetros utilizados

Los hiperparámetros principales se fijaron de forma conservadora. En Ridge se probaron cuatro valores de regularización mediante `RidgeCV`. En MLP se definió una arquitectura moderada de dos capas ocultas, regularización `alpha=0.01`, tasa inicial `0.0003`, `batch_size=64`, `max_iter=1500` y parada temprana. En HistGradientBoosting se usó aprendizaje lento, 400 iteraciones, 15 hojas máximas y regularización L2.

No se realizó una búsqueda exhaustiva de hiperparámetros. Esta decisión mantiene el proyecto comprensible y evita aumentar demasiado el coste computacional. Una línea futura sería incorporar `GridSearchCV`, `RandomizedSearchCV` o validación temporal cruzada para optimizar configuraciones.

### 9.8. Ventajas e inconvenientes de cada modelo

Ridge es rápido, estable e interpretable, pero limitado para relaciones no lineales. MLP es flexible y representa una red neuronal real, pero tarda más y es sensible a hiperparámetros. HistGradientBoosting captura relaciones no lineales y obtuvo el mejor resultado con más datos, pero es menos interpretable.

El baseline `lag 24` es muy simple y no requiere entrenamiento, pero no aprovecha toda la información disponible. Su valor está en servir como referencia.

El modo `auto` combina las ventajas de la comparación automática, pero aumenta el tiempo de entrenamiento. En conjunto, la aplicación ofrece un abanico equilibrado: una regla simple, un modelo lineal, una red neuronal, un modelo de boosting y un selector automático.
