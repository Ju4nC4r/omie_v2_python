# Capitulo 6. Fuentes de datos

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 6.1. Datos de precio del mercado diario OMIE

La fuente principal de datos utilizada en este trabajo es OMIE, el operador del mercado electrico iberico. OMIE publica informacion oficial sobre los resultados del mercado diario e intradiario, incluyendo precios marginales, energia casada y otros datos relevantes para el analisis del mercado electrico. En el proyecto desarrollado, la variable objetivo es el precio marginal espanol del mercado diario, expresado en euros por megavatio hora.

El mercado diario es especialmente adecuado para este trabajo porque ofrece una serie temporal publica, estructurada y directamente relacionada con el problema de prediccion. Cada dia se publica un conjunto de precios correspondientes a los periodos de entrega de energia. Tradicionalmente estos periodos han sido horarios, aunque el sistema tambien debe prepararse para manejar resoluciones cuarto-horarias cuando aparecen en los ficheros publicados.

En la aplicacion practica, los datos de OMIE se descargan automaticamente a partir del rango de fechas indicado por el usuario. Esta automatizacion evita tener que descargar manualmente cada fichero diario y permite repetir experimentos con distintos periodos. El usuario puede seleccionar un rango en la interfaz grafica o indicar fechas mediante linea de comandos. El sistema recorre cada dia del intervalo, intenta descargar el fichero correspondiente y lo transforma en una tabla procesable.

Los datos de OMIE tienen una ventaja importante: proceden de una fuente oficial y reproducible. Esto significa que cualquier persona puede reconstruir el mismo conjunto de precios si utiliza las mismas fechas y el mismo procedimiento de descarga. Para un Trabajo Fin de Grado, esta trazabilidad es fundamental, ya que permite justificar el origen de la variable objetivo y verificar los resultados obtenidos.

La variable extraida de OMIE es `price_eur_mwh`, que representa el precio marginal espanol del periodo. Esta columna se convierte en la salida que los modelos intentan predecir. A partir de ella se generan tambien variables retardadas, medias moviles, diferencias y estadisticos recientes. Por tanto, OMIE no solo proporciona la variable objetivo, sino tambien la base historica de la que se obtienen muchas variables explicativas.

El uso de OMIE como fuente principal tambien impone ciertas limitaciones. Los ficheros pueden no estar disponibles para algun dia concreto, pueden cambiar ligeramente de formato o pueden publicarse con distinta resolucion temporal. Ademas, el precio del mercado diario no incluye por si solo toda la informacion que explica su comportamiento. Factores como demanda, meteorologia, generacion renovable, gas, CO2 o interconexiones no estan completamente representados en el historico de precios. Por eso el proyecto contempla la incorporacion opcional de datos externos procedentes de ESIOS.

### 6.2. Formato de los ficheros `MARGINALPDBC`

El proyecto utiliza los ficheros publicos `MARGINALPDBC` de OMIE. Estos ficheros contienen informacion diaria sobre precios marginales del mercado diario para Espana y Portugal. Cada fichero corresponde a una fecha concreta y contiene filas con los periodos de entrega de ese dia.

El programa espera encontrar lineas con campos separados por punto y coma. A partir de esas lineas se extraen principalmente los siguientes datos: ano, mes, dia, periodo, precio marginal portugues y precio marginal espanol. Aunque el fichero puede contener cabeceras, comentarios u otros elementos, el parser del proyecto filtra las lineas relevantes y transforma cada registro en una observacion tabular.

El esquema conceptual utilizado por la aplicacion es el siguiente:

```text
anio;mes;dia;periodo;marginal_pt;marginal_es;
```

El campo `periodo` indica la posicion temporal dentro del dia. Si el fichero contiene 24 periodos, cada periodo se interpreta como una hora. Si contiene 96 periodos, cada periodo se interpreta como un cuarto de hora. Esta distincion es importante porque afecta a la construccion del `timestamp`, a los retardos temporales y a la interpretacion de variables como `lag_24`.

El parser convierte los campos de fecha y periodo en una columna temporal llamada `timestamp`. Para ello, primero identifica cuantos periodos tiene el dia. Si el maximo periodo del dia es superior a 25, el programa considera que la resolucion es de 15 minutos. En caso contrario, considera que la resolucion es horaria. A continuacion calcula el instante de cada observacion sumando al inicio del dia el desplazamiento correspondiente al periodo.

