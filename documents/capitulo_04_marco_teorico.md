# Capítulo 4. Marco teórico

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 4.1. Funcionamiento del mercado eléctrico español

El sistema eléctrico español esta formado por un conjunto de actividades técnicas, económicas y regulatorias cuyo objetivo es garantizar el suministro de electricidad a consumidores finales. Para que el sistema funcione correctamente debe existir equilibrio continuo entre generación y demanda. Este equilibrio es especialmente complejo porque la electricidad, a diferencia de otros bienes, no se almacena masivamente de forma sencilla y económica. Por ello, la producción debe adaptarse de manera constante al consumo.

En términos generales, el sector eléctrico se organiza en varias actividades: generación, transporte, distribución, comercialización y consumo. La generación corresponde a las instalaciones que producen energía eléctrica, como centrales nucleares, ciclos combinados, centrales hidráulicas, parques eólicos, plantas solares fotovoltaicas, termosolares o cogeneraciones. El transporte se realiza mediante redes de alta tensión y permite llevar electricidad desde los centros de generación hasta las zonas de consumo. La distribución acerca esa energía a consumidores finales mediante redes de media y baja tensión. La comercialización gestiona la relación contractual con los consumidores.

El precio de la electricidad se forma en distintos mercados y mecanismos. Uno de los más importantes es el mercado diario, donde se negocia energía para cada periodo del día siguiente. También existen mercados intradiarios, servicios de ajuste y mecanismos de balance gestionados para mantener la seguridad del sistema. El precio que se analiza en este trabajo corresponde al mercado diario, concretamente al precio marginal español publicado por OMIE.

En el mercado diario, los generadores presentan ofertas de venta y los compradores presentan ofertas de adquisición de energía. El algoritmo de casación ordena ofertas de acuerdo con criterios económicos y técnicos, determinando el precio resultante para cada periodo. El precio marginal es el precio de la última unidad necesaria para cubrir la demanda casada. Esto significa que todas las unidades casadas en ese periodo reciben, en general, el precio marginal correspondiente.

La estructura marginalista del mercado implica que tecnologías con costes variables bajos, como eólica, solar o nuclear, pueden desplazar a tecnologías más caras. Cuando la demanda puede cubrirse con tecnologías de bajo coste variable, el precio tiende a ser más bajo. En cambio, cuando es necesario recurrir a tecnologías con costes variables superiores, como ciclos combinados de gas, el precio puede elevarse. Esta dinámica explica por que factores como la demanda, el viento, la radiación solar, el gas o el CO2 influyen en el precio.

El sistema eléctrico español está integrado en el Mercado Ibérico de Electricidad, compartido con Portugal. Por ello, los precios de España y Portugal pueden coincidir o diferir en función de la capacidad de interconexión y de las condiciones de mercado. Cuando no existen restricciones relevantes entre ambas zonas, los precios tienden a converger. Si aparecen congestiónes, pueden producirse precios distintos.

Para desarrollar modelos predictivos es necesario entender que el precio del mercado diario no es una variable aislada. Es el resultado de la interacción entre ofertas, demanda, tecnologías disponibles, restricciones, meteorología y expectativas. Esta complejidad justifica el uso de técnicas de aprendizaje automático, pero también obliga a ser prudentes en la interpretación de los resultados.

### 4.2. Mercado diario e intradiario

El mercado diario es el mecanismo donde se negocia la mayor parte de la energía eléctrica para el día siguiente. Los agentes presentan sus ofertas antes de una hora límite y el operador del mercado realiza la casación. El resultado es un programa de energía y un precio para cada periodo. Tradicionalmente, estos periodos han sido horarios, aunque el sistema avanza hacia resoluciones temporales más cortas, como periodos cuarto-horarios.

El mercado diario tiene gran importancia porque proporciona una referencia pública y transparente del precio de la energía. Muchos contratos y análisis energéticos utilizan este precio como base. Aunque no toda la energía se compra directamente en el mercado diario, su señal económica es fundamental para el conjunto del sistema.

El mercado intradiario permite ajustar posiciones después del mercado diario. La demanda real, la generación renovable o la disponibilidad de las centrales pueden diferir de las previsiones iniciales. Por ello, los agentes necesitan mecanismos para corregir desviaciones y adaptar su programa. Los mercados intradiarios contribuyen a mejorar la eficiencia del sistema al permitir ajustes más cercanos al tiempo real.

