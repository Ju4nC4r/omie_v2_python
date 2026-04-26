# Capitulo 8. Ingenieria de variables

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 8.1. Variables de calendario

La ingenieria de variables es una de las fases mas importantes en un proyecto de prediccion del precio electrico. Los modelos de aprendizaje automatico no trabajan directamente con el concepto abstracto de mercado, sino con columnas numericas construidas a partir de los datos disponibles. Por ello, la calidad de las variables influye de forma decisiva en la capacidad predictiva del sistema.

En este proyecto, la primera familia de variables procede del calendario. El precio electrico presenta patrones temporales claros: cambia segun la hora del dia, el dia de la semana, el mes y el tipo de jornada. Estos patrones no explican todo el comportamiento del mercado, pero proporcionan una base inicial muy relevante. Por ejemplo, una madrugada suele tener un perfil de demanda distinto al de una hora punta, y un domingo no se comporta igual que un dia laborable.

La columna `timestamp` permite extraer la informacion temporal necesaria. A partir de ella se obtiene la hora, el minuto, el dia de la semana y el mes. Estas variables capturan regularidades asociadas al consumo electrico y a la disponibilidad de generacion. En invierno y verano pueden aparecer comportamientos diferentes por calefaccion, refrigeracion o cambios de irradiacion solar. Del mismo modo, los dias laborables suelen presentar mayor actividad industrial y comercial que los fines de semana.

El proyecto conserva tambien la variable `period`, que indica la posicion de la observacion dentro del dia. Esta variable es especialmente util porque procede directamente del fichero OMIE y mantiene una relacion clara con la estructura del mercado. En datos horarios, `period` toma valores de 1 a 24. En datos cuarto-horarios, puede tomar valores de 1 a 96. Por tanto, ayuda al modelo a conocer donde se situa cada observacion dentro de la jornada.

Otra variable de calendario incluida es `is_weekend`. Esta columna vale 1 cuando la observacion corresponde a sabado o domingo, y 0 en caso contrario. Su objetivo es diferenciar dias con patrones de demanda diferentes. Aunque el dia de la semana ya se codifica mediante variables ciclicas, disponer de un indicador directo de fin de semana facilita al modelo capturar cambios bruscos entre dias laborables y no laborables.

Las variables de calendario tienen la ventaja de estar disponibles siempre. No dependen de APIs externas ni de descargas adicionales. Para realizar una inferencia futura, el sistema conoce de antemano la fecha y hora del periodo que quiere predecir. Esto las convierte en variables robustas y adecuadas para una primera version del modelo.

Sin embargo, estas variables tienen limitaciones. Saber que una observacion ocurre un martes a las 10:00 no informa por si solo sobre la demanda real, la generacion eolica, la disponibilidad nuclear o el precio del gas. Por tanto, las variables de calendario deben entenderse como una base estructural, no como una explicacion completa del precio. Su valor aumenta cuando se combinan con retardos del precio y variables externas.

### 8.2. Variables ciclicas de hora, dia y mes

Muchas variables temporales tienen naturaleza ciclica. La hora del dia no es una magnitud lineal simple: las 23:00 y las 00:00 estan cerca en el ciclo diario, aunque si se codifican como numeros 23 y 0 parezcan valores muy alejados. Lo mismo ocurre con los dias de la semana y con los meses del ano. Diciembre y enero son consecutivos, pero numericamente 12 y 1 estan separados por una distancia grande.

Para resolver este problema, el proyecto utiliza codificacion mediante seno y coseno. Esta tecnica transforma una variable ciclica en dos variables continuas que representan su posicion sobre una circunferencia. De esta manera, los extremos del ciclo quedan correctamente unidos. El modelo puede aprender que el final de un dia esta cerca del comienzo del siguiente, o que el final de una semana esta cerca del inicio de la siguiente.

En el caso de la hora y el minuto, el programa calcula primero `minute_of_day`, que representa los minutos transcurridos desde el inicio del dia. Despues genera `time_of_day_sin` y `time_of_day_cos` aplicando funciones trigonometricas sobre el ciclo completo de 1440 minutos. Esta representacion es mas precisa que usar solo la hora, ya que tambien distingue observaciones cuarto-horarias.

