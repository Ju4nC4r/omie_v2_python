# Capítulo 10. Metodología de evaluación

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 10.1. Validación temporal

La evaluación de modelos en series temporales debe respetar el orden cronológico de los datos. En este proyecto, el dataset supervisado se divide en dos bloques: el 80 % inicial se utiliza para entrenamiento y el 20 % final para validación. Esta estrategia simula un escenario real, en el que se dispone de información pasada para predecir periodos posteriores.

La división temporal es más adecuada que una partición aleatoria. Si se mezclaran filas de todo el periodo, el modelo podría entrenar con datos futuros y validarse sobre datos pasados. Esto produciría métricas demasiado optimistas y no representaria el usó real de la aplicación.

La validación temporal permite evaluar la capacidad del modelo para generalizar hacia adelante. En el mercado eléctrico esto es fundamental, porque las condiciones cambian con el tiempo y el objetivo es anticipar precios futuros, no explicar precios ya conocidos.

En la implementación, está división se realiza después de construir el dataset supervisado. Primero se generan las variables respetando el orden temporal y eliminando filas incompletas; después se separa la matriz resultante. La proporción utilizada es 80 % para entrenamiento y 20 % para validación. Esta solución ofrece un equilibrio entre disponer de suficientes datos para ajustar el modelo y conservar un tramo final representativo para evaluar.

### 10.2. Evitar fuga de información futura

La fuga de información ocurre cuando el modelo recibe directa o indirectamente datos que no estarían disponibles en el momento de predecir. En este proyecto se toman varias medidas para evitarla.

Primero, los retardos se calculan siempre con valores anteriores al periodo objetivo. Segundo, las medias, desviaciones, mínimos y máximos móviles se calculan sobre el precio desplazado un periodo. Esto impide que el precio que se quiere predecir forme parte de sus propias variables explicativas.

Tercero, la unión con ESIOS se realiza hacia atrás mediante `merge_asof`, usando la última previsión disponible y no una observación futura. Cuarto, la separación entre entrenamiento y validación respeta el orden temporal.

Estas decisiones son esenciales para que las métricas sean creibles. Un modelo con fuga de información podría obtener resultados excelentes en validación y fallar completamente en inferencia real.

La fuga de información es especialmente peligrosa en este proyecto porque muchas variables se derivan de la propia variable objetivo. Si una media móvil incluyera el precio actual, el modelo estaría recibiendo una pista indirecta del valor que debe predecir. Por eso la implementación usa el precio desplazado antes de calcular medias, desviaciones, mínimos y máximos.

### 10.3. Métrica MAE

MAE significa error absoluto medio. Se calcula como la media de las diferencias absolutas entre el valor real y la predicción. En este proyecto se expresa en `EUR/MWh`, la misma unidad que el precio eléctrico.

La principal ventaja del MAE es su interpretabilidad. Un MAE de `10 EUR/MWh` significa que, en promedio, el modelo se equivoca diez euros por megavatio hora. Esta lectura es directa y fácil de explicar.

El modo `auto` utiliza MAE como criterio principal de selección. El modelo con menor MAE en validación temporal se guarda como mejor candidato. Esta decisión es coherente con el objetivo práctico de reducir el error medio en unidades económicas reales.

Otra ventaja del MAE es que permite comparar modelos de forma sencilla. Si un modelo obtiene `3 EUR/MWh` y otro `5 EUR/MWh`, la interpretación es inmediata. No obstante, MAE no distingue si los errores se concentran en pocos picos o se distribuyen uniformemente; por eso se acompaña de RMSE.

### 10.4. Métrica RMSE

RMSE significa raíz del error cuadrático medio. A diferencia del MAE, eleva los errores al cuadrado antes de promediarlos y después toma la raíz. Esto hace que penalice más los errores grandes.

En el mercado eléctrico, RMSE es útil porque los picos de precio son relevantes. Un modelo puede tener buen MAE pero fallar mucho en episodios extremos. Si el RMSE es mucho mayor que el MAE, puede indicar que existen errores puntuales importantes.

El proyecto calcula RMSE junto con MAE para tener una visión más completa. MAE resume el error medio típico; RMSE alerta sobre desviaciones grandes.

La relación entre RMSE y MAE ayuda a interpretar el tipo de error. Si RMSE es mucho mayor que MAE, significa que existen algunos errores grandes. En el mercado eléctrico, esos errores pueden ser especialmente relevantes porque los picos de precio tienen impacto económico elevado.

### 10.5. Métrica R2