Además de los mercados diario e intradiario, existen servicios de ajuste y balance. Estos mecanismos permiten al operador del sistema mantener el equilibrio físico entre generación y demanda, resolver restricciones técnicas y garantizar la seguridad del suministro. Aunque estos servicios no son el objeto principal de este trabajo, forman parte del contexto general que afecta a la operación eléctrica.

La predicción del precio del mercado diario se diferencia de la predicción intradiaria en el horizonte temporal y en la información disponible. Para el mercado diario se intenta anticipar el precio antes de que se conozca la casación del día siguiente. En cambio, en mercados intradiarios pueden incorporarse datos más recientes. Este trabajo se centra en el precio publicado por OMIE para el mercado diario, aunque la metodología podría extenderse a otros horizontes.

Para un modelo de aprendizaje automático, el mercado diario ofrece una serie temporal estructurada. Cada periodo tiene un precio, una fecha, una posición dentro del día y un contexto histórico. Esto permite generar variables como retardos, medias móviles o indicadores de calendario. Sin embargo, el mercado diario también está influido por variables externas que no siempre están presentes en el histórico de precios, como la demanda esperada o la previsión meteorológica.

### 4.3. Papel de OMIE en el mercado eléctrico

OMIE es el Operador del Mercado Ibérico de Energía en el polo español. Su función principal es gestionar los mercados mayoristas de electricidad en el ámbito ibérico, incluyendo el mercado diario y diferentes sesiones intradiarias. OMIE recibe ofertas de compra y venta, ejecuta los procesos de casación y pública resultados de mercado.

Para este trabajo, OMIE es especialmente relevante porque proporciona los datos de precio marginal utilizados como variable objetivo. En concreto, se emplean los ficheros `MARGINALPDBC`, que contienen información diaria del precio marginal para Portugal y España. El campo `marginal_es` representa el precio marginal español y se expresa en euros por megavatio hora.

La disponibilidad pública de estos ficheros permite construir una base histórica de precios. El proyecto desarrollado descarga automáticamente los ficheros diarios, los almacena en cache y los transforma en un formato tabular. Esta automatización facilita repetir experimentos, ampliar rangos temporales y mantener separada la fuente original de los datos procesados.

El formato de los ficheros OMIE requiere parseo. Cada fila incluye información como año, mes, día, periodo, precio marginal portugués y precio marginal español. A partir de estos campos se genera un timestamp que permite ordenar las observaciones y unirlas con otras fuentes de datos. Esta normalización es indispensable para cualquier análisis posterior.

OMIE no solo publica precios, sino también otros resultados de mercado que podrían ser útiles en futuras extensiónes. Sin embargo, este trabajo se centra en el precio marginal español por ser la variable más directamente relacionada con el objetivo de predicción. Incorporar más datos de OMIE, como volúmenes casados u ofertas agregadas, podría mejorar el modelo, pero queda fuera del alcance inicial.

Desde el punto de vista metodológico, OMIE proporciona una fuente fiable y oficial para el precio del mercado diario. Esto reduce incertidumbre sobre la procedencia de la variable objetivo y permite que el proyecto sea reproducible. Cualquier usuario con acceso a internet puede descargar los mismos ficheros y reconstruir el dataset.

### 4.4. Papel de Red Eléctrica y ESIOS

Red Eléctrica desempena el papel de operador del sistema eléctrico español. Su responsabilidad principal es garantizar la continuidad y seguridad del suministro, manteniendo el equilibrio entre generación y demanda en tiempo real. Para ello coordina la operación del sistema, gestiona restricciones técnicas y supervisa el funcionamiento de la red de transporte.

ESIOS es el Sistema de Información del Operador del Sistema. A través de ESIOS se publican numerosos indicadores relacionados con la demanda, la generación, la programación, las previsiones y otros aspectos del sistema eléctrico. Esta plataforma constituye una fuente de datos muy valiosa para análisis energéticos.

En este trabajo, ESIOS se utiliza de forma opcional para incorporar previsiones de generación renovable. En concreto, se consideran indicadores de previsión eólica, solar fotovoltaica y solar térmica. Estas variables pueden aportar información adicional sobre la disponibilidad esperada de energía renovable, que es un factor relevante en la formación del precio.

