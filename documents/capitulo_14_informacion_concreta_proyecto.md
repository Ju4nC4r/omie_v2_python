# Capítulo 14. Información concreta del proyecto implementado

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 14.1. Nombre del proyecto: `omie_v2_python`

El proyecto implementado recibe el nombre de `omie_v2_python`. Este nombre identifica el repositorio local y remoto donde se ha desarrollado la aplicación práctica asociada al Trabajo Fin de Grado. La denominación refleja dos ideas principales: por un lado, el uso de datos procedentes de OMIE; por otro, la implementación en Python de una segunda versión o evolución del sistema.

El objetivo de `omie_v2_python` es construir una herramienta capaz de descargar datos del mercado eléctrico español, generar variables de entrenamiento, entrenar varios modelos predictivos y realizar inferencias sobre el precio del siguiente periodo disponible. El proyecto no se limita a un cuaderno experimental, sino que se organiza como un paquete Python con comandos reutilizables, interfaz gráfica y documentación.

La existencia de un nombre de proyecto concreto facilita la trazabilidad. Permite referirse a la aplicación de forma unívoca dentro del documento, en el repositorio Git y en las instrucciones de ejecución. También ayuda a diferenciar el trabajo teórico del TFG de la implementación práctica que lo acompaña.

En el contexto del TFG, `omie_v2_python` representa el resultado aplicado del estudio. Los capítulos anteriores describen el mercado, las fuentes de datos, la preparación y las variables; este capítulo fija la información técnica concreta del software construido.

### 14.2. Lenguaje utilizado: Python

El lenguaje utilizado para implementar el proyecto es Python. La elección de Python se justifica por su amplio uso en ciencia de datos, aprendizaje automático y automatización de procesos. Dispone de bibliotecas maduras para tratamiento de datos, descarga HTTP, modelado predictivo, serialización de modelos y generación de gráficas.

En este proyecto, Python se utiliza para todas las fases del flujo. La descarga de datos OMIE y ESIOS se realiza mediante peticiones HTTP. El parseo y transformación de datos se apoya en pandas. El cálculo numérico utiliza numpy. El entrenamiento de modelos se realiza con scikit-learn. La serialización emplea joblib. Las gráficas de validación se generan con matplotlib. La interfaz gráfica se construye con Tkinter, disponible en el ecosistema estándar de Python.

Python también facilita la organización modular. El código se divide en ficheros especializados: descarga y parseo de datos, integración con ESIOS, generación de variables, entrenamiento, inferencia e interfaz gráfica. Esta separación hace que el proyecto sea más mantenible y permite explicar cada parte en capítulos independientes del TFG.

Otra ventaja de Python es su accesibilidad académica. Es un lenguaje habitual en asignaturas de programación, análisis de datos e inteligencia artificial. Esto permite que el proyecto sea comprensible para estudiantes y evaluadores, sin requerir herramientas propietarias ni entornos complejos.

El proyecto exige Python `>=3.10`, lo que permite utilizar características modernas del lenguaje y mantener compatibilidad con versiones actuales. Esta versión mínima queda declarada en el fichero `pyproject.toml`, junto con las dependencias necesarias.

### 14.3. Entorno virtual: `.venv`

El proyecto se ejecuta dentro de un entorno virtual denominado `.venv`. Un entorno virtual permite aislar las dependencias del proyecto respecto al Python global del sistema. Esto es especialmente importante en trabajos reproducibles, ya que evita conflictos entre versiones de bibliotecas instaladas para otros proyectos.

El uso de `.venv` permite instalar las dependencias necesarias sin modificar la configuración global del equipo. Una vez creado y activado el entorno, se instalan paquetes como pandas, numpy, requests, scikit-learn, joblib y matplotlib. También se puede instalar el proyecto en modo editable, de manera que los comandos definidos en `pyproject.toml` queden disponibles.

El flujo habitual consiste en crear el entorno, activarlo, instalar dependencias y ejecutar la aplicación. De forma conceptual, el proceso es:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Después de estos pasos, el usuario puede ejecutar comandos como `omie-price-gui`, `omie-price-train` y `omie-price-predict`. Esto mejora la ergonomia del proyecto, porque no es necesario invocar directamente los ficheros Python internos.

El directorio `.venv` no se incluye en Git. Es un artefacto local que cada usuario puede regenerar. El repositorio debe contener el código fuente y la declaración de dependencias, no el entorno virtual completo. Esta decisión reduce el tamaño del repositorio y sigue buenas prácticas de desarrollo.

### 14.4. Paquete principal: `omie_price_nn`

