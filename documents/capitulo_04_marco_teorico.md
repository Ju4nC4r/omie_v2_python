# Capitulo 4. Marco teorico

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 4.1. Funcionamiento del mercado electrico espanol

El sistema electrico espanol esta formado por un conjunto de actividades tecnicas, economicas y regulatorias cuyo objetivo es garantizar el suministro de electricidad a consumidores finales. Para que el sistema funcione correctamente debe existir equilibrio continuo entre generacion y demanda. Este equilibrio es especialmente complejo porque la electricidad, a diferencia de otros bienes, no se almacena masivamente de forma sencilla y economica. Por ello, la produccion debe adaptarse de manera constante al consumo.

En terminos generales, el sector electrico se organiza en varias actividades: generacion, transporte, distribucion, comercializacion y consumo. La generacion corresponde a las instalaciones que producen energia electrica, como centrales nucleares, ciclos combinados, centrales hidraulicas, parques eolicos, plantas solares fotovoltaicas, termosolares o cogeneraciones. El transporte se realiza mediante redes de alta tension y permite llevar electricidad desde los centros de generacion hasta las zonas de consumo. La distribucion acerca esa energia a consumidores finales mediante redes de media y baja tension. La comercializacion gestiona la relacion contractual con los consumidores.

El precio de la electricidad se forma en distintos mercados y mecanismos. Uno de los mas importantes es el mercado diario, donde se negocia energia para cada periodo del dia siguiente. Tambien existen mercados intradiarios, servicios de ajuste y mecanismos de balance gestionados para mantener la seguridad del sistema. El precio que se analiza en este trabajo corresponde al mercado diario, concretamente al precio marginal espanol publicado por OMIE.

En el mercado diario, los generadores presentan ofertas de venta y los compradores presentan ofertas de adquisicion de energia. El algoritmo de casacion ordena ofertas de acuerdo con criterios economicos y tecnicos, determinando el precio resultante para cada periodo. El precio marginal es el precio de la ultima unidad necesaria para cubrir la demanda casada. Esto significa que todas las unidades casadas en ese periodo reciben, en general, el precio marginal correspondiente.

La estructura marginalista del mercado implica que tecnologias con costes variables bajos, como eolica, solar o nuclear, pueden desplazar a tecnologias mas caras. Cuando la demanda puede cubrirse con tecnologias de bajo coste variable, el precio tiende a ser mas bajo. En cambio, cuando es necesario recurrir a tecnologias con costes variables superiores, como ciclos combinados de gas, el precio puede elevarse. Esta dinamica explica por que factores como la demanda, el viento, la radiacion solar, el gas o el CO2 influyen en el precio.

El sistema electrico espanol esta integrado en el Mercado Iberico de Electricidad, compartido con Portugal. Por ello, los precios de Espana y Portugal pueden coincidir o diferir en funcion de la capacidad de interconexion y de las condiciones de mercado. Cuando no existen restricciones relevantes entre ambas zonas, los precios tienden a converger. Si aparecen congestiones, pueden producirse precios distintos.

Para desarrollar modelos predictivos es necesario entender que el precio del mercado diario no es una variable aislada. Es el resultado de la interaccion entre ofertas, demanda, tecnologias disponibles, restricciones, meteorologia y expectativas. Esta complejidad justifica el uso de tecnicas de aprendizaje automatico, pero tambien obliga a ser prudentes en la interpretacion de los resultados.

### 4.2. Mercado diario e intradiario

El mercado diario es el mecanismo donde se negocia la mayor parte de la energia electrica para el dia siguiente. Los agentes presentan sus ofertas antes de una hora limite y el operador del mercado realiza la casacion. El resultado es un programa de energia y un precio para cada periodo. Tradicionalmente, estos periodos han sido horarios, aunque el sistema avanza hacia resoluciones temporales mas cortas, como periodos cuarto-horarios.

El mercado diario tiene gran importancia porque proporciona una referencia publica y transparente del precio de la energia. Muchos contratos y analisis energeticos utilizan este precio como base. Aunque no toda la energia se compra directamente en el mercado diario, su senal economica es fundamental para el conjunto del sistema.

El mercado intradiario permite ajustar posiciones despues del mercado diario. La demanda real, la generacion renovable o la disponibilidad de las centrales pueden diferir de las previsiones iniciales. Por ello, los agentes necesitan mecanismos para corregir desviaciones y adaptar su programa. Los mercados intradiarios contribuyen a mejorar la eficiencia del sistema al permitir ajustes mas cercanos al tiempo real.

