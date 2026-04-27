# Capítulo 19. Planificación del proyecto

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 19.1. Fases del desarrollo

El desarrollo del proyecto se organizó de forma incremental. En lugar de intentar construir desde el principio una aplicación completa, se comenzó con una versión sencilla capaz de descargar datos de OMIE, preparar una serie temporal y entrenar un primer modelo. A partir de esa base se fueron incorporando mejoras funcionales, técnicas y documentales.

La primera fase consistio en definir el objetivo del trabajo: predecir el precio del mercado eléctrico español a partir de datos públicos. En esta fase se eligio Python como lenguaje principal y se preparo un entorno virtual `.venv` para aislar dependencias.

La segunda fase fue la obtención de datos. Se implementó la descarga automatizada de ficheros `MARGINALPDBC` de OMIE, su almacenamiento en cache y su parseo en un formato tabular. Esta fase era imprescindible porque todo el modelo depende de disponer de una serie histórica fiable.

La tercera fase fue la preparación del dataset supervisado. Se construyeron timestamps, se ordenaron observaciones, se generaron variables temporales y se transformo el problema en una tarea de regresión supervisada.

La cuarta fase fue el entrenamiento inicial. Aunque el planteamiento original se centraba en una red neuronal sencilla, el proyecto evolucióno para incluir varios modelos: Ridge, MLP e HistGradientBoosting. También se incorporo el modo `auto`, que compara candidatos y selecciona el mejor según MAE.

La quinta fase fue la interfaz gráfica. Se desarrolló una GUI con Tkinter para ejecutar extracción, preparación, entrenamiento, test e inferencia. Esta interfaz facilitó la demostración del proyecto y mejoró la experiencia de usuario.

La sexta fase fue la integración opcional de ESIOS. Se añadió la posibilidad de incorporar previsiones de generación eólica, solar fotovoltaica y solar térmica. Esta ampliación acercó el modelo a variables físicas relevantes del sistema eléctrico.

La séptima fase fue la documentación. Se amplio el README, se creo el directorio `documents/`, se generó el índice del Proyecto y se desarrollaron los capítulos de la memoria en ficheros Markdown separados.

### 19.2. Cronograma estimado

El proyecto puede representarse mediante un cronograma aproximado por bloques de trabajo. Aunque el desarrollo real se realizó de forma iterativa, la planificación académica puede organizarse en etapas.

Una planificación razonable sería:

| Fase | Duración estimada | Resultado |
| --- | ---: | --- |
| Análisis inicial | 1 semana | Definicion del problema y alcance |
| Entorno y estructura | 1 semana | Proyecto Python con `.venv` |
| Descarga OMIE | 1-2 semanas | Módulo `data.py` funcional |
| Preparación de variables | 1-2 semanas | Dataset supervisado |
| Modelos predictivos | 2 semanas | Ridge, MLP, boosting y modo `auto` |
| Evaluación | 1 semana | MAE, RMSE, R2 y baseline |
| Interfaz gráfica | 1-2 semanas | GUI con fases del flujo |
| Integración ESIOS | 1-2 semanas | Variables renovables opcionales |
| Documentación técnica | 2 semanas | README y resumen del desarrollo |
| Memoria Proyecto | 4-6 semanas | Capítulos del documento |
| Revisión final | 1-2 semanas | Correcciones, figuras y anexos |

Este cronograma muestra que el proyecto combina tareas de software, datos, experimentación y redaccion académica. No se trata solo de entrenar un modelo, sino de construir un sistema reproducible y explicarlo adecuadamente.

### 19.3. Herramientas utilizadas

Las herramientas principales utilizadas fueron Python, Git, GitHub, OMIE, ESIOS, scikit-learn, pandas, numpy, matplotlib, joblib y Tkinter.

Python fue el lenguaje de implementación. pandas se utilizó para manipular datos tabulares y series temporales. numpy permitió calcular variables cíclicas. requests se usó para descargar datos desde OMIE y ESIOS. scikit-learn proporcionó los modelos de aprendizaje automático y las métricas. joblib se empleó para guardar el modelo entrenado. matplotlib generó la gráfica de validación.

Tkinter se utilizó para la interfaz gráfica. Aunque existen frameworks más modernos, Tkinter tiene la ventaja de estar disponible en el ecosistema Python y ser suficiente para una aplicación local de demostración.

Git se usó para controlar versiones. El repositorio remoto de GitHub se configuró como destino para públicar el proyecto, aunque la subida dependía de resolver la autenticación SSH. El uso de commits por hitos permitió mantener trazabilidad del desarrollo.

Markdown se utilizó para la documentación. Tanto el README como los capítulos del Proyecto se redactaron en este formato, lo que facilita versionado, lectura y futura conversión a otros formatos.

### 19.4. Riesgos identificados

Durante la planificación y desarrollo se identificaron varios riesgos.

El primer riesgo fue la disponibilidad de datos. Aunque OMIE publica datos oficiales, algunos ficheros pueden no estar disponibles para fechas concretas o puede haber fallos de red. Para mitigarlo, el programa registra fallos por día y continúa si existen otros datos válidos.

El segundo riesgo fue la calidad y alineación temporal de datos. La combinación de datos horarios, cuarto-horarios y previsiones ESIOS puede producir desajustes. Se mitigó mediante normalización de `timestamp` y unión temporal con tolerancia.

El tercer riesgo fue el sobreajuste. El proyecto genera muchas variables y utiliza modelos flexibles. Para reducir este riesgo se usó validación temporal, regularización y comparación contra baseline.

El cuarto riesgo fue la usabilidad. El entrenamiento podía parecer bloqueado en ejecuciones largas. Se mitigó incorporando logs y barra de progreso en la GUI.

El quinto riesgo fue la autenticación con GitHub. Los intentos de subida fallaron por clave SSH no autorizada. Se documento como configurar SSH en macOS.

El sexto riesgo fue el alcance. El problema de predecir precios eléctricos puede crecer mucho si se incorporan demanda, meteorología, combustibles, CO2 e interconexiones. Se delimitó el proyecto para mantener una versión funcional y dejar mejoras como líneas futuras.

### 19.5. Gestión del repositorio

El repositorio se gestionó con Git. Cada avance importante se guardó en un commit. Esto incluye la creación inicial de la aplicación, la interfaz gráfica, la selección de modelos, la integración ESIOS, la ampliación del README y el desarrollo de capítulos del Proyecto.

La politica seguida fue no versiónar artefactos generados como datos, modelos, caches o entornos virtuales. Estos elementos se excluyeron mediante `.gitignore`. El repositorio contiene código, configuración y documentación; los datos y modelos se regeneran ejecutando la aplicación.

El repositorio remoto configurado es:

```text
https://github.com/Ju4nC4r/omie_v2_python.git
```

También se trabajo con configuración SSH:

```text
git@github.com:Ju4nC4r/omie_v2_python.git
```

Para completar la públicacion remota es necesario que la clave SSH del equipo este registrada en GitHub. Una vez resuelto, los commits locales pueden subirse con `git push`.

La gestión del repositorio aporta trazabilidad al Proyecto. Permite demostrar que el proyecto se desarrolló de forma incremental y que cada funcionalidad queda registrada históricamente.
