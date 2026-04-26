# Capítulo 13. Aplicación práctica desarrollada

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 13.1. Descripción general de la aplicación

La aplicación práctica desarrollada en este Trabajo Fin de Grado se denomina `omie_v2_python`. Se trata de un proyecto en Python orientado a descargar datos públicos del mercado eléctrico español, preparar una serie temporal supervisada, entrenar distintos modelos de aprendizaje automático y realizar inferencias sobre el precio del siguiente periodo disponible. La aplicación materializa los conceptos teóricos y metodológicos descritos en los capítulos anteriores.

El sistema está disenado como una herramienta local y reproducible. No depende de una plataforma externa para ejecutar el entrenamiento, sino que puede instalarse en un entorno virtual Python mediante `.venv`. Esta decisión facilita su usó académico, permite controlar dependencias y evita que el proyecto quede ligado a un servicio concreto. El usuario puede ejecutar el flujo completo en su equipo, revisar los ficheros generados y repetir experimentos con distintos rangos temporales.

La aplicación dispone de dos formás principales de usó. La primera es una interfaz gráfica basada en Tkinter, accesible mediante el comando `omie-price-gui`. Esta interfaz permite ejecutar las distintas fases del proceso sin escribir comandos largos. La segunda es una interfaz por consola mediante los comandos `omie-price-train` y `omie-price-predict`, pensada para usuarios que prefieren trabajar de forma más directa o automatizar pruebas.

Desde el punto de vista funcional, la aplicación cubre cinco bloques: extracción de datos, preparación de datos, entrenamiento, test e inferencia. La extracción obtiene ficheros OMIE y, opcionalmente, previsiones renovables de ESIOS. La preparación convierte esos datos en una matriz de entrenamiento. El entrenamiento ajusta uno o varios modelos. El test calcula métricas de validación temporal. La inferencia predice el precio del siguiente periodo usando el modelo guardado.

El proyecto no pretende ser una herramienta comercial de predicción del mercado eléctrico. Su objetivo es académico y demostrativo. Sin embargo, se ha construido con una estructura realista: separación en módulos, cache local, control de errores, modelos seleccionables, métricas, gráfica de validación e integración opcional de variables externas. Esto permite que la aplicación sea una base sólida para futuras ampliaciones.

Una característica importante es que el programa conserva artefactos generados durante la ejecución. Los datos procesados se guardan en `data/processed/`, los modelos entrenados en `models/` y la gráfica de validación como `models/validation_plot.png`. Esta organización permite inspeccionar resultados, repetir inferencias y mantener una trazabilidad razonable del flujo de trabajo.

La aplicación desarrollada conecta directamente con el problema planteado en el TFG: predecir el precio del mercado eléctrico español a partir de datos históricos y variables explicativas. La contribución práctica consiste en transformar ese problema en un software ejecutable, documentado y versionado con Git.

### 13.2. Objetivo de la aplicación

El objetivo principal de la aplicación es facilitar la experimentación con modelos de predicción del precio del mercado diario eléctrico español. Para ello, el sistema automatiza tareas que, de otro modo, serían manuales y repetitivas: descargar datos, limpiar ficheros, generar variables, entrenar modelos, calcular métricas y realizar predicciones.

Desde una perspectiva académica, la aplicación permite comprobar de forma práctica como influyen las decisiones metodológicas sobre el resultado final. Por ejemplo, el usuario puede entrenar con pocos meses o con un año completo, seleccionar un modelo concreto o usar el modo automático, activar o no variables ESIOS y comparar las métricas obtenidas. Esto convierte el proyecto en una plataforma de experimentación.

Otro objetivo es hacer visible el flujo completo de un proyecto de machine learning. En muchos ejemplos teóricos se muestra solo el entrenamiento del modelo, pero en un caso real hay muchas fases previas y posteriores. La aplicación muestra que la predicción no empieza en el algoritmo, sino en la calidad de los datos y en la forma de transformarlos. También muestra que el resultado debe evaluarse y compararse contra una referencia.

La aplicación persigue también un objetivo didáctico. El usuario puede observar que una red neuronal no siempre es automáticamente superior a un modelo lineal o a un modelo basado en árboles. El sistema permite comparar Ridge, MLP e HistGradientBoosting bajo el mismo dataset y la misma validación temporal. Esta comparación ayuda a entender que la calidad del modelo depende del problema, de los datos y de la preparación de variables.