Por ejemplo, en un dia horario, el periodo 1 se interpreta como las 00:00, el periodo 2 como las 01:00 y asi sucesivamente. En un dia cuarto-horario, el periodo 1 se interpreta como las 00:00, el periodo 2 como las 00:15, el periodo 3 como las 00:30 y el periodo 4 como las 00:45. Esta normalizacion permite combinar dias de distinta granularidad dentro de una misma estructura temporal.

Una vez procesado el fichero, cada observacion queda representada con columnas como `date`, `period`, `timestamp`, `price_pt_eur_mwh` y `price_eur_mwh`. La columna portuguesa se conserva porque puede resultar util para analisis posteriores, aunque el objetivo del modelo desarrollado es el precio espanol. Mantener informacion adicional sin usarla necesariamente en la primera version facilita futuras ampliaciones.

El tratamiento de los ficheros `MARGINALPDBC` es una parte critica de la aplicacion. Si el parseo falla, todo el pipeline posterior queda comprometido. Por ese motivo, el codigo comprueba que el contenido descargado corresponde realmente a un fichero esperado de OMIE y lanza errores claros cuando no es asi. Esta gestion de errores permite detectar problemas de descarga, cambios de formato o dias no disponibles.

### 6.3. Datos de prevision eolica de ESIOS

Ademas de OMIE, el proyecto permite incorporar datos opcionales procedentes de ESIOS, el sistema de informacion del operador del sistema electrico gestionado por Red Electrica. En concreto, una de las variables externas consideradas es la prevision de generacion eolica. Esta informacion es relevante porque la energia eolica tiene un impacto directo en la formacion de precios del mercado electrico.

La generacion eolica presenta costes variables muy bajos. Cuando hay alta disponibilidad de viento, la produccion eolica puede desplazar a tecnologias mas caras dentro del orden de merito. Esto tiende a reducir el precio marginal, especialmente si la demanda no es suficientemente alta como para requerir tecnologias de mayor coste. Por el contrario, en periodos de bajo viento, el sistema puede necesitar recurrir a tecnologias como ciclos combinados, lo que puede elevar el precio.

En el programa, la prevision eolica se obtiene mediante el indicador ESIOS `541`, asociado a la columna `wind_forecast_mwh`. Esta variable representa una prevision de produccion eolica en MWh para el sistema electrico peninsular. Su inclusion permite que el modelo no dependa exclusivamente del historico de precios y calendario, sino que incorpore una senal fisica sobre la generacion renovable esperada.

El uso de prevision, y no solo de generacion real, es metodologicamente importante. En un escenario de prediccion real, antes de conocer el precio futuro tampoco se conoce con certeza la generacion renovable futura. Lo que puede utilizarse de forma coherente es una prevision disponible antes del periodo objetivo. Por tanto, las variables de ESIOS se plantean como informacion exogena que podria estar disponible en el momento de realizar la prediccion.

La integracion con ESIOS requiere un token de acceso. Por este motivo, el proyecto mantiene esta fuente como opcional. Si el usuario no dispone de token, el sistema puede entrenar usando solo datos OMIE. Si dispone de token, puede activar la opcion ESIOS desde la interfaz grafica o desde la linea de comandos. Esta decision evita que el proyecto dependa obligatoriamente de una API externa con autenticacion.

La variable eolica se une al dataset principal mediante `timestamp`. Cuando las resoluciones temporales no coinciden exactamente, el proyecto utiliza una union temporal aproximada basada en la ultima observacion disponible dentro de una tolerancia. Esta estrategia permite combinar precios cuarto-horarios con previsiones que pueden tener otra granularidad.

### 6.4. Datos de prevision solar fotovoltaica de ESIOS

La segunda fuente externa incorporada desde ESIOS es la prevision de generacion solar fotovoltaica. En el sistema electrico espanol, la energia solar fotovoltaica ha adquirido un peso creciente y su impacto en los precios es cada vez mas visible. Durante las horas centrales del dia, una alta generacion solar puede reducir la necesidad de tecnologias mas caras y presionar los precios a la baja.

La prevision solar fotovoltaica se obtiene mediante el indicador ESIOS `542`, que el programa transforma en la columna `solar_pv_forecast_mwh`. Esta variable representa la produccion fotovoltaica prevista y permite capturar patrones que no se deducen completamente del calendario. Aunque la hora y el mes indican de forma indirecta cuando puede haber radiacion solar, no informan sobre nubosidad, condiciones meteorologicas concretas o variabilidad diaria.

La energia solar tiene un perfil muy marcado. Su produccion se concentra en las horas con radiacion, desaparece durante la noche y varia segun la estacion del ano. En primavera y verano, las horas solares pueden tener un efecto especialmente relevante sobre el precio. En determinados periodos, una alta penetracion fotovoltaica puede llevar a precios muy bajos o incluso cercanos a cero si coincide con baja demanda y elevada produccion renovable.

