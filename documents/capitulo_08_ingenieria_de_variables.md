# Capítulo 8. Ingeniería de variables

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 8.1. Variables de calendario

La ingeniería de variables es una de las fases más importantes en un proyecto de predicción del precio eléctrico. Los modelos de aprendizaje automático no trabajan directamente con el concepto abstracto de mercado, sino con columnas numéricas construidas a partir de los datos disponibles. Por ello, la calidad de las variables influye de forma decisiva en la capacidad predictiva del sistema.

En este proyecto, la primera familia de variables procede del calendario. El precio eléctrico presenta patrones temporales claros: cambia según la hora del día, el día de la semana, el mes y el tipo de jornada. Estos patrones no explican todo el comportamiento del mercado, pero proporcionan una base inicial muy relevante. Por ejemplo, una madrugada suele tener un perfil de demanda distinto al de una hora punta, y un domingo no se comporta igual que un día laborable.

La columna `timestamp` permite extraer la información temporal necesaria. A partir de ella se obtiene la hora, el minuto, el día de la semana y el mes. Estas variables capturan regularidades asociadas al consumo eléctrico y a la disponibilidad de generación. En invierno y verano pueden aparecer comportamientos diferentes por calefacción, refrigeración o cambios de irradiación solar. Del mismo modo, los días laborables suelen presentar mayor actividad industrial y comercial que los fines de semana.

El proyecto conserva también la variable `period`, que indica la posición de la observación dentro del día. Esta variable es especialmente útil porque procede directamente del fichero OMIE y mantiene una relación clara con la estructura del mercado. En datos horarios, `period` toma valores de 1 a 24. En datos cuarto-horarios, puede tomar valores de 1 a 96. Por tanto, ayuda al modelo a conocer dónde se sitúa cada observación dentro de la jornada.

Otra variable de calendario incluida es `is_weekend`. Esta columna vale 1 cuando la observación corresponde a sábado o domingo, y 0 en caso contrario. Su objetivo es diferenciar días con patrones de demanda diferentes. Aunque el día de la semana ya se codifica mediante variables cíclicas, disponer de un indicador directo de fin de semana facilita al modelo capturar cambios bruscos entre días laborables y no laborables.

Las variables de calendario tienen la ventaja de estar disponibles siempre. No dependen de APIs externas ni de descargas adicionales. Para realizar una inferencia futura, el sistema conoce de antemano la fecha y hora del periodo que quiere predecir. Esto las convierte en variables robustas y adecuadas para una primera versión del modelo.

Sin embargo, estas variables tienen limitaciones. Saber que una observación ocurre un martes a las 10:00 no informa por sí solo sobre la demanda real, la generación eólica, la disponibilidad nuclear o el precio del gas. Por tanto, las variables de calendario deben entenderse como una base estructural, no como una explicación completa del precio. Su valor aumenta cuando se combinan con retardos del precio y variables externas.

### 8.2. Variables cíclicas de hora, día y mes

Muchas variables temporales tienen naturaleza cíclica. La hora del día no es una magnitud lineal simple: las 23:00 y las 00:00 están cerca en el ciclo diario, aunque si se codifican como números 23 y 0 parezcan valores muy alejados. Lo mismo ocurre con los días de la semana y con los meses del año. Diciembre y enero son consecutivos, pero numéricamente 12 y 1 están separados por una distancia grande.

Para resolver este problema, el proyecto utiliza codificación mediante seno y coseno. Esta técnica transforma una variable cíclica en dos variables continuas que representan su posición sobre una circunferencia. De está manera, los extremos del ciclo quedan correctamente unidos. El modelo puede aprender que el final de un día está cerca del comienzo del siguiente, o que el final de una semana está cerca del inicio de la siguiente.

En el caso de la hora y el minuto, el programa calcula primero `minute_of_day`, que representa los minutos transcurridos desde el inicio del día. Después genera `time_of_day_sin` y `time_of_day_cos` aplicando funciones trigonométricas sobre el ciclo completo de 1440 minutos. Esta representación es más precisa que usar solo la hora, ya que también distingue observaciones cuarto-horarias.