Ademas, se generan `hour_sin` y `hour_cos` a partir de la hora del dia. Aunque puede parecer redundante con `time_of_day_sin` y `time_of_day_cos`, ambas representaciones pueden aportar informacion complementaria. La variable basada en minuto del dia captura con mas detalle la posicion temporal, mientras que la hora resume el comportamiento horario tradicional.

Para el dia de la semana se calculan `dow_sin` y `dow_cos`. Estas variables codifican un ciclo de siete dias. Permiten representar diferencias entre lunes, martes, miercoles, jueves, viernes, sabado y domingo, manteniendo la continuidad entre domingo y lunes. Este tipo de codificacion es util porque el mercado electrico presenta perfiles semanales reconocibles.

Para el mes se calculan `month_sin` y `month_cos`. Estas variables representan el ciclo anual y permiten capturar estacionalidad. El precio electrico puede verse afectado por temperatura, demanda estacional, disponibilidad hidraulica, radiacion solar y patrones de consumo asociados a cada epoca del ano. Aunque el modelo no incorpora directamente meteorologia en esta version, el mes puede actuar como aproximacion parcial a factores estacionales.

La codificacion ciclica es especialmente beneficiosa para modelos lineales y redes neuronales. Si se usaran valores enteros sin transformar, el modelo podria interpretar relaciones artificiales entre numeros. Por ejemplo, podria considerar que diciembre esta mucho mas lejos de enero que de noviembre, cuando en realidad enero y diciembre son meses contiguos en el ciclo anual. Las variables seno/coseno reducen este problema.

En modelos basados en arboles, como HistGradientBoosting, la necesidad de codificacion ciclica puede ser menor, porque los arboles pueden dividir el espacio de variables por umbrales. Aun asi, mantener la misma representacion para todos los modelos permite compararlos con una matriz de entrada comun. Esta decision simplifica el pipeline y evita crear preparaciones distintas para cada algoritmo.

### 8.3. Retardos del precio electrico

Los retardos del precio son variables fundamentales en la prediccion de series temporales. Un retardo consiste en incluir como entrada el valor pasado de la variable que se quiere predecir. En este proyecto, la variable objetivo es `marginal_es`, y los retardos se construyen desplazando esa columna hacia atras distintos numeros de periodos.

El precio electrico presenta dependencia temporal. El precio de un periodo no suele ser completamente independiente del precio anterior. Las condiciones que influyen en el mercado, como demanda, disponibilidad de generacion o contexto de combustibles, tienden a persistir durante varias horas o dias. Por ello, conocer precios recientes aporta informacion relevante para estimar precios futuros.

El proyecto utiliza los retardos `1`, `2`, `3`, `4`, `5`, `6`, `12`, `23`, `24`, `25`, `48`, `72`, `168` y `336`. Los retardos cortos capturan continuidad inmediata. Por ejemplo, `price_lag_1` recoge el precio del periodo inmediatamente anterior y `price_lag_2` el de dos periodos antes. Estos valores ayudan al modelo a detectar tendencias recientes o cambios suaves.

Los retardos intermedios, como `12`, `23`, `24` y `25`, buscan capturar patrones diarios. En datos horarios, `price_lag_24` aproxima el precio del mismo periodo del dia anterior. Los retardos `23` y `25` rodean ese punto y permiten al modelo observar pequenas variaciones alrededor del ciclo diario. Esta estrategia es util porque los perfiles de precio suelen repetirse parcialmente de un dia a otro.

Los retardos mas largos, como `168` y `336`, capturan patrones semanales. En datos horarios, 168 periodos equivalen a una semana, y 336 a dos semanas. Esto permite comparar una observacion con el mismo momento de semanas anteriores. La demanda y el comportamiento del mercado pueden tener regularidades semanales, por lo que estos retardos aportan contexto de mas largo plazo.

Es importante recordar que el significado temporal exacto de un retardo depende de la resolucion de los datos. En datos horarios, un retardo de 24 periodos equivale a un dia. En datos cuarto-horarios, equivale a seis horas. El proyecto documenta esta limitacion y mantiene una implementacion basada en periodos. En futuras versiones se podria mejorar calculando retardos por duracion real, por ejemplo 24 horas o 7 dias.

Los retardos tienen una ventaja importante: se obtienen exclusivamente de datos historicos del precio. No requieren fuentes externas y estan disponibles siempre que exista suficiente historico. Sin embargo, tambien tienen una limitacion: si el mercado cambia bruscamente por un evento externo no reflejado en precios pasados, los retardos pueden no anticipar correctamente el nuevo comportamiento.

