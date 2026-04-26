# Capítulo 2. Introducción

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 2.1. Motivación del estudio

El sistema eléctrico se encuentra inmerso en una transformación profunda. La necesidad de reducir emisiones, aumentar la eficiencia energética y favorecer la penetración de energías renovables ha cambiado la forma en que se planifica, opera y analiza el mercado eléctrico. En este contexto, el precio de la electricidad se ha convertido en una variable de gran interés para empresas, instituciones, consumidores y agentes del sector energético.

La electricidad no es un producto convencional. A diferencia de otros bienes, su almacenamiento a gran escala continúa siendo limitado, por lo que la producción y el consumo deben mantenerse equilibrados de forma casi instantánea. Esta característica hace que el precio eléctrico sea especialmente sensible a cambios en la demanda, en la disponibilidad de generación, en la meteorología y en el coste de las tecnologías marginales. Como consecuencia, su predicción constituye un problema complejo y de alto valor práctico.

En el caso español, el mercado diario gestionado por OMIE establece precios para los distintos periodos del día siguiente. Estos precios son utilizados como referencia por numerosos agentes y afectan directa o indirectamente a consumidores domesticos, industrias, comercializadoras, generadores y operadores. Una mejor comprensión de su comportamiento permite tomar decisiones más informadas, diseñar estrategias de compra o venta y evaluar el impacto de nuevas tecnologías.

La motivacion principal de este trabajo surge de combinar dos áreas de interés: el mercado eléctrico y el aprendizaje automático. Por un lado, el mercado eléctrico ofrece datos reales, públicos y con dinámicas complejas. Por otro, las técnicas de machine learning permiten extraer patrones de grandes volúmenes de datos y generar predicciones a partir de variables históricas y externas. La unión de ambos elementos da lugar a un caso de estudio aplicado, actual y con utilidad académica.

Además, la creciente presencia de energías renovables aumenta la necesidad de modelos que puedan incorporar información externa. La generación eólica y solar introduce variabilidad en la oferta eléctrica y afecta de forma significativa al precio. Una elevada producción renovable puede reducir el precio en determinadas horas, mientras que una baja disponibilidad puede favorecer precios superiores. Por tanto, integrar datos de previsión renovable puede mejorar la capacidad explicativa de los modelos.

Desde el punto de vista formativo, este trabajo permite aplicar conocimientos de programación, análisis de datos, estadistica, series temporales, aprendizaje automático y sistemas eléctricos. No se trata solo de entrenar un modelo, sino de construir un flujo completo: descarga de datos, limpieza, almacenamiento, generación de variables, entrenamiento, evaluación, inferencia y documentación. Esta visión integral es una de las principales motivaciones del proyecto.

### 2.2. Importancia de la predicción del precio eléctrico

La predicción del precio eléctrico tiene importancia tanto económica como operativa. En un mercado liberalizado, los agentes necesitan anticipar el comportamiento futuro de los precios para optimizar sus decisiones. Una comercializadora puede usar previsiones para definir estrategias de compra; un generador puede planificar ofertas; un consumidor industrial puede desplazar consumos; y un gestor de almacenamiento puede decidir cuándo cargar o descargar energía.

En el caso de consumidores intensivos en energía, incluso pequeñas mejoras en la predicción pueden traducirse en ahorros relevantes. Industrias con procesos flexibles pueden programar parte de su consumo en horas de menor precio. Del mismo modo, instalaciones con autoconsumo, baterías o gestión activa de demanda pueden beneficiarse de estimaciones del precio para optimizar su operación.

La predicción también es relevante para estudiar la integración de renovables. La eólica y la solar tienen costes variables reducidos, pero su producción depende de factores meteorológicos. Cuando su penetración es alta, los precios pueden experimentar caídas pronunciadas en determinadas franjas horarias. Anticipar estos patrones resulta útil para analizar el impacto de la transición energética y para diseñar mecanismos de gestión de flexibilidad.

Desde la perspectiva del operador y de los analistas del sistema, disponer de modelos de predicción contribuye a comprender mejor los factores que explican la formación de precios. Aunque un modelo de aprendizaje automático no sustituye al conocimiento técnico del mercado, puede complementar el análisis tradicional detectando relaciones entre variables, patrones recurrentes o situaciones atipicas.