Además, se generan `hour_sin` y `hour_cos` a partir de la hora del día. Aunque puede parecer redundante con `time_of_day_sin` y `time_of_day_cos`, ambas representaciones pueden aportar información complementaria. La variable basada en minuto del día captura con más detalle la posición temporal, mientras que la hora resume el comportamiento horario tradicional.

Para el día de la semana se calculan `dow_sin` y `dow_cos`. Estas variables codifican un ciclo de siete días. Permiten representar diferencias entre lunes, martes, miercoles, jueves, viernes, sábado y domingo, manteniendo la continuidad entre domingo y lunes. Este tipo de codificación es útil porque el mercado eléctrico presenta perfiles semanales reconocibles.

Para el mes se calculan `month_sin` y `month_cos`. Estas variables representan el ciclo anual y permiten capturar estacionalidad. El precio eléctrico puede verse afectado por temperatura, demanda estacional, disponibilidad hidráulica, radiación solar y patrones de consumo asociados a cada época del año. Aunque el modelo no incorpora directamente meteorología en esta versión, el mes puede actuar como aproximación parcial a factores estacionales.

La codificación cíclica es especialmente beneficiosa para modelos lineales y redes neuronales. Si se usaran valores enteros sin transformar, el modelo podría interpretar relaciones artificiales entre números. Por ejemplo, podría considerar que diciembre está mucho más lejos de enero que de noviembre, cuando en realidad enero y diciembre son meses contiguos en el ciclo anual. Las variables seno/coseno reducen este problema.

En modelos basados en árboles, como HistGradientBoosting, la necesidad de codificación cíclica puede ser menor, porque los árboles pueden dividir el espacio de variables por umbrales. Aun así, mantener la misma representación para todos los modelos permite compararlos con una matriz de entrada común. Esta decisión simplifica el pipeline y evita crear preparaciones distintas para cada algoritmo.

### 8.3. Retardos del precio eléctrico

Los retardos del precio son variables fundamentales en la predicción de series temporales. Un retardo consiste en incluir como entrada el valor pasado de la variable que se quiere predecir. En este proyecto, la variable objetivo es `marginal_es`, y los retardos se construyen desplazando esa columna hacia atrás distintos números de periodos.

El precio eléctrico presenta dependencia temporal. El precio de un periodo no suele ser completamente independiente del precio anterior. Las condiciones que influyen en el mercado, como demanda, disponibilidad de generación o contexto de combustibles, tienden a persistir durante varias horas o días. Por ello, conocer precios recientes aporta información relevante para estimar precios futuros.

El proyecto utiliza los retardos `1`, `2`, `3`, `4`, `5`, `6`, `12`, `23`, `24`, `25`, `48`, `72`, `168` y `336`. Los retardos cortos capturan continuidad inmediata. Por ejemplo, `price_lag_1` recoge el precio del periodo inmediatamente anterior y `price_lag_2` el de dos periodos antes. Estos valores ayudan al modelo a detectar tendencias recientes o cambios suaves.

Los retardos intermedios, como `12`, `23`, `24` y `25`, buscan capturar patrones diarios. En datos horarios, `price_lag_24` aproxima el precio del mismo periodo del día anterior. Los retardos `23` y `25` rodean ese punto y permiten al modelo observar pequeñas variaciones alrededor del ciclo diario. Esta estrategia es útil porque los perfiles de precio suelen repetirse parcialmente de un día a otro.

Los retardos más largos, como `168` y `336`, capturan patrones semanales. En datos horarios, 168 periodos equivalen a una semana, y 336 a dos semanas. Esto permite comparar una observación con el mismo momento de semanas anteriores. La demanda y el comportamiento del mercado pueden tener regularidades semanales, por lo que estos retardos aportan contexto de más largo plazo.

Es importante recordar que el significado temporal exacto de un retardo depende de la resolución de los datos. En datos horarios, un retardo de 24 periodos equivale a un día. En datos cuarto-horarios, equivale a seis horas. El proyecto documenta esta limitación y mantiene una implementación basada en periodos. En futuras versiones se podría mejorar calculando retardos por duración real, por ejemplo 24 horas o 7 días.

Los retardos tienen una ventaja importante: se obtienen exclusivamente de datos históricos del precio. No requieren fuentes externas y están disponibles siempre que exista suficiente histórico. Sin embargo, también tienen una limitación: si el mercado cambia bruscamente por un evento externo no reflejado en precios pasados, los retardos pueden no anticipar correctamente el nuevo comportamiento.

