# Capítulo 6. Fuentes de datos

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 6.1. Datos de precio del mercado diario OMIE

La fuente principal de datos utilizada en este trabajo es OMIE, el operador del mercado eléctrico ibérico. OMIE publica información oficial sobre los resultados del mercado diario e intradiario, incluyendo precios marginales, energía casada y otros datos relevantes para el análisis del mercado eléctrico. En el proyecto desarrollado, la variable objetivo es el precio marginal español del mercado diario, expresado en euros por megavatio hora.

El mercado diario es especialmente adecuado para este trabajo porque ofrece una serie temporal pública, estructurada y directamente relacionada con el problema de predicción. Cada día se publica un conjunto de precios correspondientes a los periodos de entrega de energía. Tradicionalmente estos periodos han sido horarios, aunque el sistema también debe prepararse para manejar resoluciones cuarto-horarias cuando aparecen en los ficheros publicados.

En la aplicación práctica, los datos de OMIE se descargan automáticamente a partir del rango de fechas indicado por el usuario. Esta automatización evita tener que descargar manualmente cada fichero diario y permite repetir experimentos con distintos periodos. El usuario puede seleccionar un rango en la interfaz gráfica o indicar fechas mediante línea de comandos. El sistema recorre cada día del intervalo, intenta descargar el fichero correspondiente y lo transforma en una tabla procesable.

Los datos de OMIE tienen una ventaja importante: proceden de una fuente oficial y reproducible. Esto significa que cualquier persona puede reconstruir el mismo conjunto de precios si utiliza las mismas fechas y el mismo procedimiento de descarga. Para un Trabajo Fin de Grado, está trazabilidad es fundamental, ya que permite justificar el origen de la variable objetivo y verificar los resultados obtenidos.

La variable extraida de OMIE es `price_eur_mwh`, que representa el precio marginal español del periodo. Esta columna se convierte en la salida que los modelos intentan predecir. A partir de ella se generan también variables retardadas, medias móviles, diferencias y estadísticos recientes. Por tanto, OMIE no solo proporciona la variable objetivo, sino también la base histórica de la que se obtienen muchas variables explicativas.

El uso de OMIE como fuente principal también impone ciertas limitaciones. Los ficheros pueden no estar disponibles para algún día concreto, pueden cambiar ligeramente de formato o pueden publicarse con distinta resolución temporal. Además, el precio del mercado diario no incluye por sí solo toda la información que explica su comportamiento. Factores como demanda, meteorología, generación renovable, gas, CO2 o interconexiones no están completamente representados en el histórico de precios. Por eso el proyecto contempla la incorporación opcional de datos externos procedentes de ESIOS.

### 6.2. Formato de los ficheros `MARGINALPDBC`

El proyecto utiliza los ficheros públicos `MARGINALPDBC` de OMIE. Estos ficheros contienen información diaria sobre precios marginales del mercado diario para España y Portugal. Cada fichero corresponde a una fecha concreta y contiene filas con los periodos de entrega de ese día.

El programa espera encontrar líneas con campos separados por punto y coma. A partir de esas líneas se extraen principalmente los siguientes datos: año, mes, día, periodo, precio marginal portugués y precio marginal español. Aunque el fichero puede contener cabeceras, comentarios u otros elementos, el parser del proyecto filtra las líneas relevantes y transforma cada registro en una observación tabular.

El esquema conceptual utilizado por la aplicación es el siguiente:

```text
anio;mes;día;periodo;marginal_pt;marginal_es;
```

El campo `periodo` indica la posición temporal dentro del día. Si el fichero contiene 24 periodos, cada periodo se interpreta como una hora. Si contiene 96 periodos, cada periodo se interpreta como un cuarto de hora. Esta distinción es importante porque afecta a la construcción del `timestamp`, a los retardos temporales y a la interpretación de variables como `lag_24`.

El parser convierte los campos de fecha y periodo en una columna temporal llamada `timestamp`. Para ello, primero identifica cuantos periodos tiene el día. Si el máximo periodo del día es superior a 25, el programa considera que la resolución es de 15 minutos. En caso contrario, considera que la resolución es horaria. A continuacion calcula el instante de cada observación sumando al inicio del día el desplazamiento correspondiente al periodo.

Por ejemplo, en un día horario, el periodo 1 se interpreta como las 00:00, el periodo 2 como las 01:00 y así sucesivamente. En un día cuarto-horario, el periodo 1 se interpreta como las 00:00, el periodo 2 como las 00:15, el periodo 3 como las 00:30 y el periodo 4 como las 00:45. Esta normalización permite combinar días de distinta granularidad dentro de una misma estructura temporal.

