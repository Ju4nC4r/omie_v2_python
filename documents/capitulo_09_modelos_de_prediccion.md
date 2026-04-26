# Capitulo 9. Modelos de prediccion

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 9.1. Modelo baseline `lag 24`

El primer modelo de referencia utilizado en el proyecto es el baseline `lag 24`. Este baseline no es un modelo de aprendizaje automatico entrenado, sino una regla sencilla que utiliza como prediccion el precio observado 24 periodos antes. Su utilidad principal es proporcionar una referencia minima contra la que comparar los modelos mas avanzados.

En problemas de series temporales, un baseline es imprescindible. Sin una referencia simple, una metrica aislada puede parecer buena aunque el modelo no este aportando valor real. Por ejemplo, si el precio electrico presenta mucha persistencia temporal, una regla basada en el precio anterior podria obtener resultados razonables. El modelo de machine learning debe mejorar esa regla para justificar su complejidad.

El baseline `lag 24` se obtiene directamente de la matriz de variables, usando la columna `price_lag_24`. En datos horarios, esta variable representa aproximadamente el precio del mismo periodo del dia anterior. Esto tiene sentido porque el mercado electrico muestra patrones diarios: las horas nocturnas, solares y punta tienden a repetirse parcialmente entre dias consecutivos.

No obstante, existe una limitacion importante. Cuando los datos son cuarto-horarios, 24 periodos equivalen a seis horas, no a un dia completo. Por tanto, la interpretacion de `lag 24` depende de la resolucion temporal. En la version actual se mantiene como baseline simple basado en periodos, pero una mejora futura seria definir un baseline basado en duracion real, por ejemplo 24 horas.

En los experimentos realizados, el baseline fue claramente superado por los modelos entrenados. Esto confirma que las variables de calendario, retardos multiples, ventanas moviles y modelos de aprendizaje automatico aportan informacion adicional frente a una regla simple.

### 9.2. Regresion Ridge `RidgeCV`

El primer modelo entrenable incorporado es una regresion Ridge con seleccion de regularizacion mediante `RidgeCV`. Ridge es una extension de la regresion lineal que penaliza coeficientes demasiado grandes. Esta penalizacion ayuda a reducir el sobreajuste y mejora la estabilidad cuando existen muchas variables correlacionadas.

En este proyecto, las variables de entrada incluyen numerosos retardos, medias moviles, desviaciones, diferencias y ratios. Muchas de estas variables estan relacionadas entre si. Por ejemplo, `price_lag_24`, `price_roll_24_mean` y `price_diff_24` contienen informacion conectada con el comportamiento diario. En este contexto, una regresion lineal sin regularizacion podria producir coeficientes inestables. Ridge reduce ese riesgo.

La implementacion utiliza un pipeline con `RobustScaler` y `TransformedTargetRegressor`. El escalado de variables mejora el comportamiento del modelo porque las entradas tienen magnitudes distintas. La transformacion de la variable objetivo con `StandardScaler` ayuda a estabilizar el ajuste.

Los valores de alpha probados por `RidgeCV` son:

```text
0.1, 1.0, 10.0, 100.0
```

Ridge tiene varias ventajas. Es rapido, reproducible, relativamente interpretable y funciona bien con datasets de tamano moderado. En el experimento de enero a marzo de 2025 fue el mejor modelo, con un MAE de `10.02 EUR/MWh`. Esto demuestra que un modelo lineal regularizado puede ser competitivo si las variables estan bien construidas.

Su principal limitacion es que modela relaciones lineales. Si el precio depende de interacciones complejas entre hora, renovables, volatilidad y nivel de precio, Ridge puede no capturarlas completamente. Aun asi, es una excelente referencia entrenable.

### 9.3. Red neuronal `MLPRegressor`

La red neuronal del proyecto se implementa mediante `MLPRegressor`, un perceptron multicapa de scikit-learn. Este modelo representa la idea inicial del proyecto: entrenar una red neuronal sencilla para inferir el precio del mercado electrico espanol.

La arquitectura utilizada tiene dos capas ocultas:

```text
64 neuronas
32 neuronas
```

La funcion de activacion es `relu`, el optimizador es `adam` y se utiliza parada temprana. La parada temprana detiene el entrenamiento cuando el modelo deja de mejorar sobre una fraccion de validacion interna, lo que ayuda a reducir el sobreajuste. Tambien se fija `random_state=42` para mejorar la reproducibilidad.

La red neuronal recibe variables tabulares, no secuencias completas. Es decir, no se alimenta con una ventana temporal en bruto, sino con variables ya construidas: calendario, ciclos, retardos, medias moviles, diferencias, ratios y, si procede, variables ESIOS. Esta decision simplifica el modelo y permite integrarlo dentro del mismo pipeline que los demas algoritmos.

El MLP puede aprender relaciones no lineales. Por ejemplo, puede captar que una misma prevision solar tiene efectos distintos segun la hora del dia, o que un precio retardado alto tiene distinta interpretacion segun la volatilidad reciente. Esta flexibilidad es su principal ventaja.

Sin embargo, tambien presenta inconvenientes. Es mas sensible a hiperparametros, suele tardar mas en entrenar y puede necesitar mas datos para generalizar correctamente. En los experimentos realizados no siempre fue el mejor modelo: en enero-marzo de 2025 quedo por detras de Ridge y boosting; con casi todo 2025 mejoro y obtuvo un MAE de `3.98 EUR/MWh`, aunque no supero a HistGradientBoosting.