Para evitar fuga de información, cada retardo se calcula usando valores anteriores al periodo objetivo. El modelo no recibe el precio que intenta predecir, sino precios ya observados. Esta disciplina temporal es esencial para que la evaluación sea realista. Una variable mal desplazada podría introducir el valor futuro en el entrenamiento y generar métricas artificialmente buenas.

### 8.4. Medias móviles

Las medias móviles resumen el nivel reciente del precio. En lugar de proporcionar al modelo un único valor pasado, calculan el promedio de una ventana de observaciones anteriores. Esto suaviza fluctuaciones puntuales y permite capturar el contexto general del mercado en distintos horizontes temporales.

El proyecto calcula medias móviles para ventanas de `3`, `6`, `12`, `24`, `48` y `168` periodos. Las ventanas cortas reflejan el comportamiento reciente. Por ejemplo, una media de 3 o 6 periodos indica si el precio acaba de subir o bajar en el entorno inmediato. Las ventanas de 24 y 48 periodos aproximan el nivel de uno o dos días en datos horarios. La ventana de 168 periodos resume aproximadamente una semana horaria.

Estas variables ayudan al modelo a diferenciar entre precios aislados y tendencias sostenidas. Un precio alto en el periodo anterior puede tener interpretaciones distintas si la media reciente también es alta o si se trata de un pico puntual. La media móvil proporciona contexto y reduce la sensibilidad a valores extremos aislados.

Las medias móviles se calculan sobre `shifted_price`, es decir, sobre el precio desplazado un periodo. Esta decisión evita que la media de una fila incluya el precio objetivo de esa misma fila. Si se usara directamente la serie sin desplazar, la media móvil podría contener información del valor que se quiere predecir, generando fuga de información futura.

El uso de varias ventanas permite capturar dinámicas a distintas escalas. El mercado eléctrico puede tener movimientos de corto plazo asociados a una hora concreta, pero también tendencias de varios días. Un modelo puede aprender que una subida reciente es más relevante cuando coincide con una media semanal alta, o que un precio bajo es más probable si las medias de varias ventanas están descendiendo.

Las medias móviles son especialmente útiles para modelos lineales, porque convierten patrones temporales en variables tabulares. En lugar de exigir al modelo que deduzca la tendencia desde muchos retardos individuales, se le ofrece una medida ya resumida. También pueden beneficiar a modelos de árboles y redes neuronales, al aportar señales estables.

La principal limitación es que las medias móviles necesitan histórico suficiente. Las primeras filas del dataset no pueden tener una media de 168 periodos si todavía no existen 168 observaciones previas. Por ello, estas filas se eliminan durante la construcción del dataset supervisado. Este coste es asumible cuando se entrena con rangos amplios.

### 8.5. Desviaciones móviles

Además del nivel medio, es importante representar la volatilidad reciente. La desviación movil mide cuanto se han alejado los precios de su media dentro de una ventana temporal. En el mercado eléctrico, la volatilidad es una característica relevante: periodos con precios estables no se comportan igual que periodos con cambios bruscos o picos frecuentes.

El proyecto calcula desviaciones móviles para las mismas ventanas que las medias: `3`, `6`, `12`, `24`, `48` y `168` periodos. De este modo, el modelo recibe información sobre volatilidad a corto, medio y largo plazo. Una desviación alta puede indicar incertidumbre, transición de régimen o presencia reciente de precios extremos.

Por ejemplo, si la media de las últimas 24 observaciones es moderada pero la desviación es alta, significa que el precio ha oscilado mucho. En cambio, una media similar con desviación baja indica estabilidad. Estos dos contextos pueden llevar a predicciones distintas, aunque el nivel promedio sea parecido.

La desviación movil puede ayudar especialmente en episodios de mercado tensiónado. Cuando el sistema alterna entre horas baratas y horas caras, la media por sí sola puede ocultar esa variabilidad. La desviación aporta una medida complementaria que permite al modelo detectar comportamientos irregulares.

Igual que las medias, las desviaciones se calculan sobre el precio desplazado un periodo. Esto mantiene la coherencia temporal y evita utilizar el valor objetivo dentro de la variable explicativa. La prevencion de fuga de información es una regla constante en toda la ingeniería de variables.

