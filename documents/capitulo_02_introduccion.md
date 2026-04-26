# Capitulo 2. Introduccion

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 2.1. Motivacion del estudio

El sistema electrico se encuentra inmerso en una transformacion profunda. La necesidad de reducir emisiones, aumentar la eficiencia energetica y favorecer la penetracion de energias renovables ha cambiado la forma en que se planifica, opera y analiza el mercado electrico. En este contexto, el precio de la electricidad se ha convertido en una variable de gran interes para empresas, instituciones, consumidores y agentes del sector energetico.

La electricidad no es un producto convencional. A diferencia de otros bienes, su almacenamiento a gran escala continua siendo limitado, por lo que la produccion y el consumo deben mantenerse equilibrados de forma casi instantanea. Esta caracteristica hace que el precio electrico sea especialmente sensible a cambios en la demanda, en la disponibilidad de generacion, en la meteorologia y en el coste de las tecnologias marginales. Como consecuencia, su prediccion constituye un problema complejo y de alto valor practico.

En el caso espanol, el mercado diario gestionado por OMIE establece precios para los distintos periodos del dia siguiente. Estos precios son utilizados como referencia por numerosos agentes y afectan directa o indirectamente a consumidores domesticos, industrias, comercializadoras, generadores y operadores. Una mejor comprension de su comportamiento permite tomar decisiones mas informadas, disenar estrategias de compra o venta y evaluar el impacto de nuevas tecnologias.

La motivacion principal de este trabajo surge de combinar dos areas de interes: el mercado electrico y el aprendizaje automatico. Por un lado, el mercado electrico ofrece datos reales, publicos y con dinamicas complejas. Por otro, las tecnicas de machine learning permiten extraer patrones de grandes volumenes de datos y generar predicciones a partir de variables historicas y externas. La union de ambos elementos da lugar a un caso de estudio aplicado, actual y con utilidad academica.

Ademas, la creciente presencia de energias renovables aumenta la necesidad de modelos que puedan incorporar informacion externa. La generacion eolica y solar introduce variabilidad en la oferta electrica y afecta de forma significativa al precio. Una elevada produccion renovable puede reducir el precio en determinadas horas, mientras que una baja disponibilidad puede favorecer precios superiores. Por tanto, integrar datos de prevision renovable puede mejorar la capacidad explicativa de los modelos.

Desde el punto de vista formativo, este trabajo permite aplicar conocimientos de programacion, analisis de datos, estadistica, series temporales, aprendizaje automatico y sistemas electricos. No se trata solo de entrenar un modelo, sino de construir un flujo completo: descarga de datos, limpieza, almacenamiento, generacion de variables, entrenamiento, evaluacion, inferencia y documentacion. Esta vision integral es una de las principales motivaciones del proyecto.

### 2.2. Importancia de la prediccion del precio electrico

La prediccion del precio electrico tiene importancia tanto economica como operativa. En un mercado liberalizado, los agentes necesitan anticipar el comportamiento futuro de los precios para optimizar sus decisiones. Una comercializadora puede usar previsiones para definir estrategias de compra; un generador puede planificar ofertas; un consumidor industrial puede desplazar consumos; y un gestor de almacenamiento puede decidir cuando cargar o descargar energia.

En el caso de consumidores intensivos en energia, incluso pequenas mejoras en la prediccion pueden traducirse en ahorros relevantes. Industrias con procesos flexibles pueden programar parte de su consumo en horas de menor precio. Del mismo modo, instalaciones con autoconsumo, baterias o gestion activa de demanda pueden beneficiarse de estimaciones del precio para optimizar su operacion.

La prediccion tambien es relevante para estudiar la integracion de renovables. La eolica y la solar tienen costes variables reducidos, pero su produccion depende de factores meteorologicos. Cuando su penetracion es alta, los precios pueden experimentar caidas pronunciadas en determinadas franjas horarias. Anticipar estos patrones resulta util para analizar el impacto de la transicion energetica y para disenar mecanismos de gestion de flexibilidad.

Desde la perspectiva del operador y de los analistas del sistema, disponer de modelos de prediccion contribuye a comprender mejor los factores que explican la formacion de precios. Aunque un modelo de aprendizaje automatico no sustituye al conocimiento tecnico del mercado, puede complementar el analisis tradicional detectando relaciones entre variables, patrones recurrentes o situaciones atipicas.