### 9.4. Modelo `HistGradientBoostingRegressor`

El tercer modelo entrenable es `HistGradientBoostingRegressor`, un algoritmo basado en arboles de decision y boosting. Este modelo construye arboles de forma secuencial, intentando corregir errores cometidos por los arboles anteriores. Es especialmente adecuado para datos tabulares con relaciones no lineales.

En el proyecto se configura con:

```text
loss = absolute_error
max_iter = 400
learning_rate = 0.04
max_leaf_nodes = 15
l2_regularization = 0.1
random_state = 42
```

La funcion de perdida `absolute_error` esta alineada con la metrica MAE, que es el criterio principal de seleccion del modo `auto`. El numero de iteraciones y la tasa de aprendizaje buscan un equilibrio entre precision y riesgo de sobreajuste. La regularizacion L2 ayuda a estabilizar el modelo.

Este modelo puede capturar umbrales e interacciones. Por ejemplo, puede aprender reglas no lineales relacionadas con horas solares, fines de semana, volatilidad alta o precios retardados extremos. Esta capacidad es valiosa en el mercado electrico, donde la relacion entre variables y precio rara vez es puramente lineal.

En los experimentos con casi todo 2025, HistGradientBoosting fue el mejor candidato, con:

```text
MAE: 3.17 EUR/MWh
RMSE: 4.59 EUR/MWh
R2: 0.973
```

Su principal inconveniente es que resulta menos interpretable que Ridge. Aunque se pueden estudiar importancias de variables o dependencias parciales, la explicacion directa es mas dificil. Aun asi, su rendimiento practico justifica su inclusion.

### 9.5. Modo automatico de seleccion de modelo

El modo `auto` no es un algoritmo predictivo, sino una estrategia de comparacion. Cuando se selecciona, el sistema entrena los tres modelos candidatos: `ridge`, `mlp` e `hist_gradient_boosting`. Despues evalua cada uno sobre el mismo tramo de validacion temporal y selecciona el que obtiene menor MAE.

Este enfoque evita elegir el modelo por intuicion. El mercado electrico puede comportarse de forma distinta segun el periodo de entrenamiento, la cantidad de datos y las variables disponibles. Por ello, el modelo ganador puede cambiar. De hecho, en enero-marzo de 2025 gano Ridge, mientras que con casi todo 2025 gano HistGradientBoosting.

El modo `auto` aporta comodidad y rigor. Comodidad porque el usuario ejecuta un solo entrenamiento. Rigor porque todos los candidatos se comparan con el mismo dataset y el mismo criterio. La aplicacion guarda el mejor modelo en `models/omie_model.joblib`.

Su desventaja es el tiempo de ejecucion. Entrenar tres modelos tarda mas que entrenar uno. Por eso la GUI muestra logs de progreso por candidato, evitando que el usuario piense que el entrenamiento se ha quedado bloqueado.

### 9.6. Justificacion de los modelos seleccionados

Los tres modelos seleccionados cubren enfoques complementarios. Ridge representa una aproximacion lineal regularizada; MLP representa una red neuronal sencilla; HistGradientBoosting representa un modelo no lineal basado en arboles. Esta diversidad permite comparar familias distintas sin convertir el proyecto en un sistema excesivamente complejo.

La seleccion tambien responde al objetivo academico del TFG. No se busca solo obtener una metrica, sino entender como distintos enfoques se comportan ante el mismo problema. Ridge permite explicar la regularizacion; MLP introduce redes neuronales; boosting muestra la potencia de los modelos de arboles en datos tabulares.

Ademas, los tres modelos estan disponibles en scikit-learn, lo que simplifica la implementacion, instalacion y reproducibilidad. Todos pueden entrenarse localmente sin depender de servicios externos ni GPUs.

### 9.7. Hiperparametros utilizados

Los hiperparametros principales se fijaron de forma conservadora. En Ridge se probaron cuatro valores de regularizacion mediante `RidgeCV`. En MLP se definio una arquitectura moderada de dos capas ocultas, regularizacion `alpha=0.01`, tasa inicial `0.0003`, `batch_size=64`, `max_iter=1500` y parada temprana. En HistGradientBoosting se uso aprendizaje lento, 400 iteraciones, 15 hojas maximas y regularizacion L2.

No se realizo una busqueda exhaustiva de hiperparametros. Esta decision mantiene el proyecto comprensible y evita aumentar demasiado el coste computacional. Una linea futura seria incorporar `GridSearchCV`, `RandomizedSearchCV` o validacion temporal cruzada para optimizar configuraciones.

### 9.8. Ventajas e inconvenientes de cada modelo

Ridge es rapido, estable e interpretable, pero limitado para relaciones no lineales. MLP es flexible y representa una red neuronal real, pero tarda mas y es sensible a hiperparametros. HistGradientBoosting captura relaciones no lineales y obtuvo el mejor resultado con mas datos, pero es menos interpretable.

El baseline `lag 24` es muy simple y no requiere entrenamiento, pero no aprovecha toda la informacion disponible. Su valor esta en servir como referencia.

El modo `auto` combina las ventajas de la comparacion automatica, pero aumenta el tiempo de entrenamiento. En conjunto, la aplicacion ofrece un abanico equilibrado: una regla simple, un modelo lineal, una red neuronal, un modelo de boosting y un selector automatico.
