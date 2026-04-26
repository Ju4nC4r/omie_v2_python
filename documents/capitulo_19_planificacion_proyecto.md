# Capitulo 19. Planificacion del proyecto

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 19.1. Fases del desarrollo

El desarrollo del proyecto se organizo de forma incremental. En lugar de intentar construir desde el principio una aplicacion completa, se comenzo con una version sencilla capaz de descargar datos de OMIE, preparar una serie temporal y entrenar un primer modelo. A partir de esa base se fueron incorporando mejoras funcionales, tecnicas y documentales.

La primera fase consistio en definir el objetivo del trabajo: predecir el precio del mercado electrico espanol a partir de datos publicos. En esta fase se eligio Python como lenguaje principal y se preparo un entorno virtual `.venv` para aislar dependencias.

La segunda fase fue la obtencion de datos. Se implemento la descarga automatizada de ficheros `MARGINALPDBC` de OMIE, su almacenamiento en cache y su parseo en un formato tabular. Esta fase era imprescindible porque todo el modelo depende de disponer de una serie historica fiable.

La tercera fase fue la preparacion del dataset supervisado. Se construyeron timestamps, se ordenaron observaciones, se generaron variables temporales y se transformo el problema en una tarea de regresion supervisada.

La cuarta fase fue el entrenamiento inicial. Aunque el planteamiento original se centraba en una red neuronal sencilla, el proyecto evoluciono para incluir varios modelos: Ridge, MLP e HistGradientBoosting. Tambien se incorporo el modo `auto`, que compara candidatos y selecciona el mejor segun MAE.

La quinta fase fue la interfaz grafica. Se desarrollo una GUI con Tkinter para ejecutar extraccion, preparacion, entrenamiento, test e inferencia. Esta interfaz facilito la demostracion del proyecto y mejoro la experiencia de usuario.

La sexta fase fue la integracion opcional de ESIOS. Se anadio la posibilidad de incorporar previsiones de generacion eolica, solar fotovoltaica y solar termica. Esta ampliacion acerco el modelo a variables fisicas relevantes del sistema electrico.

La septima fase fue la documentacion. Se amplio el README, se creo el directorio `documents/`, se genero el indice del TFG y se desarrollaron los capitulos de la memoria en ficheros Markdown separados.

### 19.2. Cronograma estimado

El proyecto puede representarse mediante un cronograma aproximado por bloques de trabajo. Aunque el desarrollo real se realizo de forma iterativa, la planificacion academica puede organizarse en etapas.

Una planificacion razonable seria:

| Fase | Duracion estimada | Resultado |
| --- | ---: | --- |
| Analisis inicial | 1 semana | Definicion del problema y alcance |
| Entorno y estructura | 1 semana | Proyecto Python con `.venv` |
| Descarga OMIE | 1-2 semanas | Modulo `data.py` funcional |
| Preparacion de variables | 1-2 semanas | Dataset supervisado |
| Modelos predictivos | 2 semanas | Ridge, MLP, boosting y modo `auto` |
| Evaluacion | 1 semana | MAE, RMSE, R2 y baseline |
| Interfaz grafica | 1-2 semanas | GUI con fases del flujo |
| Integracion ESIOS | 1-2 semanas | Variables renovables opcionales |
| Documentacion tecnica | 2 semanas | README y resumen del desarrollo |
| Memoria TFG | 4-6 semanas | Capitulos del documento |
| Revision final | 1-2 semanas | Correcciones, figuras y anexos |

Este cronograma muestra que el proyecto combina tareas de software, datos, experimentacion y redaccion academica. No se trata solo de entrenar un modelo, sino de construir un sistema reproducible y explicarlo adecuadamente.

### 19.3. Herramientas utilizadas

Las herramientas principales utilizadas fueron Python, Git, GitHub, OMIE, ESIOS, scikit-learn, pandas, numpy, matplotlib, joblib y Tkinter.

Python fue el lenguaje de implementacion. pandas se utilizo para manipular datos tabulares y series temporales. numpy permitio calcular variables ciclicas. requests se uso para descargar datos desde OMIE y ESIOS. scikit-learn proporciono los modelos de aprendizaje automatico y las metricas. joblib se empleo para guardar el modelo entrenado. matplotlib genero la grafica de validacion.

Tkinter se utilizo para la interfaz grafica. Aunque existen frameworks mas modernos, Tkinter tiene la ventaja de estar disponible en el ecosistema Python y ser suficiente para una aplicacion local de demostracion.

Git se uso para controlar versiones. El repositorio remoto de GitHub se configuro como destino para publicar el proyecto, aunque la subida dependia de resolver la autenticacion SSH. El uso de commits por hitos permitio mantener trazabilidad del desarrollo.

Markdown se utilizo para la documentacion. Tanto el README como los capitulos del TFG se redactaron en este formato, lo que facilita versionado, lectura y futura conversion a otros formatos.

### 19.4. Riesgos identificados

Durante la planificacion y desarrollo se identificaron varios riesgos.

El primer riesgo fue la disponibilidad de datos. Aunque OMIE publica datos oficiales, algunos ficheros pueden no estar disponibles para fechas concretas o puede haber fallos de red. Para mitigarlo, el programa registra fallos por dia y continua si existen otros datos validos.

El segundo riesgo fue la calidad y alineacion temporal de datos. La combinacion de datos horarios, cuarto-horarios y previsiones ESIOS puede producir desajustes. Se mitigo mediante normalizacion de `timestamp` y union temporal con tolerancia.

El tercer riesgo fue el sobreajuste. El proyecto genera muchas variables y utiliza modelos flexibles. Para reducir este riesgo se uso validacion temporal, regularizacion y comparacion contra baseline.

El cuarto riesgo fue la usabilidad. El entrenamiento podia parecer bloqueado en ejecuciones largas. Se mitigo incorporando logs y barra de progreso en la GUI.

El quinto riesgo fue la autenticacion con GitHub. Los intentos de subida fallaron por clave SSH no autorizada. Se documento como configurar SSH en macOS.

El sexto riesgo fue el alcance. El problema de predecir precios electricos puede crecer mucho si se incorporan demanda, meteorologia, combustibles, CO2 e interconexiones. Se delimito el proyecto para mantener una version funcional y dejar mejoras como lineas futuras.

### 19.5. Gestion del repositorio

El repositorio se gestiono con Git. Cada avance importante se guardo en un commit. Esto incluye la creacion inicial de la aplicacion, la interfaz grafica, la seleccion de modelos, la integracion ESIOS, la ampliacion del README y el desarrollo de capitulos del TFG.

La politica seguida fue no versionar artefactos generados como datos, modelos, caches o entornos virtuales. Estos elementos se excluyeron mediante `.gitignore`. El repositorio contiene codigo, configuracion y documentacion; los datos y modelos se regeneran ejecutando la aplicacion.

El repositorio remoto configurado es:

```text
https://github.com/Ju4nC4r/omie_v2_python.git
```

Tambien se trabajo con configuracion SSH:

```text
git@github.com:Ju4nC4r/omie_v2_python.git
```

Para completar la publicacion remota es necesario que la clave SSH del equipo este registrada en GitHub. Una vez resuelto, los commits locales pueden subirse con `git push`.

La gestion del repositorio aporta trazabilidad al TFG. Permite demostrar que el proyecto se desarrollo de forma incremental y que cada funcionalidad queda registrada historicamente.
