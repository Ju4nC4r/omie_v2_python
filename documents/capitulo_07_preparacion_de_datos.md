# Capitulo 7. Preparacion de datos

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 7.1. Descarga automatizada de datos OMIE

La preparacion de datos comienza con la descarga automatizada de los precios publicados por OMIE. Esta fase es esencial porque el modelo predictivo depende de una serie historica fiable, ordenada y suficientemente amplia. En el proyecto desarrollado, la descarga se realiza a partir de un rango de fechas definido por el usuario. El sistema recorre cada dia del intervalo y solicita el fichero diario correspondiente al precio marginal del mercado diario.

La automatizacion evita una tarea manual repetitiva y reduce errores. Si el usuario tuviera que descargar cada fichero diario a mano, el proceso seria lento, dificil de reproducir y propenso a omisiones. En cambio, el programa genera automaticamente el nombre esperado del fichero mediante la fecha, por ejemplo `marginalpdbc_YYYYMMDD.1`, y lo solicita a traves del endpoint publico de descarga de OMIE.

Cada fichero descargado se almacena en el directorio `data/raw/`. Esta carpeta actua como cache de datos originales. Si el fichero ya existe y tiene contenido, el sistema lo reutiliza en lugar de descargarlo de nuevo. Esta decision mejora la eficiencia del flujo de trabajo, especialmente cuando se repiten entrenamientos sobre el mismo periodo o cuando se hacen pruebas cambiando solo el modelo.

El proceso de descarga incluye comprobaciones basicas de validez. Despues de recibir la respuesta del servidor, el programa verifica que el contenido contiene la marca esperada `MARGINALPDBC`. Si no aparece, se interpreta que OMIE no ha devuelto el fichero correcto o que ha ocurrido algun problema. En ese caso, se lanza un error descriptivo con informacion de la fecha afectada.

En rangos largos puede ocurrir que algun dia concreto no este disponible o que se produzca un error temporal de red. El programa esta preparado para registrar fallos por dia sin detener necesariamente todo el proceso. Si al menos se cargan algunos ficheros validos, se concatenan y se continua. Si no se consigue cargar ningun fichero, se detiene la ejecucion con un mensaje de error. Esta estrategia permite trabajar con periodos amplios sin que un unico dia problematico inutilice todo el experimento.

Una vez descargados y parseados los ficheros diarios, los datos se agrupan en un unico `DataFrame`. El resultado se ordena cronologicamente y se eliminan duplicados por `timestamp`. Finalmente, el conjunto procesado se guarda como `data/processed/omie_prices.csv`. Este fichero es la primera version estructurada del dataset y sirve de entrada para fases posteriores.

La descarga automatizada de OMIE cumple tres objetivos metodologicos. Primero, garantiza que la fuente de precios sea oficial y reproducible. Segundo, permite ampliar facilmente el periodo de entrenamiento. Tercero, separa claramente los datos originales de los datos procesados. Esta separacion es importante para depurar errores y para reconstruir el proceso desde el inicio si fuera necesario.

### 7.2. Descarga opcional de datos ESIOS

La segunda fuente de datos del proyecto es ESIOS, utilizada de forma opcional. Mientras que OMIE proporciona el precio objetivo, ESIOS permite incorporar informacion externa sobre prevision de generacion renovable. En concreto, el sistema contempla la descarga de prevision eolica, solar fotovoltaica y solar termica. Estas variables pueden ayudar a explicar variaciones de precio que no se deducen completamente del calendario o del historico de precios.

La descarga de ESIOS requiere un token de acceso. Por este motivo, el programa no obliga a usar esta fuente. El usuario puede entrenar un modelo usando solo OMIE o activar ESIOS si dispone de credenciales. Esta decision hace que el proyecto sea accesible desde el primer momento y, al mismo tiempo, permite enriquecer el modelo cuando se cuenta con informacion adicional.

En la implementacion, los indicadores utilizados son `541` para prevision eolica, `542` para prevision solar fotovoltaica y `543` para prevision solar termica. Cada indicador se descarga mediante la API de ESIOS y se transforma en una tabla con dos columnas principales: `timestamp` y valor. Posteriormente, cada valor se renombra con el nombre de variable utilizado por el modelo: `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`.

Las fechas recibidas desde ESIOS se normalizan a la zona horaria `Europe/Madrid` y despues se eliminan las marcas de zona horaria para mantener consistencia con los datos de OMIE. Esta normalizacion es necesaria porque una diferencia de zona horaria podria desplazar observaciones y provocar que una prevision se asociara al periodo equivocado. En series temporales energeticas, un desfase de una hora puede degradar mucho la calidad del dataset.

