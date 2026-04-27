# Capítulo 5. Estado del arte

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 5.1. Modelos estadísticos clásicos para predicción de precios

La predicción del precio eléctrico ha sido estudiada durante décadas desde enfoques estadísticos, econométricos y computacionales. Antes de la expansión del aprendizaje automático moderno, los métodos clásicos de series temporales fueron la herramienta principal para modelar precios, demanda y generación. Estos métodos siguen siendo relevantes porque proporcionan una base conceptual sólida, son interpretables y permiten establecer líneas de comparación frente a modelos más complejos.

Uno de los enfoques tradicionales más utilizados es el basado en modelos autorregresivos. En un modelo autorregresivo, el valor actual de una serie se explica a partir de valores pasados de la misma serie. En el contexto del mercado eléctrico, esto significa que el precio de un periodo puede depender del precio observado en periodos anteriores. Esta idea encaja bien con el comportamiento del precio eléctrico, que suele mostrar continuidad temporal: las condiciones de mercado de una hora no son completamente independientes de las horas previas.

Los modelos AR, ARMA y ARIMA han sido ampliamente utilizados en problemas de predicción de series temporales. Los modelos AR capturan dependencias autorregresivas; los modelos MA incorporan componentes de media móvil sobre errores pasados; y los modelos ARIMA incluyen diferenciacion para tratar series no estacionarias. En mercados eléctricos, la no estacionariedad aparece por cambios en demanda, combustible, regulacion, penetración renovable o estructura del mercado. Por ello, la estacionariedad es una cuestión importante en los modelos clásicos.

También existen variantes estacionales como SARIMA, que permiten modelar patrones repetitivos. En el precio eléctrico, la estacionalidad es especialmente importante. Existen ciclos diarios, semanales y anuales. El comportamiento de una hora nocturna no es el mismo que el de una hora punta; un sábado no se comporta igual que un martes laborable; y los meses de verano e invierno presentan condiciones distintas. Los modelos estacionales intentan representar estas regularidades de forma explícita.

Otra familia clasíca son los modelos de suavizado exponencial. Estos métodos asignan mayor peso a observaciones recientes y menor peso a observaciones antiguas. Son útiles cuando la serie presenta tendencias o cambios progresivos. Sin embargo, pueden resultar limitados cuando el precio eléctrico muestra saltos bruscos, episodios de precios muy altos, precios cercanos a cero o cambios no lineales causados por renovables y combustibles.

Los modelos de regresión lineal también han sido utilizados para explicar el precio eléctrico mediante variables externas. Por ejemplo, pueden incluirse demanda prevista, generación eólica, generación solar, temperatura, precio del gas o precio del CO2. La principal ventaja de estos modelos es su interpretabilidad. Cada coeficiente indica la relación aproximada entre una variable explicativa y el precio objetivo. No obstante, la relación real entre variables y precio suele ser no lineal, por lo que la regresión lineal puede quedarse corta si no se enriquecen las variables.

La regresión Ridge, utilizada en este proyecto, puede considerarse una extensión regularizada de la regresión lineal. Su objetivo es ajustar un modelo lineal evitando que los coeficientes crezcan demasiado. Esto resulta útil cuando se generan muchas variables a partir de calendarios, retardos y medias móviles. La regularización reduce el riesgo de sobreajuste y mejora la estabilidad del modelo. Aunque Ridge no captura relaciones no lineales complejas por sí misma, puede ofrecer resultados competitivos cuando las variables están bien disenadas.

Los modelos estadísticos clásicos presentan ventajas importantes. Son relativamente sencillos, rápidos de entrenar, interpretables y fáciles de reproducir. Permiten entender patrones básicos de la serie y ofrecen un punto de partida razonable. Además, en problemas donde los datos son limitados, un modelo sencillo puede generalizar mejor que un modelo muy flexible.

Sin embargo, los precios eléctricos presentan características que dificultan el usó exclusivo de métodos clásicos. La serie puede contener picos extremos, cambios estructurales, influencia meteorológica, efectos regulatorios, saturación renovable, restricciones de red e interacción entre mercados. Muchos de estos elementos generan relaciones no lineales y dependencias complejas. Por está razón, los enfoques modernos suelen combinar variables de calendario, histórico de precios y variables externas con técnicas de aprendizaje automático.

