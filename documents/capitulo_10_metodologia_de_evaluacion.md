# Capitulo 10. Metodologia de evaluacion

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 10.1. Validacion temporal

La evaluacion de modelos en series temporales debe respetar el orden cronologico de los datos. En este proyecto, el dataset supervisado se divide en dos bloques: el 80 % inicial se utiliza para entrenamiento y el 20 % final para validacion. Esta estrategia simula un escenario real, en el que se dispone de informacion pasada para predecir periodos posteriores.

La division temporal es mas adecuada que una particion aleatoria. Si se mezclaran filas de todo el periodo, el modelo podria entrenar con datos futuros y validarse sobre datos pasados. Esto produciria metricas demasiado optimistas y no representaria el uso real de la aplicacion.

La validacion temporal permite evaluar la capacidad del modelo para generalizar hacia adelante. En el mercado electrico esto es fundamental, porque las condiciones cambian con el tiempo y el objetivo es anticipar precios futuros, no explicar precios ya conocidos.

En la implementacion, esta division se realiza despues de construir el dataset supervisado. Primero se generan las variables respetando el orden temporal y eliminando filas incompletas; despues se separa la matriz resultante. La proporcion utilizada es 80 % para entrenamiento y 20 % para validacion. Esta solucion ofrece un equilibrio entre disponer de suficientes datos para ajustar el modelo y conservar un tramo final representativo para evaluar.

### 10.2. Evitar fuga de informacion futura

La fuga de informacion ocurre cuando el modelo recibe directa o indirectamente datos que no estarian disponibles en el momento de predecir. En este proyecto se toman varias medidas para evitarla.

Primero, los retardos se calculan siempre con valores anteriores al periodo objetivo. Segundo, las medias, desviaciones, minimos y maximos moviles se calculan sobre el precio desplazado un periodo. Esto impide que el precio que se quiere predecir forme parte de sus propias variables explicativas.

Tercero, la union con ESIOS se realiza hacia atras mediante `merge_asof`, usando la ultima prevision disponible y no una observacion futura. Cuarto, la separacion entre entrenamiento y validacion respeta el orden temporal.

Estas decisiones son esenciales para que las metricas sean creibles. Un modelo con fuga de informacion podria obtener resultados excelentes en validacion y fallar completamente en inferencia real.

La fuga de informacion es especialmente peligrosa en este proyecto porque muchas variables se derivan de la propia variable objetivo. Si una media movil incluyera el precio actual, el modelo estaria recibiendo una pista indirecta del valor que debe predecir. Por eso la implementacion usa el precio desplazado antes de calcular medias, desviaciones, minimos y maximos.

### 10.3. Metrica MAE

MAE significa error absoluto medio. Se calcula como la media de las diferencias absolutas entre el valor real y la prediccion. En este proyecto se expresa en `EUR/MWh`, la misma unidad que el precio electrico.

La principal ventaja del MAE es su interpretabilidad. Un MAE de `10 EUR/MWh` significa que, en promedio, el modelo se equivoca diez euros por megavatio hora. Esta lectura es directa y facil de explicar.

El modo `auto` utiliza MAE como criterio principal de seleccion. El modelo con menor MAE en validacion temporal se guarda como mejor candidato. Esta decision es coherente con el objetivo practico de reducir el error medio en unidades economicas reales.

Otra ventaja del MAE es que permite comparar modelos de forma sencilla. Si un modelo obtiene `3 EUR/MWh` y otro `5 EUR/MWh`, la interpretacion es inmediata. No obstante, MAE no distingue si los errores se concentran en pocos picos o se distribuyen uniformemente; por eso se acompana de RMSE.

### 10.4. Metrica RMSE

RMSE significa raiz del error cuadratico medio. A diferencia del MAE, eleva los errores al cuadrado antes de promediarlos y despues toma la raiz. Esto hace que penalice mas los errores grandes.

En el mercado electrico, RMSE es util porque los picos de precio son relevantes. Un modelo puede tener buen MAE pero fallar mucho en episodios extremos. Si el RMSE es mucho mayor que el MAE, puede indicar que existen errores puntuales importantes.

El proyecto calcula RMSE junto con MAE para tener una vision mas completa. MAE resume el error medio tipico; RMSE alerta sobre desviaciones grandes.

La relacion entre RMSE y MAE ayuda a interpretar el tipo de error. Si RMSE es mucho mayor que MAE, significa que existen algunos errores grandes. En el mercado electrico, esos errores pueden ser especialmente relevantes porque los picos de precio tienen impacto economico elevado.

### 10.5. Metrica R2