También existe una dimensión académica. La predicción de precios eléctricos es un problema suficientemente complejo para evaluar distintos enfoques: modelos lineales, modelos basados en árboles, redes neuronales y técnicas específicas de series temporales. La existencia de datos públicos permite reproducir experimentos y comparar resultados, siempre que se documente adecuadamente la metodología.

La importancia de la predicción no implica que sea una tarea sencilla. El precio eléctrico puede verse afectado por eventos excepcionales, cambios regulatorios, indisponibilidades de generación, variaciones bruscas de demanda, cambios meteorológicos y tensión en mercados de combustibles. Por ello, el objetivo realista no es eliminar el error, sino reducirlo frente a referencias simples y comprender en que situaciones el modelo falla.

En este trabajo, la importancia de la predicción se refleja en la comparación con una baseline sencilla: el precio de 24 periodos antes. Esta referencia permite responder una pregunta fundamental: el modelo desarrollado, con sus variables y algoritmos, aporta información adicional respecto a repetir el precio del día anterior. Si la respuesta es positiva, el sistema demuestra valor predictivo inicial.

### 2.3. Problema a resolver

El problema que se aborda consiste en estimar el precio marginal del mercado eléctrico español para un periodo futuro a partir de información histórica y, opcionalmente, de variables externas de generación renovable. En términos de aprendizaje automático, se formula como un problema de regresión supervisada sobre una serie temporal.

La variable objetivo es:

```text
marginal_es
```

Esta variable representa el precio marginal español publicado por OMIE, expresado en euros por megavatio hora. A partir de una secuencia histórica de precios y variables asociadas, el modelo debe generar una estimación numérica para el siguiente periodo disponible.

El problema presenta varias dificultades. La primera es la naturaleza temporal de los datos. No se puede tratar cada observación como completamente independiente, ya que el precio actual suele estar relacionado con precios anteriores, patrones horarios y comportamiento semanal. Por ello, es necesario construir variables que representen adecuadamente esa dependencia temporal.

La segunda dificultad es la presencia de estacionalidad y ciclos. Existen patrones diarios, semanales y mensuales. Por ejemplo, el comportamiento del precio durante una madrugada puede ser diferente al de una hora punta; un domingo puede diferir de un día laborable; y determinados meses pueden presentar condiciones de demanda o generación distintas. El modelo debe disponer de variables que reflejen estos ciclos.

La tercera dificultad es la influencia de variables externas. El precio no depende solo de su propio histórico. Factores como la demanda, la producción renovable, el gas, el CO2 o las interconexiones pueden modificar la formación de precios. En este proyecto se aborda una primera aproximación incorporando previsión eólica y solar de ESIOS, aunque se reconoce que existen otras variables relevantes que quedan fuera del alcance inicial.

La cuarta dificultad es evitar fuga de información futura. En problemas temporales, una mala separación de datos puede producir resultados artificialmente optimistas. Si se entrena con datos posteriores al periodo evaluado, el modelo estaría usando información que no estaría disponible en una situación real. Por ello, la evaluación se realiza mediante una separación cronológica.

La quinta dificultad es la variabilidad del mercado. Hay días atípicos, festivos, episodios de precios extremos y periodos donde el comportamiento cambia. Un modelo puede funcionar bien en un rango temporal y peor en otro. Por tanto, el sistema debe permitir repetir experimentos con distintos periodos y comparar modelos de forma flexible.

El problema se concreta finalmente en desarrollar una aplicación que permita:

- descargar datos históricos de OMIE
- preparar un dataset supervisado
- añadir variables externas opcionales de ESIOS
- entrenar diferentes modelos
- comparar métricas de validación
- guardar el modelo seleccionado
- realizar inferencia para el siguiente periodo

### 2.4. Alcance del trabajo

El alcance del trabajo se centra en construir un prototipo funcional de predicción del precio del mercado diario eléctrico español. El sistema no pretende competir con herramientas profesionales de predicción energética ni cubrir todos los factores que influyen en el mercado. Su objetivo es académico y experimental.

El proyecto trabaja principalmente con datos de OMIE. Estos datos permiten obtener el precio marginal español para cada periodo. Se ha implementado un parser específico para los ficheros `MARGINALPDBC`, contemplando tanto días con 24 periodos como días con 96 periodos. Esta flexibilidad es importante porque el sistema eléctrico evoluciona hacia resoluciones temporales más finas.