En el marco de este trabajo, los modelos clásicos se entienden como referencia metodológica. La idea de usar retardos, ciclos y medias móviles procede directamente del análisis de series temporales. Aunque la aplicación no implementa modelos ARIMA completos, si incorpora su intuición principal: el pasado contiene información relevante para anticipar el futuro. Esta aproximación permite construir un sistema sencillo, reproducible y extensible.

### 5.2. Modelos de machine learning aplicados a energía

El aprendizaje automático ha adquirido un papel cada vez más importante en la predicción energética. A diferencia de los modelos estadísticos tradicionales, los modelos de machine learning no requieren especificar de forma tan rigida la relación entre entradas y salida. En lugar de imponer una ecuacion concreta, aprenden patrones a partir de datos históricos. Esto los hace atractivos para mercados eléctricos, donde el precio depende de muchas variables que interactuan entre si.

En el ámbito energético, el machine learning se utiliza para predecir demanda, generación renovable, precios de mercado, consumo de edificios, pérdidas en redes, indisponibilidades y otros fenómenos. La disponibilidad de datos públicos, sensores, sistemas de información y APIs ha facilitado el desarrollo de modelos cada vez más ricos. En el caso español, fuentes como OMIE y ESIOS permiten construir datasets con información de mercado y sistema.

Los modelos supervisados son los más habituales para la predicción de precios. En este enfoque se dispone de ejemplos históricos formados por variables de entrada y una variable objetivo. En este proyecto, las entradas incluyen calendario, variables cíclicas, retardos del precio, estadísticos móviles y, opcionalmente, previsiones renovables. La salida es el precio marginal español del mercado diario.

Entre los modelos de machine learning aplicados a energía se encuentran la regresión lineal regularizada, los árboles de decisión, los random forests, los métodos de boosting, las máquinas de vectores soporte y las redes neuronales. Cada familia tiene fortalezas y limitaciones. La elección depende del tamaño del dataset, la calidad de las variables, la necesidad de interpretabilidad, el coste computacional y el objetivo del sistema.

Los árboles de decisión permiten dividir el espacio de variables en regiones. Por ejemplo, un árbol puede aprender que determinados rangos de hora, demanda o generación renovable se asocian a precios diferentes. Su interpretación es intuitiva, pero un único árbol puede sobreajustar fácilmente. Por ello, en la práctica se suelen utilizar conjuntos de árboles, como random forests o gradient boosting.

Los random forests combinan muchos árboles entrenados sobre subconjuntos de datos y variables. Suelen ser robustos y capturan no linealidades, pero pueden resultar menos precisos que boosting en algunos problemas tabulares y generar modelos de mayor tamaño. Los métodos de boosting, en cambio, construyen modelos de forma secuencial: cada nuevo árbol intenta corregir errores de los anteriores. Esta estrategia suele lograr muy buen rendimiento en datos tabulares.

Las máquinas de vectores soporte han sido utilizadas en series temporales energéticas por su capacidad para modelar relaciones no lineales mediante kernels. No obstante, pueden ser costosas en datasets grandes y requieren una selección cuidadosa de hiperparámetros. En problemas prácticos, su usó puede ser menos directo que otros modelos disponibles en bibliotecas como scikit-learn.

Una cuestión esencial en machine learning aplicado a energía es la ingeniería de variables. El modelo no observa directamente el funcionamiento físico del sistema, sino las variables que se le proporcionan. Por tanto, el rendimiento depende en gran medida de la calidad de esas variables. Incluir hora, día, mes, fines de semana, retardos, medias móviles y renovables puede marcar una diferencia notable.

También es fundamental respetar la naturaleza temporal de los datos. En un problema de predicción real, el modelo no debe usar información futura para predecir el pasado. Por ello, la división entre entrenamiento y validación debe hacerse temporalmente. El proyecto adopta esta idea: se entrena con la parte inicial del periodo y se valida con la parte final. Esta metodología es más realista que mezclar aleatoriamente observaciones de distintos días.