Ademas de los mercados diario e intradiario, existen servicios de ajuste y balance. Estos mecanismos permiten al operador del sistema mantener el equilibrio fisico entre generacion y demanda, resolver restricciones tecnicas y garantizar la seguridad del suministro. Aunque estos servicios no son el objeto principal de este trabajo, forman parte del contexto general que afecta a la operacion electrica.

La prediccion del precio del mercado diario se diferencia de la prediccion intradiaria en el horizonte temporal y en la informacion disponible. Para el mercado diario se intenta anticipar el precio antes de que se conozca la casacion del dia siguiente. En cambio, en mercados intradiarios pueden incorporarse datos mas recientes. Este trabajo se centra en el precio publicado por OMIE para el mercado diario, aunque la metodologia podria extenderse a otros horizontes.

Para un modelo de aprendizaje automatico, el mercado diario ofrece una serie temporal estructurada. Cada periodo tiene un precio, una fecha, una posicion dentro del dia y un contexto historico. Esto permite generar variables como retardos, medias moviles o indicadores de calendario. Sin embargo, el mercado diario tambien esta influido por variables externas que no siempre estan presentes en el historico de precios, como la demanda esperada o la prevision meteorologica.

### 4.3. Papel de OMIE en el mercado electrico

OMIE es el Operador del Mercado Iberico de Energia en el polo espanol. Su funcion principal es gestionar los mercados mayoristas de electricidad en el ambito iberico, incluyendo el mercado diario y diferentes sesiones intradiarias. OMIE recibe ofertas de compra y venta, ejecuta los procesos de casacion y publica resultados de mercado.

Para este trabajo, OMIE es especialmente relevante porque proporciona los datos de precio marginal utilizados como variable objetivo. En concreto, se emplean los ficheros `MARGINALPDBC`, que contienen informacion diaria del precio marginal para Portugal y Espana. El campo `marginal_es` representa el precio marginal espanol y se expresa en euros por megavatio hora.

La disponibilidad publica de estos ficheros permite construir una base historica de precios. El proyecto desarrollado descarga automaticamente los ficheros diarios, los almacena en cache y los transforma en un formato tabular. Esta automatizacion facilita repetir experimentos, ampliar rangos temporales y mantener separada la fuente original de los datos procesados.

El formato de los ficheros OMIE requiere parseo. Cada fila incluye informacion como ano, mes, dia, periodo, precio marginal portugues y precio marginal espanol. A partir de estos campos se genera un timestamp que permite ordenar las observaciones y unirlas con otras fuentes de datos. Esta normalizacion es indispensable para cualquier analisis posterior.

OMIE no solo publica precios, sino tambien otros resultados de mercado que podrian ser utiles en futuras extensiones. Sin embargo, este trabajo se centra en el precio marginal espanol por ser la variable mas directamente relacionada con el objetivo de prediccion. Incorporar mas datos de OMIE, como volumenes casados u ofertas agregadas, podria mejorar el modelo, pero queda fuera del alcance inicial.

Desde el punto de vista metodologico, OMIE proporciona una fuente fiable y oficial para el precio del mercado diario. Esto reduce incertidumbre sobre la procedencia de la variable objetivo y permite que el proyecto sea reproducible. Cualquier usuario con acceso a internet puede descargar los mismos ficheros y reconstruir el dataset.

### 4.4. Papel de Red Electrica y ESIOS

Red Electrica desempena el papel de operador del sistema electrico espanol. Su responsabilidad principal es garantizar la continuidad y seguridad del suministro, manteniendo el equilibrio entre generacion y demanda en tiempo real. Para ello coordina la operacion del sistema, gestiona restricciones tecnicas y supervisa el funcionamiento de la red de transporte.

ESIOS es el Sistema de Informacion del Operador del Sistema. A traves de ESIOS se publican numerosos indicadores relacionados con la demanda, la generacion, la programacion, las previsiones y otros aspectos del sistema electrico. Esta plataforma constituye una fuente de datos muy valiosa para analisis energeticos.