Para evitar fuga de informacion, cada retardo se calcula usando valores anteriores al periodo objetivo. El modelo no recibe el precio que intenta predecir, sino precios ya observados. Esta disciplina temporal es esencial para que la evaluacion sea realista. Una variable mal desplazada podria introducir el valor futuro en el entrenamiento y generar metricas artificialmente buenas.

### 8.4. Medias moviles

Las medias moviles resumen el nivel reciente del precio. En lugar de proporcionar al modelo un unico valor pasado, calculan el promedio de una ventana de observaciones anteriores. Esto suaviza fluctuaciones puntuales y permite capturar el contexto general del mercado en distintos horizontes temporales.

El proyecto calcula medias moviles para ventanas de `3`, `6`, `12`, `24`, `48` y `168` periodos. Las ventanas cortas reflejan el comportamiento reciente. Por ejemplo, una media de 3 o 6 periodos indica si el precio acaba de subir o bajar en el entorno inmediato. Las ventanas de 24 y 48 periodos aproximan el nivel de uno o dos dias en datos horarios. La ventana de 168 periodos resume aproximadamente una semana horaria.

Estas variables ayudan al modelo a diferenciar entre precios aislados y tendencias sostenidas. Un precio alto en el periodo anterior puede tener interpretaciones distintas si la media reciente tambien es alta o si se trata de un pico puntual. La media movil proporciona contexto y reduce la sensibilidad a valores extremos aislados.

Las medias moviles se calculan sobre `shifted_price`, es decir, sobre el precio desplazado un periodo. Esta decision evita que la media de una fila incluya el precio objetivo de esa misma fila. Si se usara directamente la serie sin desplazar, la media movil podria contener informacion del valor que se quiere predecir, generando fuga de informacion futura.

El uso de varias ventanas permite capturar dinamicas a distintas escalas. El mercado electrico puede tener movimientos de corto plazo asociados a una hora concreta, pero tambien tendencias de varios dias. Un modelo puede aprender que una subida reciente es mas relevante cuando coincide con una media semanal alta, o que un precio bajo es mas probable si las medias de varias ventanas estan descendiendo.

Las medias moviles son especialmente utiles para modelos lineales, porque convierten patrones temporales en variables tabulares. En lugar de exigir al modelo que deduzca la tendencia desde muchos retardos individuales, se le ofrece una medida ya resumida. Tambien pueden beneficiar a modelos de arboles y redes neuronales, al aportar senales estables.

La principal limitacion es que las medias moviles necesitan historico suficiente. Las primeras filas del dataset no pueden tener una media de 168 periodos si todavia no existen 168 observaciones previas. Por ello, estas filas se eliminan durante la construccion del dataset supervisado. Este coste es asumible cuando se entrena con rangos amplios.

### 8.5. Desviaciones moviles

Ademas del nivel medio, es importante representar la volatilidad reciente. La desviacion movil mide cuanto se han alejado los precios de su media dentro de una ventana temporal. En el mercado electrico, la volatilidad es una caracteristica relevante: periodos con precios estables no se comportan igual que periodos con cambios bruscos o picos frecuentes.

El proyecto calcula desviaciones moviles para las mismas ventanas que las medias: `3`, `6`, `12`, `24`, `48` y `168` periodos. De este modo, el modelo recibe informacion sobre volatilidad a corto, medio y largo plazo. Una desviacion alta puede indicar incertidumbre, transicion de regimen o presencia reciente de precios extremos.

Por ejemplo, si la media de las ultimas 24 observaciones es moderada pero la desviacion es alta, significa que el precio ha oscilado mucho. En cambio, una media similar con desviacion baja indica estabilidad. Estos dos contextos pueden llevar a predicciones distintas, aunque el nivel promedio sea parecido.

La desviacion movil puede ayudar especialmente en episodios de mercado tensionado. Cuando el sistema alterna entre horas baratas y horas caras, la media por si sola puede ocultar esa variabilidad. La desviacion aporta una medida complementaria que permite al modelo detectar comportamientos irregulares.

Igual que las medias, las desviaciones se calculan sobre el precio desplazado un periodo. Esto mantiene la coherencia temporal y evita utilizar el valor objetivo dentro de la variable explicativa. La prevencion de fuga de informacion es una regla constante en toda la ingenieria de variables.

