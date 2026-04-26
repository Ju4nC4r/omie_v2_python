# Capítulo 3. Objetivos

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 3.1. Objetivo general

El objetivo general de este Trabajo Fin de Grado es desarrollar, documentar y evaluar una aplicación capaz de predecir el precio del mercado eléctrico español utilizando técnicas de aprendizaje automático sobre datos públicos de OMIE y, de forma opcional, datos de previsión de generación renovable procedentes de ESIOS/REE.

El trabajo no pretende construir una herramienta profesional de predicción energética, sino un prototipo académico y funcional que permita recorrer todas las fases principales de un proyecto de ciencia de datos aplicado al sector eléctrico. Estas fases incluyen la obtención de datos, su limpieza, la generación de variables, el entrenamiento de modelos, la validación, la inferencia y la presentación de resultados.

La aplicación desarrollada debe permitir analizar si diferentes modelos de machine learning son capaces de mejorar una estrategia de referencia sencilla basada en repetir el precio observado 24 periodos antes. Esta comparación resulta importante porque evita evaluar los modelos de forma aislada y permite comprobar si realmente aportan valor frente a una regla simple.

El objetivo general también incluye estudiar la influencia de variables relacionadas con la producción renovable. La generación eólica y solar tiene un papel cada vez más relevante en la formación del precio eléctrico. Por ello, se plantea incorporar estas variables como extensión opcional del modelo, con el fin de observar si su inclusión puede mejorar la capacidad predictiva.

Desde el punto de vista práctico, el resultado esperado es una herramienta ejecutable en Python, con interfaz de consola e interfaz gráfica, que facilite la experimentación con distintos rangos temporales y modelos de predicción. Esta herramienta debe servir como base para obtener resultados, analizar errores y proponer mejoras futuras.

### 3.2. Objetivos específicos

Para alcanzar el objetivo general se definen los siguientes objetivos específicos.

#### 3.2.1. Automatizar la descarga de datos OMIE

El primer objetivo específico consiste en implementar un sistema que permita descargar automáticamente los ficheros diarios de OMIE correspondientes al precio marginal del mercado diario. Estos ficheros deben almacenarse localmente para evitar descargas repetidas y facilitar la reproducibilidad de los experimentos.

El sistema debe ser capaz de construir la URL de descarga a partir de una fecha, comprobar si el fichero ya existe en cache y parsear su contenido para extraer los campos relevantes.

#### 3.2.2. Parsear y normalizar los datos de mercado

Una vez descargados los ficheros, es necesario transformarlos en un formato tabular homogeneo. El parser debe extraer la fecha, el periodo, el precio marginal portugués y el precio marginal español.

También debe generar una columna `timestamp` que permita ordenar y unir datos temporalmente. Esta parte es especialmente importante porque los datos pueden ser horarios o cuarto-horarios. Por tanto, el sistema debe detectar si un día contiene 24 o 96 periodos y asignar correctamente el instante temporal asociado.

#### 3.2.3. Construir un dataset supervisado

El tercer objetivo consiste en transformar la serie histórica de precios en un problema de aprendizaje supervisado. Para ello se deben crear variables de entrada y una variable objetivo.

La variable objetivo será:

```text
marginal_es
```

Las variables de entrada incluirán información temporal, retardos de precio, medias móviles, desviaciones móviles, mínimos, máximos, diferencias y ratios.

#### 3.2.4. Incorporar variables externas opcionales

El trabajo debe permitir incorporar información externa de ESIOS, concretamente previsiones de generación eólica y solar. Esta funcionalidad debe ser opcional, ya que requiere disponer de un token de acceso a la API.

Los indicadores considerados son:

```text
541 -> previsión eólica
542 -> previsión solar fotovoltaica
543 -> previsión solar térmica
```

El objetivo es enriquecer el dataset con variables que representen la disponibilidad esperada de energía renovable.

#### 3.2.5. Implementar varios modelos de predicción