Un objetivo adicional es facilitar futuras mejoras. El sistema ya está preparado para incorporar variables externas, como previsión eólica y solar, mediante ESIOS. Este patrón puede extenderse en el futuro a demanda prevista, meteorología, precios de gas, CO2, interconexiones, festivos o datos intradiarios. La aplicación no se plantea como un producto cerrado, sino como una base ampliable.

En síntesis, el objetivo de la aplicación es convertir el estudio de predicción del precio eléctrico en un proceso ejecutable y verificable. No se limita a presentar teoria, sino que permite entrenar modelos reales con datos reales, obtener métricas y observar errores concretos.

### 13.3. Datos utilizados

La aplicación utiliza como fuente principal los datos de OMIE correspondientes al precio marginal del mercado diario. Estos datos se descargan mediante ficheros `MARGINALPDBC`, que contienen el precio marginal español y portugués para cada periodo del día. La variable objetivo del modelo es el precio marginal español, almacenado internamente como `marginal_es`.

El usuario define el rango temporal de trabajo. Puede entrenar con un periodo corto, como varios meses, o con un periodo amplio, como todo un año. Cuanto mayor sea el rango, más ejemplos tendrá el modelo para aprender patrones horarios, diarios, semanales y estacionales. Sin embargo, rangos más amplios también pueden incluir cambios de régimen, variaciones de resolución temporal y días no disponibles.

Los datos OMIE se almacenan primero en `data/raw/` como ficheros originales. Después se procesan y se guardan en `data/processed/omie_prices.csv`. Esta separación entre datos brutos y datos procesados permite repetir experimentos sin descargar de nuevo los ficheros y facilita la depuración si aparece algún problema.

