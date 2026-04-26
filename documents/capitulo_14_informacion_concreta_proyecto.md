# Capitulo 14. Informacion concreta del proyecto implementado

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 14.1. Nombre del proyecto: `omie_v2_python`

El proyecto implementado recibe el nombre de `omie_v2_python`. Este nombre identifica el repositorio local y remoto donde se ha desarrollado la aplicacion practica asociada al Trabajo Fin de Grado. La denominacion refleja dos ideas principales: por un lado, el uso de datos procedentes de OMIE; por otro, la implementacion en Python de una segunda version o evolucion del sistema.

El objetivo de `omie_v2_python` es construir una herramienta capaz de descargar datos del mercado electrico espanol, generar variables de entrenamiento, entrenar varios modelos predictivos y realizar inferencias sobre el precio del siguiente periodo disponible. El proyecto no se limita a un cuaderno experimental, sino que se organiza como un paquete Python con comandos reutilizables, interfaz grafica y documentacion.

La existencia de un nombre de proyecto concreto facilita la trazabilidad. Permite referirse a la aplicacion de forma univoca dentro del documento, en el repositorio Git y en las instrucciones de ejecucion. Tambien ayuda a diferenciar el trabajo teorico del TFG de la implementacion practica que lo acompana.

En el contexto del TFG, `omie_v2_python` representa el resultado aplicado del estudio. Los capitulos anteriores describen el mercado, las fuentes de datos, la preparacion y las variables; este capitulo fija la informacion tecnica concreta del software construido.

### 14.2. Lenguaje utilizado: Python

El lenguaje utilizado para implementar el proyecto es Python. La eleccion de Python se justifica por su amplio uso en ciencia de datos, aprendizaje automatico y automatizacion de procesos. Dispone de bibliotecas maduras para tratamiento de datos, descarga HTTP, modelado predictivo, serializacion de modelos y generacion de graficas.

En este proyecto, Python se utiliza para todas las fases del flujo. La descarga de datos OMIE y ESIOS se realiza mediante peticiones HTTP. El parseo y transformacion de datos se apoya en pandas. El calculo numerico utiliza numpy. El entrenamiento de modelos se realiza con scikit-learn. La serializacion emplea joblib. Las graficas de validacion se generan con matplotlib. La interfaz grafica se construye con Tkinter, disponible en el ecosistema estandar de Python.

Python tambien facilita la organizacion modular. El codigo se divide en ficheros especializados: descarga y parseo de datos, integracion con ESIOS, generacion de variables, entrenamiento, inferencia e interfaz grafica. Esta separacion hace que el proyecto sea mas mantenible y permite explicar cada parte en capitulos independientes del TFG.

Otra ventaja de Python es su accesibilidad academica. Es un lenguaje habitual en asignaturas de programacion, analisis de datos e inteligencia artificial. Esto permite que el proyecto sea comprensible para estudiantes y evaluadores, sin requerir herramientas propietarias ni entornos complejos.

El proyecto exige Python `>=3.10`, lo que permite utilizar caracteristicas modernas del lenguaje y mantener compatibilidad con versiones actuales. Esta version minima queda declarada en el fichero `pyproject.toml`, junto con las dependencias necesarias.

### 14.3. Entorno virtual: `.venv`

El proyecto se ejecuta dentro de un entorno virtual denominado `.venv`. Un entorno virtual permite aislar las dependencias del proyecto respecto al Python global del sistema. Esto es especialmente importante en trabajos reproducibles, ya que evita conflictos entre versiones de bibliotecas instaladas para otros proyectos.

El uso de `.venv` permite instalar las dependencias necesarias sin modificar la configuracion global del equipo. Una vez creado y activado el entorno, se instalan paquetes como pandas, numpy, requests, scikit-learn, joblib y matplotlib. Tambien se puede instalar el proyecto en modo editable, de manera que los comandos definidos en `pyproject.toml` queden disponibles.

El flujo habitual consiste en crear el entorno, activarlo, instalar dependencias y ejecutar la aplicacion. De forma conceptual, el proceso es:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Despues de estos pasos, el usuario puede ejecutar comandos como `omie-price-gui`, `omie-price-train` y `omie-price-predict`. Esto mejora la ergonomia del proyecto, porque no es necesario invocar directamente los ficheros Python internos.

El directorio `.venv` no se incluye en Git. Es un artefacto local que cada usuario puede regenerar. El repositorio debe contener el codigo fuente y la declaracion de dependencias, no el entorno virtual completo. Esta decision reduce el tamano del repositorio y sigue buenas practicas de desarrollo.

### 14.4. Paquete principal: `omie_price_nn`