La integración de ESIOS requiere un token de acceso a su API. Por ese motivo se ha implementado como funcionalidad opcional. El sistema puede funcionar usando solo OMIE, pero si el usuario dispone de token ESIOS puede enriquecer el dataset. Esta decisión permite mantener la accesibilidad del proyecto sin renunciar a incorporar variables externas.

Los datos procedentes de ESIOS se unen con los datos de OMIE mediante la columna temporal `timestamp`. Dado que pueden existir diferencias de resolución temporal, el sistema utiliza una aproximación que asigna la última previsión disponible dentro de una tolerancia definida. Esta estrategia permite combinar datos horarios con observaciones de precio que pueden ser cuarto-horarias.

El papel de ESIOS en el modelo es aportar contexto físico del sistema. Mientras que OMIE proporciona el precio resultante del mercado, ESIOS puede proporcionar información sobre condiciones esperadas del sistema, como renovables. Esta combinación es más rica que usar únicamente histórico de precios.

### 4.5. Factores que influyen en el precio eléctrico

El precio eléctrico depende de múltiples factores que actuan simultaneamente. Uno de los más importantes es la demanda. Cuando la demanda es alta, el sistema necesita recurrir a más generación para cubrir el consumo. Si las tecnologías de menor coste no son suficientes, entran tecnologías más caras y el precio marginal puede aumentar.

La disponibilidad de generación es otro factor clave. Las centrales pueden estar disponibles, indisponibles por mantenimiento o limitadas por condiciones técnicas. La generación hidráulica depende de reservas y estrategias de gestión del agua. La nuclear suele operar de forma estable, pero sus paradas afectan a la oferta base. Los ciclos combinados dependen del coste del gas y de su posición en el orden de mérito.

La producción renovable tiene un efecto creciente. La eólica y la solar presentan costes variables muy bajos y, cuando están disponibles, desplazan a tecnologías más caras. Sin embargo, su producción depende de condiciones meteorológicas. Esto introduce variabilidad y hace que el precio pueda cambiar notablemente entre días aparentemente similares.

El precio del gas natural influye especialmente cuando los ciclos combinados marcan el precio marginal. Si el gas es caro, el coste de producir electricidad con está tecnología aumenta. Del mismo modo, los derechos de emision de CO2 afectan a tecnologías emisoras, incrementando sus costes variables.

Las interconexiones internacionales también pueden influir. Si existe capacidad para importar energía más barata o exportar energía hacia mercados con precios superiores, el equilibrio local cambia. Cuando hay congestiónes, pueden aparecer diferencias entre zonas.

Los factores de calendario son igualmente relevantes. Los días laborables suelen presentar perfiles de demanda distintos a fines de semana y festivos. Las horas nocturnas, horas punta y horas solares tienen comportamientos diferenciados. Por ello, los modelos incluyen variables de hora, día de la semana, mes e indicador de fin de semana.

Por último, existen factores excepcionales: olas de frío o calor, eventos regulatorios, indisponibilidades inesperadas, cambios bruscos de combustible o episodios extremos de renovables. Estos eventos son difíciles de predecir con modelos basados solo en histórico. Su existencia explica por que incluso modelos con buenas métricas pueden cometer errores significativos en momentos concretos.

### 4.6. Generación renovable y formación de precios

La generación renovable ocupa un papel central en la evolución reciente del mercado eléctrico. Tecnologias como la eólica y la solar fotovoltaica tienen costes variables reducidos. Cuando producen mucha energía, pueden cubrir una parte importante de la demanda y reducir la necesidad de tecnologías más caras. Este efecto tiende a disminuir el precio marginal en determinadas horas.

La solar fotovoltaica presenta un patrón diario marcado. Su producción se concentra durante las horas de luz y alcanza valores más altos alrededor de las horas centrales del día. En días soleados, la abundancia de generación solar puede provocar precios bajos durante esas franjas. En cambio, al anochecer, la caída de producción solar puede coincidir con demanda elevada, generando rampas de precio.

