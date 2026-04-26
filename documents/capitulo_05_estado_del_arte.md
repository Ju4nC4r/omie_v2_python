# Capitulo 5. Estado del arte

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 5.1. Modelos estadisticos clasicos para prediccion de precios

La prediccion del precio electrico ha sido estudiada durante decadas desde enfoques estadisticos, econometricos y computacionales. Antes de la expansion del aprendizaje automatico moderno, los metodos clasicos de series temporales fueron la herramienta principal para modelar precios, demanda y generacion. Estos metodos siguen siendo relevantes porque proporcionan una base conceptual solida, son interpretables y permiten establecer lineas de comparacion frente a modelos mas complejos.

Uno de los enfoques tradicionales mas utilizados es el basado en modelos autorregresivos. En un modelo autorregresivo, el valor actual de una serie se explica a partir de valores pasados de la misma serie. En el contexto del mercado electrico, esto significa que el precio de un periodo puede depender del precio observado en periodos anteriores. Esta idea encaja bien con el comportamiento del precio electrico, que suele mostrar continuidad temporal: las condiciones de mercado de una hora no son completamente independientes de las horas previas.

Los modelos AR, ARMA y ARIMA han sido ampliamente utilizados en problemas de prediccion de series temporales. Los modelos AR capturan dependencias autorregresivas; los modelos MA incorporan componentes de media movil sobre errores pasados; y los modelos ARIMA incluyen diferenciacion para tratar series no estacionarias. En mercados electricos, la no estacionariedad aparece por cambios en demanda, combustible, regulacion, penetracion renovable o estructura del mercado. Por ello, la estacionariedad es una cuestion importante en los modelos clasicos.

Tambien existen variantes estacionales como SARIMA, que permiten modelar patrones repetitivos. En el precio electrico, la estacionalidad es especialmente importante. Existen ciclos diarios, semanales y anuales. El comportamiento de una hora nocturna no es el mismo que el de una hora punta; un sabado no se comporta igual que un martes laborable; y los meses de verano e invierno presentan condiciones distintas. Los modelos estacionales intentan representar estas regularidades de forma explicita.

Otra familia clasica son los modelos de suavizado exponencial. Estos metodos asignan mayor peso a observaciones recientes y menor peso a observaciones antiguas. Son utiles cuando la serie presenta tendencias o cambios progresivos. Sin embargo, pueden resultar limitados cuando el precio electrico muestra saltos bruscos, episodios de precios muy altos, precios cercanos a cero o cambios no lineales causados por renovables y combustibles.

Los modelos de regresion lineal tambien han sido utilizados para explicar el precio electrico mediante variables externas. Por ejemplo, pueden incluirse demanda prevista, generacion eolica, generacion solar, temperatura, precio del gas o precio del CO2. La principal ventaja de estos modelos es su interpretabilidad. Cada coeficiente indica la relacion aproximada entre una variable explicativa y el precio objetivo. No obstante, la relacion real entre variables y precio suele ser no lineal, por lo que la regresion lineal puede quedarse corta si no se enriquecen las variables.

La regresion Ridge, utilizada en este proyecto, puede considerarse una extension regularizada de la regresion lineal. Su objetivo es ajustar un modelo lineal evitando que los coeficientes crezcan demasiado. Esto resulta util cuando se generan muchas variables a partir de calendarios, retardos y medias moviles. La regularizacion reduce el riesgo de sobreajuste y mejora la estabilidad del modelo. Aunque Ridge no captura relaciones no lineales complejas por si misma, puede ofrecer resultados competitivos cuando las variables estan bien disenadas.

Los modelos estadisticos clasicos presentan ventajas importantes. Son relativamente sencillos, rapidos de entrenar, interpretables y faciles de reproducir. Permiten entender patrones basicos de la serie y ofrecen un punto de partida razonable. Ademas, en problemas donde los datos son limitados, un modelo sencillo puede generalizar mejor que un modelo muy flexible.

Sin embargo, los precios electricos presentan caracteristicas que dificultan el uso exclusivo de metodos clasicos. La serie puede contener picos extremos, cambios estructurales, influencia meteorologica, efectos regulatorios, saturacion renovable, restricciones de red e interaccion entre mercados. Muchos de estos elementos generan relaciones no lineales y dependencias complejas. Por esta razon, los enfoques modernos suelen combinar variables de calendario, historico de precios y variables externas con tecnicas de aprendizaje automatico.