Los modelos de machine learning ofrecen ventajas claras: pueden capturar no linealidades, combinar muchas variables, adaptarse a distintos contextos y mejorar con más datos. Sin embargo, también presentan riesgos. Un modelo demasiado complejo puede aprender ruido histórico y fallar en datos nuevos. Además, los resultados pueden degradarse si cambia la estructura del mercado, si faltan variables importantes o si se produce un evento excepcional no representado en el entrenamiento.

En este trabajo, el machine learning se aplica con un enfoque práctico e incremental. Primero se construye un modelo pequeño basado en histórico y calendario. Después se incorporan modelos alternativos y variables renovables opcionales. Esta progresion permite entender qué aporta cada mejora y evita depender desde el principio de una arquitectura excesivamente compleja.

### 5.3. Redes neuronales en predicción de series temporales

Las redes neuronales son una de las familias más conocidas dentro del aprendizaje automático. Su popularidad se debe a su capacidad para aproximar relaciones no lineales complejas. En predicción de precios eléctricos, las redes neuronales han sido empleadas para capturar patrones horarios, dependencias temporales, interacciones entre variables y comportamientos difíciles de representar con modelos lineales.

Una red neuronal artificial esta formada por capas de neuronas conectadas mediante pesos. Durante el entrenamiento, el modelo ajusta esos pesos para reducir el error entre sus predicciones y los valores reales. En problemas de regresión, como la predicción de precios, la salida de la red es un valor numérico continuo. El aprendizaje se realiza normalmente mediante algoritmos de optimización que minimizan una función de pérdida.

El tipo de red más sencillo es el perceptrón multicapa, conocido como MLP. Este modelo esta formado por una capa de entrada, una o varias capas ocultas y una capa de salida. Las capas ocultas aplican transformaciones no lineales que permiten aprender relaciones más flexibles que una regresión lineal. El proyecto incorpora `MLPRegressor`, una implementación de scikit-learn de este tipo de red.

El MLP puede funcionar bien con variables tabulares generadas previamente. En este caso, la red no recibe una secuencia completa como tal, sino un conjunto de variables que resumen información temporal: hora, día, retardos, medias móviles, diferencias y previsiones renovables. Esta estrategia reduce la complejidad de la red y permite trabajar con una arquitectura sencilla.

En predicción de series temporales también se han utilizado redes recurrentes, como RNN, LSTM y GRU. Estas arquitecturas están disenadas para procesar secuencias y mantener memoria de estados anteriores. Las LSTM, en particular, fueron muy populares para problemas donde era necesario aprender dependencias a largo plazo. En el mercado eléctrico podrían utilizarse para modelar secuencias de precios, demanda y generación.

Más recientemente, también se han aplicado arquitecturas basadas en atencion y Transformers a series temporales. Estos modelos pueden capturar relaciones entre distintos puntos temporales sin depender exclusivamente de una recurrencia secuencial. Sin embargo, suelen requerir más datos, más potencia computacional y una configuración más compleja. Para un Proyecto centrado en una aplicación local y reproducible, pueden resultar excesivos como primera aproximación.

Las redes neuronales tienen la ventaja de ser flexibles. Pueden combinar muchas variables y aprender relaciones no lineales. No obstante, presentan varias dificultades. La primera es la sensibilidad a hiperparámetros: número de capas, número de neuronas, función de activación, tasa de aprendizaje, regularización y número de iteraciones. La segunda es el riesgo de sobreajuste, especialmente cuando el dataset no es muy grande. La tercera es la menor interpretabilidad frente a modelos lineales.

En mercados eléctricos, las redes neuronales pueden cometer errores importantes si el periodo de entrenamiento no contiene situaciones similares a las que se quieren predecir. Por ejemplo, si cambian los precios del gas, la estructura de demanda o la penetración renovable, la red puede extrapolar mal. Por ello, aunque una red neuronal pueda mejorar la precisión, no elimina la necesidad de buenas variables, validación temporal y análisis de errores.