Las desviaciones tambien tienen limitaciones. En ventanas muy cortas pueden ser ruidosas, y en ventanas largas pueden reaccionar lentamente a cambios recientes. Por eso se incluyen varias escalas. El modelo decide durante el entrenamiento que ventanas son mas utiles para reducir el error.

En modelos lineales, la desviacion movil introduce una aproximacion sencilla a la volatilidad. En modelos no lineales, puede interactuar con otras variables. Por ejemplo, el impacto de un retardo alto puede ser diferente si la volatilidad reciente tambien es alta. Esta clase de interacciones es una de las razones para incluir modelos como HistGradientBoosting.

### 8.6. Minimos y maximos recientes

Los minimos y maximos moviles permiten describir el rango reciente del precio. Mientras que la media resume el nivel central y la desviacion mide dispersion, los minimos y maximos indican los extremos observados en una ventana temporal. En mercados electricos, los extremos son importantes porque los picos de precio y los precios muy bajos tienen gran significado economico.

El proyecto calcula `price_roll_24_min`, `price_roll_24_max`, `price_roll_168_min` y `price_roll_168_max`. Estas variables representan el minimo y maximo de las ultimas 24 y 168 observaciones, siempre usando precios anteriores al objetivo. En datos horarios, estas ventanas aproximan un dia y una semana.

El minimo reciente puede ser informativo en periodos con abundante generacion renovable o baja demanda. Si el precio ha alcanzado niveles muy bajos en las ultimas horas, el modelo puede interpretar que existe un contexto de mercado barato. El maximo reciente, por el contrario, puede indicar tension, demanda elevada o entrada de tecnologias caras.

El rango formado por minimo y maximo tambien aporta informacion indirecta sobre amplitud de precios. Dos periodos pueden tener la misma media reciente, pero uno puede haber oscilado entre valores muy bajos y muy altos, mientras que otro se ha mantenido estable. Los extremos ayudan a distinguir esos contextos.

Estas variables son sencillas de calcular y faciles de interpretar. Un analista puede entender rapidamente que significa el maximo de las ultimas 24 observaciones. Esta interpretabilidad es valiosa en un TFG, porque permite explicar como se transforma la serie original antes de entrenar los modelos.

Los minimos y maximos tambien pueden ayudar a los modelos basados en arboles, que son buenos detectando umbrales. Por ejemplo, el modelo puede aprender reglas del tipo: si el maximo reciente supera cierto valor y la hora corresponde a una franja punta, el precio esperado puede ser mas alto. Aunque el modelo no se exprese asi literalmente en el documento, esa es la intuicion que justifica estas variables.

La limitacion principal es que los extremos pueden estar afectados por valores atipicos. Un unico pico muy alto puede mantener elevado el maximo movil durante toda la ventana, aunque el mercado ya haya vuelto a la normalidad. Por eso no se utilizan solos, sino combinados con medias, desviaciones, retardos y variables de calendario.

### 8.7. Diferencias frente a periodos anteriores

Las diferencias entre precios retardados permiten representar cambios recientes. En lugar de mirar solo el nivel absoluto del precio, el modelo recibe informacion sobre si el precio esta subiendo o bajando respecto a referencias anteriores. Esto es importante porque la direccion del cambio puede contener informacion predictiva.

El proyecto calcula tres diferencias principales: `price_diff_1`, `price_diff_24` y `price_diff_168`. La primera compara el ultimo precio disponible con el precio de dos periodos atras. En la practica, mide la variacion mas inmediata. Si `price_diff_1` es positiva, el precio acaba de subir; si es negativa, acaba de bajar.

La diferencia `price_diff_24` compara el ultimo precio disponible con el precio de 24 periodos antes. En datos horarios, esto aproxima la diferencia frente al mismo entorno del dia anterior. Esta variable ayuda a detectar si el mercado esta mas caro o mas barato que en la jornada previa.

La diferencia `price_diff_168` compara el ultimo precio disponible con el precio de 168 periodos antes. En datos horarios, esta referencia equivale aproximadamente a una semana. Puede capturar cambios semanales, como una subida general de precios respecto a la semana anterior o una caida asociada a condiciones renovables favorables.