En este trabajo, ESIOS se utiliza de forma opcional para incorporar previsiones de generacion renovable. En concreto, se consideran indicadores de prevision eolica, solar fotovoltaica y solar termica. Estas variables pueden aportar informacion adicional sobre la disponibilidad esperada de energia renovable, que es un factor relevante en la formacion del precio.

La integracion de ESIOS requiere un token de acceso a su API. Por ese motivo se ha implementado como funcionalidad opcional. El sistema puede funcionar usando solo OMIE, pero si el usuario dispone de token ESIOS puede enriquecer el dataset. Esta decision permite mantener la accesibilidad del proyecto sin renunciar a incorporar variables externas.

Los datos procedentes de ESIOS se unen con los datos de OMIE mediante la columna temporal `timestamp`. Dado que pueden existir diferencias de resolucion temporal, el sistema utiliza una aproximacion que asigna la ultima prevision disponible dentro de una tolerancia definida. Esta estrategia permite combinar datos horarios con observaciones de precio que pueden ser cuarto-horarias.

El papel de ESIOS en el modelo es aportar contexto fisico del sistema. Mientras que OMIE proporciona el precio resultante del mercado, ESIOS puede proporcionar informacion sobre condiciones esperadas del sistema, como renovables. Esta combinacion es mas rica que usar unicamente historico de precios.

### 4.5. Factores que influyen en el precio electrico

El precio electrico depende de multiples factores que actuan simultaneamente. Uno de los mas importantes es la demanda. Cuando la demanda es alta, el sistema necesita recurrir a mas generacion para cubrir el consumo. Si las tecnologias de menor coste no son suficientes, entran tecnologias mas caras y el precio marginal puede aumentar.

La disponibilidad de generacion es otro factor clave. Las centrales pueden estar disponibles, indisponibles por mantenimiento o limitadas por condiciones tecnicas. La generacion hidraulica depende de reservas y estrategias de gestion del agua. La nuclear suele operar de forma estable, pero sus paradas afectan a la oferta base. Los ciclos combinados dependen del coste del gas y de su posicion en el orden de merito.

La produccion renovable tiene un efecto creciente. La eolica y la solar presentan costes variables muy bajos y, cuando estan disponibles, desplazan a tecnologias mas caras. Sin embargo, su produccion depende de condiciones meteorologicas. Esto introduce variabilidad y hace que el precio pueda cambiar notablemente entre dias aparentemente similares.

El precio del gas natural influye especialmente cuando los ciclos combinados marcan el precio marginal. Si el gas es caro, el coste de producir electricidad con esta tecnologia aumenta. Del mismo modo, los derechos de emision de CO2 afectan a tecnologias emisoras, incrementando sus costes variables.

Las interconexiones internacionales tambien pueden influir. Si existe capacidad para importar energia mas barata o exportar energia hacia mercados con precios superiores, el equilibrio local cambia. Cuando hay congestiones, pueden aparecer diferencias entre zonas.

Los factores de calendario son igualmente relevantes. Los dias laborables suelen presentar perfiles de demanda distintos a fines de semana y festivos. Las horas nocturnas, horas punta y horas solares tienen comportamientos diferenciados. Por ello, los modelos incluyen variables de hora, dia de la semana, mes e indicador de fin de semana.

Por ultimo, existen factores excepcionales: olas de frio o calor, eventos regulatorios, indisponibilidades inesperadas, cambios bruscos de combustible o episodios extremos de renovables. Estos eventos son dificiles de predecir con modelos basados solo en historico. Su existencia explica por que incluso modelos con buenas metricas pueden cometer errores significativos en momentos concretos.

### 4.6. Generacion renovable y formacion de precios

La generacion renovable ocupa un papel central en la evolucion reciente del mercado electrico. Tecnologias como la eolica y la solar fotovoltaica tienen costes variables reducidos. Cuando producen mucha energia, pueden cubrir una parte importante de la demanda y reducir la necesidad de tecnologias mas caras. Este efecto tiende a disminuir el precio marginal en determinadas horas.

La solar fotovoltaica presenta un patron diario marcado. Su produccion se concentra durante las horas de luz y alcanza valores mas altos alrededor de las horas centrales del dia. En dias soleados, la abundancia de generacion solar puede provocar precios bajos durante esas franjas. En cambio, al anochecer, la caida de produccion solar puede coincidir con demanda elevada, generando rampas de precio.