En el proyecto desarrollado, la red neuronal se ha incluido como uno de los modelos seleccionables desde la interfaz gráfica. Esto permite al usuario comparar su comportamiento con Ridge y con HistGradientBoosting. El objetivo no es afirmar que la red neuronal sea siempre el mejor modelo, sino ofrecer una alternativa no lineal y evaluarla de forma objetiva mediante métricas.

La decisión de utilizar `MLPRegressor` es coherente con el enfoque didáctico del proyecto. Es suficientemente sencilla para ejecutarse en un entorno local, se integra bien con scikit-learn y permite mostrar los fundamentos del entrenamiento neuronal. Al mismo tiempo, deja abierta la posibilidad de evolucionar hacia arquitecturas más específicas de series temporales en trabajos futuros.

### 5.4. Modelos basados en árboles y boosting

Los modelos basados en árboles son especialmente relevantes en datos tabulares. A diferencia de las redes neuronales, que requieren ajustar pesos en capas, los árboles dividen el espacio de variables mediante reglas. Estas reglas pueden capturar interacciones no lineales de forma natural. Por ejemplo, el modelo puede aprender que una misma cantidad de generación solar tiene efectos distintos según la hora del día, el día de la semana o el nivel de precio previo.

Un árbol de decisión por sí solo puede ser fácil de interpretar, pero también tiende a sobreajustar. Si se deja crecer demasiado, puede memorizar patrones específicos del entrenamiento que no se repiten en validación. Para superar esta limitación se utilizan métodos de conjunto, que combinan muchos árboles. Dentro de estos métodos destacan random forest y gradient boosting.

El gradient boosting construye árboles de manera secuencial. El primer árbol realiza una predicción inicial; los siguientes intentan corregir los errores residuales de los anteriores. De esta forma, el modelo va refinando la predicción paso a paso. Este enfoque ha demostrado un rendimiento muy alto en numerosos problemas de datos estructurados, incluyendo predicción energética.

El proyecto incorpora `HistGradientBoostingRegressor`, una implementación eficiente de scikit-learn basada en histogramas. Esta variante agrupa valores continuós en bins, lo que permite acelerar el entrenamiento y manejar datasets de tamaño medio con buen rendimiento. En las pruebas realizadas con datos amplios de 2025, este modelo fue seleccionado como mejor alternativa en modo automático, con métricas superiores a los modelos más simples.

Los modelos de boosting presentan varias ventajas. Capturan no linealidades, manejan interacciones entre variables y suelen funcionar bien sin necesidad de escalar todas las entradas. Además, son adecuados cuando se dispone de muchas variables derivadas, como retardos, medias móviles, diferencias y señales de calendario. Esto encaja bien con la estructura del dataset construido en el proyecto.

Otra ventaja de los árboles es que pueden trabajar con relaciones por tramos. El precio eléctrico no siempre responde de forma continúa y lineal a una variable. Puede haber umbrales: por ejemplo, a partir de cierto nivel de generación renovable el precio baja de manera más marcada; o en ciertas horas punta el efecto de la demanda se amplifica. Los árboles pueden representar este tipo de comportamiento mediante divisiones sucesivas.

Sin embargo, los modelos de boosting también requieren cuidado. Si se configuran con demasiada complejidad, pueden sobreajustar. Parámetros como profundidad, número de iteraciones, tasa de aprendizaje, regularización y número mínimo de observaciones por hoja influyen en el resultado. Aunque scikit-learn ofrece valores por defecto razonables, un estudio más avanzado podría incorporar búsqueda de hiperparámetros.

Otra limitación es la interpretabilidad. Aunque un modelo de árbol puede explicarse fácilmente, un conjunto de muchos árboles es más difícil de interpretar de forma directa. Existen técnicas para estimar importancia de variables, dependencias parciales o explicaciones locales, pero no forman parte del alcance principal de este proyecto. Aun así, el rendimiento práctico de boosting justifica su inclusión.

En comparación con una red neuronal, HistGradientBoosting puede ser más estable en datasets tabulares pequeños o medianos. También suele requerir menos ajuste inicial. En comparación con Ridge, puede capturar relaciones no lineales que el modelo lineal no representa. Por ello, constituye una alternativa muy adecuada para el problema de predicción del precio eléctrico.

