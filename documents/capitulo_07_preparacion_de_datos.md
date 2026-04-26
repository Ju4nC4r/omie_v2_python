# Capítulo 7. Preparación de datos

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 7.1. Descarga automatizada de datos OMIE

La preparación de datos comienza con la descarga automatizada de los precios publicados por OMIE. Esta fase es esencial porque el modelo predictivo depende de una serie histórica fiable, ordenada y suficientemente amplia. En el proyecto desarrollado, la descarga se realiza a partir de un rango de fechas definido por el usuario. El sistema recorre cada día del intervalo y solicita el fichero diario correspondiente al precio marginal del mercado diario.

La automatización evita una tarea manual repetitiva y reduce errores. Si el usuario tuviera que descargar cada fichero diario a maño, el proceso sería lento, difícil de reproducir y propenso a omisiones. En cambio, el programa genera automáticamente el nombre esperado del fichero mediante la fecha, por ejemplo `marginalpdbc_YYYYMMDD.1`, y lo solicita a través del endpoint público de descarga de OMIE.

Cada fichero descargado se almacena en el directorio `data/raw/`. Esta carpeta actua como cache de datos originales. Si el fichero ya existe y tiene contenido, el sistema lo reutiliza en lugar de descargarlo de nuevo. Esta decisión mejora la eficiencia del flujo de trabajo, especialmente cuando se repiten entrenamientos sobre el mismo periodo o cuando se hacen pruebas cambiando solo el modelo.

El proceso de descarga incluye comprobaciones básicas de validez. Después de recibir la respuesta del servidor, el programa verifica que el contenido contiene la marca esperada `MARGINALPDBC`. Si no aparece, se interpreta que OMIE no ha devuelto el fichero correcto o que ha ocurrido algún problema. En ese caso, se lanza un error descriptivo con información de la fecha afectada.

En rangos largos puede ocurrir que algún día concreto no esté disponible o que se produzca un error temporal de red. El programa está preparado para registrar fallos por día sin detener necesariamente todo el proceso. Si al menos se cargan algunos ficheros válidos, se concatenan y se continúa. Si no se consigue cargar ningún fichero, se detiene la ejecución con un mensaje de error. Esta estrategia permite trabajar con periodos amplios sin que un único día problemático inutilice todo el experimento.

Una vez descargados y parseados los ficheros diarios, los datos se agrupan en un único `DataFrame`. El resultado se ordena cronológicamente y se eliminan duplicados por `timestamp`. Finalmente, el conjunto procesado se guarda como `data/processed/omie_prices.csv`. Este fichero es la primera versión estructurada del dataset y sirve de entrada para fases posteriores.

La descarga automatizada de OMIE cumple tres objetivos metodológicos. Primero, garantiza que la fuente de precios sea oficial y reproducible. Segundo, permite ampliar fácilmente el periodo de entrenamiento. Tercero, separa claramente los datos originales de los datos procesados. Esta separación es importante para depurar errores y para reconstruir el proceso desde el inicio si fuera necesario.

### 7.2. Descarga opcional de datos ESIOS

La segunda fuente de datos del proyecto es ESIOS, utilizada de forma opcional. Mientras que OMIE proporciona el precio objetivo, ESIOS permite incorporar información externa sobre previsión de generación renovable. En concreto, el sistema contempla la descarga de previsión eólica, solar fotovoltaica y solar térmica. Estas variables pueden ayudar a explicar variaciones de precio que no se deducen completamente del calendario o del histórico de precios.

La descarga de ESIOS requiere un token de acceso. Por este motivo, el programa no obliga a usar está fuente. El usuario puede entrenar un modelo usando solo OMIE o activar ESIOS si dispone de credenciales. Esta decisión hace que el proyecto sea accesible desde el primer momento y, al mismo tiempo, permite enriquecer el modelo cuando se cuenta con información adicional.

En la implementación, los indicadores utilizados son `541` para previsión eólica, `542` para previsión solar fotovoltaica y `543` para previsión solar térmica. Cada indicador se descarga mediante la API de ESIOS y se transforma en una tabla con dos columnas principales: `timestamp` y valor. Posteriormente, cada valor se renombra con el nombre de variable utilizado por el modelo: `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`.