La eolica tiene un comportamiento mas variable y menos ligado al ciclo diario. Su produccion depende de las condiciones de viento, que pueden mantenerse durante varias horas o dias, pero tambien cambiar rapidamente. Una alta produccion eolica durante la noche puede reducir precios en horas tradicionalmente menos demandadas. Una baja eolica en momentos de alta demanda puede contribuir a precios superiores.

El efecto de las renovables no se limita a reducir precios. Tambien puede aumentar la volatilidad. Cuando la produccion renovable cambia rapidamente, el sistema debe adaptarse con otras tecnologias. Esta variabilidad puede reflejarse en el mercado si las previsiones cambian o si la disponibilidad real difiere de lo esperado.

Para un modelo predictivo, incorporar prevision renovable puede ser muy valioso. El precio historico contiene informacion indirecta sobre el comportamiento pasado de las renovables, pero no necesariamente sobre la renovable esperada para el siguiente periodo. Por ello, variables como prevision eolica o solar pueden aportar informacion adicional.

En este proyecto, las variables renovables procedentes de ESIOS se incorporan como columnas externas. Se consideran prevision eolica, solar fotovoltaica y solar termica. Ademas, se calculan variables agregadas como prevision solar total, prevision renovable total y ratio entre viento y solar. Estas variables intentan representar de forma sencilla la disponibilidad renovable esperada.

### 4.7. Particularidades de la energia eolica

La energia eolica se basa en transformar la energia cinetica del viento en electricidad. Su produccion depende de la velocidad del viento, la disponibilidad de los aerogeneradores y las caracteristicas del emplazamiento. En el sistema electrico espanol, la eolica tiene una presencia significativa y puede cubrir una parte relevante de la demanda en determinados momentos.

Una caracteristica importante de la eolica es su variabilidad. Aunque las previsiones meteorologicas permiten anticipar la produccion con cierta precision, siempre existe incertidumbre. Cambios en los patrones de viento pueden modificar la generacion esperada, afectando al equilibrio de oferta y demanda.

Desde el punto de vista del precio, una elevada produccion eolica suele ejercer presion bajista, ya que desplaza tecnologias con mayor coste variable. Este efecto puede ser especialmente visible en horas de baja demanda, como la noche, cuando una alta eolica puede cubrir una proporción considerable del consumo.

No obstante, la relacion entre eolica y precio no es perfectamente lineal. Depende de la demanda, de la produccion de otras tecnologias, de la disponibilidad hidraulica, de la solar, de las interconexiones y del contexto general del mercado. Por ello, modelos no lineales pueden ser utiles para capturar interacciones entre variables.

En el proyecto, la prevision eolica se representa mediante la columna `wind_forecast_mwh`. Esta variable se obtiene de ESIOS y se une al dataset de precios. Su objetivo es proporcionar al modelo informacion anticipada sobre la generacion eolica esperada.

### 4.8. Particularidades de la energia solar fotovoltaica

La energia solar fotovoltaica convierte la radiacion solar en electricidad. Su produccion esta condicionada por la hora del dia, la estacion del ano, la nubosidad, la temperatura y la potencia instalada. A diferencia de la eolica, la solar presenta un ciclo diario muy marcado: no produce durante la noche y concentra su generacion en horas diurnas.

En el mercado electrico, la solar tiene un impacto creciente. Durante horas centrales del dia, especialmente en meses con alta radiacion, puede reducir significativamente el precio. Este fenomeno se asocia a menudo con la llamada curva de pato, en la que la demanda neta baja durante las horas solares y aumenta rapidamente al final del dia cuando la produccion solar cae.

La solar fotovoltaica puede producir precios muy bajos si coincide con demanda moderada y alta generacion renovable. Sin embargo, su desaparicion al anochecer puede requerir la entrada de otras tecnologias, lo que puede elevar precios en horas posteriores. Por esta razon, no solo importa la cantidad de solar, sino tambien su perfil temporal.

En este proyecto se considera la prevision solar fotovoltaica mediante la columna `solar_pv_forecast_mwh`. Tambien se incorpora prevision solar termica, representada por `solar_thermal_forecast_mwh`. La suma de ambas permite obtener una medida agregada de generacion solar esperada.

La inclusion de variables solares puede ayudar al modelo a diferenciar dias con perfiles de precio similares en historico pero condiciones solares distintas. Por ejemplo, dos dias laborables de primavera pueden tener demanda parecida, pero precios diferentes si uno presenta alta radiacion solar y otro no.

