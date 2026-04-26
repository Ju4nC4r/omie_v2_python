# Capitulo 13. Aplicacion practica desarrollada

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 13.1. Descripcion general de la aplicacion

La aplicacion practica desarrollada en este Trabajo Fin de Grado se denomina `omie_v2_python`. Se trata de un proyecto en Python orientado a descargar datos publicos del mercado electrico espanol, preparar una serie temporal supervisada, entrenar distintos modelos de aprendizaje automatico y realizar inferencias sobre el precio del siguiente periodo disponible. La aplicacion materializa los conceptos teoricos y metodologicos descritos en los capitulos anteriores.

El sistema esta disenado como una herramienta local y reproducible. No depende de una plataforma externa para ejecutar el entrenamiento, sino que puede instalarse en un entorno virtual Python mediante `.venv`. Esta decision facilita su uso academico, permite controlar dependencias y evita que el proyecto quede ligado a un servicio concreto. El usuario puede ejecutar el flujo completo en su equipo, revisar los ficheros generados y repetir experimentos con distintos rangos temporales.

La aplicacion dispone de dos formas principales de uso. La primera es una interfaz grafica basada en Tkinter, accesible mediante el comando `omie-price-gui`. Esta interfaz permite ejecutar las distintas fases del proceso sin escribir comandos largos. La segunda es una interfaz por consola mediante los comandos `omie-price-train` y `omie-price-predict`, pensada para usuarios que prefieren trabajar de forma mas directa o automatizar pruebas.

Desde el punto de vista funcional, la aplicacion cubre cinco bloques: extraccion de datos, preparacion de datos, entrenamiento, test e inferencia. La extraccion obtiene ficheros OMIE y, opcionalmente, previsiones renovables de ESIOS. La preparacion convierte esos datos en una matriz de entrenamiento. El entrenamiento ajusta uno o varios modelos. El test calcula metricas de validacion temporal. La inferencia predice el precio del siguiente periodo usando el modelo guardado.

El proyecto no pretende ser una herramienta comercial de prediccion del mercado electrico. Su objetivo es academico y demostrativo. Sin embargo, se ha construido con una estructura realista: separacion en modulos, cache local, control de errores, modelos seleccionables, metricas, grafica de validacion e integracion opcional de variables externas. Esto permite que la aplicacion sea una base solida para futuras ampliaciones.

Una caracteristica importante es que el programa conserva artefactos generados durante la ejecucion. Los datos procesados se guardan en `data/processed/`, los modelos entrenados en `models/` y la grafica de validacion como `models/validation_plot.png`. Esta organizacion permite inspeccionar resultados, repetir inferencias y mantener una trazabilidad razonable del flujo de trabajo.

La aplicacion desarrollada conecta directamente con el problema planteado en el TFG: predecir el precio del mercado electrico espanol a partir de datos historicos y variables explicativas. La contribucion practica consiste en transformar ese problema en un software ejecutable, documentado y versionado con Git.

### 13.2. Objetivo de la aplicacion

El objetivo principal de la aplicacion es facilitar la experimentacion con modelos de prediccion del precio del mercado diario electrico espanol. Para ello, el sistema automatiza tareas que, de otro modo, serian manuales y repetitivas: descargar datos, limpiar ficheros, generar variables, entrenar modelos, calcular metricas y realizar predicciones.

Desde una perspectiva academica, la aplicacion permite comprobar de forma practica como influyen las decisiones metodologicas sobre el resultado final. Por ejemplo, el usuario puede entrenar con pocos meses o con un ano completo, seleccionar un modelo concreto o usar el modo automatico, activar o no variables ESIOS y comparar las metricas obtenidas. Esto convierte el proyecto en una plataforma de experimentacion.

Otro objetivo es hacer visible el flujo completo de un proyecto de machine learning. En muchos ejemplos teoricos se muestra solo el entrenamiento del modelo, pero en un caso real hay muchas fases previas y posteriores. La aplicacion muestra que la prediccion no empieza en el algoritmo, sino en la calidad de los datos y en la forma de transformarlos. Tambien muestra que el resultado debe evaluarse y compararse contra una referencia.

La aplicacion persigue tambien un objetivo didactico. El usuario puede observar que una red neuronal no siempre es automaticamente superior a un modelo lineal o a un modelo basado en arboles. El sistema permite comparar Ridge, MLP e HistGradientBoosting bajo el mismo dataset y la misma validacion temporal. Esta comparacion ayuda a entender que la calidad del modelo depende del problema, de los datos y de la preparacion de variables.