El paquete principal del proyecto es `omie_price_nn`. Este paquete se encuentra dentro del directorio `src/`, siguiendo una estructura habitual en proyectos Python modernos. La organización mediante `src/` ayuda a evitar importaciones accidentales desde el directorio raíz y favorece una instalación más limpia del paquete.

Dentro de `omie_price_nn` se agrupan los módulos principales de la aplicación. El módulo `data.py` contiene funciones para descargar y parsear datos OMIE. El módulo `esios.py` gestiona la descarga y unión de variables renovables desde ESIOS. El módulo `features.py` construye las variables de entrada y el dataset supervisado. El módulo `train.py` entrena los modelos y calcula métricas. El módulo `predict.py` realiza inferencia. El módulo `gui.py` implementa la interfaz gráfica.

Esta división permite separar responsabilidades. Cada módulo tiene un cometido claro y puede estudiarse de forma independiente. Por ejemplo, si se quiere mejorar la descarga de datos OMIE, se trabaja principalmente en `data.py`. Si se quiere añadir una nueva variable meteorológica, probablemente se ampliaría la lógica de datos externos y generación de variables.

El nombre `omie_price_nn` hace referencia al precio OMIE y a la red neuronal, que era una de las ideas iniciales del proyecto. Aunque la aplicación ha evolucionado para incluir varios modelos, el nombre conserva esa orientación original hacia la predicción mediante aprendizaje automático.

El paquete está definido en `pyproject.toml` mediante la configuración de setuptools. Esto permite instalarlo como paquete local y exponer comandos de consola. La decisión de empaquetar el proyecto, en lugar de mantener scripts sueltos, aporta profesionalidad y facilita la reproducibilidad.

### 14.5. Repositorio GitHub: `https://github.com/Ju4nC4r/omie_v2_python.git`

El repositorio remoto configurado para el proyecto es `https://github.com/Ju4nC4r/omie_v2_python.git`. Este repositorio permite alojar el código y la documentación en GitHub, facilitando su consulta, versionado y posible entrega. Durante el desarrollo también se configuró acceso por SSH, aunque las operaciones de subida dependen de que la clave SSH local esté autorizada en GitHub.

El uso de Git y GitHub cumple varias funciones. En primer lugar, permite mantener un historial de cambios. Cada avance relevante, como la creación de la interfaz gráfica, la inclusión de modelos, la integración con ESIOS o la redaccion de capítulos, queda registrado mediante commits. En segundo lugar, facilita recuperar versiones anteriores si fuera necesario. En tercer lugar, permite compartir el proyecto.

El repositorio no debe contener datos descargados, modelos entrenados ni entornos virtuales. Estos elementos están excluidos mediante `.gitignore`. Esta práctica es adecuada porque los datos y modelos pueden regenerarse, ocupar espacio o depender de ejecuciones concretas. Lo importante es versiónar el código que permite producirlos.

Desde el punto de vista documental, la existencia de un repositorio remoto refuerza la trazabilidad del TFG. No solo se entrega una memoria, sino también una implementación versiónada. Esto permite verificar que la aplicación descrita en el documento existe y puede ejecutarse siguiendo las instrucciones.

### 14.6. Comando de interfaz gráfica: `omie-price-gui`

El comando `omie-price-gui` ejecuta la interfaz gráfica del proyecto. Esta interfaz está implementada con Tkinter y permite manejar la aplicación desde una ventana. Su objetivo es hacer visible el flujo completo del modelo: extracción de datos, preparación, entrenamiento, test e inferencia.

La interfaz incluye campos para indicar fechas de inicio y fin, un selector de modelo, una opción para activar ESIOS y un campo para introducir el token. También muestra logs de ejecución y progreso, lo que ayuda a entender en que fase se encuentra el proceso. Esta información es importante porque algunos entrenamientos, especialmente `mlp` o `auto`, pueden tardar más que otros.

El comando queda definido en `pyproject.toml` dentro de la sección `[project.scripts]`. Esto permite invocarlo directamente después de instalar el paquete en el entorno virtual. La entrada apunta a `omie_price_nn.gui:main`, que es la función principal de la interfaz.

La existencia de una GUI aporta valor didáctico. Un evaluador puede ejecutar la aplicación y ver las fases del modelo sin tener que recordar comandos. También permite presentar el proyecto como una herramienta completa, no solo como una colección de scripts.

### 14.7. Comando de entrenamiento: `omie-price-train`

El comando `omie-price-train` ejecuta el entrenamiento desde consola. Permite indicar fecha inicial, fecha final, modelo seleccionado y usó opcional de ESIOS. Es la via más directa para reproducir experimentos y comparar resultados.