Una vez descargados los indicadores, el programa los combina en una unica tabla de generacion prevista. A partir de las variables originales se calculan tambien variables derivadas. `solar_forecast_mwh` suma la prevision solar fotovoltaica y la solar termica. `renewable_forecast_mwh` suma la prevision eolica y la solar total. `wind_solar_ratio` relaciona la prevision eolica con la solar. Estas variables resumen la estructura renovable prevista y pueden facilitar el aprendizaje del modelo.

Los datos de ESIOS tambien se almacenan en cache dentro de `data/processed/`, con nombres que incluyen el rango temporal, como `esios_generation_YYYYMMDD_YYYYMMDD.csv`. Esto evita repetir llamadas a la API si se vuelve a entrenar sobre el mismo periodo. La cache es especialmente util en APIs autenticadas, donde conviene reducir peticiones innecesarias.

La descarga opcional de ESIOS representa una mejora respecto al modelo inicial. El precio electrico no depende solo de su propia historia. Factores fisicos del sistema, como la disponibilidad prevista de renovables, son relevantes en la formacion del precio. Incorporar estas variables permite que el modelo observe parte del contexto del mercado y no solo patrones pasados.

### 7.3. Limpieza de datos

La limpieza de datos transforma los ficheros descargados en una estructura coherente para el entrenamiento. En los ficheros `MARGINALPDBC`, no todas las lineas contienen observaciones de precio. Algunas lineas pueden ser cabeceras, comentarios o separadores. El parser descarta lineas vacias, lineas que comienzan con `MARGINALPDBC` y lineas que comienzan con `*`. Despues divide las lineas restantes por punto y coma y comprueba que existan suficientes campos.

Los valores numericos se convierten a formato decimal. En los ficheros de OMIE, los precios pueden aparecer con coma decimal, por lo que el programa reemplaza la coma por punto antes de convertirlos a `float`. Esta conversion es necesaria para que pandas y scikit-learn puedan operar con los precios como variables numericas.

Cada fila valida genera un registro con fecha, periodo, precio marginal portugues y precio marginal espanol. Aunque el objetivo del modelo es el precio espanol, conservar el precio portugues puede ser util para analisis futuros, dado que ambos mercados pertenecen al entorno iberico. Sin embargo, en la version actual del modelo, la variable objetivo es `marginal_es`.

Una parte importante de la limpieza es la eliminacion de duplicados. Despues de concatenar todos los dias descargados, el programa elimina observaciones duplicadas usando la columna `timestamp`. Esto evita que una misma hora o periodo aparezca dos veces en el entrenamiento, lo que podria sesgar el modelo y alterar las metricas.

Tambien se ordenan las observaciones cronologicamente. El orden temporal es imprescindible para construir retardos, medias moviles y diferencias. Si los registros estuvieran desordenados, el precio anterior podria no ser realmente anterior y las variables derivadas perderian sentido. Por esta razon, el sistema ordena por fecha y periodo durante el parseo y posteriormente por `timestamp` tras concatenar todos los datos.

En el caso de ESIOS, la limpieza incluye convertir los valores de la API a numericos, agrupar registros por `timestamp` y sumar valores cuando corresponde. Tambien se ordenan las observaciones y se gestionan posibles valores ausentes despues de unir los distintos indicadores. Esta limpieza busca obtener una tabla renovable compacta y alineable con OMIE.

La limpieza de datos no pretende modificar artificialmente el comportamiento del mercado. Su objetivo es eliminar elementos no estructurados, normalizar formatos y asegurar que cada fila represente una observacion temporal valida. Esta fase es discreta, pero decisiva: un modelo avanzado no compensa errores basicos de parseo, duplicados o desorden temporal.

### 7.4. Normalizacion de fechas y periodos

La normalizacion temporal convierte la informacion de fecha y periodo en una columna comun llamada `timestamp`. Esta columna es el eje del proyecto. Permite ordenar observaciones, unir OMIE con ESIOS, calcular variables temporales, separar entrenamiento y validacion e inferir el siguiente periodo disponible.

En los ficheros OMIE, cada fila incluye ano, mes, dia y periodo. El periodo indica la posicion dentro del dia, pero no es por si solo una fecha completa. Por ello, el programa crea primero una fecha base y despues suma un desplazamiento temporal en funcion del periodo. El desplazamiento depende de la frecuencia detectada para ese dia.