Las fechas recibidas desde ESIOS se normalizan a la zona horaria `Europe/Madrid` y después se eliminan las marcas de zona horaria para mantener consistencia con los datos de OMIE. Esta normalización es necesaria porque una diferencia de zona horaria podría desplazar observaciones y provocar que una previsión se asociara al periodo equivocado. En series temporales energéticas, un desfase de una hora puede degradar mucho la calidad del dataset.

Una vez descargados los indicadores, el programa los combina en una única tabla de generación prevista. A partir de las variables originales se calculan también variables derivadas. `solar_forecast_mwh` suma la previsión solar fotovoltaica y la solar térmica. `renewable_forecast_mwh` suma la previsión eólica y la solar total. `wind_solar_ratio` relaciona la previsión eólica con la solar. Estas variables resumen la estructura renovable prevista y pueden facilitar el aprendizaje del modelo.

Los datos de ESIOS también se almacenan en cache dentro de `data/processed/`, con nombres que incluyen el rango temporal, como `esios_generation_YYYYMMDD_YYYYMMDD.csv`. Esto evita repetir llamadas a la API si se vuelve a entrenar sobre el mismo periodo. La cache es especialmente útil en APIs autenticadas, donde conviene reducir peticiones innecesarias.

La descarga opcional de ESIOS representa una mejora respecto al modelo inicial. El precio eléctrico no depende solo de su propia historia. Factores físicos del sistema, como la disponibilidad prevista de renovables, son relevantes en la formación del precio. Incorporar estas variables permite que el modelo observe parte del contexto del mercado y no solo patrones pasados.

### 7.3. Limpieza de datos

La limpieza de datos transforma los ficheros descargados en una estructura coherente para el entrenamiento. En los ficheros `MARGINALPDBC`, no todas las líneas contienen observaciones de precio. Algunas líneas pueden ser cabeceras, comentarios o separadores. El parser descarta líneas vacías, líneas que comienzan con `MARGINALPDBC` y líneas que comienzan con `*`. Después divide las líneas restantes por punto y coma y comprueba que existan suficientes campos.

Los valores numericos se convierten a formato decimal. En los ficheros de OMIE, los precios pueden aparecer con coma decimal, por lo que el programa reemplaza la coma por punto antes de convertirlos a `float`. Esta conversión es necesaria para que pandas y scikit-learn puedan operar con los precios como variables numéricas.

Cada fila válida genera un registro con fecha, periodo, precio marginal portugués y precio marginal español. Aunque el objetivo del modelo es el precio español, conservar el precio portugués puede ser útil para análisis futuros, dado que ambos mercados pertenecen al entorno ibérico. Sin embargo, en la versión actual del modelo, la variable objetivo es `marginal_es`.

Una parte importante de la limpieza es la eliminacion de duplicados. Después de concatenar todos los días descargados, el programa elimina observaciones duplicadas usando la columna `timestamp`. Esto evita que una misma hora o periodo aparezca dos veces en el entrenamiento, lo que podría sesgar el modelo y alterar las métricas.

También se ordenan las observaciones cronológicamente. El orden temporal es imprescindible para construir retardos, medias móviles y diferencias. Si los registros estuvieran desordenados, el precio anterior podría no ser realmente anterior y las variables derivadas perderian sentido. Por está razón, el sistema ordena por fecha y periodo durante el parseo y posteriormente por `timestamp` tras concatenar todos los datos.

En el caso de ESIOS, la limpieza incluye convertir los valores de la API a numericos, agrupar registros por `timestamp` y sumar valores cuando corresponde. También se ordenan las observaciones y se gestionan posibles valores ausentes después de unir los distintos indicadores. Esta limpieza busca obtener una tabla renovable compacta y alíneable con OMIE.

La limpieza de datos no pretende modificar artificialmente el comportamiento del mercado. Su objetivo es eliminar elementos no estructurados, normalizar formatos y asegurar que cada fila represente una observación temporal válida. Esta fase es discreta, pero decisiva: un modelo avanzado no compensa errores básicos de parseo, duplicados o desorden temporal.

### 7.4. Normalización de fechas y periodos

La normalización temporal convierte la información de fecha y periodo en una columna común llamada `timestamp`. Esta columna es el eje del proyecto. Permite ordenar observaciones, unir OMIE con ESIOS, calcular variables temporales, separar entrenamiento y validación e inferir el siguiente periodo disponible.