Dentro de la aplicación práctica, el usuario puede seleccionar manualmente este modelo o dejar que el modo `auto` lo compare con Ridge y MLP. Esta opción refuerza el carácter experimental del proyecto: no se presupone un ganador, sino que se evalúa cada modelo bajo las mismas condiciones de datos y validación.

### 5.5. Comparación de enfoques existentes

La literatura y la práctica muestran que no existe un único modelo universalmente superior para la predicción de precios eléctricos. El rendimiento depende del mercado, el horizonte de predicción, las variables disponibles, la resolución temporal, el periodo histórico y los criterios de evaluación. Por ello, una buena metodología debe comparar varios enfoques en igualdad de condiciones.

Los modelos estadísticos clásicos destacan por su simplicidad e interpretabilidad. Son adecuados para establecer líneas base y entender componentes temporales. Pueden funcionar razonablemente bien cuando los patrones son estables, pero tienden a ser limitados ante relaciones no lineales o cambios bruscos. Su mayor valor en este trabajo es conceptual: inspirán el uso de retardos y variables temporales.

Los modelos lineales regularizados, como Ridge, representan un equilibrio entre sencillez y robustez. Son rápidos, reproducibles y menos propensos al sobreajuste que una regresión lineal sin regularización. Funciónan especialmente bien cuando se dispone de variables bien construidas. No obstante, su estructura lineal limita la capacidad para capturar interacciones complejas.

Las redes neuronales aportan flexibilidad y capacidad no lineal. Pueden mejorar resultados si hay suficientes datos y una configuración adecuada. Sin embargo, son más sensibles a hiperparámetros, pueden tardar más en entrenar y son menos interpretables. En un entorno didáctico, su inclusión permite mostrar como se comporta un modelo neuronal frente a alternativas más clasícas.

Los modelos basados en boosting suelen obtener muy buenos resultados en datos tabulares. Capturan interacciones, no requieren tanta preparación como algunos modelos neuronales y pueden ser eficientes. Su principal inconveniente es que pueden perder interpretabilidad y requieren controlar el sobreajuste. En el proyecto, HistGradientBoosting ha mostrado un comportamiento muy competitivo.

Una forma útil de comparar enfoques es considerar varias dimensiónes: precisión, interpretabilidad, coste computacional, fácilidad de configuración, robustez ante datos limitados y escalabilidad. Ridge puntua bien en interpretabilidad, rapidez y estabilidad. MLP destaca en flexibilidad, aunque requiere más cuidado. HistGradientBoosting destaca en precisión sobre datos tabulares y captura de no linealidades.

También debe compararse cada modelo con un baseline sencillo. En predicción eléctrica, un baseline habitual es asumir que el precio futuro se parece al de un periodo anterior, por ejemplo el mismo periodo del día previo. En el proyecto se utiliza un baseline `lag 24`, que permite saber si un modelo aporta valor real sobre una regla simple. Esta comparación es importante porque un modelo complejo no justifica su usó si no mejora claramente una referencia básica.

El enfoque adoptado en este trabajo consiste en implementar varios modelos dentro de una misma aplicación. Todos comparten el mismo pipeline de datos, las mismas variables y la misma estrategia de validación temporal. Esto evita comparaciones injustas y permite que las diferencias observadas se deban principalmente al modelo, no a cambios en el tratamiento de datos.

El modo automático de selección refuerza esta idea. En lugar de exigir que el usuario elija siempre un algoritmo, el sistema puede entrenar las alternativas disponibles y seleccionar la que obtiene menor MAE en validación. Este criterio es sencillo y práctico, aunque podría ampliarse en el futuro con evaluaciones por mes, por hora, por régimen de precios o mediante backtesting más completo.

En conjunto, el estado del arte sugiere que la mejor estrategia no consiste en elegir ciegamente el modelo más complejo, sino en combinar buena preparación de datos, variables relevantes, validación temporal rigurosa y comparación contra referencias simples. Esta filosofía guia el desarrollo del proyecto.

### 5.6. Principales retos detectados en la literatura