Opcionalmente, la aplicación puede incorporar datos de ESIOS. En concreto, utiliza previsiones de generación eólica, solar fotovoltaica y solar térmica. Estas previsiones se transforman en columnas como `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. También se generan variables derivadas: `solar_forecast_mwh`, `renewable_forecast_mwh` y `wind_solar_ratio`.

La incorporación de ESIOS requiere un token. El usuario puede introducirlo en la interfaz gráfica o establecerlo mediante la variable de entorno `ESIOS_TOKEN`. Si no se proporciona token, el programa funciona igualmente con datos OMIE. Esta decisión mantiene la aplicación accesible, pero permite enriquecerla cuando se dispone de credenciales.

Los datos utilizados no se suben al repositorio Git. Las carpetas de datos, modelos y caches están excluidas mediante `.gitignore`. Esto es adecuado porque los datos pueden ocupar espacio, regenerarse y cambiar según el periodo descargado. El repositorio contiene el código y la documentación; los datos se reconstruyen mediante la propia aplicación.

### 13.4. Flujo de trabajo en la interfaz gráfica

La interfaz gráfica se ejecuta con el comando `omie-price-gui`. Su finalidad es permitir que el usuario recorra el flujo completo sin depender exclusivamente de la línea de comandos. La ventana incluye campos para indicar la fecha inicial, la fecha final, el modelo deseado, la activación de ESIOS y el token correspondiente cuando sea necesario.

El flujo se organiza en fases visibles. Primero se realiza la extracción de datos. En esta fase, el programa descarga los ficheros OMIE para el rango seleccionado y, si está activada la opción ESIOS, descarga también las previsiones renovables. La interfaz muestra mensajes de progreso para que el usuario sepa qué está ocurriendo y pueda detectar errores de red, token o disponibilidad de datos.

La segunda fase es la preparación de datos. El sistema transforma los datos descargados en un dataset útil para entrenamiento. Esto incluye parseo, normalización de fechas, ordenación temporal, unión con ESIOS si procede y construcción de variables. Aunque parte de este proceso ocurre internamente, la interfaz lo presenta como una fase separada para hacer visible la importancia de la preparación.

La tercera fase es el entrenamiento y test. En ella se entrena el modelo elegido y se calculan métricas de validación temporal. La interfaz permite seleccionar un modelo concreto o el modo automático. Durante la ejecución se muestran logs y una barra de progreso, especialmente útil cuando se entrena `mlp` o cuando se utiliza `auto`, ya que pueden tardar más que una regresión Ridge.

La cuarta fase es la inferencia. Una vez existe un modelo guardado, la aplicación puede estimar el precio del siguiente periodo disponible en el dataset. Esta predicción se realiza usando las mismas variables esperadas por el modelo entrenado. Si el modelo fue entrenado con ESIOS, el sistema intenta conservar y utilizar las columnas externas correspondientes.

El valor de la GUI no es solo estético. En un TFG técnico, una interfaz gráfica facilita la demostración del proyecto ante un tribunal o un usuario no especializado. Permite mostrar claramente que el sistema no es un script aislado, sino una aplicación con fases, opciones y resultados interpretables.

### 13.5. Selección manual de modelos

La aplicación permite seleccionar manualmente el modelo de entrenamiento. Las opciones principales son `ridge`, `mlp` e `hist_gradient_boosting`. Cada una representa una familia diferente de aprendizaje automático y permite observar comportamientos distintos sobre el mismo problema.

La opción `ridge` utiliza una regresión lineal regularizada mediante RidgeCV. Es un modelo rápido, estable e interpretable en comparación con alternativas más complejas. Resulta adecuado como primera aproximación porque aprovecha bien variables de calendario, retardos y medias móviles. Su regularización ayuda a controlar coeficientes excesivos cuando existen muchas variables correlacionadas.

La opción `mlp` utiliza una red neuronal multicapa mediante `MLPRegressor`. Este modelo puede capturar relaciones no lineales entre variables, por ejemplo interacciones entre hora, precio previo, volatilidad y generación renovable. Su entrenamiento puede ser más lento y sensible a hiperparámetros, pero representa la idea inicial de entrenar una red neuronal sencilla para el problema.

La opción `hist_gradient_boosting` utiliza `HistGradientBoostingRegressor`, un modelo basado en árboles de decisión entrenados secuencialmente. Es una alternativa potente para datos tabulares y suele capturar bien relaciones no lineales y efectos por umbrales. En pruebas realizadas con datos amplios de 2025, este tipo de modelo obtuvo muy buen rendimiento en validación temporal.

Permitir selección manual tiene valor experimental. El usuario puede repetir el mismo entrenamiento con distintos modelos y comparar métricas. Esto ayuda a entender que el algoritmo no debe elegirse por intuición, sino por evaluación. También permite observar diferencias de tiempo de entrenamiento y estabilidad.

La interfaz valida que el modelo elegido sea correcto. Si el usuario intenta ejecutar una opción no válida, el sistema muestra un error. Esta comprobación evita ejecuciones inconsistentes y mejora la robustez de la aplicación.

### 13.6. Modo automático de selección

Además de la selección manual, la aplicación incorpora un modo `auto`. Este modo no es un modelo independiente, sino una estrategia de comparación. Entrena los modelos candidatos disponibles, calcula métricas sobre el tramo de validación temporal y guarda el modelo que obtiene menor MAE.

El modo automático es especialmente útil cuando el usuario no sabe de antemano qué modelo funcionara mejor para un rango de fechas concreto. El comportamiento del mercado puede cambiar según el periodo, la cantidad de datos y la presencia o ausencia de variables ESIOS. Por ello, un modelo que funciona mejor en un experimento no tiene por que ser siempre superior.

La métrica utilizada para seleccionar el mejor modelo es MAE, error absoluto medio. Esta métrica mide el error medio en EUR/MWh sin elevar los errores al cuadrado. Es fácil de interpretar y permite comparar modelos de forma directa. El modo `auto` también calcula otras métricas, como RMSE y R2, pero la selección principal se basa en MAE.

La ventaja del modo `auto` es que ofrece una decisión basada en datos. En lugar de asumir que una red neuronal o un modelo de boosting será mejor, el sistema lo comprueba. Esta filosofía es coherente con el enfoque experimental del TFG: formular una metodología, entrenar alternativas, medir resultados y elegir según evidencia.

El inconveniente es que tarda más, porque entrena varios modelos. En la interfaz gráfica esto se compensa mostrando progreso y logs por candidato. Asi el usuario puede entender que el programa no se ha bloqueado, sino que está evaluando distintas alternativas.

El modelo seleccionado se guarda en `models/omie_model.joblib`, junto con información sobre las columnas de entrada esperadas. Esto permite que la fase de inferencia útilice la misma estructura de variables que se usó durante el entrenamiento. Mantener está coherencia entre entrenamiento e inferencia es fundamental.

### 13.7. Entrenamiento con datos OMIE

El entrenamiento básico utiliza únicamente datos OMIE. En este modo, el modelo aprende a partir de variables de calendario y del histórico del propio precio. Aunque no incorpora demanda, meteorología ni renovables externas, esta configuración permite construir una primera referencia funcional y reproducible.

El usuario puede ejecutar este entrenamiento desde la interfaz gráfica o desde consola. Un ejemplo de comando es:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Este comando descarga o reutiliza los datos OMIE del periodo indicado, genera las variables y entrena los modelos según la opción seleccionada. Al finalizar, muestra las métricas obtenidas y guarda el modelo. También genera una gráfica de validación que compara valores reales, predicciones y baseline.

Entrenar solo con OMIE tiene varias ventajas. No requiere token ESIOS, depende de una única fuente principal y permite ejecutar el proyecto con menos configuración. También es una buena forma de comprobar que el pipeline funciona antes de incorporar variables externas.

La principal limitación es que el modelo solo observa el resultado histórico del mercado, no las causas externas que influyen en el precio. Puede aprender patrones horarios y semanales, pero no sabe directamente si se espera mucha eólica, poca solar, alta demanda o precios elevados del gas. Por eso se considera un punto de partida, no una versión final del sistema.

Durante los experimentos realizados en el proyecto, el entrenamiento con datos OMIE mostró que ampliar el periodo histórico mejora notablemente la estabilidad del modelo. Con pocos meses se obtiene una primera aproximación; con un año completo se capturan más situaciones de mercado, aunque también aparecen retos como días no disponibles o cambios de resolución temporal.

### 13.8. Entrenamiento con variables ESIOS opcionales

El entrenamiento con ESIOS incorpora variables externas de previsión renovable. Para activarlo, el usuario debe marcar la opción ESIOS en la interfaz gráfica o usar el argumento `--include-esios` en consola. También debe proporcionar un token mediante el campo correspondiente o mediante la variable de entorno `ESIOS_TOKEN`.

Un ejemplo de entrenamiento con ESIOS es:

```bash
export ESIOS_TOKEN="tu_token_esios"
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios
```

Cuando esta opción está activa, el programa descarga previsiones de eólica, solar fotovoltaica y solar térmica. Después las une con los precios OMIE mediante `timestamp` y genera variables derivadas. El dataset resultante contiene más información que el basado solo en OMIE.

La motivacion es que la generación renovable influye en la formación del precio. Una alta previsión eólica o solar suele desplazar tecnologías más caras y puede reducir el precio marginal. Una baja previsión renovable puede coincidir con mayor necesidad de tecnologías de respaldo y precios más altos. Incluir estas variables permite que el modelo observe parte de ese contexto físico.

La aplicación valida que exista token cuando el usuario activa ESIOS. Si no hay token, se muestra un error antes de iniciar el flujo completo. Esta validación temprana evita procesos largos que acabarían fallando en la descarga de la API.

El entrenamiento con ESIOS también introduce retos. Las previsiones deben estar bien alineadas temporalmente, pueden existir huecos y la calidad de la predicción renovable afecta al resultado final. Además, al entrenar con ESIOS, la inferencia debe disponer de las mismas columnas que el modelo espera. Por eso el flujo normal conserva el dataset enriquecido en `data/processed/omie_features.csv`.

Desde el punto de vista del TFG, esta funcionalidad demuestra como el modelo puede evolucionar desde una aproximación pequeña, basada en calendario e histórico, hacia una aproximación más rica que incorpora variables explicativas externas.

### 13.9. Inferencia del siguiente periodo

La inferencia consiste en utilizar el modelo entrenado para predecir el precio del siguiente periodo disponible. Esta fase se ejecuta desde la interfaz gráfica o mediante el comando `omie-price-predict`. El sistema carga el modelo guardado en `models/omie_model.joblib` y el dataset procesado, genera las variables necesarias para el siguiente instante y calcula la predicción.

El programa determina el siguiente `timestamp` a partir de la frecuencia observada en los datos recientes. Si los datos son horarios, predice la hora siguiente. Si son cuarto-horarios, predice el siguiente cuarto de hora. Esta lógica permite que la aplicación se adapte a la resolución de los datos disponibles.

Para construir la fila de inferencia, el sistema crea una observación futura con precio desconocido. A continuacion calcula variables de calendario, retardos, medias móviles, diferencias y ratios usando el histórico disponible. Si el modelo espera variables ESIOS y el dataset las contiene, se propagan los últimos valores externos disponibles. Si no existe suficiente histórico para calcular todas las variables, el programa lanza un error.

La inferencia mantiene la coherencia con el entrenamiento mediante la lista de columnas esperadas por el modelo. Esto es importante porque un modelo entrenado con ciertas variables no debe recibir otra estructura distinta en predicción. Guardar las columnas junto con el modelo evita inconsistencias entre entrenamiento e inferencia.

El resultado de la inferencia es un valor en EUR/MWh para el siguiente periodo. Este valor debe interpretarse como una estimación, no como una certeza. El mercado eléctrico puede verse afectado por eventos no incluidos en el modelo, errores de previsión renovable o cambios bruscos de condiciones. Por ello, la predicción debe acompañarse de métricas y análisis de error.

La fase de inferencia es relevante porque conecta el entrenamiento con un usó práctico. No basta con entrenar y validar un modelo históricamente; una aplicación predictiva debe ser capaz de recibir datos recientes y generar una estimación futura. Esta funcionalidad completa el flujo de machine learning.

### 13.10. Comparación entre predicción y valor real

Una parte importante de la aplicación práctica es la comparación entre la predicción generada y el valor real publicado posteriormente por OMIE. Esta comparación permite evaluar el error en un caso concreto y entender las limitaciones del modelo. Aunque las métricas agregadas son necesarias, los ejemplos individuales ayudan a interpretar el comportamiento real de la aplicación.

Durante las pruebas del proyecto se realizó una inferencia para el periodo `2026-01-01 00:00`. El modelo entrenado con datos de 2025 predijo un precio de `94.20 EUR/MWh`, mientras que el valor real extraido de OMIE fue `112.01 EUR/MWh`. El error absoluto fue de `17.81 EUR/MWh`, equivalente a un error relativo aproximado del `15.90 %`.

Este resultado muestra una idea importante: incluso un modelo con buenas métricas globales puede fallar en periodos concretos. El 1 de enero es un día festivo con patrones de demanda particulares, y puede diferir de jornadas normales. Además, el modelo puede no incorporar todas las variables necesarias para anticipar correctamente ese comportamiento, como demanda prevista, meteorología, disponibilidad de tecnologías, gas, CO2 o festivos.

La comparación con el valor real permite identificar líneas de mejora. Una primera mejora sería incorporar calendarios de festivos nacionales y autonómicos. Otra sería incluir demanda prevista y generación renovable prevista de forma más completa. También podría mejorarse el tratamiento de datos cuarto-horarios, adaptando retardos a duraciones reales en lugar de a número de periodos.

La aplicación ya incorpora una referencia adicional mediante el baseline `lag 24`. Este baseline predice usando el precio de 24 periodos antes. Comparar el modelo contra esta regla simple permite saber si el aprendizaje automático aporta valor. En los experimentos realizados, los modelos entrenados mejoraron claramente este baseline en métricas agregadas, aunque eso no elimina errores puntuales.

El análisis de casos concretos es una herramienta diagnóstica. Cuando una predicción falla, no debe interpretarse solo como un número negativo, sino como una oportunidad para estudiar que información faltaba. Si el error se concentra en festivos, horas solares, picos de gas o cambios de resolución, esas observaciones orientan futuras mejoras del sistema.

En conclusión, la aplicación práctica desarrollada permite recorrer todo el ciclo: obtener datos, preparar variables, entrenar modelos, evaluar resultados, inferir el siguiente periodo y comparar la predicción con valores reales. Esta capacidad convierte el proyecto en una demostración completa de predicción aplicada al mercado eléctrico español, con un equilibrio razonable entre sencillez, utilidad y posibilidades de ampliación.
