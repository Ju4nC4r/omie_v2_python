# Capitulo 3. Objetivos

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 3.1. Objetivo general

El objetivo general de este Trabajo Fin de Grado es desarrollar, documentar y evaluar una aplicacion capaz de predecir el precio del mercado electrico espanol utilizando tecnicas de aprendizaje automatico sobre datos publicos de OMIE y, de forma opcional, datos de prevision de generacion renovable procedentes de ESIOS/REE.

El trabajo no pretende construir una herramienta profesional de prediccion energetica, sino un prototipo academico y funcional que permita recorrer todas las fases principales de un proyecto de ciencia de datos aplicado al sector electrico. Estas fases incluyen la obtencion de datos, su limpieza, la generacion de variables, el entrenamiento de modelos, la validacion, la inferencia y la presentacion de resultados.

La aplicacion desarrollada debe permitir analizar si diferentes modelos de machine learning son capaces de mejorar una estrategia de referencia sencilla basada en repetir el precio observado 24 periodos antes. Esta comparacion resulta importante porque evita evaluar los modelos de forma aislada y permite comprobar si realmente aportan valor frente a una regla simple.

El objetivo general tambien incluye estudiar la influencia de variables relacionadas con la produccion renovable. La generacion eolica y solar tiene un papel cada vez mas relevante en la formacion del precio electrico. Por ello, se plantea incorporar estas variables como extension opcional del modelo, con el fin de observar si su inclusion puede mejorar la capacidad predictiva.

Desde el punto de vista practico, el resultado esperado es una herramienta ejecutable en Python, con interfaz de consola e interfaz grafica, que facilite la experimentacion con distintos rangos temporales y modelos de prediccion. Esta herramienta debe servir como base para obtener resultados, analizar errores y proponer mejoras futuras.

### 3.2. Objetivos especificos

Para alcanzar el objetivo general se definen los siguientes objetivos especificos.

#### 3.2.1. Automatizar la descarga de datos OMIE

El primer objetivo especifico consiste en implementar un sistema que permita descargar automaticamente los ficheros diarios de OMIE correspondientes al precio marginal del mercado diario. Estos ficheros deben almacenarse localmente para evitar descargas repetidas y facilitar la reproducibilidad de los experimentos.

El sistema debe ser capaz de construir la URL de descarga a partir de una fecha, comprobar si el fichero ya existe en cache y parsear su contenido para extraer los campos relevantes.

#### 3.2.2. Parsear y normalizar los datos de mercado

Una vez descargados los ficheros, es necesario transformarlos en un formato tabular homogeneo. El parser debe extraer la fecha, el periodo, el precio marginal portugues y el precio marginal espanol.

Tambien debe generar una columna `timestamp` que permita ordenar y unir datos temporalmente. Esta parte es especialmente importante porque los datos pueden ser horarios o cuarto-horarios. Por tanto, el sistema debe detectar si un dia contiene 24 o 96 periodos y asignar correctamente el instante temporal asociado.

#### 3.2.3. Construir un dataset supervisado

El tercer objetivo consiste en transformar la serie historica de precios en un problema de aprendizaje supervisado. Para ello se deben crear variables de entrada y una variable objetivo.

La variable objetivo sera:

```text
marginal_es
```

Las variables de entrada incluiran informacion temporal, retardos de precio, medias moviles, desviaciones moviles, minimos, maximos, diferencias y ratios.

#### 3.2.4. Incorporar variables externas opcionales

El trabajo debe permitir incorporar informacion externa de ESIOS, concretamente previsiones de generacion eolica y solar. Esta funcionalidad debe ser opcional, ya que requiere disponer de un token de acceso a la API.

Los indicadores considerados son:

```text
541 -> prevision eolica
542 -> prevision solar fotovoltaica
543 -> prevision solar termica
```

El objetivo es enriquecer el dataset con variables que representen la disponibilidad esperada de energia renovable.

#### 3.2.5. Implementar varios modelos de prediccion