En los ficheros OMIE, cada fila incluye año, mes, día y periodo. El periodo indica la posición dentro del día, pero no es por sí solo una fecha completa. Por ello, el programa crea primero una fecha base y después suma un desplazamiento temporal en función del periodo. El desplazamiento depende de la frecuencia detectada para ese día.

Si el día contiene 24 periodos, cada periodo se interpreta como una hora. El periodo 1 corresponde al inicio del día, el periodo 2 a la siguiente hora y así sucesivamente. Si el día contiene 96 periodos, cada periodo representa 15 minutos. En ese caso, el periodo 2 corresponde a las 00:15, el periodo 3 a las 00:30 y el periodo 4 a las 00:45.

La deteccion de frecuencia se realiza calculando el periodo máximo de cada día. Si el máximo es superior a 25, el programa considera que el día es cuarto-horario; en caso contrario, lo considera horario. Esta regla permite procesar tanto ficheros históricos horarios como ficheros con resolución más fina sin pedir configuración adicional al usuario.

La normalización de fechas también afecta a ESIOS. Los datos de la API pueden venir con información de zona horaria. El programa convierte esos valores a hora local de Madrid y elimina la zona horaria para que los `timestamp` sean comparables con los de OMIE. Esta decisión evita errores de unión derivados de mezclar fechas con y sin zona horaria.

Una vez normalizadas las fechas, todas las fases posteriores pueden trabajar con una misma referencia temporal. Esto simplifica el diseño del pipeline. En lugar de depender de combinaciones de año, mes, día y periodo, el sistema utiliza `timestamp` como clave principal. La columna `period` se conserva porqué aporta información útil al modelo y a la interpretación del periodo dentro del día.

La normalización temporal también facilita la deteccion del siguiente periodo para inferencia. El programa calcula la diferencia temporal más frecuente entre observaciones recientes y la suma al último `timestamp`. Asi puede predecir una hora siguiente en datos horarios o un cuarto de hora siguiente en datos cuarto-horarios. Esta flexibilidad es importante porque el mercado puede evolucionar hacia resoluciones temporales distintas.

### 7.5. Unión de datos por `timestamp`

Cuando se activan variables ESIOS, es necesario combinar los datos de precio de OMIE con las previsiones renovables. La unión se realiza a través de la columna `timestamp`, que actua como referencia temporal común. Esta decisión permite que cada observación de precio incorpore la información renovable prevista disponible para el mismo periodo o para el instante inmediatamente anterior.

La unión no siempre puede hacerse mediante igualdad exacta. OMIE puede contener datos horarios o cuarto-horarios, mientras que ESIOS se descarga con truncado horario. Si se exigiera coincidencia exacta, algunas observaciones de OMIE quedarian sin variables externas, especialmente en datos de 15 minutos. Para resolverlo, el proyecto utiliza una unión temporal aproximada mediante `merge_asof`.

La unión aproximada se realiza hacia atrás. Esto significa que para cada `timestamp` de OMIE se busca la última previsión ESIOS disponible anterior o igual al instante de precio. Además, se aplica una tolerancia de una hora. Esta condicion evita asociar una previsión demasiado antigua a un precio posterior. Es una decisión metodológica razonable para combinar resoluciones temporales distintas sin introducir información futura.

El hecho de usar una unión hacia atrás es importante para evitar fuga de información. En un contexto predictivo, no debería utilizarse una observación futura de ESIOS para explicar un precio anterior. Aunque las variables sean previsiones, mantener una disciplina temporal coherente ayuda a que el dataset se parezca más a un escenario real de inferencia.

Después de la unión, las columnas renovables pueden contener huecos. El programa aplica relleno hacia delante y hacia atrás sobre las columnas ESIOS. Esta técnica cubre pequeños desajustes o huecos derivados de la diferencia de frecuencia. No obstante, debe interpretarse como una solución práctica. En un trabajo futuro podría refinarse usando reglas más estrictas, interpolación o validación de cobertura por periodo.

La unión por `timestamp` permite construir un dataset enriquecido. Cada fila combina el precio marginal español, el periodo, el instante temporal y, si están disponibles, las previsiones renovables. De este modo, el modelo recibe información histórica y externa en una misma matriz de entrenamiento.

Esta fase es una de las más delicadas del pipeline. Una unión mal realizada puede desplazar variables, duplicar registros o introducir datos futuros. Por eso la normalización previa de fechas, la ordenación cronológica y la tolerancia temporal son decisiones fundamentales para asegurar la validez del conjunto final.