Incorporar la prevision solar fotovoltaica permite al modelo diferenciar mejor entre dias aparentemente similares desde el punto de vista del calendario. Dos dias de marzo a la misma hora pueden tener precios distintos si uno presenta alta generacion solar y otro presenta nubosidad o menor produccion esperada. Esta informacion adicional puede mejorar la precision, especialmente en las horas centrales del dia.

Al igual que ocurre con la eolica, la variable solar fotovoltaica se descarga y cachea cuando el usuario activa ESIOS. El objetivo es evitar llamadas repetidas a la API y hacer que los experimentos sean mas reproducibles. Una vez descargados, los datos se almacenan localmente y se reutilizan si se entrena de nuevo con el mismo rango temporal.

Desde el punto de vista de la ingenieria de variables, `solar_pv_forecast_mwh` se incorpora como columna externa. Posteriormente puede combinarse con otras variables para generar indicadores derivados, como generacion solar total o ratio entre eolica y solar. Estas transformaciones permiten que el modelo reciba informacion mas compacta sobre la estructura renovable prevista.

### 6.5. Datos de prevision solar termica de ESIOS

La tercera variable externa considerada es la prevision de generacion solar termica, obtenida mediante el indicador ESIOS `543`. En el programa se almacena como `solar_thermal_forecast_mwh`. Aunque la solar termica tiene menor peso que la fotovoltaica en el sistema actual, sigue siendo una fuente relevante para representar la generacion renovable disponible.

La solar termica presenta caracteristicas diferentes a la fotovoltaica. Algunas instalaciones pueden contar con almacenamiento termico, lo que permite cierta gestion temporal de la energia generada. Esto significa que su perfil de produccion no tiene por que coincidir exactamente con el de la fotovoltaica. Incluir ambas variables por separado permite que el modelo aprenda diferencias entre tecnologias solares.