Otro objetivo específico es implementar y comparar modelos de distinta naturaleza:

- `RidgeCV`
- `MLPRegressor`
- `HistGradientBoostingRegressor`

Estos modelos representan enfoques lineales, neuronales y basados en árboles. La comparación entre ellos permite analizar que tipo de modelo se adapta mejor a los datos disponibles.

#### 3.2.6. Implementar un modo automático de selección

El sistema debe incluir un modo `auto` que entrene los modelos disponibles, compare sus métricas en validación temporal y seleccione el que obtenga menor error absoluto medio.

Este modo facilita el uso de la aplicación, ya que permite obtener un modelo competitivo sin que el usuario tenga que ejecutar manualmente cada alternativa.

#### 3.2.7. Evaluar los modelos con métricas adecuadas

Los modelos deben evaluarse utilizando métricas de regresión adecuadas:

- MAE
- RMSE
- R2

Además, se debe comparar el rendimiento frente a una baseline `lag 24`, que usa el precio observado 24 periodos antes como predicción.

#### 3.2.8. Desarrollar una interfaz gráfica

Se plantea desarrollar una interfaz gráfica sencilla que permita ejecutar el flujo completo sin necesidad de escribir comandos. Esta interfaz debe permitir:

- seleccionar rango de fechas
- elegir modelo
- activar o desactivar ESIOS
- introducir token ESIOS
- ejecutar extracción
- preparar datos
- entrenar y evaluar
- realizar inferencia
- abrir la gráfica de validación

#### 3.2.9. Proporcionar comandos de consola

Aunque la interfaz gráfica facilita el usó, también es necesario disponer de comandos de consola para automatizar experimentos. Los comandos principales son:

```text
omie-price-train
omie-price-predict
omie-price-gui
```

Estos comandos permiten integrar el proyecto en flujos reproducibles y ejecutar entrenamientos con diferentes parámetros.

#### 3.2.10. Documentar el proyecto y su usó

Finalmente, el trabajo debe incluir documentación suficiente para instalar, ejecutar y entender el sistema. Esto incluye:

- README del repositorio
- documentación académica en `documents/`
- índice del TFG
- capítulos desarrollados
- resumen del hilo de desarrollo
- explicación de modelos, datos y métricas

### 3.3. Requisitos funcionales de la aplicación

Los requisitos funcionales describen que debe hacer la aplicación desde el punto de vista del usuario.

#### RF1. Descargar datos OMIE

La aplicación debe permitir descargar datos históricos de OMIE para un rango de fechas definido por el usuario.

#### RF2. Cachear ficheros descargados

Los ficheros descargados deben almacenarse en `data/raw/` para evitar descargas repetidas.

#### RF3. Generar dataset procesado

La aplicación debe transformar los ficheros brutos en un CSV procesado:

```text
data/processed/omie_prices.csv
```

#### RF4. Crear variables de entrenamiento

El sistema debe generar automáticamente las variables necesarias para entrenar los modelos.

#### RF5. Activar ESIOS de forma opcional

El usuario debe poder activar la inclusión de variables de previsión eólica y solar mediante ESIOS.

#### RF6. Validar token ESIOS

Si se activa ESIOS, la aplicación debe comprobar que existe token antes de intentar modificar o descargar datos.

#### RF7. Selecciónar modelo

El usuario debe poder elegir entre:

```text
auto
ridge
mlp
hist_gradient_boosting
```

#### RF8. Entrenar modelo

La aplicación debe entrenar el modelo seleccionado con los datos disponibles.

#### RF9. Evaluar resultados

Tras el entrenamiento, el sistema debe mostrar métricas de rendimiento.

#### RF10. Guardar modelo entrenado

El modelo debe guardarse en:

```text
models/omie_model.joblib
```

#### RF11. Generar gráfica de validación

La aplicación debe generar una gráfica comparando valores reales, predicción y baseline.