Tambien existe una dimension academica. La prediccion de precios electricos es un problema suficientemente complejo para evaluar distintos enfoques: modelos lineales, modelos basados en arboles, redes neuronales y tecnicas especificas de series temporales. La existencia de datos publicos permite reproducir experimentos y comparar resultados, siempre que se documente adecuadamente la metodologia.

La importancia de la prediccion no implica que sea una tarea sencilla. El precio electrico puede verse afectado por eventos excepcionales, cambios regulatorios, indisponibilidades de generacion, variaciones bruscas de demanda, cambios meteorologicos y tension en mercados de combustibles. Por ello, el objetivo realista no es eliminar el error, sino reducirlo frente a referencias simples y comprender en que situaciones el modelo falla.

En este trabajo, la importancia de la prediccion se refleja en la comparacion con una baseline sencilla: el precio de 24 periodos antes. Esta referencia permite responder una pregunta fundamental: el modelo desarrollado, con sus variables y algoritmos, aporta informacion adicional respecto a repetir el precio del dia anterior. Si la respuesta es positiva, el sistema demuestra valor predictivo inicial.

### 2.3. Problema a resolver

El problema que se aborda consiste en estimar el precio marginal del mercado electrico espanol para un periodo futuro a partir de informacion historica y, opcionalmente, de variables externas de generacion renovable. En terminos de aprendizaje automatico, se formula como un problema de regresion supervisada sobre una serie temporal.

La variable objetivo es:

```text
marginal_es
```

Esta variable representa el precio marginal espanol publicado por OMIE, expresado en euros por megavatio hora. A partir de una secuencia historica de precios y variables asociadas, el modelo debe generar una estimacion numerica para el siguiente periodo disponible.

El problema presenta varias dificultades. La primera es la naturaleza temporal de los datos. No se puede tratar cada observacion como completamente independiente, ya que el precio actual suele estar relacionado con precios anteriores, patrones horarios y comportamiento semanal. Por ello, es necesario construir variables que representen adecuadamente esa dependencia temporal.

La segunda dificultad es la presencia de estacionalidad y ciclos. Existen patrones diarios, semanales y mensuales. Por ejemplo, el comportamiento del precio durante una madrugada puede ser diferente al de una hora punta; un domingo puede diferir de un dia laborable; y determinados meses pueden presentar condiciones de demanda o generacion distintas. El modelo debe disponer de variables que reflejen estos ciclos.

La tercera dificultad es la influencia de variables externas. El precio no depende solo de su propio historico. Factores como la demanda, la produccion renovable, el gas, el CO2 o las interconexiones pueden modificar la formacion de precios. En este proyecto se aborda una primera aproximacion incorporando prevision eolica y solar de ESIOS, aunque se reconoce que existen otras variables relevantes que quedan fuera del alcance inicial.

La cuarta dificultad es evitar fuga de informacion futura. En problemas temporales, una mala separacion de datos puede producir resultados artificialmente optimistas. Si se entrena con datos posteriores al periodo evaluado, el modelo estaria usando informacion que no estaria disponible en una situacion real. Por ello, la evaluacion se realiza mediante una separacion cronologica.

La quinta dificultad es la variabilidad del mercado. Hay dias atipicos, festivos, episodios de precios extremos y periodos donde el comportamiento cambia. Un modelo puede funcionar bien en un rango temporal y peor en otro. Por tanto, el sistema debe permitir repetir experimentos con distintos periodos y comparar modelos de forma flexible.

El problema se concreta finalmente en desarrollar una aplicacion que permita:

- descargar datos historicos de OMIE
- preparar un dataset supervisado
- anadir variables externas opcionales de ESIOS
- entrenar diferentes modelos
- comparar metricas de validacion
- guardar el modelo seleccionado
- realizar inferencia para el siguiente periodo

### 2.4. Alcance del trabajo

El alcance del trabajo se centra en construir un prototipo funcional de prediccion del precio del mercado diario electrico espanol. El sistema no pretende competir con herramientas profesionales de prediccion energetica ni cubrir todos los factores que influyen en el mercado. Su objetivo es academico y experimental.

El proyecto trabaja principalmente con datos de OMIE. Estos datos permiten obtener el precio marginal espanol para cada periodo. Se ha implementado un parser especifico para los ficheros `MARGINALPDBC`, contemplando tanto dias con 24 periodos como dias con 96 periodos. Esta flexibilidad es importante porque el sistema electrico evoluciona hacia resoluciones temporales mas finas.