### 4.9. Series temporales aplicadas a mercados electricos

Una serie temporal es una secuencia de observaciones ordenadas en el tiempo. El precio electrico es una serie temporal porque cada valor esta asociado a un periodo concreto. Este orden temporal es fundamental: el precio de un periodo puede depender de periodos anteriores y de patrones que se repiten.

En los mercados electricos aparecen varios tipos de patrones temporales. Existen patrones diarios, asociados a ciclos de actividad humana y produccion solar. Existen patrones semanales, relacionados con diferencias entre dias laborables y fines de semana. Tambien existen patrones estacionales, vinculados a temperatura, hidraulicidad, radiacion solar y consumo.

Para que un modelo de aprendizaje automatico pueda trabajar con una serie temporal, es habitual transformar la secuencia en un dataset supervisado. Esto se hace creando variables retardadas. Por ejemplo, para predecir el precio actual se pueden usar precios de una hora antes, del dia anterior o de la semana anterior. Estas variables permiten que modelos no especificamente temporales puedan aprender dependencias historicas.

Tambien se emplean medias moviles y medidas de dispersion. Una media movil resume el nivel reciente de la serie, mientras que una desviacion movil refleja volatilidad. Minimos y maximos recientes pueden indicar rangos de precio. Diferencias y ratios ayudan a capturar cambios bruscos o relaciones relativas entre periodos.

Otro aspecto importante es la validacion temporal. En series temporales no es adecuado mezclar aleatoriamente observaciones pasadas y futuras. Si se hiciera, el modelo podria entrenar con informacion posterior al periodo que se evalua. Por ello, este proyecto usa una separacion cronologica: los datos iniciales se emplean para entrenamiento y los ultimos para validacion.

La prediccion de precios electricos combina patrones regulares con eventos dificiles de anticipar. Por ello, las metricas globales deben complementarse con analisis de errores concretos. Un modelo puede tener buen MAE medio, pero fallar en dias festivos, precios extremos o cambios bruscos de renovable. Este analisis resulta esencial para entender las limitaciones del sistema.

### 4.10. Conceptos basicos de aprendizaje automatico supervisado

El aprendizaje automatico supervisado consiste en entrenar modelos a partir de ejemplos donde se conocen tanto las variables de entrada como la salida deseada. En este trabajo, las variables de entrada son caracteristicas temporales, retardos del precio y variables externas opcionales. La salida deseada es el precio `marginal_es`.

El problema se formula como regresion, ya que la variable objetivo es numerica y continua. El modelo debe aprender una funcion que relacione las variables de entrada con el precio esperado. Una vez entrenado, puede aplicarse a nuevas observaciones para generar predicciones.

Un aspecto fundamental es la division entre entrenamiento y validacion. El conjunto de entrenamiento se utiliza para ajustar el modelo. El conjunto de validacion se reserva para evaluar su comportamiento sobre datos no usados durante el ajuste. En este proyecto, la division se realiza respetando el orden temporal.

El sobreajuste es uno de los riesgos principales. Un modelo sobreajustado aprende demasiado bien los detalles del conjunto de entrenamiento, incluyendo ruido, y generaliza mal a datos nuevos. Para reducir este riesgo se utilizan tecnicas como regularizacion, validacion temporal y comparacion con modelos mas simples.

Los modelos implementados presentan caracteristicas diferentes. `RidgeCV` introduce regularizacion en un modelo lineal. `MLPRegressor` utiliza una red neuronal capaz de aprender relaciones no lineales. `HistGradientBoostingRegressor` combina multiples arboles de decision para mejorar progresivamente la prediccion. Comparar estos enfoques permite analizar si la complejidad adicional se traduce en mejores resultados.

Las metricas permiten cuantificar el rendimiento. El MAE expresa el error medio en unidades directamente interpretables. El RMSE penaliza errores grandes. El R2 indica la proporcion de variacion explicada. Ninguna metrica es suficiente por si sola, por lo que se analizan conjuntamente.

Finalmente, es importante destacar que un modelo de aprendizaje automatico no comprende el mercado en sentido humano. Aprende relaciones estadisticas presentes en los datos. Por ello, su utilidad depende de la calidad de las variables, la representatividad del historico y la estabilidad de los patrones. Esta idea es clave para interpretar los resultados del trabajo con cautela.