En el marco de este trabajo, los modelos clasicos se entienden como referencia metodologica. La idea de usar retardos, ciclos y medias moviles procede directamente del analisis de series temporales. Aunque la aplicacion no implementa modelos ARIMA completos, si incorpora su intuicion principal: el pasado contiene informacion relevante para anticipar el futuro. Esta aproximacion permite construir un sistema sencillo, reproducible y extensible.

### 5.2. Modelos de machine learning aplicados a energia

El aprendizaje automatico ha adquirido un papel cada vez mas importante en la prediccion energetica. A diferencia de los modelos estadisticos tradicionales, los modelos de machine learning no requieren especificar de forma tan rigida la relacion entre entradas y salida. En lugar de imponer una ecuacion concreta, aprenden patrones a partir de datos historicos. Esto los hace atractivos para mercados electricos, donde el precio depende de muchas variables que interactuan entre si.

En el ambito energetico, el machine learning se utiliza para predecir demanda, generacion renovable, precios de mercado, consumo de edificios, perdidas en redes, indisponibilidades y otros fenomenos. La disponibilidad de datos publicos, sensores, sistemas de informacion y APIs ha facilitado el desarrollo de modelos cada vez mas ricos. En el caso espanol, fuentes como OMIE y ESIOS permiten construir datasets con informacion de mercado y sistema.

Los modelos supervisados son los mas habituales para la prediccion de precios. En este enfoque se dispone de ejemplos historicos formados por variables de entrada y una variable objetivo. En este proyecto, las entradas incluyen calendario, variables ciclicas, retardos del precio, estadisticos moviles y, opcionalmente, previsiones renovables. La salida es el precio marginal espanol del mercado diario.

Entre los modelos de machine learning aplicados a energia se encuentran la regresion lineal regularizada, los arboles de decision, los random forests, los metodos de boosting, las maquinas de vectores soporte y las redes neuronales. Cada familia tiene fortalezas y limitaciones. La eleccion depende del tamano del dataset, la calidad de las variables, la necesidad de interpretabilidad, el coste computacional y el objetivo del sistema.

Los arboles de decision permiten dividir el espacio de variables en regiones. Por ejemplo, un arbol puede aprender que determinados rangos de hora, demanda o generacion renovable se asocian a precios diferentes. Su interpretacion es intuitiva, pero un unico arbol puede sobreajustar facilmente. Por ello, en la practica se suelen utilizar conjuntos de arboles, como random forests o gradient boosting.

Los random forests combinan muchos arboles entrenados sobre subconjuntos de datos y variables. Suelen ser robustos y capturan no linealidades, pero pueden resultar menos precisos que boosting en algunos problemas tabulares y generar modelos de mayor tamano. Los metodos de boosting, en cambio, construyen modelos de forma secuencial: cada nuevo arbol intenta corregir errores de los anteriores. Esta estrategia suele lograr muy buen rendimiento en datos tabulares.

Las maquinas de vectores soporte han sido utilizadas en series temporales energeticas por su capacidad para modelar relaciones no lineales mediante kernels. No obstante, pueden ser costosas en datasets grandes y requieren una seleccion cuidadosa de hiperparametros. En problemas practicos, su uso puede ser menos directo que otros modelos disponibles en bibliotecas como scikit-learn.

Una cuestion esencial en machine learning aplicado a energia es la ingenieria de variables. El modelo no observa directamente el funcionamiento fisico del sistema, sino las variables que se le proporcionan. Por tanto, el rendimiento depende en gran medida de la calidad de esas variables. Incluir hora, dia, mes, fines de semana, retardos, medias moviles y renovables puede marcar una diferencia notable.

Tambien es fundamental respetar la naturaleza temporal de los datos. En un problema de prediccion real, el modelo no debe usar informacion futura para predecir el pasado. Por ello, la division entre entrenamiento y validacion debe hacerse temporalmente. El proyecto adopta esta idea: se entrena con la parte inicial del periodo y se valida con la parte final. Esta metodologia es mas realista que mezclar aleatoriamente observaciones de distintos dias.