Las diferencias son utiles porque eliminan parcialmente el nivel base y se centran en la variacion. Por ejemplo, un precio de 80 EUR/MWh puede ser alto o bajo dependiendo del contexto. Si ayer a la misma hora el precio era 40, indica una subida notable. Si era 120, indica una bajada. La diferencia aporta esa perspectiva relativa.

Estas variables tambien pueden ayudar a detectar cambios de regimen. Una sucesion de diferencias positivas puede sugerir una tendencia alcista; diferencias negativas pueden indicar relajacion del mercado. Aunque el modelo no usa una secuencia explicita como una red recurrente, estas variables tabulares resumen parte de esa dinamica.

Como en el resto de variables historicas, las diferencias se calculan exclusivamente con retardos. No utilizan el precio presente que se quiere predecir. Esto mantiene la validez temporal del dataset y evita sobreestimar el rendimiento.

Una limitacion de las diferencias es que pueden amplificar ruido cuando los precios fluctuan mucho. Por eso se combinan con medias y desviaciones moviles. Mientras las diferencias capturan cambios puntuales, las medias y desviaciones ofrecen contexto sobre si esos cambios son aislados o forman parte de una dinamica mas amplia.

### 8.8. Ratios temporales

Los ratios temporales comparan el precio reciente con precios de referencia anteriores mediante una relacion proporcional. En el proyecto se calculan `price_ratio_24` y `price_ratio_168`. Estos ratios dividen el ultimo precio disponible entre el precio de 24 o 168 periodos antes, respectivamente.

La ventaja de un ratio es que expresa cambios relativos. Una subida de 10 EUR/MWh no tiene el mismo significado si el precio inicial era 20 que si era 150. En el primer caso supone un aumento del 50 %, mientras que en el segundo es una variacion mucho menor en terminos relativos. El ratio permite capturar esta diferencia.

`price_ratio_24` compara el precio reciente con la referencia de 24 periodos antes. En datos horarios, puede interpretarse como una relacion frente al dia anterior. Si el ratio es mayor que 1, el precio reciente es superior al de esa referencia. Si es menor que 1, es inferior. `price_ratio_168` ofrece una comparacion similar frente a una referencia semanal.

Para evitar divisiones por cero, el programa reemplaza por valores ausentes los denominadores iguales a cero. Posteriormente, las filas con valores ausentes en variables de entrada se eliminan del dataset supervisado. Esta decision evita generar infinitos o valores no numericos que podrian romper el entrenamiento.

Los ratios son complementarios a las diferencias. Las diferencias expresan variacion absoluta; los ratios expresan variacion relativa. Ambos puntos de vista pueden ser utiles. En mercados con precios muy cambiantes, una comparacion relativa puede ayudar al modelo a distinguir entre movimientos proporcionalmente grandes y pequenos.

No obstante, los ratios pueden ser inestables cuando el denominador es muy bajo. Si el precio de referencia es cercano a cero, un cambio pequeno puede producir un ratio muy grande. Por ello, estas variables deben interpretarse con prudencia y no sustituyen a otras senales. Su valor reside en aportar una dimension adicional al conjunto de entradas.

En modelos de boosting, los ratios pueden interactuar con variables de calendario y retardos. Por ejemplo, el modelo puede aprender que un ratio diario alto en una hora punta tiene implicaciones distintas a un ratio alto durante una madrugada. Esta capacidad de combinar variables es una de las razones por las que se incluyen multiples familias de caracteristicas.

### 8.9. Variables externas de generacion renovable

La version inicial del modelo aprende de calendario y precios historicos. Sin embargo, el precio electrico depende tambien de condiciones fisicas del sistema. Por ello, el proyecto incorpora de forma opcional variables externas de generacion renovable procedentes de ESIOS. Estas variables representan previsiones de eolica, solar fotovoltaica y solar termica.