Las desviaciones también tienen limitaciones. En ventanas muy cortas pueden ser ruidosas, y en ventanas largas pueden reaccionar lentamente a cambios recientes. Por eso se incluyen varias escalas. El modelo decide durante el entrenamiento que ventanas son más útiles para reducir el error.

En modelos lineales, la desviación movil introduce una aproximación sencilla a la volatilidad. En modelos no lineales, puede interactuar con otras variables. Por ejemplo, el impacto de un retardo alto puede ser diferente si la volatilidad reciente también es alta. Esta clase de interacciones es una de las razones para incluir modelos como HistGradientBoosting.

### 8.6. Mínimos y máximos recientes

Los mínimos y máximos móviles permiten describir el rango reciente del precio. Mientras que la media resume el nivel central y la desviación mide dispersion, los mínimos y máximos indican los extremos observados en una ventana temporal. En mercados eléctricos, los extremos son importantes porque los picos de precio y los precios muy bajos tienen gran significado económico.

El proyecto calcula `price_roll_24_min`, `price_roll_24_max`, `price_roll_168_min` y `price_roll_168_max`. Estas variables representan el mínimo y máximo de las últimas 24 y 168 observaciones, siempre usando precios anteriores al objetivo. En datos horarios, estas ventanas aproximan un día y una semana.

El mínimo reciente puede ser informativo en periodos con abundante generación renovable o baja demanda. Si el precio ha alcanzado niveles muy bajos en las últimas horas, el modelo puede interpretar que existe un contexto de mercado barato. El máximo reciente, por el contrario, puede indicar tensión, demanda elevada o entrada de tecnologías caras.

El rango formado por mínimo y máximo también aporta información indirecta sobre amplitud de precios. Dos periodos pueden tener la misma media reciente, pero uno puede haber oscilado entre valores muy bajos y muy altos, mientras que otro se ha mantenido estable. Los extremos ayudan a distinguir esos contextos.

Estas variables son sencillas de calcular y fáciles de interpretar. Un analista puede entender rápidamente qué significa el máximo de las últimas 24 observaciones. Esta interpretabilidad es valiosa en un Proyecto, porque permite explicar como se transforma la serie original antes de entrenar los modelos.

Los mínimos y máximos también pueden ayudar a los modelos basados en árboles, que son buenos detectando umbrales. Por ejemplo, el modelo puede aprender reglas del tipo: si el máximo reciente supera cierto valor y la hora corresponde a una franja punta, el precio esperado puede ser más alto. Aunque el modelo no se exprese así literalmente en el documento, esa es la intuición que justifica estas variables.

La limitación principal es que los extremos pueden estar afectados por valores atípicos. Un único pico muy alto puede mantener elevado el máximo movil durante toda la ventana, aunque el mercado ya haya vuelto a la normalidad. Por eso no se utilizan solos, sino combinados con medias, desviaciones, retardos y variables de calendario.

### 8.7. Diferencias frente a periodos anteriores

Las diferencias entre precios retardados permiten representar cambios recientes. En lugar de mirar solo el nivel absoluto del precio, el modelo recibe información sobre si el precio está subiendo o bajando respecto a referencias anteriores. Esto es importante porque la dirección del cambio puede contener información predictiva.

El proyecto calcula tres diferencias principales: `price_diff_1`, `price_diff_24` y `price_diff_168`. La primera compara el último precio disponible con el precio de dos periodos atrás. En la práctica, mide la variación más inmediata. Si `price_diff_1` es positiva, el precio acaba de subir; si es negativa, acaba de bajar.

La diferencia `price_diff_24` compara el último precio disponible con el precio de 24 periodos antes. En datos horarios, esto aproxima la diferencia frente al mismo entorno del día anterior. Esta variable ayuda a detectar si el mercado está más caro o más barato que en la jornada previa.

La diferencia `price_diff_168` compara el último precio disponible con el precio de 168 periodos antes. En datos horarios, esta referencia equivale aproximadamente a una semana. Puede capturar cambios semanales, como una subida general de precios respecto a la semana anterior o una caída asociada a condiciones renovables favorables.