Un objetivo adicional es facilitar futuras mejoras. El sistema ya esta preparado para incorporar variables externas, como prevision eolica y solar, mediante ESIOS. Este patron puede extenderse en el futuro a demanda prevista, meteorologia, precios de gas, CO2, interconexiones, festivos o datos intradiarios. La aplicacion no se plantea como un producto cerrado, sino como una base ampliable.

En sintesis, el objetivo de la aplicacion es convertir el estudio de prediccion del precio electrico en un proceso ejecutable y verificable. No se limita a presentar teoria, sino que permite entrenar modelos reales con datos reales, obtener metricas y observar errores concretos.

### 13.3. Datos utilizados

La aplicacion utiliza como fuente principal los datos de OMIE correspondientes al precio marginal del mercado diario. Estos datos se descargan mediante ficheros `MARGINALPDBC`, que contienen el precio marginal espanol y portugues para cada periodo del dia. La variable objetivo del modelo es el precio marginal espanol, almacenado internamente como `marginal_es`.

El usuario define el rango temporal de trabajo. Puede entrenar con un periodo corto, como varios meses, o con un periodo amplio, como todo un ano. Cuanto mayor sea el rango, mas ejemplos tendra el modelo para aprender patrones horarios, diarios, semanales y estacionales. Sin embargo, rangos mas amplios tambien pueden incluir cambios de regimen, variaciones de resolucion temporal y dias no disponibles.

Los datos OMIE se almacenan primero en `data/raw/` como ficheros originales. Despues se procesan y se guardan en `data/processed/omie_prices.csv`. Esta separacion entre datos brutos y datos procesados permite repetir experimentos sin descargar de nuevo los ficheros y facilita la depuracion si aparece algun problema.