Las columnas externas principales son `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. La primera recoge la prevision eolica; la segunda, la prevision solar fotovoltaica; y la tercera, la prevision solar termica. Todas se expresan en MWh y se alinean temporalmente con los datos de OMIE mediante `timestamp`.

La motivacion de estas variables es clara. La energia eolica y solar tienen costes variables bajos y pueden desplazar tecnologias mas caras en el mercado diario. Cuando la generacion renovable prevista es alta, el precio puede tender a bajar, especialmente en horas de demanda moderada. Cuando la renovable prevista es baja, el sistema puede necesitar tecnologias de mayor coste, lo que puede elevar el precio.

Estas variables permiten que el modelo diferencie situaciones que el calendario no distingue. Dos dias con la misma hora, mismo mes y mismo dia de la semana pueden tener precios distintos si uno presenta alta generacion eolica y otro no. Del mismo modo, dos mediodias de primavera pueden comportarse de forma diferente segun la prevision solar.

El uso de previsiones es importante porque respeta el contexto predictivo. Para predecir un precio futuro no deberia utilizarse la generacion real futura si no estaria disponible en el momento de la prediccion. Las previsiones son una aproximacion mas coherente a la informacion que podria conocerse antes de la casacion del mercado.

En la aplicacion, las variables ESIOS son opcionales. Si el usuario no proporciona token, el modelo se entrena sin ellas. Si activa ESIOS, el sistema las descarga, las cachea y las incorpora automaticamente a la lista de variables de entrada. Esta flexibilidad permite comparar el rendimiento con y sin informacion externa.

La inclusion de variables renovables tambien tiene retos. Es necesario alinear correctamente las fechas, gestionar ausencias y evitar usar informacion futura. Ademas, la calidad de la prevision condiciona su utilidad. Si la prevision tiene errores relevantes, el modelo puede aprender relaciones menos precisas. Aun asi, desde el punto de vista teorico, son variables muy adecuadas para mejorar la prediccion.

### 8.10. Variables derivadas de eolica y solar

Ademas de las variables renovables directas, el proyecto genera variables derivadas que resumen la informacion de eolica y solar. Estas variables son `solar_forecast_mwh`, `renewable_forecast_mwh` y `wind_solar_ratio`. Su objetivo es ofrecer al modelo senales agregadas y relaciones entre tecnologias.

`solar_forecast_mwh` se calcula sumando `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh`. Esta variable representa la prevision solar total. Aunque la fotovoltaica y la termica tienen caracteristicas distintas, en muchos contextos resulta util disponer de una medida agregada de energia solar prevista.

`renewable_forecast_mwh` suma la prevision eolica y la prevision solar total. Esta variable aproxima la cantidad de generacion renovable variable esperada. No incluye todas las tecnologias renovables del sistema, como hidraulica o biomasa, pero resume dos fuentes especialmente relevantes para el comportamiento horario del precio.

`wind_solar_ratio` divide la prevision eolica entre la prevision solar total. Esta variable describe la composicion de la generacion renovable prevista. No es lo mismo un escenario con alta eolica nocturna que uno con alta solar al mediodia. El ratio ayuda al modelo a diferenciar entre perfiles renovables distintos, incluso cuando la cantidad total sea similar.

Las variables derivadas pueden mejorar el aprendizaje porque reducen parte de la carga que tendria el modelo para descubrir relaciones por si mismo. En lugar de esperar que el algoritmo combine siempre correctamente las columnas directas, se le proporcionan agregaciones con sentido fisico. Esta tecnica es habitual en ingenieria de variables: incorporar conocimiento del dominio en columnas numericas.

Estas variables tambien facilitan la interpretacion. Si un modelo mejora al incorporar `renewable_forecast_mwh`, se puede argumentar que la cantidad renovable prevista aporta informacion relevante. Si `wind_solar_ratio` resulta util, puede indicar que la composicion eolica/solar influye en el patron de precios. Aunque el proyecto no realiza todavia analisis formal de importancia de variables, estas columnas preparan el terreno para hacerlo.

Debe tenerse en cuenta que las variables derivadas pueden introducir correlacion con las variables originales. Por ejemplo, `solar_forecast_mwh` depende directamente de las dos variables solares. Esto no es necesariamente un problema para modelos de arboles o redes, pero en modelos lineales puede aumentar la colinealidad. La regresion Ridge ayuda a mitigar este riesgo mediante regularizacion.

En conjunto, la ingenieria de variables del proyecto combina conocimiento temporal, historico de precios y senales renovables. Las variables de calendario capturan patrones estructurales; los retardos y ventanas moviles resumen la dinamica del precio; las diferencias y ratios describen cambios; y las variables ESIOS aportan contexto fisico. Esta combinacion permite que modelos relativamente sencillos trabajen con una representacion rica del mercado electrico.