Si el dia contiene 24 periodos, cada periodo se interpreta como una hora. El periodo 1 corresponde al inicio del dia, el periodo 2 a la siguiente hora y asi sucesivamente. Si el dia contiene 96 periodos, cada periodo representa 15 minutos. En ese caso, el periodo 2 corresponde a las 00:15, el periodo 3 a las 00:30 y el periodo 4 a las 00:45.

La deteccion de frecuencia se realiza calculando el periodo maximo de cada dia. Si el maximo es superior a 25, el programa considera que el dia es cuarto-horario; en caso contrario, lo considera horario. Esta regla permite procesar tanto ficheros historicos horarios como ficheros con resolucion mas fina sin pedir configuracion adicional al usuario.

La normalizacion de fechas tambien afecta a ESIOS. Los datos de la API pueden venir con informacion de zona horaria. El programa convierte esos valores a hora local de Madrid y elimina la zona horaria para que los `timestamp` sean comparables con los de OMIE. Esta decision evita errores de union derivados de mezclar fechas con y sin zona horaria.

Una vez normalizadas las fechas, todas las fases posteriores pueden trabajar con una misma referencia temporal. Esto simplifica el diseno del pipeline. En lugar de depender de combinaciones de ano, mes, dia y periodo, el sistema utiliza `timestamp` como clave principal. La columna `period` se conserva porque aporta informacion util al modelo y a la interpretacion del periodo dentro del dia.

La normalizacion temporal tambien facilita la deteccion del siguiente periodo para inferencia. El programa calcula la diferencia temporal mas frecuente entre observaciones recientes y la suma al ultimo `timestamp`. Asi puede predecir una hora siguiente en datos horarios o un cuarto de hora siguiente en datos cuarto-horarios. Esta flexibilidad es importante porque el mercado puede evolucionar hacia resoluciones temporales distintas.

### 7.5. Union de datos por `timestamp`

Cuando se activan variables ESIOS, es necesario combinar los datos de precio de OMIE con las previsiones renovables. La union se realiza a traves de la columna `timestamp`, que actua como referencia temporal comun. Esta decision permite que cada observacion de precio incorpore la informacion renovable prevista disponible para el mismo periodo o para el instante inmediatamente anterior.

La union no siempre puede hacerse mediante igualdad exacta. OMIE puede contener datos horarios o cuarto-horarios, mientras que ESIOS se descarga con truncado horario. Si se exigiera coincidencia exacta, algunas observaciones de OMIE quedarian sin variables externas, especialmente en datos de 15 minutos. Para resolverlo, el proyecto utiliza una union temporal aproximada mediante `merge_asof`.

La union aproximada se realiza hacia atras. Esto significa que para cada `timestamp` de OMIE se busca la ultima prevision ESIOS disponible anterior o igual al instante de precio. Ademas, se aplica una tolerancia de una hora. Esta condicion evita asociar una prevision demasiado antigua a un precio posterior. Es una decision metodologica razonable para combinar resoluciones temporales distintas sin introducir informacion futura.

El hecho de usar una union hacia atras es importante para evitar fuga de informacion. En un contexto predictivo, no deberia utilizarse una observacion futura de ESIOS para explicar un precio anterior. Aunque las variables sean previsiones, mantener una disciplina temporal coherente ayuda a que el dataset se parezca mas a un escenario real de inferencia.

Despues de la union, las columnas renovables pueden contener huecos. El programa aplica relleno hacia delante y hacia atras sobre las columnas ESIOS. Esta tecnica cubre pequenos desajustes o huecos derivados de la diferencia de frecuencia. No obstante, debe interpretarse como una solucion practica. En un trabajo futuro podria refinarse usando reglas mas estrictas, interpolacion o validacion de cobertura por periodo.

La union por `timestamp` permite construir un dataset enriquecido. Cada fila combina el precio marginal espanol, el periodo, el instante temporal y, si estan disponibles, las previsiones renovables. De este modo, el modelo recibe informacion historica y externa en una misma matriz de entrenamiento.

Esta fase es una de las mas delicadas del pipeline. Una union mal realizada puede desplazar variables, duplicar registros o introducir datos futuros. Por eso la normalizacion previa de fechas, la ordenacion cronologica y la tolerancia temporal son decisiones fundamentales para asegurar la validez del conjunto final.