R2 mide la proporcion de variabilidad explicada por el modelo respecto a una referencia basada en la media. Su valor ideal es 1. Valores cercanos a 1 indican que el modelo explica buena parte de la variacion de la serie. Valores bajos indican poca capacidad explicativa.

En los experimentos realizados, el R2 fue `0.871` para enero-marzo de 2025 y `0.973` para casi todo 2025. Estos valores indican buen ajuste en los tramos de validacion correspondientes.

Sin embargo, R2 debe interpretarse con prudencia. Un valor alto no garantiza que el modelo acierte todos los casos concretos. Por ejemplo, la inferencia para `2026-01-01 00:00` presento un error absoluto de `17.81 EUR/MWh` pese a que el entrenamiento anual obtuvo metricas globales buenas.

R2 tampoco expresa el error en unidades economicas. Por esta razon, en este proyecto se utiliza como metrica complementaria. Sirve para medir capacidad explicativa general, mientras que MAE y RMSE permiten valorar el error en `EUR/MWh`.

### 10.6. Comparacion contra baseline

La comparacion contra baseline permite saber si el modelo aporta valor real. En este proyecto se usa el baseline `lag 24`, basado en el precio de 24 periodos antes. Aunque es simple, representa una referencia razonable porque el precio electrico tiene ciclos diarios.

En enero-marzo de 2025, el baseline obtuvo un MAE de `20.97 EUR/MWh`, mientras que Ridge obtuvo `10.02 EUR/MWh`. En casi todo 2025, el baseline obtuvo `24.91 EUR/MWh`, mientras que HistGradientBoosting obtuvo `3.17 EUR/MWh`.

Estas comparaciones muestran que los modelos entrenados mejoraron claramente la regla simple. Sin esta comparacion, las metricas del modelo serian menos informativas.

El baseline tambien ayuda a detectar si el modelo esta realmente aprendiendo. Si un modelo complejo no mejora una regla simple, puede indicar falta de datos, variables poco informativas o sobreajuste. En los experimentos realizados, la mejora frente al baseline fue clara, especialmente en el entrenamiento con casi todo 2025.

### 10.7. Analisis de errores

El analisis de errores consiste en estudiar no solo la metrica agregada, sino tambien los casos en los que el modelo falla. Esto es especialmente importante en mercados electricos, donde pueden aparecer festivos, precios extremos, cambios de regimen o situaciones meteorologicas inusuales.

El caso de `2026-01-01 00:00` es un ejemplo. El modelo predijo `94.20 EUR/MWh` y el valor real fue `112.01 EUR/MWh`. La diferencia muestra que el modelo infraestimo un dia especial, probablemente influido por patrones de festivo y variables externas no incluidas.

Analizar estos errores permite proponer mejoras: incluir festivos, demanda prevista, meteorologia, precios de gas, CO2, interconexiones y renovables con mayor detalle.

El analisis de errores puede ampliarse por segmentos: hora del dia, dia de la semana, mes, nivel de precio, alta o baja renovable y festivos. Esta desagregacion permitiria saber si el modelo falla de manera sistematica en ciertos contextos. La grafica `models/validation_plot.png` tambien ayuda a revisar visualmente si el modelo sigue la forma general de la serie o si suaviza demasiado los picos.

### 10.8. Evaluacion por rangos temporales

Evaluar un unico rango no es suficiente para conocer bien el comportamiento del modelo. En el proyecto se compararon al menos dos rangos: enero-marzo de 2025 y casi todo 2025. Los resultados cambiaron de forma significativa: con pocos meses gano Ridge; con mas datos gano HistGradientBoosting.

Esto demuestra que la cantidad y variedad de datos influyen en el modelo seleccionado. Tambien sugiere que una evaluacion mas completa deberia incluir backtesting mensual, validacion por estaciones, evaluacion por horas del dia y analisis de periodos con alta o baja renovable.

La metodologia actual es una base solida, pero puede ampliarse. El siguiente paso natural seria entrenar y evaluar sobre ventanas temporales sucesivas, registrando metricas por periodo para comprobar la estabilidad del sistema.

Una evaluacion por rangos temporales permitiria estudiar si el modelo funciona igual en invierno, primavera, verano y otono. Tambien permitiria comparar meses con alta generacion solar, semanas con elevada eolica o periodos con precios tensionados. Esta ampliacion seria especialmente util para convertir la aplicacion en una herramienta de analisis mas robusta.

En conclusion, la metodologia de evaluacion combina validacion temporal, prevencion de fuga de informacion, metricas complementarias y comparacion contra baseline. Esta combinacion proporciona una vision mas realista que una particion aleatoria y permite interpretar los resultados con mayor rigor.