Una vez procesado el fichero, cada observación queda representada con columnas como `date`, `period`, `timestamp`, `price_pt_eur_mwh` y `price_eur_mwh`. La columna portuguésa se conserva porque puede resultar útil para análisis posteriores, aunque el objetivo del modelo desarrollado es el precio español. Mantener información adicional sin usarla necesariamente en la primera versión facilita futuras ampliaciones.

El tratamiento de los ficheros `MARGINALPDBC` es una parte crítica de la aplicación. Si el parseo falla, todo el pipeline posterior queda comprometido. Por ese motivo, el código comprueba que el contenido descargado corresponde realmente a un fichero esperado de OMIE y lanza errores claros cuando no es asi. Esta gestión de errores permite detectar problemas de descarga, cambios de formato o días no disponibles.

### 6.3. Datos de previsión eólica de ESIOS

Además de OMIE, el proyecto permite incorporar datos opcionales procedentes de ESIOS, el sistema de información del operador del sistema eléctrico gestionado por Red Eléctrica. En concreto, una de las variables externas consideradas es la previsión de generación eólica. Esta información es relevante porque la energía eólica tiene un impacto directo en la formación de precios del mercado eléctrico.

La generación eólica presenta costes variables muy bajos. Cuando hay alta disponibilidad de viento, la producción eólica puede desplazar a tecnologías más caras dentro del orden de mérito. Esto tiende a reducir el precio marginal, especialmente si la demanda no es suficientemente alta como para requerir tecnologías de mayor coste. Por el contrario, en periodos de bajo viento, el sistema puede necesitar recurrir a tecnologías como ciclos combinados, lo que puede elevar el precio.

En el programa, la previsión eólica se obtiene mediante el indicador ESIOS `541`, asociado a la columna `wind_forecast_mwh`. Esta variable representa una previsión de producción eólica en MWh para el sistema eléctrico peninsular. Su inclusión permite que el modelo no dependa exclusivamente del histórico de precios y calendario, sino que incorpore una señal física sobre la generación renovable esperada.

El uso de previsión, y no solo de generación real, es metodológicamente importante. En un escenario de predicción real, antes de conocer el precio futuro tampoco se conoce con certeza la generación renovable futura. Lo que puede utilizarse de forma coherente es una previsión disponible antes del periodo objetivo. Por tanto, las variables de ESIOS se plantean como información exógena que podría estar disponible en el momento de realizar la predicción.

La integración con ESIOS requiere un token de acceso. Por este motivo, el proyecto mantiene está fuente como opcional. Si el usuario no dispone de token, el sistema puede entrenar usando solo datos OMIE. Si dispone de token, puede activar la opción ESIOS desde la interfaz gráfica o desde la línea de comandos. Esta decisión evita que el proyecto dependa obligatoriamente de una API externa con autenticacion.

La variable eólica se une al dataset principal mediante `timestamp`. Cuando las resoluciones temporales no coinciden exactamente, el proyecto utiliza una unión temporal aproximada basada en la última observación disponible dentro de una tolerancia. Esta estrategia permite combinar precios cuarto-horarios con previsiones que pueden tener otra granularidad.

### 6.4. Datos de previsión solar fotovoltaica de ESIOS

La segunda fuente externa incorporada desde ESIOS es la previsión de generación solar fotovoltaica. En el sistema eléctrico español, la energía solar fotovoltaica ha adquirido un peso creciente y su impacto en los precios es cada vez más visible. Durante las horas centrales del día, una alta generación solar puede reducir la necesidad de tecnologías más caras y presionar los precios a la baja.

La previsión solar fotovoltaica se obtiene mediante el indicador ESIOS `542`, que el programa transforma en la columna `solar_pv_forecast_mwh`. Esta variable representa la producción fotovoltaica prevista y permite capturar patrones que no se deducen completamente del calendario. Aunque la hora y el mes indican de forma indirecta cuando puede haber radiación solar, no informan sobre nubosidad, condiciones meteorológicas concretas o variabilidad diaria.

La energía solar tiene un perfil muy marcado. Su producción se concentra en las horas con radiación, desaparece durante la noche y varia según la estacion del año. En primavera y verano, las horas solares pueden tener un efecto especialmente relevante sobre el precio. En determinados periodos, una alta penetración fotovoltaica puede llevar a precios muy bajos o incluso cercanos a cero si coincide con baja demanda y elevada producción renovable.