La predicción del precio eléctrico presenta retos específicos que la diferencian de otros problemas de series temporales. El primero es la alta volatilidad. Los precios pueden cambiar rápidamente por variaciones de demanda, disponibilidad renovable, indisponibilidades, costes de combustible o restricciones del sistema. Esta volatilidad dificulta que los modelos mantengan precisión en todos los contextos.

El segundo reto es la presencia de picos extremos. En determinados periodos pueden aparecer precios mucho más altos o mucho más bajos que la media. Estos episodios son importantes porque tienen impacto económico, pero son difíciles de aprender si aparecen pocas veces en el histórico. Un modelo entrenado principalmente con situaciones normales puede subestimar los extremos.

El tercer reto es la dependencia de variables externas. El histórico de precios contiene información útil, pero no explica por completo el mercado. Para mejorar la precisión es conveniente incorporar demanda, meteorología, generación renovable prevista, disponibilidad de tecnologías, precios de gas, CO2, interconexiones y otros factores. La dificultad está en obtener estas variables con calidad suficiente y alinearlas temporalmente.

El cuarto reto es la calidad de los datos. Los ficheros pueden no estar disponibles para ciertos días, pueden cambiar de formato o pueden tener distinta resolución temporal. En el caso del proyecto, OMIE puede públicar datos horarios o cuarto-horarios según el periodo. Esto obliga a normalizar los datos y a tener cuidado con retardos como `lag 24`, que no siempre representan exactamente el mismo concepto si cambia la frecuencia temporal.

El quinto reto es evitar fuga de información futura. En series temporales es fácil cometer errores metodológicos si se mezclan datos de entrenamiento y validación de forma aleatoria. También puede haber fuga si se calculan medias, escalados o variables usando información posterior al instante predicho. Una evaluación realista debe respetar el orden temporal.

El sexto reto es el cambio estructural. El mercado eléctrico evoluciona: aumenta la penetración renovable, cambian reglas, aparecen nuevos mecanismos, varía el peso de tecnologías y se modifican patrones de consumo. Un modelo entrenado con datos antiguos puede perder validez si el sistema cambia. Por ello, los modelos deben reentrenarse periódicamente y evaluarse con datos recientes.

El séptimo reto es la interpretabilidad. En aplicaciones energéticas, no basta con obtener una predicción; a menudo se necesita entender por que el modelo predice cierto precio. Esto es relevante para analistas, operadores, estudiantes y responsables de decisión. Los modelos complejos pueden mejorar métricas, pero dificultar la explicación. El equilibrio entre precisión e interpretabilidad es una cuestión central.

El octavo reto es la reproducibilidad. Para que un estudio sea útil académicamente, debe documentar fuentes de datos, periodo analizado, transformaciones aplicadas, modelos, hiperparámetros y métricas. Sin está trazabilidad, los resultados son difíciles de verificar. El proyecto responde a este reto mediante una estructura de código modular, entorno virtual, README, documentos del Proyecto y control de versiones con Git.

El noveno reto es la evaluación limitada. Un buen resultado en un único periodo de validación no garantiza buen comportamiento futuro. Es recomendable evaluar en distintos meses, estaciones, rangos de precio y escenarios renovables. También conviene analizar errores concretos para entender en que situaciones falla el modelo. Este punto conecta con los capítulos posteriores de metodología de evaluación y resultados experimentales.

Finalmente, existe el reto de trasladar el modelo a una aplicación usable. Muchos estudios se centran en métricas, pero no siempre ofrecen una herramienta reproducible para descargar datos, entrenar modelos e inferir resultados. La aplicación desarrollada en este trabajo busca cubrir esa parte práctica, permitiendo ejecutar el flujo completo desde consola o interfaz gráfica.

En síntesis, el estado del arte muestra que la predicción del precio eléctrico requiere combinar conocimiento del mercado, tratamiento cuidadoso de series temporales y técnicas de aprendizaje automático. Los modelos clásicos aportan interpretabilidad; las redes neuronales aportan flexibilidad; los modelos de boosting aportan precisión en datos tabulares; y la evaluación temporal permite comparar estas alternativas de forma realista. El proyecto se sitúa en ese punto intermedio: suficientemente sencillo para ser comprensible y suficientemente completo para servir como base de una aplicación predictiva real.