En la version actual del proyecto, la solar termica se utiliza tanto como variable independiente como parte de una variable agregada. El programa calcula `solar_forecast_mwh` sumando `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. Esta variable resume la generacion solar total prevista y puede ayudar al modelo a capturar el efecto conjunto de la energia solar sobre el precio.

Tambien se calcula `renewable_forecast_mwh`, que suma la prevision eolica y la prevision solar total. Este indicador representa una aproximacion a la renovable variable prevista. Aunque no incluye todas las tecnologias renovables posibles, como hidraulica o biomasa, proporciona una senal agregada util sobre la cantidad de energia de bajo coste variable que se espera en el sistema.

Otra variable derivada es `wind_solar_ratio`, que relaciona la prevision eolica con la solar. Esta variable puede ser informativa porque no todos los escenarios renovables tienen el mismo efecto. Un dia con alta eolica nocturna no tiene el mismo perfil que un dia con alta solar al mediodia. El ratio ayuda a representar la composicion de la renovable prevista, no solo su cantidad total.

La inclusion de solar termica, fotovoltaica y eolica no garantiza automaticamente una mejora de precision. El efecto dependera de la calidad de las previsiones, de la alineacion temporal y de la capacidad del modelo para aprovechar estas variables. Sin embargo, desde el punto de vista teorico y practico, son variables coherentes con la formacion del precio electrico y constituyen una mejora clara frente a un modelo basado unicamente en calendario y precios pasados.

### 6.6. Frecuencia temporal de los datos

La frecuencia temporal es uno de los aspectos mas importantes en la preparacion de datos. En el mercado electrico, los precios se publican para periodos de entrega. Durante mucho tiempo, el analisis horario ha sido la referencia principal, pero el sistema electrico avanza hacia resoluciones mas finas, como periodos de 15 minutos. Esto afecta directamente al diseno del dataset.

Un conjunto de datos horario contiene 24 observaciones por dia. Cada observacion representa una hora. En cambio, un conjunto cuarto-horario contiene 96 observaciones por dia. Esta diferencia modifica el significado de los retardos. Por ejemplo, un retardo de 24 periodos equivale a un dia completo en datos horarios, pero solo a seis horas en datos cuarto-horarios. Por tanto, la interpretacion de variables temporales debe hacerse con cuidado.

El proyecto detecta la frecuencia de cada dia a partir del numero maximo de periodos. Si el dia tiene mas de 25 periodos, considera que la resolucion es cuarto-horaria; en caso contrario, horaria. Esta heuristica permite procesar ficheros de OMIE sin exigir al usuario que indique manualmente la granularidad. El programa construye el `timestamp` correspondiente a cada periodo y ordena los datos temporalmente.

La existencia de distintas frecuencias plantea retos para los modelos. Si un dataset combina tramos horarios y cuarto-horarios, algunas variables pueden cambiar de significado. Por ejemplo, las medias moviles de 24 periodos no cubren el mismo horizonte temporal en ambos casos. En una version futura, seria conveniente adaptar los retardos a duraciones reales, como 24 horas o 7 dias, en lugar de expresarlos solo en numero de filas.

En la version actual, el enfoque es practico: se mantiene una estructura basada en periodos y se documenta la limitacion. Este planteamiento permite que el proyecto funcione con datos disponibles y sea capaz de leer ficheros con 24 o 96 periodos. No obstante, el analisis de resultados debe tener presente esta diferencia, especialmente cuando se comparan predicciones en anos o fechas con distinta resolucion.

La frecuencia temporal tambien afecta a la union con ESIOS. Las previsiones renovables pueden estar disponibles con una resolucion diferente a la del precio OMIE. Para resolverlo, el proyecto utiliza una union temporal aproximada, asignando a cada precio la ultima prevision disponible dentro de una tolerancia. Esta solucion es razonable para una primera version, aunque podria refinarse mediante interpolacion, remuestreo o seleccion explicita de la prevision vigente.

### 6.7. Tratamiento de datos horarios y cuarto-horarios

El tratamiento conjunto de datos horarios y cuarto-horarios requiere normalizar todos los registros en torno a una columna temporal comun. En el proyecto, esa columna es `timestamp`. Independientemente de que el periodo sea horario o de 15 minutos, cada observacion queda asociada a un instante concreto. Esta decision simplifica el ordenamiento, la union con fuentes externas y la construccion del dataset supervisado.

Para los datos horarios, la conversion es directa. El periodo 1 corresponde al inicio del dia y cada periodo posterior avanza una hora. Para los datos cuarto-horarios, el avance entre periodos es de 15 minutos. Esta logica se implementa durante el parseo de OMIE, antes de guardar el dataset procesado.

Una vez creado el `timestamp`, el sistema ordena las observaciones cronologicamente. Este orden es fundamental para calcular retardos y medias moviles. Si las filas estuvieran desordenadas, las variables temporales serian incorrectas y el modelo aprenderia relaciones falsas. Por ello, la ordenacion por fecha y periodo es una parte esencial del tratamiento de datos.

El cambio de resolucion tiene consecuencias sobre la validacion. En datos cuarto-horarios, un mismo numero de observaciones representa menos tiempo natural que en datos horarios. Por ejemplo, 700 filas equivalen aproximadamente a 29 dias si los datos son horarios, pero a poco mas de 7 dias si son cuarto-horarios. Esto influye en el minimo de historico necesario para construir variables y entrenar el modelo.

Tambien influye en la inferencia. El sistema predice el siguiente periodo disponible despues del ultimo `timestamp` del dataset. Si el ultimo dato es horario, el siguiente periodo sera la hora siguiente. Si es cuarto-horario, sera el siguiente cuarto de hora. Esta flexibilidad permite adaptar el flujo a los datos existentes, aunque exige que el usuario interprete correctamente el horizonte de prediccion.

Desde el punto de vista academico, este tratamiento muestra una decision de compromiso. Lo ideal seria disenar todas las variables temporales en unidades de tiempo absoluto, pero eso aumenta la complejidad del proyecto. La solucion implementada permite trabajar con ambas resoluciones de forma funcional y deja claramente identificada una linea de mejora para versiones futuras.

### 6.8. Problemas de disponibilidad y calidad de datos

La disponibilidad y calidad de los datos son factores determinantes en cualquier proyecto de prediccion. Aunque OMIE y ESIOS son fuentes oficiales, el proceso automatico de descarga puede encontrarse con distintos problemas. Por ejemplo, un fichero puede no estar disponible para una fecha concreta, la conexion puede fallar, el servidor puede devolver un error temporal o el formato del fichero puede cambiar.

Durante las pruebas del proyecto se detecto que algunos dias de 2025 no estaban disponibles desde la ruta consultada, produciendo errores de descarga. En lugar de asumir que todos los dias existen siempre, el programa debe gestionar estas situaciones de manera controlada. La robustez ante ausencias es importante porque un unico dia problematico no deberia invalidar todo el analisis si el resto del periodo es util.

Tambien pueden aparecer problemas derivados de la resolucion temporal. Un ano puede contener datos horarios en una parte y datos cuarto-horarios en otra. Esto no es necesariamente un error, pero si una caracteristica que debe tratarse explicitamente. Si no se documenta, puede inducir interpretaciones incorrectas de los retardos o de las metricas.

En ESIOS, la disponibilidad depende ademas del token de acceso y de la API. Si el token no es valido, no se pueden descargar variables renovables. Por eso el programa valida la existencia del token antes de intentar construir datos enriquecidos. Esta comprobacion temprana evita ejecuciones largas que terminan fallando tarde y mejora la experiencia de usuario.

La calidad de los datos tambien incluye la presencia de valores ausentes. Cuando se unen fuentes distintas, puede haber instantes con precio OMIE pero sin prevision ESIOS exacta. La aplicacion utiliza relleno hacia delante y hacia atras en las columnas renovables despues de la union temporal. Esta tecnica permite completar huecos pequenos, aunque debe usarse con prudencia para no introducir informacion poco realista en huecos grandes.

Otro aspecto de calidad es la coherencia de unidades. Los precios se expresan en EUR/MWh y las previsiones renovables en MWh. Aunque estas variables no tienen la misma escala, los modelos utilizados pueden trabajar con ellas si se procesan adecuadamente. En el caso de modelos lineales y redes neuronales, el escalado interno dentro de pipelines puede ayudar a estabilizar el entrenamiento.

La calidad de datos no debe verse solo como un problema tecnico, sino como parte de la metodologia. Un modelo entrenado con datos mal alineados, incompletos o interpretados incorrectamente puede obtener metricas aparentemente buenas y aun asi no ser valido. Por ello, el capitulo de preparacion de datos profundiza posteriormente en limpieza, normalizacion y gestion de ausencias.

### 6.9. Estrategia de cache y almacenamiento local

La aplicacion incorpora una estrategia de cache local para hacer el flujo de trabajo mas eficiente y reproducible. Descargar datos cada vez que se entrena el modelo seria lento, dependeria constantemente de la red y aumentaria el riesgo de fallos por disponibilidad externa. Por ello, los ficheros descargados y los datasets procesados se almacenan en directorios locales.

Los ficheros OMIE descargados se guardan en `data/raw/`. Esta carpeta actua como cache de datos originales. Si el usuario vuelve a entrenar con un rango que incluye dias ya descargados, el programa puede reutilizar esos ficheros sin solicitar de nuevo la descarga. Esto acelera los experimentos y reduce la dependencia del servidor remoto.

Los datos procesados se guardan en `data/processed/`. En esta ubicacion se almacenan datasets limpios y, cuando procede, datos enriquecidos con ESIOS. Por ejemplo, las previsiones renovables se cachean con nombres que incluyen el rango temporal, como `esios_generation_YYYYMMDD_YYYYMMDD.csv`. Este nombre facilita identificar a que periodo corresponde cada fichero.

La cache tambien es util para depuracion. Si un entrenamiento falla, se puede revisar el fichero procesado y comprobar si las columnas esperadas existen, si los timestamps estan ordenados o si hay valores ausentes. Esto convierte la cache en una herramienta de trazabilidad, no solo en una optimizacion de rendimiento.

Los modelos entrenados y graficas de validacion se guardan en `models/`. El modelo serializado se almacena como `models/omie_model.joblib`, y la grafica de validacion como `models/validation_plot.png`. Aunque estos artefactos no son fuentes de datos en sentido estricto, forman parte del flujo de almacenamiento del proyecto y permiten conectar datos, entrenamiento e inferencia.

Los directorios de datos, modelos y caches estan excluidos de Git mediante `.gitignore`. Esta decision es adecuada porque los datos descargados pueden ocupar espacio, cambiar con el tiempo o contener artefactos generados localmente. El repositorio debe almacenar codigo y documentacion, mientras que los datos se regeneran mediante los comandos del proyecto.

La separacion entre datos originales, datos procesados y modelos entrenados mejora la organizacion del sistema. `data/raw/` conserva la fuente descargada, `data/processed/` contiene los resultados intermedios y `models/` guarda los artefactos finales. Esta estructura facilita entender el pipeline completo y reproducir el trabajo desde cero.

En conclusion, las fuentes de datos del proyecto combinan una base oficial de precios de OMIE con variables renovables opcionales de ESIOS. OMIE proporciona la variable objetivo y el historico fundamental; ESIOS aporta contexto fisico sobre generacion eolica y solar prevista; y la estrategia de cache permite ejecutar experimentos de forma eficiente. La calidad, frecuencia y disponibilidad de estos datos condicionan directamente la precision del modelo, por lo que su tratamiento constituye una parte esencial del trabajo.