Opcionalmente, la aplicacion puede incorporar datos de ESIOS. En concreto, utiliza previsiones de generacion eolica, solar fotovoltaica y solar termica. Estas previsiones se transforman en columnas como `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. Tambien se generan variables derivadas: `solar_forecast_mwh`, `renewable_forecast_mwh` y `wind_solar_ratio`.

La incorporacion de ESIOS requiere un token. El usuario puede introducirlo en la interfaz grafica o establecerlo mediante la variable de entorno `ESIOS_TOKEN`. Si no se proporciona token, el programa funciona igualmente con datos OMIE. Esta decision mantiene la aplicacion accesible, pero permite enriquecerla cuando se dispone de credenciales.

Los datos utilizados no se suben al repositorio Git. Las carpetas de datos, modelos y caches estan excluidas mediante `.gitignore`. Esto es adecuado porque los datos pueden ocupar espacio, regenerarse y cambiar segun el periodo descargado. El repositorio contiene el codigo y la documentacion; los datos se reconstruyen mediante la propia aplicacion.

### 13.4. Flujo de trabajo en la interfaz grafica

La interfaz grafica se ejecuta con el comando `omie-price-gui`. Su finalidad es permitir que el usuario recorra el flujo completo sin depender exclusivamente de la linea de comandos. La ventana incluye campos para indicar la fecha inicial, la fecha final, el modelo deseado, la activacion de ESIOS y el token correspondiente cuando sea necesario.

El flujo se organiza en fases visibles. Primero se realiza la extraccion de datos. En esta fase, el programa descarga los ficheros OMIE para el rango seleccionado y, si esta activada la opcion ESIOS, descarga tambien las previsiones renovables. La interfaz muestra mensajes de progreso para que el usuario sepa que esta ocurriendo y pueda detectar errores de red, token o disponibilidad de datos.

La segunda fase es la preparacion de datos. El sistema transforma los datos descargados en un dataset util para entrenamiento. Esto incluye parseo, normalizacion de fechas, ordenacion temporal, union con ESIOS si procede y construccion de variables. Aunque parte de este proceso ocurre internamente, la interfaz lo presenta como una fase separada para hacer visible la importancia de la preparacion.

La tercera fase es el entrenamiento y test. En ella se entrena el modelo elegido y se calculan metricas de validacion temporal. La interfaz permite seleccionar un modelo concreto o el modo automatico. Durante la ejecucion se muestran logs y una barra de progreso, especialmente util cuando se entrena `mlp` o cuando se utiliza `auto`, ya que pueden tardar mas que una regresion Ridge.

La cuarta fase es la inferencia. Una vez existe un modelo guardado, la aplicacion puede estimar el precio del siguiente periodo disponible en el dataset. Esta prediccion se realiza usando las mismas variables esperadas por el modelo entrenado. Si el modelo fue entrenado con ESIOS, el sistema intenta conservar y utilizar las columnas externas correspondientes.

El valor de la GUI no es solo estetico. En un TFG tecnico, una interfaz grafica facilita la demostracion del proyecto ante un tribunal o un usuario no especializado. Permite mostrar claramente que el sistema no es un script aislado, sino una aplicacion con fases, opciones y resultados interpretables.

### 13.5. Seleccion manual de modelos

La aplicacion permite seleccionar manualmente el modelo de entrenamiento. Las opciones principales son `ridge`, `mlp` e `hist_gradient_boosting`. Cada una representa una familia diferente de aprendizaje automatico y permite observar comportamientos distintos sobre el mismo problema.

La opcion `ridge` utiliza una regresion lineal regularizada mediante RidgeCV. Es un modelo rapido, estable e interpretable en comparacion con alternativas mas complejas. Resulta adecuado como primera aproximacion porque aprovecha bien variables de calendario, retardos y medias moviles. Su regularizacion ayuda a controlar coeficientes excesivos cuando existen muchas variables correlacionadas.

La opcion `mlp` utiliza una red neuronal multicapa mediante `MLPRegressor`. Este modelo puede capturar relaciones no lineales entre variables, por ejemplo interacciones entre hora, precio previo, volatilidad y generacion renovable. Su entrenamiento puede ser mas lento y sensible a hiperparametros, pero representa la idea inicial de entrenar una red neuronal sencilla para el problema.

La opcion `hist_gradient_boosting` utiliza `HistGradientBoostingRegressor`, un modelo basado en arboles de decision entrenados secuencialmente. Es una alternativa potente para datos tabulares y suele capturar bien relaciones no lineales y efectos por umbrales. En pruebas realizadas con datos amplios de 2025, este tipo de modelo obtuvo muy buen rendimiento en validacion temporal.

Permitir seleccion manual tiene valor experimental. El usuario puede repetir el mismo entrenamiento con distintos modelos y comparar metricas. Esto ayuda a entender que el algoritmo no debe elegirse por intuicion, sino por evaluacion. Tambien permite observar diferencias de tiempo de entrenamiento y estabilidad.

La interfaz valida que el modelo elegido sea correcto. Si el usuario intenta ejecutar una opcion no valida, el sistema muestra un error. Esta comprobacion evita ejecuciones inconsistentes y mejora la robustez de la aplicacion.

### 13.6. Modo automatico de seleccion

Ademas de la seleccion manual, la aplicacion incorpora un modo `auto`. Este modo no es un modelo independiente, sino una estrategia de comparacion. Entrena los modelos candidatos disponibles, calcula metricas sobre el tramo de validacion temporal y guarda el modelo que obtiene menor MAE.

El modo automatico es especialmente util cuando el usuario no sabe de antemano que modelo funcionara mejor para un rango de fechas concreto. El comportamiento del mercado puede cambiar segun el periodo, la cantidad de datos y la presencia o ausencia de variables ESIOS. Por ello, un modelo que funciona mejor en un experimento no tiene por que ser siempre superior.

La metrica utilizada para seleccionar el mejor modelo es MAE, error absoluto medio. Esta metrica mide el error medio en EUR/MWh sin elevar los errores al cuadrado. Es facil de interpretar y permite comparar modelos de forma directa. El modo `auto` tambien calcula otras metricas, como RMSE y R2, pero la seleccion principal se basa en MAE.

La ventaja del modo `auto` es que ofrece una decision basada en datos. En lugar de asumir que una red neuronal o un modelo de boosting sera mejor, el sistema lo comprueba. Esta filosofia es coherente con el enfoque experimental del TFG: formular una metodologia, entrenar alternativas, medir resultados y elegir segun evidencia.

El inconveniente es que tarda mas, porque entrena varios modelos. En la interfaz grafica esto se compensa mostrando progreso y logs por candidato. Asi el usuario puede entender que el programa no se ha bloqueado, sino que esta evaluando distintas alternativas.

El modelo seleccionado se guarda en `models/omie_model.joblib`, junto con informacion sobre las columnas de entrada esperadas. Esto permite que la fase de inferencia utilice la misma estructura de variables que se uso durante el entrenamiento. Mantener esta coherencia entre entrenamiento e inferencia es fundamental.

### 13.7. Entrenamiento con datos OMIE

El entrenamiento basico utiliza unicamente datos OMIE. En este modo, el modelo aprende a partir de variables de calendario y del historico del propio precio. Aunque no incorpora demanda, meteorologia ni renovables externas, esta configuracion permite construir una primera referencia funcional y reproducible.

El usuario puede ejecutar este entrenamiento desde la interfaz grafica o desde consola. Un ejemplo de comando es:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Este comando descarga o reutiliza los datos OMIE del periodo indicado, genera las variables y entrena los modelos segun la opcion seleccionada. Al finalizar, muestra las metricas obtenidas y guarda el modelo. Tambien genera una grafica de validacion que compara valores reales, predicciones y baseline.

Entrenar solo con OMIE tiene varias ventajas. No requiere token ESIOS, depende de una unica fuente principal y permite ejecutar el proyecto con menos configuracion. Tambien es una buena forma de comprobar que el pipeline funciona antes de incorporar variables externas.

La principal limitacion es que el modelo solo observa el resultado historico del mercado, no las causas externas que influyen en el precio. Puede aprender patrones horarios y semanales, pero no sabe directamente si se espera mucha eolica, poca solar, alta demanda o precios elevados del gas. Por eso se considera un punto de partida, no una version final del sistema.

Durante los experimentos realizados en el proyecto, el entrenamiento con datos OMIE mostro que ampliar el periodo historico mejora notablemente la estabilidad del modelo. Con pocos meses se obtiene una primera aproximacion; con un ano completo se capturan mas situaciones de mercado, aunque tambien aparecen retos como dias no disponibles o cambios de resolucion temporal.

### 13.8. Entrenamiento con variables ESIOS opcionales

El entrenamiento con ESIOS incorpora variables externas de prevision renovable. Para activarlo, el usuario debe marcar la opcion ESIOS en la interfaz grafica o usar el argumento `--include-esios` en consola. Tambien debe proporcionar un token mediante el campo correspondiente o mediante la variable de entorno `ESIOS_TOKEN`.

Un ejemplo de entrenamiento con ESIOS es:

```bash
export ESIOS_TOKEN="tu_token_esios"
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios
```

Cuando esta opcion esta activa, el programa descarga previsiones de eolica, solar fotovoltaica y solar termica. Despues las une con los precios OMIE mediante `timestamp` y genera variables derivadas. El dataset resultante contiene mas informacion que el basado solo en OMIE.

La motivacion es que la generacion renovable influye en la formacion del precio. Una alta prevision eolica o solar suele desplazar tecnologias mas caras y puede reducir el precio marginal. Una baja prevision renovable puede coincidir con mayor necesidad de tecnologias de respaldo y precios mas altos. Incluir estas variables permite que el modelo observe parte de ese contexto fisico.

La aplicacion valida que exista token cuando el usuario activa ESIOS. Si no hay token, se muestra un error antes de iniciar el flujo completo. Esta validacion temprana evita procesos largos que acabarian fallando en la descarga de la API.

El entrenamiento con ESIOS tambien introduce retos. Las previsiones deben estar bien alineadas temporalmente, pueden existir huecos y la calidad de la prediccion renovable afecta al resultado final. Ademas, al entrenar con ESIOS, la inferencia debe disponer de las mismas columnas que el modelo espera. Por eso el flujo normal conserva el dataset enriquecido en `data/processed/omie_features.csv`.

Desde el punto de vista del TFG, esta funcionalidad demuestra como el modelo puede evolucionar desde una aproximacion pequena, basada en calendario e historico, hacia una aproximacion mas rica que incorpora variables explicativas externas.

### 13.9. Inferencia del siguiente periodo

La inferencia consiste en utilizar el modelo entrenado para predecir el precio del siguiente periodo disponible. Esta fase se ejecuta desde la interfaz grafica o mediante el comando `omie-price-predict`. El sistema carga el modelo guardado en `models/omie_model.joblib` y el dataset procesado, genera las variables necesarias para el siguiente instante y calcula la prediccion.

El programa determina el siguiente `timestamp` a partir de la frecuencia observada en los datos recientes. Si los datos son horarios, predice la hora siguiente. Si son cuarto-horarios, predice el siguiente cuarto de hora. Esta logica permite que la aplicacion se adapte a la resolucion de los datos disponibles.

Para construir la fila de inferencia, el sistema crea una observacion futura con precio desconocido. A continuacion calcula variables de calendario, retardos, medias moviles, diferencias y ratios usando el historico disponible. Si el modelo espera variables ESIOS y el dataset las contiene, se propagan los ultimos valores externos disponibles. Si no existe suficiente historico para calcular todas las variables, el programa lanza un error.

La inferencia mantiene la coherencia con el entrenamiento mediante la lista de columnas esperadas por el modelo. Esto es importante porque un modelo entrenado con ciertas variables no debe recibir otra estructura distinta en prediccion. Guardar las columnas junto con el modelo evita inconsistencias entre entrenamiento e inferencia.

El resultado de la inferencia es un valor en EUR/MWh para el siguiente periodo. Este valor debe interpretarse como una estimacion, no como una certeza. El mercado electrico puede verse afectado por eventos no incluidos en el modelo, errores de prevision renovable o cambios bruscos de condiciones. Por ello, la prediccion debe acompanarse de metricas y analisis de error.

La fase de inferencia es relevante porque conecta el entrenamiento con un uso practico. No basta con entrenar y validar un modelo historicamente; una aplicacion predictiva debe ser capaz de recibir datos recientes y generar una estimacion futura. Esta funcionalidad completa el flujo de machine learning.

### 13.10. Comparacion entre prediccion y valor real

Una parte importante de la aplicacion practica es la comparacion entre la prediccion generada y el valor real publicado posteriormente por OMIE. Esta comparacion permite evaluar el error en un caso concreto y entender las limitaciones del modelo. Aunque las metricas agregadas son necesarias, los ejemplos individuales ayudan a interpretar el comportamiento real de la aplicacion.

Durante las pruebas del proyecto se realizo una inferencia para el periodo `2026-01-01 00:00`. El modelo entrenado con datos de 2025 predijo un precio de `94.20 EUR/MWh`, mientras que el valor real extraido de OMIE fue `112.01 EUR/MWh`. El error absoluto fue de `17.81 EUR/MWh`, equivalente a un error relativo aproximado del `15.90 %`.

Este resultado muestra una idea importante: incluso un modelo con buenas metricas globales puede fallar en periodos concretos. El 1 de enero es un dia festivo con patrones de demanda particulares, y puede diferir de jornadas normales. Ademas, el modelo puede no incorporar todas las variables necesarias para anticipar correctamente ese comportamiento, como demanda prevista, meteorologia, disponibilidad de tecnologias, gas, CO2 o festivos.

La comparacion con el valor real permite identificar lineas de mejora. Una primera mejora seria incorporar calendarios de festivos nacionales y autonomicos. Otra seria incluir demanda prevista y generacion renovable prevista de forma mas completa. Tambien podria mejorarse el tratamiento de datos cuarto-horarios, adaptando retardos a duraciones reales en lugar de a numero de periodos.

La aplicacion ya incorpora una referencia adicional mediante el baseline `lag 24`. Este baseline predice usando el precio de 24 periodos antes. Comparar el modelo contra esta regla simple permite saber si el aprendizaje automatico aporta valor. En los experimentos realizados, los modelos entrenados mejoraron claramente este baseline en metricas agregadas, aunque eso no elimina errores puntuales.

El analisis de casos concretos es una herramienta diagnostica. Cuando una prediccion falla, no debe interpretarse solo como un numero negativo, sino como una oportunidad para estudiar que informacion faltaba. Si el error se concentra en festivos, horas solares, picos de gas o cambios de resolucion, esas observaciones orientan futuras mejoras del sistema.

En conclusion, la aplicacion practica desarrollada permite recorrer todo el ciclo: obtener datos, preparar variables, entrenar modelos, evaluar resultados, inferir el siguiente periodo y comparar la prediccion con valores reales. Esta capacidad convierte el proyecto en una demostracion completa de prediccion aplicada al mercado electrico espanol, con un equilibrio razonable entre sencillez, utilidad y posibilidades de ampliacion.