La eólica tiene un comportamiento más variable y menos ligado al ciclo diario. Su producción depende de las condiciones de viento, que pueden mantenerse durante varias horas o días, pero también cambiar rápidamente. Una alta producción eólica durante la noche puede reducir precios en horas tradicionalmente menos demandadas. Una baja eólica en momentos de alta demanda puede contribuir a precios superiores.

El efecto de las renovables no se limita a reducir precios. También puede aumentar la volatilidad. Cuando la producción renovable cambia rápidamente, el sistema debe adaptarse con otras tecnologías. Esta variabilidad puede reflejarse en el mercado si las previsiones cambian o si la disponibilidad real difiere de lo esperado.

Para un modelo predictivo, incorporar previsión renovable puede ser muy valioso. El precio histórico contiene información indirecta sobre el comportamiento pasado de las renovables, pero no necesariamente sobre la renovable esperada para el siguiente periodo. Por ello, variables como previsión eólica o solar pueden aportar información adicional.

En este proyecto, las variables renovables procedentes de ESIOS se incorporan como columnas externas. Se consideran previsión eólica, solar fotovoltaica y solar térmica. Además, se calculan variables agregadas como previsión solar total, previsión renovable total y ratio entre viento y solar. Estas variables intentan representar de forma sencilla la disponibilidad renovable esperada.

### 4.7. Particularidades de la energía eólica

La energía eólica se basa en transformar la energía cinetica del viento en electricidad. Su producción depende de la velocidad del viento, la disponibilidad de los aerogeneradores y las características del emplazamiento. En el sistema eléctrico español, la eólica tiene una presencia significativa y puede cubrir una parte relevante de la demanda en determinados momentos.

Una característica importante de la eólica es su variabilidad. Aunque las previsiones meteorológicas permiten anticipar la producción con cierta precisión, siempre existe incertidumbre. Cambios en los patrones de viento pueden modificar la generación esperada, afectando al equilibrio de oferta y demanda.

Desde el punto de vista del precio, una elevada producción eólica suele ejercer presión bajista, ya que desplaza tecnologías con mayor coste variable. Este efecto puede ser especialmente visible en horas de baja demanda, como la noche, cuando una alta eólica puede cubrir una proporción considerable del consumo.

No obstante, la relación entre eólica y precio no es perfectamente lineal. Depende de la demanda, de la producción de otras tecnologías, de la disponibilidad hidráulica, de la solar, de las interconexiones y del contexto general del mercado. Por ello, modelos no lineales pueden ser útiles para capturar interacciones entre variables.

En el proyecto, la previsión eólica se representa mediante la columna `wind_forecast_mwh`. Esta variable se obtiene de ESIOS y se une al dataset de precios. Su objetivo es proporcionar al modelo información anticipada sobre la generación eólica esperada.

### 4.8. Particularidades de la energía solar fotovoltaica

La energía solar fotovoltaica convierte la radiación solar en electricidad. Su producción está condicionada por la hora del día, la estacion del año, la nubosidad, la temperatura y la potencia instalada. A diferencia de la eólica, la solar presenta un ciclo diario muy marcado: no produce durante la noche y concentra su generación en horas diurnas.

En el mercado eléctrico, la solar tiene un impacto creciente. Durante horas centrales del día, especialmente en meses con alta radiación, puede reducir significativamente el precio. Este fenomeno se asocia a menudo con la llamada curva de pato, en la que la demanda neta baja durante las horas solares y aumenta rápidamente al final del día cuando la producción solar cae.

La solar fotovoltaica puede producir precios muy bajos si coincide con demanda moderada y alta generación renovable. Sin embargo, su desaparicion al anochecer puede requerir la entrada de otras tecnologías, lo que puede elevar precios en horas posteriores. Por está razón, no solo importa la cantidad de solar, sino también su perfil temporal.

En este proyecto se considera la previsión solar fotovoltaica mediante la columna `solar_pv_forecast_mwh`. También se incorpora previsión solar térmica, representada por `solar_thermal_forecast_mwh`. La suma de ambas permite obtener una medida agregada de generación solar esperada.

La inclusión de variables solares puede ayudar al modelo a diferenciar días con perfiles de precio similares en histórico pero condiciones solares distintas. Por ejemplo, dos días laborables de primavera pueden tener demanda parecida, pero precios diferentes si uno presenta alta radiación solar y otro no.