Como extensión, se incorpora la posibilidad de usar datos de ESIOS. Esta funcionalidad es opcional porque requiere token de acceso. Cuando está activa, el sistema descarga previsiones de generación eólica, solar fotovoltaica y solar térmica. Estas variables se unen al dataset principal y se utilizan como entradas adicionales para los modelos.

En cuanto a modelos, el trabajo se limita a tres enfoques de machine learning supervisado: `RidgeCV`, `MLPRegressor` e `HistGradientBoostingRegressor`. La selección responde a la necesidad de comparar modelos de distinta naturaleza sin incrementar excesivamente la complejidad. Se deja fuera del alcance inicial el uso de modelos más avanzados como redes recurrentes, transformers o arquitecturas específicas para series temporales.

La evaluación se basa en una partición temporal simple entre entrenamiento y validación. No se implementa aún un sistema completo de backtesting mensual o rolling window, aunque se identifica como línea futura. Las métricas principales son MAE, RMSE y R2, junto con una comparación contra la baseline `lag 24`.

La aplicación práctica incluye tanto una interfaz de consola como una interfaz gráfica. La interfaz gráfica no busca ser una herramienta comercial, sino una forma clara de ejecutar y demostrar el flujo. Permite seleccionar fechas, elegir modelo, activar ESIOS, entrenar, consultar métricas y ejecutar inferencia.

Quedan fuera del alcance inicial varias mejoras importantes:

- incorporación de demanda prevista
- variables meteorológicas
- festivos nacionales y autonómicos
- precios de gas y CO2
- interconexiones internacionales
- predicción de todo el día siguiente
- optimización avanzada de hiperparámetros
- despliegue web o en nube

Estas limitaciones no invalidan el trabajo, sino que delimitan su ámbito. El objetivo es construir una base sólida y extensible que pueda ampliarse posteriormente.

### 2.5. Estructura del documento

El documento se organiza en capítulos que siguen la evolución natural del proyecto, desde el contexto teórico hasta la aplicación práctica y los resultados.

El primer capítulo presenta el resumen general del trabajo. En el se describe el contexto, los objetivos, la metodología, los resultados esperados y la aplicación desarrollada.

El segundo capítulo, correspondiente a está introducción, desarrolla la motivacion del estudio, la importancia de predecir el precio eléctrico, el problema a resolver, el alcance del trabajo y la estructura general del documento.

Los capítulos posteriores profundizan en el marco teórico, explicando el funcionamiento del mercado eléctrico español, el papel de OMIE, la función de ESIOS/REE y los factores que influyen en la formación del precio.

También se incluye un capítulo de estado del arte, donde se revisan enfoques clásicos y modernos para predicción de precios eléctricos, incluyendo modelos estadísticos, aprendizaje automático y redes neuronales.

Los capítulos dedicados a fuentes de datos y preparación explican como se obtienen, limpian y organizan los datos. Se detalla el uso de ficheros OMIE, la integración opcional con ESIOS y la construcción del dataset supervisado.

El capítulo de ingeniería de variables describe las transformaciones aplicadas a los datos: variables temporales, retardos, medias móviles, diferencias, ratios y variables renovables.

El capítulo de modelos presenta los algoritmos utilizados: baseline, Ridge, MLP y gradient boosting. Se justifican sus características y se explican sus ventajas e inconvenientes.

La metodología de evaluación se desarrolla en un capítulo específico, donde se presentan las métricas MAE, RMSE y R2, así como la importancia de la validación temporal.

La parte práctica se recoge en los capítulos de diseño e implementación. En ellos se describe la arquitectura del software, los módulos desarrollados, la interfaz gráfica, los comandos de consola y la gestión de artefactos.

Finalmente, el documento incluye capítulos de resultados, discusión, conclusiones y líneas futuras. En ellos se analizan los experimentos realizados, se interpretan los errores, se valoran las limitaciones del sistema y se proponen mejoras posteriores.

Esta estructura permite presentar el trabajo de forma progresiva: primero se explica el problema, después se describe la metodología, luego se muestra la implementación y finalmente se analizan los resultados.