Un ejemplo de usó es:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

El comando acepta modelos como `ridge`, `mlp`, `hist_gradient_boosting` y `auto`. Cuando se utiliza `auto`, el programa entrena varios candidatos y selecciona el de menor MAE en validación temporal. Si se desea incorporar ESIOS, se añade `--include-esios` y se proporciona un token mediante `--esios-token` o mediante la variable de entorno `ESIOS_TOKEN`.

Durante el entrenamiento se descargan o reutilizan datos, se generan variables, se separa entrenamiento y validación, se ajustan modelos y se calculan métricas. Al finalizar, se guarda el modelo y se genera una gráfica. Este comando es especialmente útil para documentar experimentos en el TFG, porque permite escribir exactamente qué rango y qué modelo se utilizaron.

La interfaz gráfica llama internamente a la misma lógica de entrenamiento. Esto evita duplicar comportamiento y mantiene coherencia entre usó grafico y usó por consola.

### 14.8. Comando de predicción: `omie-price-predict`

El comando `omie-price-predict` realiza la inferencia del siguiente periodo disponible usando el modelo entrenado. Carga el modelo guardado, lee el dataset procesado y genera las variables necesarias para el siguiente `timestamp`. Después muestra la predicción en EUR/MWh.

Este comando completa el ciclo de machine learning. Entrenar un modelo y obtener métricas históricas es importante, pero una aplicación predictiva debe ser capaz de generar una estimación futura. `omie-price-predict` permite realizar esta fase de forma sencilla y repetible.

La predicción depende del modelo guardado en `models/omie_model.joblib` y de los datos procesados disponibles. Si el modelo fue entrenado con variables ESIOS, el dataset usado para inferencia debe conservar esas columnas. Por eso el flujo normal guarda el dataset enriquecido cuando se usa ESIOS.

El comando también comprueba que exista suficiente histórico para construir las variables necesarias. Si faltan retardos o medias móviles, la predicción no puede realizarse correctamente. Esta comprobación evita devolver resultados basados en información incompleta.

### 14.9. Modelo guardado: `models/omie_model.joblib`

El modelo entrenado se guarda en `models/omie_model.joblib`. Este fichero contiene el artefacto serializado que se utiliza posteriormente para inferencia. Guardar el modelo evita tener que reentrenar cada vez que se quiera predecir el siguiente periodo.

La serialización se realiza con joblib, una biblioteca habitual en proyectos de scikit-learn. Joblib permite guardar objetos Python como pipelines, modelos entrenados, escaladores y metadatos asociados. En este proyecto, el modelo guardado incluye la información necesaria para reproducir la predicción con la misma lista de variables usada durante el entrenamiento.

El directorio `models/` se considera un directorio de artefactos generados. No se versióna en Git porque los modelos pueden variar según el rango de fechas, el algoritmo seleccionado, las variables ESIOS o la versión de dependencias. Lo que se versióna es el código que permite generar el modelo.

La existencia de `models/omie_model.joblib` permite separar entrenamiento e inferencia. Un usuario puede entrenar una vez, revisar métricas y después realizar predicciones sin repetir todo el proceso. Esta separación es una práctica habitual en aplicaciones de machine learning.

### 14.10. Gráfica generada: `models/validation_plot.png`

Además del modelo, la aplicación genera una gráfica de validación en `models/validation_plot.png`. Esta gráfica compara visualmente valores reales, predicciones del modelo y baseline en el tramo de validación. Su objetivo es complementar las métricas numéricas con una representación visual.

Las métricas como MAE, RMSE y R2 resumen el comportamiento del modelo, pero no muestran dónde se producen los errores. Una gráfica permite observar si el modelo sigue bien la forma general de la serie, si suaviza demasiado los picos, si falla en determinados tramos o si se separa del valor real en momentos concretos.

La gráfica se guarda como artefacto local, igual que el modelo. No se incluye en Git por defecto, porque depende de cada ejecución. Sin embargo, puede utilizarse en la memoria del TFG para ilustrar resultados concretos si se desea fijar un experimento.

El fichero `validation_plot.png` aporta valor durante la depuración. Si las métricas parecen extrañas, la gráfica ayuda a detectar problemas de alineación temporal, predicciones planas, errores sistemáticos o comportamiento anómalo del baseline. Por tanto, no es solo una salida estética, sino una herramienta de análisis.

En conjunto, la información concreta del proyecto muestra que la aplicación está organizada como un software ejecutable: tiene nombre, paquete, entorno, comandos, artefactos, repositorio y una estructura clara. Esta concrecion permite pasar de la descripción teórica a una implementación verificable.