R2 mide la proporción de variabilidad explicada por el modelo respecto a una referencia basada en la media. Su valor ideal es 1. Valores cercanos a 1 indican que el modelo explica buena parte de la variación de la serie. Valores bajos indican poca capacidad explicativa.

En los experimentos realizados, el R2 fue `0.871` para enero-marzo de 2025 y `0.973` para casi todo 2025. Estos valores indican buen ajuste en los tramos de validación correspondientes.

Sin embargo, R2 debe interpretarse con prudencia. Un valor alto no garantiza que el modelo acierte todos los casos concretos. Por ejemplo, la inferencia para `2026-01-01 00:00` presento un error absoluto de `17.81 EUR/MWh` pese a que el entrenamiento anual obtuvo métricas globales buenas.

R2 tampoco expresa el error en unidades económicas. Por está razón, en este proyecto se utiliza como métrica complementaria. Sirve para medir capacidad explicativa general, mientras que MAE y RMSE permiten valorar el error en `EUR/MWh`.

### 10.6. Comparación contra baseline

La comparación contra baseline permite saber si el modelo aporta valor real. En este proyecto se usa el baseline `lag 24`, basado en el precio de 24 periodos antes. Aunque es simple, representa una referencia razonable porque el precio eléctrico tiene ciclos diarios.

En enero-marzo de 2025, el baseline obtuvo un MAE de `20.97 EUR/MWh`, mientras que Ridge obtuvo `10.02 EUR/MWh`. En casi todo 2025, el baseline obtuvo `24.91 EUR/MWh`, mientras que HistGradientBoosting obtuvo `3.17 EUR/MWh`.

Estas comparaciones muestran que los modelos entrenados mejoraron claramente la regla simple. Sin esta comparación, las métricas del modelo serían menos informativas.

El baseline también ayuda a detectar si el modelo está realmente aprendiendo. Si un modelo complejo no mejora una regla simple, puede indicar falta de datos, variables poco informativas o sobreajuste. En los experimentos realizados, la mejora frente al baseline fue clara, especialmente en el entrenamiento con casi todo 2025.

### 10.7. Análisis de errores

El análisis de errores consiste en estudiar no solo la métrica agregada, sino también los casos en los que el modelo falla. Esto es especialmente importante en mercados eléctricos, donde pueden aparecer festivos, precios extremos, cambios de régimen o situaciones meteorológicas inusuales.

El caso de `2026-01-01 00:00` es un ejemplo. El modelo predijo `94.20 EUR/MWh` y el valor real fue `112.01 EUR/MWh`. La diferencia muestra que el modelo infraestimo un día especial, probablemente influido por patrones de festivo y variables externas no incluidas.

Analizar estos errores permite proponer mejoras: incluir festivos, demanda prevista, meteorología, precios de gas, CO2, interconexiones y renovables con mayor detalle.

El análisis de errores puede ampliarse por segmentos: hora del día, día de la semana, mes, nivel de precio, alta o baja renovable y festivos. Esta desagregación permitiría saber si el modelo falla de manera sistemática en ciertos contextos. La gráfica `models/validation_plot.png` también ayuda a revisar visualmente si el modelo sigue la forma general de la serie o si suaviza demasiado los picos.

### 10.8. Evaluación por rangos temporales

Evaluar un único rango no es suficiente para conocer bien el comportamiento del modelo. En el proyecto se compararon al menos dos rangos: enero-marzo de 2025 y casi todo 2025. Los resultados cambiaron de forma significativa: con pocos meses ganó Ridge; con más datos ganó HistGradientBoosting.

Esto demuestra que la cantidad y variedad de datos influyen en el modelo seleccionado. También sugiere que una evaluación más completa debería incluir backtesting mensual, validación por estaciones, evaluación por horas del día y análisis de periodos con alta o baja renovable.

La metodología actual es una base sólida, pero puede ampliarse. El siguiente paso natural sería entrenar y evaluar sobre ventanas temporales sucesivas, registrando métricas por periodo para comprobar la estabilidad del sistema.

Una evaluación por rangos temporales permitiría estudiar si el modelo funciona igual en invierno, primavera, verano y otoño. También permitiría comparar meses con alta generación solar, semanas con elevada eólica o periodos con precios tensiónados. Esta ampliación sería especialmente útil para convertir la aplicación en una herramienta de análisis más robusta.

En conclusión, la metodología de evaluación combina validación temporal, prevencion de fuga de información, métricas complementarias y comparación contra baseline. Esta combinación proporciona una visión más realista que una partición aleatoria y permite interpretar los resultados con mayor rigor.