### 7.6. Gestion de datos ausentes

Los datos ausentes aparecen por varias razones. En OMIE puede faltar un fichero diario, puede existir un error de descarga o puede haber cambios en la disponibilidad del servidor. En ESIOS puede faltar una prevision para una hora, el token puede no ser valido o la API puede devolver valores incompletos. Ademas, la propia ingenieria de variables genera valores ausentes al calcular retardos y medias moviles en las primeras filas.

El proyecto gestiona ausencias en varios niveles. En la descarga de OMIE, los fallos por dia se acumulan en una lista. Si algun dia falla pero otros se cargan correctamente, el proceso continua y muestra una advertencia. Esta estrategia permite entrenar con rangos amplios aunque haya algunos huecos. Si no se carga ningun fichero, la ejecucion se detiene porque no existe base suficiente para construir el dataset.

En la integracion de ESIOS, si no se reciben valores de generacion para el rango seleccionado, se lanza un error. Esto evita entrenar un modelo supuestamente enriquecido con columnas externas vacias. Tambien se exige que el usuario proporcione token cuando activa ESIOS. La validacion temprana del token evita que el sistema avance durante varios pasos para fallar al final.

Despues de unir ESIOS con OMIE, las columnas renovables se completan mediante relleno hacia delante y hacia atras. El relleno hacia delante utiliza el ultimo valor conocido para completar observaciones posteriores. El relleno hacia atras cubre huecos iniciales usando el primer valor disponible. Esta combinacion es util para pequenos huecos, aunque debe considerarse una aproximacion.

La gestion mas importante de ausentes ocurre durante la construccion del dataset supervisado. Las variables retardadas, medias moviles y desviaciones no pueden calcularse para las primeras observaciones porque no existe suficiente historico previo. Por ejemplo, un retardo de 336 periodos requiere al menos 336 observaciones anteriores. Estas primeras filas quedan con valores `NaN`.

El programa elimina las filas que tienen valores ausentes en las columnas de entrada o en la variable objetivo. Esta decision garantiza que scikit-learn reciba una matriz completa. Tambien evita que el modelo aprenda de observaciones incompletas o mal definidas. La consecuencia es que se pierde una parte inicial del periodo, pero se gana consistencia en el entrenamiento.

La eliminacion de filas con ausentes implica que el usuario debe elegir un rango temporal suficientemente amplio. Si el intervalo es demasiado corto, los retardos largos y las ventanas moviles dejaran pocas filas utiles. Por esta razon, el README recomienda utilizar varios meses de datos y el programa puede avisar cuando no hay historico suficiente para construir variables de prediccion.

La gestion de ausencias forma parte de la calidad del modelo. No se trata solo de evitar errores de ejecucion; tambien se trata de asegurar que cada observacion de entrenamiento represente informacion disponible y coherente. Una politica clara de ausentes mejora la reproducibilidad y facilita explicar por que ciertas filas se descartan.

### 7.7. Construccion del dataset supervisado

Una vez descargados, limpiados y normalizados los datos, el proyecto construye un dataset supervisado. En aprendizaje supervisado, cada ejemplo se compone de unas variables de entrada y una salida conocida. En este caso, las entradas son caracteristicas temporales, historicas y opcionalmente renovables; la salida es el precio marginal espanol `marginal_es`.

La construccion comienza anadiendo variables temporales. A partir del `timestamp` se calculan variables ciclicas de hora, minuto del dia, dia de la semana y mes. El uso de senos y cosenos permite representar ciclos de forma continua. Por ejemplo, las 23:00 y las 00:00 estan cerca en el ciclo diario, aunque numericamente 23 y 0 parezcan alejados. Esta codificacion es especialmente util para modelos lineales y redes neuronales.

Tambien se crea la variable `is_weekend`, que indica si la observacion corresponde a sabado o domingo. Los fines de semana suelen presentar patrones de demanda diferentes a los dias laborables, por lo que esta variable aporta informacion relevante. La columna `period` se conserva como caracteristica adicional, ya que representa la posicion dentro del dia.

Despues se calculan retardos del precio. El proyecto utiliza retardos de `1`, `2`, `3`, `4`, `5`, `6`, `12`, `23`, `24`, `25`, `48`, `72`, `168` y `336` periodos. Estos retardos capturan informacion reciente, diaria y semanal. Por ejemplo, `price_lag_1` representa el precio inmediatamente anterior, mientras que `price_lag_168` aproxima el comportamiento de la semana anterior en datos horarios.