Los modelos de machine learning ofrecen ventajas claras: pueden capturar no linealidades, combinar muchas variables, adaptarse a distintos contextos y mejorar con mas datos. Sin embargo, tambien presentan riesgos. Un modelo demasiado complejo puede aprender ruido historico y fallar en datos nuevos. Ademas, los resultados pueden degradarse si cambia la estructura del mercado, si faltan variables importantes o si se produce un evento excepcional no representado en el entrenamiento.

En este trabajo, el machine learning se aplica con un enfoque practico e incremental. Primero se construye un modelo pequeno basado en historico y calendario. Despues se incorporan modelos alternativos y variables renovables opcionales. Esta progresion permite entender que aporta cada mejora y evita depender desde el principio de una arquitectura excesivamente compleja.

### 5.3. Redes neuronales en prediccion de series temporales

Las redes neuronales son una de las familias mas conocidas dentro del aprendizaje automatico. Su popularidad se debe a su capacidad para aproximar relaciones no lineales complejas. En prediccion de precios electricos, las redes neuronales han sido empleadas para capturar patrones horarios, dependencias temporales, interacciones entre variables y comportamientos dificiles de representar con modelos lineales.

Una red neuronal artificial esta formada por capas de neuronas conectadas mediante pesos. Durante el entrenamiento, el modelo ajusta esos pesos para reducir el error entre sus predicciones y los valores reales. En problemas de regresion, como la prediccion de precios, la salida de la red es un valor numerico continuo. El aprendizaje se realiza normalmente mediante algoritmos de optimizacion que minimizan una funcion de perdida.

El tipo de red mas sencillo es el perceptron multicapa, conocido como MLP. Este modelo esta formado por una capa de entrada, una o varias capas ocultas y una capa de salida. Las capas ocultas aplican transformaciones no lineales que permiten aprender relaciones mas flexibles que una regresion lineal. El proyecto incorpora `MLPRegressor`, una implementacion de scikit-learn de este tipo de red.

El MLP puede funcionar bien con variables tabulares generadas previamente. En este caso, la red no recibe una secuencia completa como tal, sino un conjunto de variables que resumen informacion temporal: hora, dia, retardos, medias moviles, diferencias y previsiones renovables. Esta estrategia reduce la complejidad de la red y permite trabajar con una arquitectura sencilla.

En prediccion de series temporales tambien se han utilizado redes recurrentes, como RNN, LSTM y GRU. Estas arquitecturas estan disenadas para procesar secuencias y mantener memoria de estados anteriores. Las LSTM, en particular, fueron muy populares para problemas donde era necesario aprender dependencias a largo plazo. En el mercado electrico podrian utilizarse para modelar secuencias de precios, demanda y generacion.

Mas recientemente, tambien se han aplicado arquitecturas basadas en atencion y Transformers a series temporales. Estos modelos pueden capturar relaciones entre distintos puntos temporales sin depender exclusivamente de una recurrencia secuencial. Sin embargo, suelen requerir mas datos, mas potencia computacional y una configuracion mas compleja. Para un TFG centrado en una aplicacion local y reproducible, pueden resultar excesivos como primera aproximacion.

Las redes neuronales tienen la ventaja de ser flexibles. Pueden combinar muchas variables y aprender relaciones no lineales. No obstante, presentan varias dificultades. La primera es la sensibilidad a hiperparametros: numero de capas, numero de neuronas, funcion de activacion, tasa de aprendizaje, regularizacion y numero de iteraciones. La segunda es el riesgo de sobreajuste, especialmente cuando el dataset no es muy grande. La tercera es la menor interpretabilidad frente a modelos lineales.

En mercados electricos, las redes neuronales pueden cometer errores importantes si el periodo de entrenamiento no contiene situaciones similares a las que se quieren predecir. Por ejemplo, si cambian los precios del gas, la estructura de demanda o la penetracion renovable, la red puede extrapolar mal. Por ello, aunque una red neuronal pueda mejorar la precision, no elimina la necesidad de buenas variables, validacion temporal y analisis de errores.