Las diferencias son útiles porque eliminan parcialmente el nivel base y se centran en la variación. Por ejemplo, un precio de 80 EUR/MWh puede ser alto o bajo dependiendo del contexto. Si ayer a la misma hora el precio era 40, indica una subida notable. Si era 120, indica una bajada. La diferencia aporta esa perspectiva relativa.

Estas variables también pueden ayudar a detectar cambios de régimen. Una sucesion de diferencias positivas puede sugerir una tendencia alcista; diferencias negativas pueden indicar relajacion del mercado. Aunque el modelo no usa una secuencia explícita como una red recurrente, estas variables tabulares resumen parte de esa dinámica.

Como en el resto de variables históricas, las diferencias se calculan exclusivamente con retardos. No utilizan el precio presente que se quiere predecir. Esto mantiene la validez temporal del dataset y evita sobreestimar el rendimiento.

Una limitación de las diferencias es que pueden amplificar ruido cuando los precios fluctúan mucho. Por eso se combinan con medias y desviaciones móviles. Mientras las diferencias capturan cambios puntuales, las medias y desviaciones ofrecen contexto sobre si esos cambios son aislados o forman parte de una dinámica más amplia.

### 8.8. Ratios temporales

Los ratios temporales comparan el precio reciente con precios de referencia anteriores mediante una relación proporcional. En el proyecto se calculan `price_ratio_24` y `price_ratio_168`. Estos ratios dividen el último precio disponible entre el precio de 24 o 168 periodos antes, respectivamente.

La ventaja de un ratio es que expresa cambios relativos. Una subida de 10 EUR/MWh no tiene el mismo significado si el precio inicial era 20 que si era 150. En el primer caso supone un aumento del 50 %, mientras que en el segundo es una variación mucho menor en términos relativos. El ratio permite capturar esta diferencia.

`price_ratio_24` compara el precio reciente con la referencia de 24 periodos antes. En datos horarios, puede interpretarse como una relación frente al día anterior. Si el ratio es mayor que 1, el precio reciente es superior al de esa referencia. Si es menor que 1, es inferior. `price_ratio_168` ofrece una comparación similar frente a una referencia semanal.

Para evitar divisiones por cero, el programa reemplaza por valores ausentes los denominadores iguales a cero. Posteriormente, las filas con valores ausentes en variables de entrada se eliminan del dataset supervisado. Esta decisión evita generar infinitos o valores no numericos que podrían romper el entrenamiento.

Los ratios son complementarios a las diferencias. Las diferencias expresan variación absoluta; los ratios expresan variación relativa. Ambos puntos de vista pueden ser útiles. En mercados con precios muy cambiantes, una comparación relativa puede ayudar al modelo a distinguir entre movimientos proporcionalmente grandes y pequeños.

No obstante, los ratios pueden ser inestables cuando el denominador es muy bajo. Si el precio de referencia es cercano a cero, un cambio pequeño puede producir un ratio muy grande. Por ello, estas variables deben interpretarse con prudencia y no sustituyen a otras señales. Su valor reside en aportar una dimensión adicional al conjunto de entradas.

En modelos de boosting, los ratios pueden interactuar con variables de calendario y retardos. Por ejemplo, el modelo puede aprender que un ratio diario alto en una hora punta tiene implicaciones distintas a un ratio alto durante una madrugada. Esta capacidad de combinar variables es una de las razones por las que se incluyen múltiples familias de características.

### 8.9. Variables externas de generación renovable

La versión inicial del modelo aprende de calendario y precios históricos. Sin embargo, el precio eléctrico depende también de condiciones físicas del sistema. Por ello, el proyecto incorpora de forma opcional variables externas de generación renovable procedentes de ESIOS. Estas variables representan previsiones de eólica, solar fotovoltaica y solar térmica.