Como extension, se incorpora la posibilidad de usar datos de ESIOS. Esta funcionalidad es opcional porque requiere token de acceso. Cuando esta activa, el sistema descarga previsiones de generacion eolica, solar fotovoltaica y solar termica. Estas variables se unen al dataset principal y se utilizan como entradas adicionales para los modelos.

En cuanto a modelos, el trabajo se limita a tres enfoques de machine learning supervisado: `RidgeCV`, `MLPRegressor` e `HistGradientBoostingRegressor`. La seleccion responde a la necesidad de comparar modelos de distinta naturaleza sin incrementar excesivamente la complejidad. Se deja fuera del alcance inicial el uso de modelos mas avanzados como redes recurrentes, transformers o arquitecturas especificas para series temporales.

La evaluacion se basa en una particion temporal simple entre entrenamiento y validacion. No se implementa aun un sistema completo de backtesting mensual o rolling window, aunque se identifica como linea futura. Las metricas principales son MAE, RMSE y R2, junto con una comparacion contra la baseline `lag 24`.

La aplicacion practica incluye tanto una interfaz de consola como una interfaz grafica. La interfaz grafica no busca ser una herramienta comercial, sino una forma clara de ejecutar y demostrar el flujo. Permite seleccionar fechas, elegir modelo, activar ESIOS, entrenar, consultar metricas y ejecutar inferencia.

Quedan fuera del alcance inicial varias mejoras importantes:

- incorporacion de demanda prevista
- variables meteorologicas
- festivos nacionales y autonomicos
- precios de gas y CO2
- interconexiones internacionales
- prediccion de todo el dia siguiente
- optimizacion avanzada de hiperparametros
- despliegue web o en nube

Estas limitaciones no invalidan el trabajo, sino que delimitan su ambito. El objetivo es construir una base solida y extensible que pueda ampliarse posteriormente.

### 2.5. Estructura del documento

El documento se organiza en capitulos que siguen la evolucion natural del proyecto, desde el contexto teorico hasta la aplicacion practica y los resultados.

El primer capitulo presenta el resumen general del trabajo. En el se describe el contexto, los objetivos, la metodologia, los resultados esperados y la aplicacion desarrollada.

El segundo capitulo, correspondiente a esta introduccion, desarrolla la motivacion del estudio, la importancia de predecir el precio electrico, el problema a resolver, el alcance del trabajo y la estructura general del documento.

Los capitulos posteriores profundizan en el marco teorico, explicando el funcionamiento del mercado electrico espanol, el papel de OMIE, la funcion de ESIOS/REE y los factores que influyen en la formacion del precio.

Tambien se incluye un capitulo de estado del arte, donde se revisan enfoques clasicos y modernos para prediccion de precios electricos, incluyendo modelos estadisticos, aprendizaje automatico y redes neuronales.

Los capitulos dedicados a fuentes de datos y preparacion explican como se obtienen, limpian y organizan los datos. Se detalla el uso de ficheros OMIE, la integracion opcional con ESIOS y la construccion del dataset supervisado.

El capitulo de ingenieria de variables describe las transformaciones aplicadas a los datos: variables temporales, retardos, medias moviles, diferencias, ratios y variables renovables.

El capitulo de modelos presenta los algoritmos utilizados: baseline, Ridge, MLP y gradient boosting. Se justifican sus caracteristicas y se explican sus ventajas e inconvenientes.

La metodologia de evaluacion se desarrolla en un capitulo especifico, donde se presentan las metricas MAE, RMSE y R2, asi como la importancia de la validacion temporal.

La parte practica se recoge en los capitulos de diseno e implementacion. En ellos se describe la arquitectura del software, los modulos desarrollados, la interfaz grafica, los comandos de consola y la gestion de artefactos.

Finalmente, el documento incluye capitulos de resultados, discusion, conclusiones y lineas futuras. En ellos se analizan los experimentos realizados, se interpretan los errores, se valoran las limitaciones del sistema y se proponen mejoras posteriores.

Esta estructura permite presentar el trabajo de forma progresiva: primero se explica el problema, despues se describe la metodologia, luego se muestra la implementacion y finalmente se analizan los resultados.

