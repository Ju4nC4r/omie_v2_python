# Capitulo 11. Diseno de la aplicacion practica

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 11.1. Arquitectura general del software

La aplicacion se disena como un sistema modular en Python. En lugar de concentrar toda la logica en un unico script, el proyecto separa responsabilidades: descarga de datos, integracion con ESIOS, generacion de variables, entrenamiento, inferencia e interfaz grafica.

Esta arquitectura facilita el mantenimiento. Si se desea modificar el parser de OMIE, se trabaja en el modulo de datos. Si se quiere anadir una nueva variable, se modifica el modulo de features. Si se quiere cambiar un modelo, se actua sobre el modulo de entrenamiento.

La arquitectura tambien permite dos formas de uso: comandos de consola y GUI. Ambas comparten la misma logica interna, lo que evita duplicar implementaciones.

El diseno se apoya en una estructura de pipeline. Cada fase produce una salida que alimenta a la siguiente: los datos descargados alimentan la preparacion, el dataset supervisado alimenta el entrenamiento, el modelo entrenado alimenta la inferencia y las metricas alimentan el analisis. Esta organizacion facilita explicar el sistema y localizar errores.

### 11.2. Modulos principales del proyecto

Los modulos principales son:

```text
data.py
esios.py
features.py
train.py
predict.py
gui.py
```

`data.py` descarga y parsea OMIE. `esios.py` obtiene y une previsiones renovables. `features.py` construye variables y datasets. `train.py` entrena modelos y genera metricas. `predict.py` realiza inferencia. `gui.py` presenta una interfaz grafica para ejecutar el flujo.

Esta division refleja el pipeline de machine learning: obtener datos, transformarlos, entrenar, evaluar y predecir.

El modulo `features.py` actua como puente entre las fuentes de datos y los modelos. Los modelos no necesitan conocer el formato original de OMIE o ESIOS; reciben una matriz numerica. Esta separacion permite modificar modelos sin tocar el parser y ampliar variables sin cambiar la interfaz de entrenamiento.

### 11.3. Flujo de ejecucion completo

El flujo completo comienza con la seleccion de fechas. A partir de ellas, el sistema descarga ficheros OMIE y los guarda en cache. Si se activa ESIOS, descarga tambien prevision eolica y solar.

Despues se normalizan fechas, se ordenan observaciones y se construyen variables. A continuacion se crea el dataset supervisado, se separa en entrenamiento y validacion, se entrenan modelos y se calculan metricas.

Finalmente, el modelo seleccionado se guarda en disco y puede usarse para inferir el siguiente periodo. La grafica de validacion se genera como apoyo visual.

El flujo puede ejecutarse completo o por fases. Ejecutarlo por fases resulta util durante pruebas, porque permite saber si un problema esta en la descarga, la preparacion, el entrenamiento o la inferencia. Esta decision mejora la usabilidad y facilita la demostracion del proyecto.

### 11.4. Interfaz grafica

La interfaz grafica se implementa con Tkinter y se ejecuta con:

```bash
omie-price-gui
```

Incluye campos para fecha inicial, fecha final, selector de modelo, checkbox ESIOS y token. Tambien muestra estado del flujo, logs, barra de progreso y botones para cada fase.

Las fases visibles son:

- extraccion
- preparacion
- entrenamiento + test
- inferencia
- apertura de grafica
- limpieza de log

La GUI fue disenada para que el usuario vea que el proceso avanza, especialmente durante entrenamientos largos.

Internamente, la GUI usa hilos y una cola de eventos para mantener la ventana activa mientras se ejecutan tareas largas. De este modo, el usuario recibe logs y cambios de estado sin que la interfaz parezca bloqueada. Esta mejora fue importante tras detectar que el entrenamiento podia parecer "tostado" durante ejecuciones largas.

### 11.5. Interfaz por consola

La interfaz por consola se basa en:

```text
omie-price-train
omie-price-predict
```

`omie-price-train` permite entrenar indicando fechas, modelo y uso de ESIOS. `omie-price-predict` realiza inferencia con el modelo guardado.

La consola es util para reproducir experimentos, automatizar ejecuciones y documentar comandos exactos en la memoria del TFG. La GUI, en cambio, es mas adecuada para demostraciones visuales.

Disponer de consola y GUI aporta dos beneficios complementarios. La consola favorece reproducibilidad, porque los comandos pueden copiarse en la memoria. La GUI favorece accesibilidad, porque permite usar el sistema mediante botones y campos de texto.

### 11.6. Gestion de artefactos generados

La aplicacion genera varios artefactos:

```text
data/raw/
data/processed/omie_prices.csv
data/processed/omie_features.csv
data/processed/esios_generation_*.csv
models/omie_model.joblib
models/validation_plot.png
```

Los datos brutos y procesados se separan para mejorar trazabilidad. El modelo se guarda para inferencia posterior. La grafica permite inspeccionar visualmente la validacion.

Estos artefactos no se versionan en Git porque dependen de ejecuciones concretas y pueden regenerarse.

La separacion de artefactos mantiene limpio el repositorio. Los datos y modelos pueden variar segun el rango temporal, el algoritmo y el uso de ESIOS. Por ello, el repositorio conserva el codigo y la documentacion, mientras que los artefactos se regeneran localmente.

### 11.7. Configuracion del entorno Python

El diseno contempla ejecucion local mediante `.venv`. Esto aisla dependencias y permite reproducir el entorno de trabajo. El paquete se instala en modo editable para exponer comandos.

El fichero `pyproject.toml` declara dependencias y scripts. Esta aproximacion es mas ordenada que ejecutar ficheros sueltos y facilita que el proyecto sea usado por otra persona siguiendo el README.

La configuracion del entorno forma parte del diseno porque condiciona la reproducibilidad. Un usuario que clone el proyecto puede crear `.venv`, instalar dependencias y ejecutar los mismos comandos. Esto reduce la distancia entre codigo fuente y aplicacion funcional.

### 11.8. Control de versiones con Git

El proyecto se gestiona con Git. Cada avance relevante se guarda en un commit: interfaz grafica, seleccion de modelos, ESIOS, README y capitulos del TFG.

El control de versiones aporta trazabilidad. Permite saber cuando se introdujo cada funcionalidad y facilita recuperar cambios. El repositorio remoto configurado apunta a GitHub, aunque la subida requiere tener correctamente configurada la clave SSH.

En un TFG tecnico, Git no es solo una herramienta auxiliar: demuestra una metodologia de trabajo ordenada.

El uso de commits por hitos permite reconstruir la evolucion del proyecto: creacion del paquete, GUI, modelos, ESIOS, README y documentacion del TFG. En conclusion, el diseno de la aplicacion busca un equilibrio entre sencillez, modularidad y utilidad practica.