Incorporar la previsión solar fotovoltaica permite al modelo diferenciar mejor entre días aparentemente similares desde el punto de vista del calendario. Dos días de marzo a la misma hora pueden tener precios distintos si uno presenta alta generación solar y otro presenta nubosidad o menor producción esperada. Esta información adicional puede mejorar la precisión, especialmente en las horas centrales del día.

Al igual qué ocurre con la eólica, la variable solar fotovoltaica se descarga y cachea cuando el usuario activa ESIOS. El objetivo es evitar llamadas repetidas a la API y hacer que los experimentos sean más reproducibles. Una vez descargados, los datos se almacenan localmente y se reutilizan si se entrena de nuevo con el mismo rango temporal.

Desde el punto de vista de la ingeniería de variables, `solar_pv_forecast_mwh` se incorpora como columna externa. Posteriormente puede combinarse con otras variables para generar indicadores derivados, como generación solar total o ratio entre eólica y solar. Estas transformaciones permiten que el modelo reciba información más compacta sobre la estructura renovable prevista.

### 6.5. Datos de previsión solar térmica de ESIOS

La tercera variable externa considerada es la previsión de generación solar térmica, obtenida mediante el indicador ESIOS `543`. En el programa se almacena como `solar_thermal_forecast_mwh`. Aunque la solar térmica tiene menor peso que la fotovoltaica en el sistema actual, sigue siendo una fuente relevante para representar la generación renovable disponible.

La solar térmica presenta características diferentes a la fotovoltaica. Algunas instalaciones pueden contar con almacenamiento termico, lo que permite cierta gestión temporal de la energía generada. Esto significa que su perfil de producción no tiene por que coincidir exactamente con el de la fotovoltaica. Incluir ambas variables por separado permite que el modelo aprenda diferencias entre tecnologías solares.