El paquete principal del proyecto es `omie_price_nn`. Este paquete se encuentra dentro del directorio `src/`, siguiendo una estructura habitual en proyectos Python modernos. La organizacion mediante `src/` ayuda a evitar importaciones accidentales desde el directorio raiz y favorece una instalacion mas limpia del paquete.

Dentro de `omie_price_nn` se agrupan los modulos principales de la aplicacion. El modulo `data.py` contiene funciones para descargar y parsear datos OMIE. El modulo `esios.py` gestiona la descarga y union de variables renovables desde ESIOS. El modulo `features.py` construye las variables de entrada y el dataset supervisado. El modulo `train.py` entrena los modelos y calcula metricas. El modulo `predict.py` realiza inferencia. El modulo `gui.py` implementa la interfaz grafica.

Esta division permite separar responsabilidades. Cada modulo tiene un cometido claro y puede estudiarse de forma independiente. Por ejemplo, si se quiere mejorar la descarga de datos OMIE, se trabaja principalmente en `data.py`. Si se quiere anadir una nueva variable meteorologica, probablemente se ampliaria la logica de datos externos y generacion de variables.

El nombre `omie_price_nn` hace referencia al precio OMIE y a la red neuronal, que era una de las ideas iniciales del proyecto. Aunque la aplicacion ha evolucionado para incluir varios modelos, el nombre conserva esa orientacion original hacia la prediccion mediante aprendizaje automatico.

El paquete esta definido en `pyproject.toml` mediante la configuracion de setuptools. Esto permite instalarlo como paquete local y exponer comandos de consola. La decision de empaquetar el proyecto, en lugar de mantener scripts sueltos, aporta profesionalidad y facilita la reproducibilidad.

### 14.5. Repositorio GitHub: `https://github.com/Ju4nC4r/omie_v2_python.git`

El repositorio remoto configurado para el proyecto es `https://github.com/Ju4nC4r/omie_v2_python.git`. Este repositorio permite alojar el codigo y la documentacion en GitHub, facilitando su consulta, versionado y posible entrega. Durante el desarrollo tambien se configuro acceso por SSH, aunque las operaciones de subida dependen de que la clave SSH local este autorizada en GitHub.

El uso de Git y GitHub cumple varias funciones. En primer lugar, permite mantener un historial de cambios. Cada avance relevante, como la creacion de la interfaz grafica, la inclusion de modelos, la integracion con ESIOS o la redaccion de capitulos, queda registrado mediante commits. En segundo lugar, facilita recuperar versiones anteriores si fuera necesario. En tercer lugar, permite compartir el proyecto.

El repositorio no debe contener datos descargados, modelos entrenados ni entornos virtuales. Estos elementos estan excluidos mediante `.gitignore`. Esta practica es adecuada porque los datos y modelos pueden regenerarse, ocupar espacio o depender de ejecuciones concretas. Lo importante es versionar el codigo que permite producirlos.

Desde el punto de vista documental, la existencia de un repositorio remoto refuerza la trazabilidad del TFG. No solo se entrega una memoria, sino tambien una implementacion versionada. Esto permite verificar que la aplicacion descrita en el documento existe y puede ejecutarse siguiendo las instrucciones.

### 14.6. Comando de interfaz grafica: `omie-price-gui`

El comando `omie-price-gui` ejecuta la interfaz grafica del proyecto. Esta interfaz esta implementada con Tkinter y permite manejar la aplicacion desde una ventana. Su objetivo es hacer visible el flujo completo del modelo: extraccion de datos, preparacion, entrenamiento, test e inferencia.

La interfaz incluye campos para indicar fechas de inicio y fin, un selector de modelo, una opcion para activar ESIOS y un campo para introducir el token. Tambien muestra logs de ejecucion y progreso, lo que ayuda a entender en que fase se encuentra el proceso. Esta informacion es importante porque algunos entrenamientos, especialmente `mlp` o `auto`, pueden tardar mas que otros.

El comando queda definido en `pyproject.toml` dentro de la seccion `[project.scripts]`. Esto permite invocarlo directamente despues de instalar el paquete en el entorno virtual. La entrada apunta a `omie_price_nn.gui:main`, que es la funcion principal de la interfaz.

La existencia de una GUI aporta valor didactico. Un evaluador puede ejecutar la aplicacion y ver las fases del modelo sin tener que recordar comandos. Tambien permite presentar el proyecto como una herramienta completa, no solo como una coleccion de scripts.

### 14.7. Comando de entrenamiento: `omie-price-train`

El comando `omie-price-train` ejecuta el entrenamiento desde consola. Permite indicar fecha inicial, fecha final, modelo seleccionado y uso opcional de ESIOS. Es la via mas directa para reproducir experimentos y comparar resultados.