Otro objetivo especifico es implementar y comparar modelos de distinta naturaleza:

- `RidgeCV`
- `MLPRegressor`
- `HistGradientBoostingRegressor`

Estos modelos representan enfoques lineales, neuronales y basados en arboles. La comparacion entre ellos permite analizar que tipo de modelo se adapta mejor a los datos disponibles.

#### 3.2.6. Implementar un modo automatico de seleccion

El sistema debe incluir un modo `auto` que entrene los modelos disponibles, compare sus metricas en validacion temporal y seleccione el que obtenga menor error absoluto medio.

Este modo facilita el uso de la aplicacion, ya que permite obtener un modelo competitivo sin que el usuario tenga que ejecutar manualmente cada alternativa.

#### 3.2.7. Evaluar los modelos con metricas adecuadas

Los modelos deben evaluarse utilizando metricas de regresion adecuadas:

- MAE
- RMSE
- R2

Ademas, se debe comparar el rendimiento frente a una baseline `lag 24`, que usa el precio observado 24 periodos antes como prediccion.

#### 3.2.8. Desarrollar una interfaz grafica

Se plantea desarrollar una interfaz grafica sencilla que permita ejecutar el flujo completo sin necesidad de escribir comandos. Esta interfaz debe permitir:

- seleccionar rango de fechas
- elegir modelo
- activar o desactivar ESIOS
- introducir token ESIOS
- ejecutar extraccion
- preparar datos
- entrenar y evaluar
- realizar inferencia
- abrir la grafica de validacion

#### 3.2.9. Proporcionar comandos de consola

Aunque la interfaz grafica facilita el uso, tambien es necesario disponer de comandos de consola para automatizar experimentos. Los comandos principales son:

```text
omie-price-train
omie-price-predict
omie-price-gui
```

Estos comandos permiten integrar el proyecto en flujos reproducibles y ejecutar entrenamientos con diferentes parametros.

#### 3.2.10. Documentar el proyecto y su uso

Finalmente, el trabajo debe incluir documentacion suficiente para instalar, ejecutar y entender el sistema. Esto incluye:

- README del repositorio
- documentacion academica en `documents/`
- indice del TFG
- capitulos desarrollados
- resumen del hilo de desarrollo
- explicacion de modelos, datos y metricas

### 3.3. Requisitos funcionales de la aplicacion

Los requisitos funcionales describen que debe hacer la aplicacion desde el punto de vista del usuario.

#### RF1. Descargar datos OMIE

La aplicacion debe permitir descargar datos historicos de OMIE para un rango de fechas definido por el usuario.

#### RF2. Cachear ficheros descargados

Los ficheros descargados deben almacenarse en `data/raw/` para evitar descargas repetidas.

#### RF3. Generar dataset procesado

La aplicacion debe transformar los ficheros brutos en un CSV procesado:

```text
data/processed/omie_prices.csv
```

#### RF4. Crear variables de entrenamiento

El sistema debe generar automaticamente las variables necesarias para entrenar los modelos.

#### RF5. Activar ESIOS de forma opcional

El usuario debe poder activar la inclusion de variables de prevision eolica y solar mediante ESIOS.

#### RF6. Validar token ESIOS

Si se activa ESIOS, la aplicacion debe comprobar que existe token antes de intentar modificar o descargar datos.

#### RF7. Seleccionar modelo

El usuario debe poder elegir entre:

```text
auto
ridge
mlp
hist_gradient_boosting
```

#### RF8. Entrenar modelo

La aplicacion debe entrenar el modelo seleccionado con los datos disponibles.

#### RF9. Evaluar resultados

Tras el entrenamiento, el sistema debe mostrar metricas de rendimiento.

#### RF10. Guardar modelo entrenado

El modelo debe guardarse en:

```text
models/omie_model.joblib
```

#### RF11. Generar grafica de validacion

La aplicacion debe generar una grafica comparando valores reales, prediccion y baseline.