### 7.6. Gestión de datos ausentes

Los datos ausentes aparecen por varias razones. En OMIE puede faltar un fichero diario, puede existir un error de descarga o puede haber cambios en la disponibilidad del servidor. En ESIOS puede faltar una previsión para una hora, el token puede no ser válido o la API puede devolver valores incompletos. Además, la propia ingeniería de variables genera valores ausentes al calcular retardos y medias móviles en las primeras filas.

El proyecto gestiona ausencias en varios niveles. En la descarga de OMIE, los fallos por día se acumulan en una lista. Si algún día falla pero otros se cargan correctamente, el proceso continúa y muestra una advertencia. Esta estrategia permite entrenar con rangos amplios aunque haya algunos huecos. Si no se carga ningún fichero, la ejecución se detiene porque no existe base suficiente para construir el dataset.

En la integración de ESIOS, si no se reciben valores de generación para el rango seleccionado, se lanza un error. Esto evita entrenar un modelo supuestamente enriquecido con columnas externas vacías. También se exige que el usuario proporcione token cuando activa ESIOS. La validación temprana del token evita que el sistema avance durante varios pasos para fallar al final.

Después de unir ESIOS con OMIE, las columnas renovables se completan mediante relleno hacia delante y hacia atrás. El relleno hacia delante utiliza el último valor conocido para completar observaciones posteriores. El relleno hacia atrás cubre huecos iniciales usando el primer valor disponible. Esta combinación es útil para pequeños huecos, aunque debe considerarse una aproximación.

La gestión más importante de ausentes ocurre durante la construcción del dataset supervisado. Las variables retardadas, medias móviles y desviaciones no pueden calcularse para las primeras observaciones porque no existe suficiente histórico previo. Por ejemplo, un retardo de 336 periodos requiere al menos 336 observaciones anteriores. Estas primeras filas quedan con valores `NaN`.

El programa elimina las filas que tienen valores ausentes en las columnas de entrada o en la variable objetivo. Esta decisión garantiza que scikit-learn reciba una matriz completa. También evita que el modelo aprenda de observaciones incompletas o mal definidas. La consecuencia es que se pierde una parte inicial del periodo, pero se gana consistencia en el entrenamiento.

La eliminacion de filas con ausentes implica que el usuario debe elegir un rango temporal suficientemente amplio. Si el intervalo es demasiado corto, los retardos largos y las ventanas móviles dejaran pocas filas útiles. Por está razón, el README recomienda utilizar varios meses de datos y el programa puede avisar cuando no hay histórico suficiente para construir variables de predicción.

La gestión de ausencias forma parte de la calidad del modelo. No se trata solo de evitar errores de ejecución; también se trata de asegurar que cada observación de entrenamiento represente información disponible y coherente. Una politica clara de ausentes mejora la reproducibilidad y facilita explicar por que ciertas filas se descartan.

### 7.7. Construcción del dataset supervisado

Una vez descargados, limpiados y normalizados los datos, el proyecto construye un dataset supervisado. En aprendizaje supervisado, cada ejemplo se compone de unas variables de entrada y una salida conocida. En este caso, las entradas son características temporales, históricas y opcionalmente renovables; la salida es el precio marginal español `marginal_es`.

La construcción comienza anadiendo variables temporales. A partir del `timestamp` se calculan variables cíclicas de hora, minuto del día, día de la semana y mes. El uso de senos y cosenos permite representar ciclos de forma continúa. Por ejemplo, las 23:00 y las 00:00 están cerca en el ciclo diario, aunque numéricamente 23 y 0 parezcan alejados. Esta codificación es especialmente útil para modelos lineales y redes neuronales.

También se crea la variable `is_weekend`, que indica si la observación corresponde a sábado o domingo. Los fines de semana suelen presentar patrones de demanda diferentes a los días laborables, por lo que esta variable aporta información relevante. La columna `period` se conserva como característica adicional, ya que representa la posición dentro del día.

Después se calculan retardos del precio. El proyecto utiliza retardos de `1`, `2`, `3`, `4`, `5`, `6`, `12`, `23`, `24`, `25`, `48`, `72`, `168` y `336` periodos. Estos retardos capturan información reciente, diaria y semanal. Por ejemplo, `price_lag_1` representa el precio inmediatamente anterior, mientras que `price_lag_168` aproxima el comportamiento de la semana anterior en datos horarios.