En el proyecto desarrollado, la red neuronal se ha incluido como uno de los modelos seleccionables desde la interfaz grafica. Esto permite al usuario comparar su comportamiento con Ridge y con HistGradientBoosting. El objetivo no es afirmar que la red neuronal sea siempre el mejor modelo, sino ofrecer una alternativa no lineal y evaluarla de forma objetiva mediante metricas.

La decision de utilizar `MLPRegressor` es coherente con el enfoque didactico del proyecto. Es suficientemente sencilla para ejecutarse en un entorno local, se integra bien con scikit-learn y permite mostrar los fundamentos del entrenamiento neuronal. Al mismo tiempo, deja abierta la posibilidad de evolucionar hacia arquitecturas mas especificas de series temporales en trabajos futuros.

### 5.4. Modelos basados en arboles y boosting

Los modelos basados en arboles son especialmente relevantes en datos tabulares. A diferencia de las redes neuronales, que requieren ajustar pesos en capas, los arboles dividen el espacio de variables mediante reglas. Estas reglas pueden capturar interacciones no lineales de forma natural. Por ejemplo, el modelo puede aprender que una misma cantidad de generacion solar tiene efectos distintos segun la hora del dia, el dia de la semana o el nivel de precio previo.

Un arbol de decision por si solo puede ser facil de interpretar, pero tambien tiende a sobreajustar. Si se deja crecer demasiado, puede memorizar patrones especificos del entrenamiento que no se repiten en validacion. Para superar esta limitacion se utilizan metodos de conjunto, que combinan muchos arboles. Dentro de estos metodos destacan random forest y gradient boosting.

El gradient boosting construye arboles de manera secuencial. El primer arbol realiza una prediccion inicial; los siguientes intentan corregir los errores residuales de los anteriores. De esta forma, el modelo va refinando la prediccion paso a paso. Este enfoque ha demostrado un rendimiento muy alto en numerosos problemas de datos estructurados, incluyendo prediccion energetica.

El proyecto incorpora `HistGradientBoostingRegressor`, una implementacion eficiente de scikit-learn basada en histogramas. Esta variante agrupa valores continuos en bins, lo que permite acelerar el entrenamiento y manejar datasets de tamano medio con buen rendimiento. En las pruebas realizadas con datos amplios de 2025, este modelo fue seleccionado como mejor alternativa en modo automatico, con metricas superiores a los modelos mas simples.

Los modelos de boosting presentan varias ventajas. Capturan no linealidades, manejan interacciones entre variables y suelen funcionar bien sin necesidad de escalar todas las entradas. Ademas, son adecuados cuando se dispone de muchas variables derivadas, como retardos, medias moviles, diferencias y senales de calendario. Esto encaja bien con la estructura del dataset construido en el proyecto.

Otra ventaja de los arboles es que pueden trabajar con relaciones por tramos. El precio electrico no siempre responde de forma continua y lineal a una variable. Puede haber umbrales: por ejemplo, a partir de cierto nivel de generacion renovable el precio baja de manera mas marcada; o en ciertas horas punta el efecto de la demanda se amplifica. Los arboles pueden representar este tipo de comportamiento mediante divisiones sucesivas.

Sin embargo, los modelos de boosting tambien requieren cuidado. Si se configuran con demasiada complejidad, pueden sobreajustar. Parametros como profundidad, numero de iteraciones, tasa de aprendizaje, regularizacion y numero minimo de observaciones por hoja influyen en el resultado. Aunque scikit-learn ofrece valores por defecto razonables, un estudio mas avanzado podria incorporar busqueda de hiperparametros.

Otra limitacion es la interpretabilidad. Aunque un modelo de arbol puede explicarse facilmente, un conjunto de muchos arboles es mas dificil de interpretar de forma directa. Existen tecnicas para estimar importancia de variables, dependencias parciales o explicaciones locales, pero no forman parte del alcance principal de este proyecto. Aun asi, el rendimiento practico de boosting justifica su inclusion.

En comparacion con una red neuronal, HistGradientBoosting puede ser mas estable en datasets tabulares pequenos o medianos. Tambien suele requerir menos ajuste inicial. En comparacion con Ridge, puede capturar relaciones no lineales que el modelo lineal no representa. Por ello, constituye una alternativa muy adecuada para el problema de prediccion del precio electrico.