#### RF12. Realizar inferencia

El sistema debe poder cargar el modelo entrenado y predecir el siguiente periodo disponible.

#### RF13. Mostrar progreso en la interfaz grafica

La GUI debe mostrar logs y barra de progreso para evitar que el usuario interprete el entrenamiento como un bloqueo.

#### RF14. Gestionar errores de forma clara

La aplicacion debe mostrar mensajes comprensibles cuando falten datos, token ESIOS o se produzcan errores de descarga.

### 3.4. Requisitos no funcionales

Los requisitos no funcionales describen condiciones de calidad, mantenibilidad y funcionamiento del sistema.

#### RNF1. Modularidad

El codigo debe estar dividido en modulos con responsabilidades claras:

- descarga de datos
- integracion ESIOS
- generacion de variables
- entrenamiento
- inferencia
- interfaz grafica

#### RNF2. Reproducibilidad

El proyecto debe poder ejecutarse de nuevo siguiendo los comandos documentados. El uso de cache local y entorno virtual facilita esta reproducibilidad.

#### RNF3. Mantenibilidad

La estructura del codigo debe permitir anadir nuevas fuentes de datos o modelos sin reescribir todo el sistema.

#### RNF4. Claridad

Los nombres de funciones, variables y ficheros deben ser comprensibles. La documentacion debe explicar el flujo sin depender exclusivamente del codigo.

#### RNF5. Robustez ante datos ausentes

El sistema debe poder continuar si algunos dias de OMIE no estan disponibles, siempre que existan datos suficientes para entrenar.

#### RNF6. Separacion entre codigo y artefactos

Los datos descargados, modelos entrenados y caches no deben versionarse en Git. Para ello se usa `.gitignore`.

#### RNF7. Ejecucion local

La aplicacion debe poder ejecutarse localmente en un ordenador sin necesidad de desplegar servicios externos.

#### RNF8. Usabilidad

La interfaz grafica debe permitir ejecutar las fases principales de forma sencilla.

#### RNF9. Trazabilidad

Los cambios relevantes deben quedar registrados mediante commits de Git.

#### RNF10. Extensibilidad

El sistema debe quedar preparado para futuras mejoras, como incorporar demanda, meteorologia, festivos o backtesting.

### 3.5. Limitaciones iniciales

El proyecto presenta varias limitaciones que deben tenerse en cuenta al interpretar los resultados.

En primer lugar, el modelo no incorpora todavia todas las variables relevantes del mercado electrico. Aunque se ha anadido soporte opcional para prevision eolica y solar, quedan fuera variables importantes como demanda prevista, temperatura, gas, CO2, interconexiones o indisponibilidades.

En segundo lugar, la evaluacion utiliza una particion temporal simple. Esto permite validar de forma inicial el comportamiento de los modelos, pero no sustituye a un backtesting completo. Para una evaluacion mas robusta seria conveniente probar multiples ventanas temporales.

En tercer lugar, la prediccion implementada se centra en el siguiente periodo disponible. En el mercado electrico, muchas aplicaciones practicas requieren predecir todo el dia siguiente. Esta funcionalidad se considera una linea futura.

En cuarto lugar, la integracion con ESIOS depende de la disponibilidad de token y de la respuesta de la API. Si el usuario no dispone de token, el sistema sigue funcionando, pero sin variables renovables.

En quinto lugar, los datos de OMIE pueden presentar dias no disponibles o cambios de formato. El sistema intenta gestionar ausencias, pero la calidad del entrenamiento dependera de la cantidad y continuidad de datos descargados.

En sexto lugar, los modelos implementados son relativamente sencillos. Esto es coherente con el objetivo academico del trabajo, pero limita la comparacion con modelos mas avanzados de prediccion de series temporales.

Finalmente, la aplicacion no debe interpretarse como herramienta de decision economica. Su finalidad es educativa, experimental y metodologica. Los resultados deben analizarse con cautela y siempre en relacion con las limitaciones de datos y modelos.