#### RF12. Realizar inferencia

El sistema debe poder cargar el modelo entrenado y predecir el siguiente periodo disponible.

#### RF13. Mostrar progreso en la interfaz gráfica

La GUI debe mostrar logs y barra de progreso para evitar que el usuario interprete el entrenamiento como un bloqueo.

#### RF14. Gestiónar errores de forma clara

La aplicación debe mostrar mensajes comprensibles cuando falten datos, token ESIOS o se produzcan errores de descarga.

### 3.4. Requisitos no funcionales

Los requisitos no funcionales describen condiciones de calidad, mantenibilidad y funcionamiento del sistema.

#### RNF1. Modularidad

El código debe estar dividido en módulos con responsabilidades claras:

- descarga de datos
- integración ESIOS
- generación de variables
- entrenamiento
- inferencia
- interfaz gráfica

#### RNF2. Reproducibilidad

El proyecto debe poder ejecutarse de nuevo siguiendo los comandos documentados. El uso de cache local y entorno virtual facilita está reproducibilidad.

#### RNF3. Mantenibilidad

La estructura del código debe permitir añadir nuevas fuentes de datos o modelos sin reescribir todo el sistema.

#### RNF4. Claridad

Los nombres de funciones, variables y ficheros deben ser comprensibles. La documentación debe explicar el flujo sin depender exclusivamente del código.

#### RNF5. Robustez ante datos ausentes

El sistema debe poder continuar si algunos días de OMIE no están disponibles, siempre que existan datos suficientes para entrenar.

#### RNF6. Separación entre código y artefactos

Los datos descargados, modelos entrenados y caches no deben versiónarse en Git. Para ello se usa `.gitignore`.

#### RNF7. Ejecución local

La aplicación debe poder ejecutarse localmente en un ordenador sin necesidad de desplegar servicios externos.

#### RNF8. Usabilidad

La interfaz gráfica debe permitir ejecutar las fases principales de forma sencilla.

#### RNF9. Trazabilidad

Los cambios relevantes deben quedar registrados mediante commits de Git.

#### RNF10. Extensibilidad

El sistema debe quedar preparado para futuras mejoras, como incorporar demanda, meteorología, festivos o backtesting.

### 3.5. Limitaciones iniciales

El proyecto presenta varias limitaciones que deben tenerse en cuenta al interpretar los resultados.

En primer lugar, el modelo no incorpora todavía todas las variables relevantes del mercado eléctrico. Aunque se ha añadido soporte opcional para previsión eólica y solar, quedan fuera variables importantes como demanda prevista, temperatura, gas, CO2, interconexiones o indisponibilidades.

En segundo lugar, la evaluación utiliza una partición temporal simple. Esto permite validar de forma inicial el comportamiento de los modelos, pero no sustituye a un backtesting completo. Para una evaluación más robusta sería conveniente probar múltiples ventanas temporales.

En tercer lugar, la predicción implementada se centra en el siguiente periodo disponible. En el mercado eléctrico, muchas aplicaciones prácticas requieren predecir todo el día siguiente. Esta funcionalidad se considera una línea futura.

En cuarto lugar, la integración con ESIOS depende de la disponibilidad de token y de la respuesta de la API. Si el usuario no dispone de token, el sistema sigue funcionando, pero sin variables renovables.

En quinto lugar, los datos de OMIE pueden presentar días no disponibles o cambios de formato. El sistema intenta gestionar ausencias, pero la calidad del entrenamiento dependerá de la cantidad y continuidad de datos descargados.

En sexto lugar, los modelos implementados son relativamente sencillos. Esto es coherente con el objetivo académico del trabajo, pero limita la comparación con modelos más avanzados de predicción de series temporales.

Finalmente, la aplicación no debe interpretarse como herramienta de decisión económica. Su finalidad es educativa, experimental y metodológica. Los resultados deben analizarse con cautela y siempre en relación con las limitaciones de datos y modelos.