Dentro de la aplicacion practica, el usuario puede seleccionar manualmente este modelo o dejar que el modo `auto` lo compare con Ridge y MLP. Esta opcion refuerza el caracter experimental del proyecto: no se presupone un ganador, sino que se evalua cada modelo bajo las mismas condiciones de datos y validacion.

### 5.5. Comparacion de enfoques existentes

La literatura y la practica muestran que no existe un unico modelo universalmente superior para la prediccion de precios electricos. El rendimiento depende del mercado, el horizonte de prediccion, las variables disponibles, la resolucion temporal, el periodo historico y los criterios de evaluacion. Por ello, una buena metodologia debe comparar varios enfoques en igualdad de condiciones.

Los modelos estadisticos clasicos destacan por su simplicidad e interpretabilidad. Son adecuados para establecer lineas base y entender componentes temporales. Pueden funcionar razonablemente bien cuando los patrones son estables, pero tienden a ser limitados ante relaciones no lineales o cambios bruscos. Su mayor valor en este trabajo es conceptual: inspiran el uso de retardos y variables temporales.

Los modelos lineales regularizados, como Ridge, representan un equilibrio entre sencillez y robustez. Son rapidos, reproducibles y menos propensos al sobreajuste que una regresion lineal sin regularizacion. Funcionan especialmente bien cuando se dispone de variables bien construidas. No obstante, su estructura lineal limita la capacidad para capturar interacciones complejas.

Las redes neuronales aportan flexibilidad y capacidad no lineal. Pueden mejorar resultados si hay suficientes datos y una configuracion adecuada. Sin embargo, son mas sensibles a hiperparametros, pueden tardar mas en entrenar y son menos interpretables. En un entorno didactico, su inclusion permite mostrar como se comporta un modelo neuronal frente a alternativas mas clasicas.

Los modelos basados en boosting suelen obtener muy buenos resultados en datos tabulares. Capturan interacciones, no requieren tanta preparacion como algunos modelos neuronales y pueden ser eficientes. Su principal inconveniente es que pueden perder interpretabilidad y requieren controlar el sobreajuste. En el proyecto, HistGradientBoosting ha mostrado un comportamiento muy competitivo.

Una forma util de comparar enfoques es considerar varias dimensiones: precision, interpretabilidad, coste computacional, facilidad de configuracion, robustez ante datos limitados y escalabilidad. Ridge puntua bien en interpretabilidad, rapidez y estabilidad. MLP destaca en flexibilidad, aunque requiere mas cuidado. HistGradientBoosting destaca en precision sobre datos tabulares y captura de no linealidades.

Tambien debe compararse cada modelo con un baseline sencillo. En prediccion electrica, un baseline habitual es asumir que el precio futuro se parece al de un periodo anterior, por ejemplo el mismo periodo del dia previo. En el proyecto se utiliza un baseline `lag 24`, que permite saber si un modelo aporta valor real sobre una regla simple. Esta comparacion es importante porque un modelo complejo no justifica su uso si no mejora claramente una referencia basica.

El enfoque adoptado en este trabajo consiste en implementar varios modelos dentro de una misma aplicacion. Todos comparten el mismo pipeline de datos, las mismas variables y la misma estrategia de validacion temporal. Esto evita comparaciones injustas y permite que las diferencias observadas se deban principalmente al modelo, no a cambios en el tratamiento de datos.

El modo automatico de seleccion refuerza esta idea. En lugar de exigir que el usuario elija siempre un algoritmo, el sistema puede entrenar las alternativas disponibles y seleccionar la que obtiene menor MAE en validacion. Este criterio es sencillo y practico, aunque podria ampliarse en el futuro con evaluaciones por mes, por hora, por regimen de precios o mediante backtesting mas completo.

En conjunto, el estado del arte sugiere que la mejor estrategia no consiste en elegir ciegamente el modelo mas complejo, sino en combinar buena preparacion de datos, variables relevantes, validacion temporal rigurosa y comparacion contra referencias simples. Esta filosofia guia el desarrollo del proyecto.

### 5.6. Principales retos detectados en la literatura