También se generan medias móviles y desviaciones móviles para ventanas de `3`, `6`, `12`, `24`, `48` y `168` periodos. Estas variables resumen el comportamiento reciente del precio. Las medias móviles suavizan fluctuaciones y permiten detectar niveles generales; las desviaciones móviles aportan información sobre volatilidad reciente.

Adicionalmente se calculan mínimos y máximos recientes en ventanas de 24 y 168 periodos, diferencias entre precios retardados y ratios frente al día o la semana anterior. Estas variables buscan capturar cambios de régimen, subidas, bajadas y relaciones relativas. El objetivo es proporcionar al modelo una visión más rica que el precio bruto.

Para evitar fuga de información, las medias móviles se calculan sobre el precio desplazado un periodo. Es decir, al generar variables para una observación, no se utiliza el precio objetivo de esa misma observación dentro de sus medias. Esta decisión es metodológicamente importante porque impide que el modelo vea indirectamente el valor que debe predecir.

Si el dataset incluye columnas ESIOS, el sistema las añade automáticamente a la lista de variables de entrada. En ese caso, la matriz de entrenamiento combina las variables base con `wind_forecast_mwh`, `solar_pv_forecast_mwh`, `solar_thermal_forecast_mwh`, `renewable_forecast_mwh`, `solar_forecast_mwh` y `wind_solar_ratio`. Si no existen, el modelo se entrena solo con variables base.

El resultado final de esta fase es una matriz `X` con variables explicativas y una serie `y` con el precio objetivo. Este par de objetos se utiliza directamente en el entrenamiento. La separación clara entre preparación de datos y entrenamiento permite reutilizar el mismo dataset con varios modelos: Ridge, MLP, HistGradientBoosting o modo automático.

### 7.8. Separación temporal entre entrenamiento y validación

La última fase de preparación antes del entrenamiento es la separación temporal entre datos de entrenamiento y datos de validación. En problemas de series temporales, esta separación debe respetar el orden cronológico. No sería correcto mezclar aleatoriamente observaciones de todo el periodo, porque el modelo podría entrenarse con datos posteriores y evaluarse sobre datos anteriores. Eso produciría una evaluación artificialmente optimista.

El enfoque adecuado consiste en entrenar con la parte inicial de la serie y validar con la parte final. Este procedimiento simula mejor un escenario real: se dispone de histórico pasado y se intenta predecir un periodo posterior. La validación temporal permite estimar cómo se comportaría el modelo ante datos no vistos situados después del periodo de entrenamiento.

En el proyecto, esta lógica se aplica después de construir el dataset supervisado. Primero se generan todas las variables respetando el orden temporal y evitando fuga de información. Después se divide la matriz resultante en un tramo de entrenamiento y otro de validación. Los modelos se ajustan con el primer tramo y se evalúan con el segundo.

La validación temporal es especialmente importante cuando se comparan modelos. Ridge, MLP y HistGradientBoosting deben evaluarse sobre el mismo tramo final para que la comparación sea justa. El modo `auto` utiliza esta idea para seleccionar el modelo con menor MAE en validación. Si cada modelo se evaluara sobre datos distintos, la selección no sería fiable.

Esta separación también permite comparar contra un baseline. El baseline `lag 24` usa como predicción el precio de 24 periodos antes. Aunque es una regla simple, representa una referencia útil. Un modelo de machine learning debe mejorar claramente esta referencia para justificar su complejidad. Evaluar ambos sobre el mismo tramo temporal hace que la comparación sea interpretable.

La preparación de datos condiciona directamente la calidad de esta validación. Si hay huecos temporales, cambios de resolución o variables mal alineadas, las métricas pueden ser difíciles de interpretar. Por eso las fases anteriores de descarga, limpieza, normalización y gestión de ausentes no son solo pasos técnicos, sino requisitos para una evaluación correcta.

En resumen, la preparación de datos transforma ficheros diarios y previsiones externas en una matriz supervisada lista para entrenamiento. El proceso descarga OMIE, incorpora ESIOS cuando procede, limpia registros, normaliza fechas, une fuentes por `timestamp`, gestiona ausencias, construye variables y respeta el orden temporal. Esta cadena de pasos permite que los modelos trabajen sobre datos coherentes y que sus resultados puedan interpretarse con rigor.