En la versión actual del proyecto, la solar térmica se utiliza tanto como variable independiente como parte de una variable agregada. El programa calcula `solar_forecast_mwh` sumando `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. Esta variable resume la generación solar total prevista y puede ayudar al modelo a capturar el efecto conjunto de la energía solar sobre el precio.

También se calcula `renewable_forecast_mwh`, que suma la previsión eólica y la previsión solar total. Este indicador representa una aproximación a la renovable variable prevista. Aunque no incluye todas las tecnologías renovables posibles, como hidráulica o biomása, proporciona una señal agregada útil sobre la cantidad de energía de bajo coste variable que se espera en el sistema.

Otra variable derivada es `wind_solar_ratio`, que relaciona la previsión eólica con la solar. Esta variable puede ser informativa porque no todos los escenarios renovables tienen el mismo efecto. Un día con alta eólica nocturna no tiene el mismo perfil que un día con alta solar al mediodía. El ratio ayuda a representar la composición de la renovable prevista, no solo su cantidad total.

La inclusión de solar térmica, fotovoltaica y eólica no garantiza automáticamente una mejora de precisión. El efecto dependerá de la calidad de las previsiones, de la alineación temporal y de la capacidad del modelo para aprovechar estas variables. Sin embargo, desde el punto de vista teórico y práctico, son variables coherentes con la formación del precio eléctrico y constituyen una mejora clara frente a un modelo basado únicamente en calendario y precios pasados.

### 6.6. Frecuencia temporal de los datos

La frecuencia temporal es uno de los aspectos más importantes en la preparación de datos. En el mercado eléctrico, los precios se publican para periodos de entrega. Durante mucho tiempo, el análisis horario ha sido la referencia principal, pero el sistema eléctrico avanza hacia resoluciones más finas, como periodos de 15 minutos. Esto afecta directamente al diseño del dataset.

Un conjunto de datos horario contiene 24 observaciones por día. Cada observación representa una hora. En cambio, un conjunto cuarto-horario contiene 96 observaciones por día. Esta diferencia modifica el significado de los retardos. Por ejemplo, un retardo de 24 periodos equivale a un día completo en datos horarios, pero solo a seis horas en datos cuarto-horarios. Por tanto, la interpretación de variables temporales debe hacerse con cuidado.

El proyecto detecta la frecuencia de cada día a partir del número máximo de periodos. Si el día tiene más de 25 periodos, considera que la resolución es cuarto-horaria; en caso contrario, horaria. Esta heuristica permite procesar ficheros de OMIE sin exigir al usuario que indique manualmente la granularidad. El programa construye el `timestamp` correspondiente a cada periodo y ordena los datos temporalmente.

La existencia de distintas frecuencias plantea retos para los modelos. Si un dataset combina tramos horarios y cuarto-horarios, algunas variables pueden cambiar de significado. Por ejemplo, las medias móviles de 24 periodos no cubren el mismo horizonte temporal en ambos casos. En una versión futura, sería conveniente adaptar los retardos a duraciones reales, como 24 horas o 7 días, en lugar de expresarlos solo en número de filas.

En la versión actual, el enfoque es práctico: se mantiene una estructura basada en periodos y se documenta la limitación. Este planteamiento permite que el proyecto funcione con datos disponibles y sea capaz de leer ficheros con 24 o 96 periodos. No obstante, el análisis de resultados debe tener presente esta diferencia, especialmente cuando se comparan predicciones en años o fechas con distinta resolución.

La frecuencia temporal también afecta a la unión con ESIOS. Las previsiones renovables pueden estar disponibles con una resolución diferente a la del precio OMIE. Para resolverlo, el proyecto utiliza una unión temporal aproximada, asignando a cada precio la última previsión disponible dentro de una tolerancia. Esta solución es razonable para una primera versión, aunque podría refinarse mediante interpolación, remuestreo o selección explícita de la previsión vigente.

### 6.7. Tratamiento de datos horarios y cuarto-horarios

El tratamiento conjunto de datos horarios y cuarto-horarios requiere normalizar todos los registros en torno a una columna temporal común. En el proyecto, esa columna es `timestamp`. Independientemente de que el periodo sea horario o de 15 minutos, cada observación queda asociada a un instante concreto. Esta decisión simplifica el ordenamiento, la unión con fuentes externas y la construcción del dataset supervisado.

Para los datos horarios, la conversión es directa. El periodo 1 corresponde al inicio del día y cada periodo posterior avanza una hora. Para los datos cuarto-horarios, el avance entre periodos es de 15 minutos. Esta lógica se implementa durante el parseo de OMIE, antes de guardar el dataset procesado.

Una vez creado el `timestamp`, el sistema ordena las observaciones cronológicamente. Este orden es fundamental para calcular retardos y medias móviles. Si las filas estuvieran desordenadas, las variables temporales serían incorrectas y el modelo aprenderia relaciones falsas. Por ello, la ordenación por fecha y periodo es una parte esencial del tratamiento de datos.

El cambio de resolución tiene consecuencias sobre la validación. En datos cuarto-horarios, un mismo número de observaciones representa menos tiempo natural que en datos horarios. Por ejemplo, 700 filas equivalen aproximadamente a 29 días si los datos son horarios, pero a poco más de 7 días si son cuarto-horarios. Esto influye en el mínimo de histórico necesario para construir variables y entrenar el modelo.

También influye en la inferencia. El sistema predice el siguiente periodo disponible después del último `timestamp` del dataset. Si el último dato es horario, el siguiente periodo será la hora siguiente. Si es cuarto-horario, será el siguiente cuarto de hora. Esta flexibilidad permite adaptar el flujo a los datos existentes, aunque exige que el usuario interprete correctamente el horizonte de predicción.

Desde el punto de vista académico, este tratamiento muestra una decisión de compromiso. Lo ideal sería diseñar todas las variables temporales en unidades de tiempo absoluto, pero eso aumenta la complejidad del proyecto. La solución implementada permite trabajar con ambas resoluciones de forma funcional y deja claramente identificada una línea de mejora para versiones futuras.

### 6.8. Problemas de disponibilidad y calidad de datos

La disponibilidad y calidad de los datos son factores determinantes en cualquier proyecto de predicción. Aunque OMIE y ESIOS son fuentes oficiales, el proceso automático de descarga puede encontrarse con distintos problemas. Por ejemplo, un fichero puede no estar disponible para una fecha concreta, la conexión puede fallar, el servidor puede devolver un error temporal o el formato del fichero puede cambiar.

Durante las pruebas del proyecto se detecto que algunos días de 2025 no estaban disponibles desde la ruta consultada, produciendo errores de descarga. En lugar de asumir que todos los días existen siempre, el programa debe gestionar estas situaciones de manera controlada. La robustez ante ausencias es importante porque un único día problemático no debería invalidar todo el análisis si el resto del periodo es útil.

También pueden aparecer problemas derivados de la resolución temporal. Un año puede contener datos horarios en una parte y datos cuarto-horarios en otra. Esto no es necesariamente un error, pero si una característica que debe tratarse explícitamente. Si no se documenta, puede inducir interpretaciones incorrectas de los retardos o de las métricas.

En ESIOS, la disponibilidad depende además del token de acceso y de la API. Si el token no es válido, no se pueden descargar variables renovables. Por eso el programa valida la existencia del token antes de intentar construir datos enriquecidos. Esta comprobación temprana evita ejecuciones largas que terminan fallando tarde y mejora la experiencia de usuario.

La calidad de los datos también incluye la presencia de valores ausentes. Cuando se unen fuentes distintas, puede haber instantes con precio OMIE pero sin previsión ESIOS exacta. La aplicación utiliza relleno hacia delante y hacia atrás en las columnas renovables después de la unión temporal. Esta técnica permite completar huecos pequeños, aunque debe usarse con prudencia para no introducir información poco realista en huecos grandes.

Otro aspecto de calidad es la coherencia de unidades. Los precios se expresan en EUR/MWh y las previsiones renovables en MWh. Aunque estas variables no tienen la misma escala, los modelos utilizados pueden trabajar con ellas si se procesan adecuadamente. En el caso de modelos lineales y redes neuronales, el escalado interno dentro de pipelines puede ayudar a estabilizar el entrenamiento.

La calidad de datos no debe verse solo como un problema técnico, sino como parte de la metodología. Un modelo entrenado con datos mal alineados, incompletos o interpretados incorrectamente puede obtener métricas aparentemente buenas y aun así no ser válido. Por ello, el capítulo de preparación de datos profundiza posteriormente en limpieza, normalización y gestión de ausencias.

### 6.9. Estrategia de cache y almacenamiento local

La aplicación incorpora una estrategia de cache local para hacer el flujo de trabajo más eficiente y reproducible. Descargar datos cada vez que se entrena el modelo sería lento, dependeria constantemente de la red y aumentaria el riesgo de fallos por disponibilidad externa. Por ello, los ficheros descargados y los datasets procesados se almacenan en directorios locales.

Los ficheros OMIE descargados se guardan en `data/raw/`. Esta carpeta actua como cache de datos originales. Si el usuario vuelve a entrenar con un rango que incluye días ya descargados, el programa puede reutilizar esos ficheros sin solicitar de nuevo la descarga. Esto acelera los experimentos y reduce la dependencia del servidor remoto.

Los datos procesados se guardan en `data/processed/`. En esta ubicación se almacenan datasets limpios y, cuando procede, datos enriquecidos con ESIOS. Por ejemplo, las previsiones renovables se cachean con nombres que incluyen el rango temporal, como `esios_generation_YYYYMMDD_YYYYMMDD.csv`. Este nombre facilita identificar a qué periodo corresponde cada fichero.

La cache también es útil para depuración. Si un entrenamiento falla, se puede revisar el fichero procesado y comprobar si las columnas esperadas existen, si los timestamps están ordenados o si hay valores ausentes. Esto convierte la cache en una herramienta de trazabilidad, no solo en una optimización de rendimiento.

Los modelos entrenados y gráficas de validación se guardan en `models/`. El modelo serializado se almacena como `models/omie_model.joblib`, y la gráfica de validación como `models/validation_plot.png`. Aunque estos artefactos no son fuentes de datos en sentido estricto, forman parte del flujo de almacenamiento del proyecto y permiten conectar datos, entrenamiento e inferencia.

Los directorios de datos, modelos y caches están excluidos de Git mediante `.gitignore`. Esta decisión es adecuada porque los datos descargados pueden ocupar espacio, cambiar con el tiempo o contener artefactos generados localmente. El repositorio debe almacenar código y documentación, mientras que los datos se regeneran mediante los comandos del proyecto.

La separación entre datos originales, datos procesados y modelos entrenados mejora la organización del sistema. `data/raw/` conserva la fuente descargada, `data/processed/` contiene los resultados intermedios y `models/` guarda los artefactos finales. Esta estructura facilita entender el pipeline completo y reproducir el trabajo desde cero.

En conclusión, las fuentes de datos del proyecto combinan una base oficial de precios de OMIE con variables renovables opcionales de ESIOS. OMIE proporciona la variable objetivo y el histórico fundamental; ESIOS aporta contexto físico sobre generación eólica y solar prevista; y la estrategia de cache permite ejecutar experimentos de forma eficiente. La calidad, frecuencia y disponibilidad de estos datos condicionan directamente la precisión del modelo, por lo que su tratamiento constituye una parte esencial del trabajo.