Las columnas externas principales son `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. La primera recoge la previsión eólica; la segunda, la previsión solar fotovoltaica; y la tercera, la previsión solar térmica. Todas se expresan en MWh y se alinean temporalmente con los datos de OMIE mediante `timestamp`.

La motivacion de estas variables es clara. La energía eólica y solar tienen costes variables bajos y pueden desplazar tecnologías más caras en el mercado diario. Cuando la generación renovable prevista es alta, el precio puede tender a bajar, especialmente en horas de demanda moderada. Cuando la renovable prevista es baja, el sistema puede necesitar tecnologías de mayor coste, lo que puede elevar el precio.

Estas variables permiten que el modelo diferencie situaciones que el calendario no distingue. Dos días con la misma hora, mismo mes y mismo día de la semana pueden tener precios distintos si uno presenta alta generación eólica y otro no. Del mismo modo, dos mediodías de primavera pueden comportarse de forma diferente según la previsión solar.

El uso de previsiones es importante porque respeta el contexto predictivo. Para predecir un precio futuro no debería utilizarse la generación real futura si no estaría disponible en el momento de la predicción. Las previsiones son una aproximación más coherente a la información que podría conocerse antes de la casación del mercado.

En la aplicación, las variables ESIOS son opcionales. Si el usuario no proporciona token, el modelo se entrena sin ellas. Si activa ESIOS, el sistema las descarga, las cachea y las incorpora automáticamente a la lista de variables de entrada. Esta flexibilidad permite comparar el rendimiento con y sin información externa.

La inclusión de variables renovables también tiene retos. Es necesario alinear correctamente las fechas, gestionar ausencias y evitar usar información futura. Además, la calidad de la previsión condiciona su utilidad. Si la previsión tiene errores relevantes, el modelo puede aprender relaciones menos precisas. Aun así, desde el punto de vista teórico, son variables muy adecuadas para mejorar la predicción.

### 8.10. Variables derivadas de eólica y solar

Además de las variables renovables directas, el proyecto genera variables derivadas que resumen la información de eólica y solar. Estas variables son `solar_forecast_mwh`, `renewable_forecast_mwh` y `wind_solar_ratio`. Su objetivo es ofrecer al modelo señales agregadas y relaciones entre tecnologías.

`solar_forecast_mwh` se calcula sumando `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. Esta variable representa la previsión solar total. Aunque la fotovoltaica y la térmica tienen características distintas, en muchos contextos resulta útil disponer de una medida agregada de energía solar prevista.

`renewable_forecast_mwh` suma la previsión eólica y la previsión solar total. Esta variable aproxima la cantidad de generación renovable variable esperada. No incluye todas las tecnologías renovables del sistema, como hidráulica o biomása, pero resume dos fuentes especialmente relevantes para el comportamiento horario del precio.

`wind_solar_ratio` divide la previsión eólica entre la previsión solar total. Esta variable describe la composición de la generación renovable prevista. No es lo mismo un escenario con alta eólica nocturna que uno con alta solar al mediodía. El ratio ayuda al modelo a diferenciar entre perfiles renovables distintos, incluso cuando la cantidad total sea similar.

Las variables derivadas pueden mejorar el aprendizaje porque reducen parte de la carga que tendría el modelo para descubrir relaciones por sí mismo. En lugar de esperar que el algoritmo combine siempre correctamente las columnas directas, se le proporcionan agregaciones con sentido físico. Esta técnica es habitual en ingeniería de variables: incorporar conocimiento del dominio en columnas numéricas.

Estas variables también facilitan la interpretación. Si un modelo mejora al incorporar `renewable_forecast_mwh`, se puede argumentar que la cantidad renovable prevista aporta información relevante. Si `wind_solar_ratio` resulta útil, puede indicar que la composición eólica/solar influye en el patrón de precios. Aunque el proyecto no realiza todavía análisis formal de importancia de variables, estas columnas preparan el terreno para hacerlo.

Debe tenerse en cuenta que las variables derivadas pueden introducir correlación con las variables originales. Por ejemplo, `solar_forecast_mwh` depende directamente de las dos variables solares. Esto no es necesariamente un problema para modelos de árboles o redes, pero en modelos lineales puede aumentar la colinealidad. La regresión Ridge ayuda a mitigar este riesgo mediante regularización.

En conjunto, la ingeniería de variables del proyecto combina conocimiento temporal, histórico de precios y señales renovables. Las variables de calendario capturan patrones estructurales; los retardos y ventanas móviles resumen la dinámica del precio; las diferencias y ratios describen cambios; y las variables ESIOS aportan contexto físico. Esta combinación permite que modelos relativamente sencillos trabajen con una representación rica del mercado eléctrico.