Tambien se generan medias moviles y desviaciones moviles para ventanas de `3`, `6`, `12`, `24`, `48` y `168` periodos. Estas variables resumen el comportamiento reciente del precio. Las medias moviles suavizan fluctuaciones y permiten detectar niveles generales; las desviaciones moviles aportan informacion sobre volatilidad reciente.

Adicionalmente se calculan minimos y maximos recientes en ventanas de 24 y 168 periodos, diferencias entre precios retardados y ratios frente al dia o la semana anterior. Estas variables buscan capturar cambios de regimen, subidas, bajadas y relaciones relativas. El objetivo es proporcionar al modelo una vision mas rica que el precio bruto.

Para evitar fuga de informacion, las medias moviles se calculan sobre el precio desplazado un periodo. Es decir, al generar variables para una observacion, no se utiliza el precio objetivo de esa misma observacion dentro de sus medias. Esta decision es metodologicamente importante porque impide que el modelo vea indirectamente el valor que debe predecir.

Si el dataset incluye columnas ESIOS, el sistema las anade automaticamente a la lista de variables de entrada. En ese caso, la matriz de entrenamiento combina las variables base con `wind_forecast_mwh`, `solar_pv_forecast_mwh`, `solar_thermal_forecast_mwh`, `renewable_forecast_mwh`, `solar_forecast_mwh` y `wind_solar_ratio`. Si no existen, el modelo se entrena solo con variables base.

El resultado final de esta fase es una matriz `X` con variables explicativas y una serie `y` con el precio objetivo. Este par de objetos se utiliza directamente en el entrenamiento. La separacion clara entre preparacion de datos y entrenamiento permite reutilizar el mismo dataset con varios modelos: Ridge, MLP, HistGradientBoosting o modo automatico.

### 7.8. Separacion temporal entre entrenamiento y validacion

La ultima fase de preparacion antes del entrenamiento es la separacion temporal entre datos de entrenamiento y datos de validacion. En problemas de series temporales, esta separacion debe respetar el orden cronologico. No seria correcto mezclar aleatoriamente observaciones de todo el periodo, porque el modelo podria entrenarse con datos posteriores y evaluarse sobre datos anteriores. Eso produciria una evaluacion artificialmente optimista.

El enfoque adecuado consiste en entrenar con la parte inicial de la serie y validar con la parte final. Este procedimiento simula mejor un escenario real: se dispone de historico pasado y se intenta predecir un periodo posterior. La validacion temporal permite estimar como se comportaria el modelo ante datos no vistos situados despues del periodo de entrenamiento.

En el proyecto, esta logica se aplica despues de construir el dataset supervisado. Primero se generan todas las variables respetando el orden temporal y evitando fuga de informacion. Despues se divide la matriz resultante en un tramo de entrenamiento y otro de validacion. Los modelos se ajustan con el primer tramo y se evaluan con el segundo.

La validacion temporal es especialmente importante cuando se comparan modelos. Ridge, MLP y HistGradientBoosting deben evaluarse sobre el mismo tramo final para que la comparacion sea justa. El modo `auto` utiliza esta idea para seleccionar el modelo con menor MAE en validacion. Si cada modelo se evaluara sobre datos distintos, la seleccion no seria fiable.

Esta separacion tambien permite comparar contra un baseline. El baseline `lag 24` usa como prediccion el precio de 24 periodos antes. Aunque es una regla simple, representa una referencia util. Un modelo de machine learning debe mejorar claramente esta referencia para justificar su complejidad. Evaluar ambos sobre el mismo tramo temporal hace que la comparacion sea interpretable.

La preparacion de datos condiciona directamente la calidad de esta validacion. Si hay huecos temporales, cambios de resolucion o variables mal alineadas, las metricas pueden ser dificiles de interpretar. Por eso las fases anteriores de descarga, limpieza, normalizacion y gestion de ausentes no son solo pasos tecnicos, sino requisitos para una evaluacion correcta.

En resumen, la preparacion de datos transforma ficheros diarios y previsiones externas en una matriz supervisada lista para entrenamiento. El proceso descarga OMIE, incorpora ESIOS cuando procede, limpia registros, normaliza fechas, une fuentes por `timestamp`, gestiona ausencias, construye variables y respeta el orden temporal. Esta cadena de pasos permite que los modelos trabajen sobre datos coherentes y que sus resultados puedan interpretarse con rigor.
