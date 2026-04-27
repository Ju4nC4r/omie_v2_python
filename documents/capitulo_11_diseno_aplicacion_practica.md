# Capítulo 11. Diseño de la aplicación práctica

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 11.1. Arquitectura general del software

La aplicación se disena como un sistema modular en Python. En lugar de concentrar toda la lógica en un único script, el proyecto separa responsabilidades: descarga de datos, integración con ESIOS, generación de variables, entrenamiento, inferencia e interfaz gráfica.

Esta arquitectura facilita el mantenimiento. Si se desea modificar el parser de OMIE, se trabaja en el módulo de datos. Si se quiere añadir una nueva variable, se modifica el módulo de features. Si se quiere cambiar un modelo, se actua sobre el módulo de entrenamiento.

La arquitectura también permite dos formás de usó: comandos de consola y GUI. Ambas comparten la misma lógica interna, lo que evita duplicar implementaciones.

El diseño se apoya en una estructura de pipeline. Cada fase produce una salida que alimenta a la siguiente: los datos descargados alimentan la preparación, el dataset supervisado alimenta el entrenamiento, el modelo entrenado alimenta la inferencia y las métricas alimentan el análisis. Esta organización facilita explicar el sistema y localizar errores.

### 11.2. Módulos principales del proyecto

Los módulos principales son:

```text
data.py
esios.py
features.py
train.py
predict.py
gui.py
```

`data.py` descarga y parsea OMIE. `esios.py` obtiene y une previsiones renovables. `features.py` construye variables y datasets. `train.py` entrena modelos y genera métricas. `predict.py` realiza inferencia. `gui.py` presenta una interfaz gráfica para ejecutar el flujo.

Esta división refleja el pipeline de machine learning: obtener datos, transformarlos, entrenar, evaluar y predecir.

El módulo `features.py` actua como puente entre las fuentes de datos y los modelos. Los modelos no necesitan conocer el formato original de OMIE o ESIOS; reciben una matriz numérica. Esta separación permite modificar modelos sin tocar el parser y ampliar variables sin cambiar la interfaz de entrenamiento.

### 11.3. Flujo de ejecución completo

El flujo completo comienza con la selección de fechas. A partir de ellas, el sistema descarga ficheros OMIE y los guarda en cache. Si se activa ESIOS, descarga también previsión eólica y solar.

Después se normalizan fechas, se ordenan observaciones y se construyen variables. A continuacion se crea el dataset supervisado, se separa en entrenamiento y validación, se entrenan modelos y se calculan métricas.

Finalmente, el modelo seleccionado se guarda en disco y puede usarse para inferir el siguiente periodo. La gráfica de validación se genera como apoyo visual.

El flujo puede ejecutarse completo o por fases. Ejecutarlo por fases resulta útil durante pruebas, porque permite saber si un problema está en la descarga, la preparación, el entrenamiento o la inferencia. Esta decisión mejora la usabilidad y facilita la demostración del proyecto.

### 11.4. Interfaz gráfica

La interfaz gráfica se implementa con Tkinter y se ejecuta con:

```bash
omie-price-gui
```

Incluye campos para fecha inicial, fecha final, selector de modelo, checkbox ESIOS y token. También muestra estado del flujo, logs, barra de progreso y botones para cada fase.

Las fases visibles son:

- extracción
- preparación
- entrenamiento + test
- inferencia
- apertura de gráfica
- limpieza de log

La GUI fue disenada para que el usuario vea que el proceso avanza, especialmente durante entrenamientos largos.

Internamente, la GUI usa hilos y una cola de eventos para mantener la ventana activa mientras se ejecutan tareas largas. De este modo, el usuario recibe logs y cambios de estado sin que la interfaz parezca bloqueada. Esta mejora fue importante tras detectar que el entrenamiento podía parecer "tostado" durante ejecuciones largas.

### 11.5. Interfaz por consola

La interfaz por consola se basa en:

```text
omie-price-train
omie-price-predict
```

`omie-price-train` permite entrenar indicando fechas, modelo y uso de ESIOS. `omie-price-predict` realiza inferencia con el modelo guardado.

La consola es útil para reproducir experimentos, automatizar ejecuciones y documentar comandos exactos en la memoria del Proyecto. La GUI, en cambio, es más adecuada para demostraciones visuales.

Disponer de consola y GUI aporta dos beneficios complementarios. La consola favorece reproducibilidad, porque los comandos pueden copiarse en la memoria. La GUI favorece accesibilidad, porque permite usar el sistema mediante botones y campos de texto.

### 11.6. Gestión de artefactos generados

La aplicación genera varios artefactos:

```text
data/raw/
data/processed/omie_prices.csv
data/processed/omie_features.csv
data/processed/esios_generation_*.csv
models/omie_model.joblib
models/validation_plot.png
```

Los datos brutos y procesados se separan para mejorar trazabilidad. El modelo se guarda para inferencia posterior. La gráfica permite inspeccionar visualmente la validación.

Estos artefactos no se versiónan en Git porque dependen de ejecuciones concretas y pueden regenerarse.

La separación de artefactos mantiene limpio el repositorio. Los datos y modelos pueden variar según el rango temporal, el algoritmo y el uso de ESIOS. Por ello, el repositorio conserva el código y la documentación, mientras que los artefactos se regeneran localmente.

### 11.7. Configuración del entorno Python

El diseño contempla ejecución local mediante `.venv`. Esto aisla dependencias y permite reproducir el entorno de trabajo. El paquete se instala en modo editable para exponer comandos.

El fichero `pyproject.toml` declara dependencias y scripts. Esta aproximación es más ordenada que ejecutar ficheros sueltos y facilita que el proyecto sea usado por otra persona siguiendo el README.

La configuración del entorno forma parte del diseño porque condiciona la reproducibilidad. Un usuario que clone el proyecto puede crear `.venv`, instalar dependencias y ejecutar los mismos comandos. Esto reduce la distancia entre código fuente y aplicación funcional.

### 11.8. Control de versiones con Git

El proyecto se gestiona con Git. Cada avance relevante se guarda en un commit: interfaz gráfica, selección de modelos, ESIOS, README y capítulos del Proyecto.

El control de versiones aporta trazabilidad. Permite saber cuando se introdujo cada funcionalidad y facilita recuperar cambios. El repositorio remoto configurado apunta a GitHub, aunque la subida requiere tener correctamente configurada la clave SSH.

En un Proyecto técnico, Git no es solo una herramienta auxiliar: demuestra una metodología de trabajo ordenada.

El uso de commits por hitos permite reconstruir la evolución del proyecto: creación del paquete, GUI, modelos, ESIOS, README y documentación del Proyecto. En conclusión, el diseño de la aplicación busca un equilibrio entre sencillez, modularidad y utilidad práctica.