La prediccion del precio electrico presenta retos especificos que la diferencian de otros problemas de series temporales. El primero es la alta volatilidad. Los precios pueden cambiar rapidamente por variaciones de demanda, disponibilidad renovable, indisponibilidades, costes de combustible o restricciones del sistema. Esta volatilidad dificulta que los modelos mantengan precision en todos los contextos.

El segundo reto es la presencia de picos extremos. En determinados periodos pueden aparecer precios mucho mas altos o mucho mas bajos que la media. Estos episodios son importantes porque tienen impacto economico, pero son dificiles de aprender si aparecen pocas veces en el historico. Un modelo entrenado principalmente con situaciones normales puede subestimar los extremos.

El tercer reto es la dependencia de variables externas. El historico de precios contiene informacion util, pero no explica por completo el mercado. Para mejorar la precision es conveniente incorporar demanda, meteorologia, generacion renovable prevista, disponibilidad de tecnologias, precios de gas, CO2, interconexiones y otros factores. La dificultad esta en obtener estas variables con calidad suficiente y alinearlas temporalmente.

El cuarto reto es la calidad de los datos. Los ficheros pueden no estar disponibles para ciertos dias, pueden cambiar de formato o pueden tener distinta resolucion temporal. En el caso del proyecto, OMIE puede publicar datos horarios o cuarto-horarios segun el periodo. Esto obliga a normalizar los datos y a tener cuidado con retardos como `lag 24`, que no siempre representan exactamente el mismo concepto si cambia la frecuencia temporal.

El quinto reto es evitar fuga de informacion futura. En series temporales es facil cometer errores metodologicos si se mezclan datos de entrenamiento y validacion de forma aleatoria. Tambien puede haber fuga si se calculan medias, escalados o variables usando informacion posterior al instante predicho. Una evaluacion realista debe respetar el orden temporal.

El sexto reto es el cambio estructural. El mercado electrico evoluciona: aumenta la penetracion renovable, cambian reglas, aparecen nuevos mecanismos, varia el peso de tecnologias y se modifican patrones de consumo. Un modelo entrenado con datos antiguos puede perder validez si el sistema cambia. Por ello, los modelos deben reentrenarse periodicamente y evaluarse con datos recientes.

El septimo reto es la interpretabilidad. En aplicaciones energeticas, no basta con obtener una prediccion; a menudo se necesita entender por que el modelo predice cierto precio. Esto es relevante para analistas, operadores, estudiantes y responsables de decision. Los modelos complejos pueden mejorar metricas, pero dificultar la explicacion. El equilibrio entre precision e interpretabilidad es una cuestion central.

El octavo reto es la reproducibilidad. Para que un estudio sea util academicamente, debe documentar fuentes de datos, periodo analizado, transformaciones aplicadas, modelos, hiperparametros y metricas. Sin esta trazabilidad, los resultados son dificiles de verificar. El proyecto responde a este reto mediante una estructura de codigo modular, entorno virtual, README, documentos del TFG y control de versiones con Git.

El noveno reto es la evaluacion limitada. Un buen resultado en un unico periodo de validacion no garantiza buen comportamiento futuro. Es recomendable evaluar en distintos meses, estaciones, rangos de precio y escenarios renovables. Tambien conviene analizar errores concretos para entender en que situaciones falla el modelo. Este punto conecta con los capitulos posteriores de metodologia de evaluacion y resultados experimentales.

Finalmente, existe el reto de trasladar el modelo a una aplicacion usable. Muchos estudios se centran en metricas, pero no siempre ofrecen una herramienta reproducible para descargar datos, entrenar modelos e inferir resultados. La aplicacion desarrollada en este trabajo busca cubrir esa parte practica, permitiendo ejecutar el flujo completo desde consola o interfaz grafica.

En sintesis, el estado del arte muestra que la prediccion del precio electrico requiere combinar conocimiento del mercado, tratamiento cuidadoso de series temporales y tecnicas de aprendizaje automatico. Los modelos clasicos aportan interpretabilidad; las redes neuronales aportan flexibilidad; los modelos de boosting aportan precision en datos tabulares; y la evaluacion temporal permite comparar estas alternativas de forma realista. El proyecto se situa en ese punto intermedio: suficientemente sencillo para ser comprensible y suficientemente completo para servir como base de una aplicacion predictiva real.