Un ejemplo de uso es:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

El comando acepta modelos como `ridge`, `mlp`, `hist_gradient_boosting` y `auto`. Cuando se utiliza `auto`, el programa entrena varios candidatos y selecciona el de menor MAE en validacion temporal. Si se desea incorporar ESIOS, se anade `--include-esios` y se proporciona un token mediante `--esios-token` o mediante la variable de entorno `ESIOS_TOKEN`.

Durante el entrenamiento se descargan o reutilizan datos, se generan variables, se separa entrenamiento y validacion, se ajustan modelos y se calculan metricas. Al finalizar, se guarda el modelo y se genera una grafica. Este comando es especialmente util para documentar experimentos en el TFG, porque permite escribir exactamente que rango y que modelo se utilizaron.

La interfaz grafica llama internamente a la misma logica de entrenamiento. Esto evita duplicar comportamiento y mantiene coherencia entre uso grafico y uso por consola.

### 14.8. Comando de prediccion: `omie-price-predict`

El comando `omie-price-predict` realiza la inferencia del siguiente periodo disponible usando el modelo entrenado. Carga el modelo guardado, lee el dataset procesado y genera las variables necesarias para el siguiente `timestamp`. Despues muestra la prediccion en EUR/MWh.

Este comando completa el ciclo de machine learning. Entrenar un modelo y obtener metricas historicas es importante, pero una aplicacion predictiva debe ser capaz de generar una estimacion futura. `omie-price-predict` permite realizar esta fase de forma sencilla y repetible.

La prediccion depende del modelo guardado en `models/omie_model.joblib` y de los datos procesados disponibles. Si el modelo fue entrenado con variables ESIOS, el dataset usado para inferencia debe conservar esas columnas. Por eso el flujo normal guarda el dataset enriquecido cuando se usa ESIOS.

El comando tambien comprueba que exista suficiente historico para construir las variables necesarias. Si faltan retardos o medias moviles, la prediccion no puede realizarse correctamente. Esta comprobacion evita devolver resultados basados en informacion incompleta.

### 14.9. Modelo guardado: `models/omie_model.joblib`

El modelo entrenado se guarda en `models/omie_model.joblib`. Este fichero contiene el artefacto serializado que se utiliza posteriormente para inferencia. Guardar el modelo evita tener que reentrenar cada vez que se quiera predecir el siguiente periodo.

La serializacion se realiza con joblib, una biblioteca habitual en proyectos de scikit-learn. Joblib permite guardar objetos Python como pipelines, modelos entrenados, escaladores y metadatos asociados. En este proyecto, el modelo guardado incluye la informacion necesaria para reproducir la prediccion con la misma lista de variables usada durante el entrenamiento.

El directorio `models/` se considera un directorio de artefactos generados. No se versiona en Git porque los modelos pueden variar segun el rango de fechas, el algoritmo seleccionado, las variables ESIOS o la version de dependencias. Lo que se versiona es el codigo que permite generar el modelo.

La existencia de `models/omie_model.joblib` permite separar entrenamiento e inferencia. Un usuario puede entrenar una vez, revisar metricas y despues realizar predicciones sin repetir todo el proceso. Esta separacion es una practica habitual en aplicaciones de machine learning.

### 14.10. Grafica generada: `models/validation_plot.png`

Ademas del modelo, la aplicacion genera una grafica de validacion en `models/validation_plot.png`. Esta grafica compara visualmente valores reales, predicciones del modelo y baseline en el tramo de validacion. Su objetivo es complementar las metricas numericas con una representacion visual.

Las metricas como MAE, RMSE y R2 resumen el comportamiento del modelo, pero no muestran donde se producen los errores. Una grafica permite observar si el modelo sigue bien la forma general de la serie, si suaviza demasiado los picos, si falla en determinados tramos o si se separa del valor real en momentos concretos.

La grafica se guarda como artefacto local, igual que el modelo. No se incluye en Git por defecto, porque depende de cada ejecucion. Sin embargo, puede utilizarse en la memoria del TFG para ilustrar resultados concretos si se desea fijar un experimento.

El fichero `validation_plot.png` aporta valor durante la depuracion. Si las metricas parecen extranas, la grafica ayuda a detectar problemas de alineacion temporal, predicciones planas, errores sistematicos o comportamiento anomalo del baseline. Por tanto, no es solo una salida estetica, sino una herramienta de analisis.

En conjunto, la informacion concreta del proyecto muestra que la aplicacion esta organizada como un software ejecutable: tiene nombre, paquete, entorno, comandos, artefactos, repositorio y una estructura clara. Esta concrecion permite pasar de la descripcion teorica a una implementacion verificable.