### 4.9. Series temporales aplicadas a mercados eléctricos

Una serie temporal es una secuencia de observaciones ordenadas en el tiempo. El precio eléctrico es una serie temporal porque cada valor está asociado a un periodo concreto. Este orden temporal es fundamental: el precio de un periodo puede depender de periodos anteriores y de patrones que se repiten.

En los mercados eléctricos aparecen varios tipos de patrones temporales. Existen patrones diarios, asociados a ciclos de actividad humana y producción solar. Existen patrones semanales, relacionados con diferencias entre días laborables y fines de semana. También existen patrones estacionales, vinculados a temperatura, hidraulicidad, radiación solar y consumo.

Para que un modelo de aprendizaje automático pueda trabajar con una serie temporal, es habitual transformar la secuencia en un dataset supervisado. Esto se hace creando variables retardadas. Por ejemplo, para predecir el precio actual se pueden usar precios de una hora antes, del día anterior o de la semana anterior. Estas variables permiten qué modelos no especificamente temporales puedan aprender dependencias históricas.

También se emplean medias móviles y medidas de dispersion. Una media móvil resume el nivel reciente de la serie, mientras que una desviación movil refleja volatilidad. Mínimos y máximos recientes pueden indicar rangos de precio. Diferencias y ratios ayudan a capturar cambios bruscos o relaciones relativas entre periodos.

Otro aspecto importante es la validación temporal. En series temporales no es adecuado mezclar aleatoriamente observaciones pasadas y futuras. Si se hiciera, el modelo podría entrenar con información posterior al periodo que se evalúa. Por ello, este proyecto usa una separación cronológica: los datos iniciales se emplean para entrenamiento y los últimos para validación.

La predicción de precios eléctricos combina patrones regulares con eventos difíciles de anticipar. Por ello, las métricas globales deben complementarse con análisis de errores concretos. Un modelo puede tener buen MAE medio, pero fallar en días festivos, precios extremos o cambios bruscos de renovable. Este análisis resulta esencial para entender las limitaciones del sistema.

### 4.10. Conceptos básicos de aprendizaje automático supervisado

El aprendizaje automático supervisado consiste en entrenar modelos a partir de ejemplos donde se conocen tanto las variables de entrada como la salida deseada. En este trabajo, las variables de entrada son características temporales, retardos del precio y variables externas opcionales. La salida deseada es el precio `marginal_es`.

El problema se formula como regresión, ya que la variable objetivo es numérica y continúa. El modelo debe aprender una función que relacione las variables de entrada con el precio esperado. Una vez entrenado, puede aplicarse a nuevas observaciones para generar predicciones.

Un aspecto fundamental es la división entre entrenamiento y validación. El conjunto de entrenamiento se utiliza para ajustar el modelo. El conjunto de validación se reserva para evaluar su comportamiento sobre datos no usados durante el ajuste. En este proyecto, la división se realiza respetando el orden temporal.

El sobreajuste es uno de los riesgos principales. Un modelo sobreajustado aprende demasiado bien los detalles del conjunto de entrenamiento, incluyendo ruido, y generaliza mal a datos nuevos. Para reducir este riesgo se utilizan técnicas como regularización, validación temporal y comparación con modelos más simples.

Los modelos implementados presentan características diferentes. `RidgeCV` introduce regularización en un modelo lineal. `MLPRegressor` utiliza una red neuronal capaz de aprender relaciones no lineales. `HistGradientBoostingRegressor` combina múltiples árboles de decisión para mejorar progresivamente la predicción. Comparar estos enfoques permite analizar si la complejidad adicional se traduce en mejores resultados.

Las métricas permiten cuantificar el rendimiento. El MAE expresa el error medio en unidades directamente interpretables. El RMSE penaliza errores grandes. El R2 indica la proporción de variación explicada. Ninguna métrica es suficiente por sí sola, por lo que se analizan conjuntamente.

Finalmente, es importante destacar que un modelo de aprendizaje automático no comprende el mercado en sentido humaño. Aprende relaciones estadisticas presentes en los datos. Por ello, su utilidad depende de la calidad de las variables, la representatividad del histórico y la estabilidad de los patrones. Esta idea es clave para interpretar los resultados del trabajo con cautela.

